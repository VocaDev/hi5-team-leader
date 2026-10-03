# -*- coding: utf-8 -*-
"""
The engine: deterministic capacity check and task assignment. No LLM, no network.

Rules (never overridable, not even by the leader):
  R1  the worker has every skill the task needs
  R2  no overlap, travel included: end of the other job + travel <= start of this task (and the reverse)
  R3  max working hours per day (worker.max_hours, default 10)
  R4  consent: nobody is booked without ACCEPT (enforced by the runtime, not here)
  R5  not unavailable / not declined this task
  R6  vehicles and equipment: never double-booked
  R7  four-eyes: a task marked not_same_as X can't go to the person doing X (e.g. code review)
Every rejection comes back as a sentence with the arithmetic, so the UI and the agent can explain it.
"""
from __future__ import annotations

from dataclasses import dataclass, field

DEFAULT_MAX_HOURS = 10
DEFAULT_TRAVEL = 30  # assumption when a zone pair is missing; flagged in the output


def to_min(hhmm: str) -> int:
    h, m = hhmm.strip().split(":")
    return int(h) * 60 + int(m)


def hhmm(minutes: int) -> str:
    minutes = max(0, minutes)
    return f"{minutes // 60:02d}:{minutes % 60:02d}"


def travel(company: dict, a: str, b: str) -> int:
    if not a or not b or a == b:
        return 0
    t = company.get("travel_min", {})
    return int(t.get(f"{a}-{b}", t.get(f"{b}-{a}", DEFAULT_TRAVEL)))


@dataclass
class Busy:
    start: int
    end: int
    zone: str
    label: str


@dataclass
class World:
    """Who/what is already busy today: existing jobs + tasks of other planned jobs."""
    company: dict
    workers: dict[str, list[Busy]] = field(default_factory=dict)
    resources: dict[str, list[Busy]] = field(default_factory=dict)  # vehicles + equipment


def job_window(job: dict) -> tuple[int, int]:
    return min(t["from_min"] for t in job["tasks"]), max(t["to_min"] for t in job["tasks"])


def build_world(company: dict, planned_jobs: list[dict], exclude_job_id: str | None = None) -> World:
    w = World(company)
    depot = company.get("company", {}).get("depot_zone", "")
    for ej in company.get("existing_jobs", []):
        a, b, z = to_min(ej["from"]), to_min(ej["to"]), ej["zone"]
        for wid in ej.get("assignments", {}):
            w.workers.setdefault(wid, []).append(Busy(a, b, z, ej["title"]))
        lead = travel(company, depot, z)
        for rid in [ej.get("vehicle")] + list(ej.get("equipment", [])):
            if rid:
                w.resources.setdefault(rid, []).append(Busy(a - lead, b + lead, z, ej["title"]))
    for job in planned_jobs:
        if job["id"] == exclude_job_id or job.get("status") == "cancelled":
            continue
        s, e = job_window(job)
        for t in job["tasks"]:
            if t.get("worker_id") and t.get("status") != "declined":
                w.workers.setdefault(t["worker_id"], []).append(Busy(t["from_min"], t["to_min"], job["zone"], job["title"]))
            for rid in [t.get("vehicle")] + list(t.get("equipment") or []):
                if rid:
                    w.resources.setdefault(rid, []).append(Busy(s, e, job["zone"], job["title"]))
    return w


def worker_by_id(company: dict, wid: str) -> dict | None:
    return next((x for x in company["workers"] if x["id"] == wid), None)


def find_worker(company: dict, name: str) -> dict | None:
    n = name.strip().lower()
    for x in company["workers"]:
        if x["name"].lower() == n or x["id"].lower() == n or n in [a.lower() for a in x.get("aliases", [])]:
            return x
    matches = [x for x in company["workers"] if x["name"].lower().startswith(n[:4])] if len(n) >= 4 else []
    return matches[0] if len(matches) == 1 else None


def check_worker(world: World, worker: dict, task: dict, zone: str, extra: list[Busy] | None = None) -> list[str]:
    """All rule violations for putting `worker` on `task` (empty list = allowed)."""
    c = world.company
    name, s, e = worker["name"], task["from_min"], task["to_min"]
    reasons = []
    missing = [sk for sk in task["skills"] if sk not in worker.get("skills", [])]
    if missing:
        reasons.append(f"R1 {name} s'ka aftësinë: {', '.join(missing)}")
    if worker["id"] in task.get("declined_by", []):
        reasons.append(f"R5 {name} e ka refuzuar këtë detyrë")
    for u in worker.get("unavailable", []):
        if to_min(u["from"]) < e and s < to_min(u["to"]):
            reasons.append(f"R5 {name} s'është në dispozicion {u['from']}–{u['to']}")
    busy = list(world.workers.get(worker["id"], [])) + list(extra or [])
    for b in busy:
        t_in, t_out = travel(c, b.zone, zone), travel(c, zone, b.zone)
        if b.end + t_in <= s or e + t_out <= b.start:
            continue
        if b.start <= s:
            reasons.append(f"R2 {name} është te '{b.label}' ({b.zone}) deri {hhmm(b.end)}; "
                           f"+ {t_in} min rrugë = {hhmm(b.end + t_in)} > {hhmm(s)}")
        else:
            reasons.append(f"R2 {name} duhet të jetë te '{b.label}' ({b.zone}) në {hhmm(b.start)}; "
                           f"{hhmm(e)} + {t_out} min rrugë = {hhmm(e + t_out)} > {hhmm(b.start)}")
    worked = sum(b.end - b.start for b in busy) + (e - s)
    max_h = worker.get("max_hours", DEFAULT_MAX_HOURS)
    if worked > max_h * 60:
        reasons.append(f"R3 {name} do të kishte {worked / 60:.1f} orë sot > maksimumi {max_h} orë")
    return reasons


def _free_resource(world: World, items: list[dict], window: tuple[int, int], taken: set[str]) -> tuple[dict | None, list[str]]:
    s, e = window
    why = []
    for it in items:
        if it["id"] in taken:
            continue
        clash = next((b for b in world.resources.get(it["id"], []) if b.start < e and s < b.end), None)
        if clash:
            why.append(f"R6 {it['name']} i zënë te '{clash.label}' {hhmm(clash.start)}–{hhmm(clash.end)}")
            continue
        return it, why
    return None, why


def plan_job(company: dict, job: dict, planned_jobs: list[dict], locked: dict[str, str] | None = None) -> dict:
    """Assign workers, a vehicle and equipment to every task of `job`.

    locked = {task_id: worker_id} assignments to keep (manual or already accepted).
    Returns the plan plus, for every task, the rejected candidates with the reason in numbers."""
    world = build_world(company, planned_jobs, exclude_job_id=job["id"])
    locked = locked or {}
    tasks = job["tasks"]
    zone = job["zone"]
    window = job_window(job)
    log: list[str] = []

    # vehicle + equipment for the whole job window
    taken: set[str] = set()
    resources: dict[str, dict] = {}
    for t in tasks:
        if t.get("vehicle_needed") and "vehicle" not in resources:
            v, why = _free_resource(world, company.get("vehicles", []), window, taken)
            log += why
            if v:
                resources["vehicle"] = v
                taken.add(v["id"])
                log.append(f"OK {v['name']} i lirë {hhmm(window[0])}–{hhmm(window[1])}")
            else:
                log.append("❌ s'ka automjet të lirë")
        for etype in t.get("equipment_types", []):
            key = f"eq:{etype}"
            if key in resources:
                continue
            items = [x for x in company.get("equipment", []) if x["type"] == etype]
            it, why = _free_resource(world, items, window, taken)
            log += why
            if it:
                resources[key] = it
                taken.add(it["id"])
                log.append(f"OK {it['name']} i lirë")
            else:
                log.append(f"❌ s'ka {etype} të lirë")

    # candidates per task, with reasons for the rejected ones
    rejected: dict[str, list[dict]] = {}
    cands: dict[str, list[dict]] = {}
    for t in tasks:
        ok, bad = [], []
        for wk in company["workers"]:
            r = check_worker(world, wk, t, zone)
            (bad if r else ok).append((wk, r))
        cands[t["id"]] = [wk for wk, _ in ok]
        rejected[t["id"]] = [{"worker": wk["name"], "reasons": r} for wk, r in bad if not all(x.startswith("R1") for x in r)]

    def load(wid: str) -> int:
        return sum(b.end - b.start for b in world.workers.get(wid, []))

    order = sorted(tasks, key=lambda t: (t["id"] not in locked, len(cands[t["id"]])))
    best: dict[str, str] = {}

    def dfs(i: int, assign: dict[str, str], allow_skip: bool) -> bool:
        nonlocal best
        if len(assign) > len(best):
            best = dict(assign)
        if i == len(order):
            return len(assign) == len(order)
        t = order[i]
        pool = cands[t["id"]]
        if t["id"] in locked:
            pool = [w for w in pool if w["id"] == locked[t["id"]]]
        pool = sorted(pool, key=lambda w: (load(w["id"]), w["name"]))
        for wk in pool:
            if any(assign.get(o) == wk["id"] for o in t.get("not_same_as", [])):
                continue  # R7 four-eyes
            if any(x.get("not_same_as") and t["id"] in x["not_same_as"] and assign.get(x["id"]) == wk["id"] for x in order[:i]):
                continue
            mine = [x for x in order[:i] if assign.get(x["id"]) == wk["id"]]
            extra = [Busy(x["from_min"], x["to_min"], zone, job["title"]) for x in mine]
            if extra and check_worker(world, wk, t, zone, extra):
                continue
            assign[t["id"]] = wk["id"]
            if dfs(i + 1, assign, allow_skip):
                return True
            del assign[t["id"]]
        return dfs(i + 1, assign, allow_skip) if allow_skip else False

    complete = dfs(0, {}, False)
    if not complete:
        dfs(0, {}, True)  # best partial plan: cover as many tasks as possible
    assign = best
    out_tasks, uncovered = [], []
    for t in tasks:
        wid = assign.get(t["id"])
        wk = worker_by_id(company, wid) if wid else None
        eq = [resources[f"eq:{et}"] for et in t.get("equipment_types", []) if f"eq:{et}" in resources]
        row = {**{k: v for k, v in t.items()}, "worker_id": wid, "worker": wk["name"] if wk else None,
               "vehicle": resources["vehicle"]["id"] if t.get("vehicle_needed") and "vehicle" in resources else None,
               "equipment": [x["id"] for x in eq],
               "bring": ([resources["vehicle"]["name"]] if t.get("vehicle_needed") and "vehicle" in resources else [])
                        + [x["name"] for x in eq]}
        out_tasks.append(row)
        if not wk:
            uncovered.append({"task_id": t["id"], "role": t["role"],
                              "why": [f"{r['worker']}: {r['reasons'][0]}" for r in rejected[t["id"]]][:4] or ["askush s'ka aftësinë"]})
    missing_res = [l for l in log if l.startswith("❌")]
    return {
        "feasible": complete and not uncovered and not missing_res,
        "tasks": out_tasks,
        "uncovered": uncovered,
        "missing_resources": missing_res,
        "rejected": rejected,
        "resource_log": log,
    }


def validate_manual(company: dict, job: dict, planned_jobs: list[dict], task_id: str, worker_id: str) -> list[str]:
    """Leader asks for a specific person. Same rules, no exceptions."""
    world = build_world(company, planned_jobs, exclude_job_id=job["id"])
    task = next(t for t in job["tasks"] if t["id"] == task_id)
    wk = worker_by_id(company, worker_id)
    others = [Busy(t["from_min"], t["to_min"], job["zone"], job["title"])
              for t in job["tasks"] if t["id"] != task_id and t.get("worker_id") == worker_id and t.get("status") != "declined"]
    reasons = check_worker(world, wk, task, job["zone"], others)
    by_id = {t["id"]: t for t in job["tasks"]}
    linked = list(task.get("not_same_as", [])) + [t["id"] for t in job["tasks"] if task_id in t.get("not_same_as", [])]
    for o in linked:
        if by_id.get(o, {}).get("worker_id") == worker_id:
            reasons.append(f"R7 4-eyes: {wk['name']} e bën '{by_id[o]['role']}', prandaj s'mund ta bëjë edhe '{task['role']}'")
    return reasons


def expand_job(template: dict, start: str) -> list[dict]:
    s = to_min(start)
    out = []
    for t in template["tasks"]:
        a, b = s + t["start_offset_min"], s + t["end_offset_min"]
        out.append({"id": t["id"], "role": t["role"], "skills": list(t.get("skills", [])),
                    "from": hhmm(a), "to": hhmm(b), "from_min": a, "to_min": b,
                    "vehicle_needed": bool(t.get("vehicle")), "equipment_types": list(t.get("equipment", [])),
                    "not_same_as": list(t.get("not_same_as", [])),
                    "status": "planned", "declined_by": []})
    return out


if __name__ == "__main__":  # quick self-check on dev data
    import json
    import sys
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2]))
    from src.config import load_pack
    company, jobs, src = load_pack()
    job = {"id": "J2", "title": "Ditëlindje test", "zone": "Mitrovice", "tasks": expand_job(jobs["birthday_bounce"], "16:00")}
    print(json.dumps(plan_job(company, job, []), ensure_ascii=False, indent=1)[:3000])
