# -*- coding: utf-8 -*-
"""
Runtime actions. Everything that changes the plan goes through here and through the engine.

The model can create a job, ask for a person and propose a plan. It can NOT approve a plan
(only the human leader: UI button or Telegram button) and it can NOT book anyone (only ACCEPT does).
"""
from __future__ import annotations

from . import state as S
from .config import load_pack
from .engine.planner import expand_job, find_worker, plan_job, validate_manual, worker_by_id

notifier = None  # set by channels.telegram_bot when Telegram is running: object with send_task(), send_leader()


def _other_jobs(st: dict, job_id: str) -> list[dict]:
    return [j for j in st["jobs"] if j["id"] != job_id]


def _apply_plan(job: dict, plan: dict) -> None:
    by_id = {t["id"]: t for t in plan["tasks"]}
    for t in job["tasks"]:
        p = by_id[t["id"]]
        for k in ("worker_id", "vehicle", "equipment"):
            t[k] = p.get(k)
    job["uncovered"] = plan["uncovered"]
    job["missing_resources"] = plan["missing_resources"]
    job["feasible"] = plan["feasible"]


def _log_plan(st: dict, job: dict, plan: dict, company: dict) -> None:
    for line in plan["resource_log"]:
        S.feed(st, "check" if line.startswith("OK") else "blocked", line)
    for t in plan["tasks"]:
        for r in plan["rejected"].get(t["id"], [])[:2]:
            S.feed(st, "check", f"✗ {t['role']}: {r['reasons'][0]}")
        if t.get("worker"):
            S.feed(st, "check", f"✓ {t['role']} {t['from']}–{t['to']} → {t['worker']}")
    for u in plan["uncovered"]:
        S.feed(st, "blocked", f"❌ {u['role']}: s'ka njeri të lirë që i plotëson rregullat")


def _summary(job: dict, company: dict) -> dict:
    return {
        "job_id": job["id"], "title": job["title"], "zone": job["zone"], "start": job["start"],
        "feasible": job.get("feasible"),
        "tasks": [{"task_id": t["id"], "role": t["role"], "from": t["from"], "to": t["to"],
                   "worker": (worker_by_id(company, t["worker_id"]) or {}).get("name") if t.get("worker_id") else None,
                   "vehicle": t.get("vehicle"), "equipment": t.get("equipment"), "status": t.get("status")}
                  for t in job["tasks"]],
        "uncovered": job.get("uncovered", []), "missing_resources": job.get("missing_resources", []),
    }


# ---------------------------------------------------------------- model-visible actions

def create_job(template_id: str, title: str, client: str, zone: str, start: str, notes: str) -> dict:
    company, jobs, _ = load_pack()
    if template_id not in jobs:
        return {"error": f"unknown template_id {template_id}"}
    if zone not in company.get("zones", []):
        return {"error": f"unknown zone {zone}; known: {company.get('zones')}"}
    try:
        tasks = expand_job(jobs[template_id], start)
    except Exception:  # noqa: BLE001
        return {"error": "start must be HH:MM"}
    with S.LOCK:
        st = S.load()
        job = {"id": f"J{len(st['jobs']) + 2}", "title": title, "client": client, "zone": zone, "start": start,
               "template": template_id, "notes": notes, "status": "draft", "tasks": tasks, "summary": ""}
        plan = plan_job(company, job, _other_jobs(st, job["id"]))
        _apply_plan(job, plan)
        st["jobs"].append(job)
        S.feed(st, "tool", f"Puna e re: {title} · {zone} · {start} · {len(tasks)} detyra")
        _log_plan(st, job, plan, company)
        S.save(st)
        return _summary(job, company)


def assign_manual(job_id: str, task_id: str, worker_name: str) -> dict:
    company, _, _ = load_pack()
    with S.LOCK:
        st = S.load()
        job = S.job_by_id(st, job_id)
        if not job or not any(t["id"] == task_id for t in job["tasks"]):
            return {"error": "unknown job_id or task_id"}
        wk = find_worker(company, worker_name)
        if not wk:
            return {"error": f"no worker matches '{worker_name}'", "workers": [w["name"] for w in company["workers"]]}
        reasons = validate_manual(company, job, _other_jobs(st, job_id), task_id, wk["id"])
        if reasons:
            st["blocked"].append({"text": f"BLOCKED: {wk['name']} → {task_id}. " + " · ".join(reasons)})
            S.feed(st, "blocked", f"⛔ BLOCKED: {wk['name']} s'mund të marrë '{task_id}'. {reasons[0]}")
            S.save(st)
            return {"status": "BLOCKED", "worker": wk["name"], "task_id": task_id, "rule_violations": reasons,
                    "note": "Rules are enforced in code and cannot be overridden by anyone."}
        locked = {t["id"]: t["worker_id"] for t in job["tasks"] if t.get("status") == "accepted" and t.get("worker_id")}
        locked[task_id] = wk["id"]
        plan = plan_job(company, job, _other_jobs(st, job_id), locked=locked)
        _apply_plan(job, plan)
        S.feed(st, "tool", f"Lideri kërkoi {wk['name']} për '{task_id}' → rregullat OK, plani u rillogarit")
        S.save(st)
        return {"status": "OK", **_summary(job, company)}


def propose_plan(job_id: str, summary: str, notes: list[dict]) -> dict:
    company, _, _ = load_pack()
    with S.LOCK:
        st = S.load()
        job = S.job_by_id(st, job_id)
        if not job:
            return {"error": "unknown job_id"}
        if any(not t.get("worker_id") for t in job["tasks"]):
            return {"error": "plan has uncovered tasks; tell the leader what is missing instead of proposing",
                    "uncovered": job.get("uncovered")}
        by = {n["task_id"]: n["note"] for n in notes}
        for t in job["tasks"]:
            t["note"] = by.get(t["id"], "")[:300]
        job["summary"] = summary
        job["status"] = "awaiting_approval"
        S.feed(st, "tool", "📋 Plani gati — pret miratimin e liderit (butoni MIRATO)")
        S.save(st)
    if notifier:
        notifier.ask_approval(job_id, summary)
    return {"status": "awaiting_approval", "job_id": job_id,
            "note": "Only the human leader can approve. Do not tell the leader it is approved."}


def get_state() -> dict:
    company, _, _ = load_pack()
    with S.LOCK:
        st = S.load()
    return {"jobs": [_summary(j, company) | {"status": j["status"]} for j in st["jobs"]]}


# ---------------------------------------------------------------- human / channel actions (not model tools)

def briefing_text(job: dict, task: dict, company: dict) -> str:
    names = {w["id"]: w["name"] for w in company["workers"]}
    res = {x["id"]: x["name"] for x in company.get("vehicles", []) + company.get("equipment", [])}
    bring = [res.get(r, r) for r in ([task.get("vehicle")] if task.get("vehicle") else []) + (task.get("equipment") or [])]
    mates = [f"{names.get(t['worker_id'])} ({t['role']})" for t in job["tasks"]
             if t.get("worker_id") and t.get("worker_id") != task.get("worker_id")]
    date = company.get("company", {}).get("date", "")
    lines = [f"📋 Detyra jote — {date}",
             f"Puna: {job['title']} · {job['zone']} · nis {job['start']}",
             f"Roli: {task['role']}",
             f"Koha: {task['from']}–{task['to']}"]
    if bring:
        lines.append("Merr me vete: " + ", ".join(bring))
    if mates:
        lines.append("Me ty: " + ", ".join(sorted(set(mates))))
    if task.get("note"):
        lines.append(f"Shënim: {task['note']}")
    lines.append("Kontakti i klientit: te lideri")
    return "\n".join(lines)


def approve(job_id: str | None = None, by: str = "leader") -> dict:
    company, _, _ = load_pack()
    with S.LOCK:
        st = S.load()
        job = S.job_by_id(st, job_id) if job_id else S.current_job(st)
        if not job or job["status"] != "awaiting_approval":
            return {"error": "no plan awaiting approval"}
        job["status"] = "sent"
        S.feed(st, "accepted", f"✅ Lideri e miratoi planin ({by}). Detyrat po dërgohen…")
        to_send = []
        for t in job["tasks"]:
            t["status"] = "sent"
            to_send.append((job, t))
        S.save(st)
    for job, t in to_send:
        _dispatch(job, t, company)
    return {"status": "sent", "job_id": job["id"]}


def _dispatch(job: dict, task: dict, company: dict) -> None:
    name = (worker_by_id(company, task["worker_id"]) or {}).get("name", "?")
    delivered = notifier.send_task(task["worker_id"], job["id"], task["id"], briefing_text(job, task, company)) if notifier else False
    S.log("sent", f"📨 {name}: '{task['role']}' {task['from']}–{task['to']}" + (" · Telegram" if delivered else " · paneli"))


def respond(job_id: str, task_id: str, worker_id: str | None, accept: bool) -> dict:
    """ACCEPT / CAN'T from a worker. worker_id comes from the channel (Telegram chat id map) or the UI panel."""
    company, _, _ = load_pack()
    with S.LOCK:
        st = S.load()
        job = S.job_by_id(st, job_id)
        task = next((t for t in (job or {}).get("tasks", []) if t["id"] == task_id), None)
        if not job or not task:
            return {"error": "unknown job/task"}
        if worker_id and task.get("worker_id") != worker_id:
            return {"error": "this task is no longer yours", "stale": True}
        if task["status"] != "sent":
            return {"error": f"task is {task['status']}", "stale": True}
        name = (worker_by_id(company, task["worker_id"]) or {}).get("name", "?")
        if accept:
            reasons = validate_manual(company, job, _other_jobs(st, job_id), task_id, task["worker_id"])
            if reasons:
                S.feed(st, "blocked", f"⛔ {name} pranoi, por rregullat s'lejojnë më: {reasons[0]}")
                accept = False
            else:
                task["status"] = "accepted"
                S.feed(st, "accepted", f"✅ {name} pranoi '{task['role']}'")
                if notifier:
                    notifier.send_progress(task["worker_id"], job_id, task_id, task["role"])
                if all(t["status"] == "accepted" for t in job["tasks"]):
                    job["status"] = "confirmed"
                    S.feed(st, "accepted", f"🎉 Të gjitha detyrat u pranuan. '{job['title']}' është konfirmuar.")
                    S.save(st)
                    if notifier:
                        notifier.send_leader(f"🎉 '{job['title']}' u konfirmua: të gjithë pranuan.")
                    return {"status": "accepted", "job": "confirmed"}
                S.save(st)
                return {"status": "accepted"}
        # decline -> next suitable person, same rules
        task["declined_by"] = list(set(task.get("declined_by", []) + [task["worker_id"]]))
        task["status"] = "planned"
        old = task["worker_id"]
        task["worker_id"] = None
        S.feed(st, "blocked", f"↩️ {name} s'mundet për '{task['role']}' → po kërkoj tjetrin…")
        locked = {t["id"]: t["worker_id"] for t in job["tasks"] if t["id"] != task_id and t.get("worker_id")}
        plan = plan_job(company, job, _other_jobs(st, job_id), locked=locked)
        new = next(t for t in plan["tasks"] if t["id"] == task_id)
        if new.get("worker_id"):
            task["worker_id"] = new["worker_id"]
            task["status"] = "sent"
            new_name = new["worker"]
            S.feed(st, "check", f"✓ '{task['role']}' → {new_name} (rregullat OK)")
            S.save(st)
            msg = f"↩️ {name} s'mundet për '{task['role']}'. Detyra iu dërgua {new_name}."
            if notifier:
                notifier.send_leader(msg)
            _dispatch(job, task, company)
            return {"status": "reassigned", "from": old, "to": new["worker_id"]}
        why = next((u["why"] for u in plan["uncovered"] if u["task_id"] == task_id), [])
        st["blocked"].append({"text": f"S'ka zëvendësues për '{task['role']}': " + " · ".join(why[:3])})
        S.feed(st, "blocked", f"🔺 S'ka zëvendësues për '{task['role']}' → vendos lideri")
        S.save(st)
        if notifier:
            notifier.send_leader(f"🔺 {name} s'mundet për '{task['role']}' dhe s'ka tjetër që i plotëson rregullat. Duhet vendimi yt.")
        return {"status": "escalated", "why": why}


# ---------------------------------------------------------------- check-in before the work (habits, not heroics)

def checkin(job_id: str | None = None) -> dict:
    """Ask everyone who accepted: are you ready? Problems surface an hour early, not 30 minutes before."""
    company, _, _ = load_pack()
    with S.LOCK:
        st = S.load()
        job = S.job_by_id(st, job_id) if job_id else S.current_job(st)
        if not job:
            return {"error": "no job"}
        targets = [t for t in job["tasks"] if t.get("status") == "accepted" and t.get("worker_id")]
        for t in targets:
            t["checkin"] = "asked"
        S.feed(st, "tool", f"⏰ Check-in para punës: {len(targets)} veta u pyetën 'A je gati?'")
        S.save(st)
    for t in targets:
        text = (f"⏰ Check-in · {job['title']}\nRoli yt: {t['role']} {t['from']}–{t['to']}\n"
                f"A je gati? (orari, transporti, gjërat që merr me vete)")
        if notifier:
            notifier.send_checkin(t["worker_id"], job["id"], t["id"], text)
    return {"status": "asked", "count": len(targets), "job_id": job["id"]}


def checkin_answer(job_id: str, task_id: str, worker_id: str | None, ok: bool) -> dict:
    company, _, _ = load_pack()
    with S.LOCK:
        st = S.load()
        job = S.job_by_id(st, job_id)
        task = next((t for t in (job or {}).get("tasks", []) if t["id"] == task_id), None)
        if not job or not task or task.get("status") != "accepted":
            return {"error": "no active task", "stale": True}
        if worker_id and task.get("worker_id") != worker_id:
            return {"error": "this task is no longer yours", "stale": True}
        name = (worker_by_id(company, task["worker_id"]) or {}).get("name", "?")
        if ok:
            task["checkin"] = "ok"
            S.feed(st, "accepted", f"👍 {name} është gati për '{task['role']}'")
            S.save(st)
            return {"status": "ready"}
        task["checkin"] = "problem"
        task["status"] = "sent"  # reopen, then the normal decline path finds the next safe person
        if job.get("status") == "confirmed":
            job["status"] = "sent"
        S.feed(st, "blocked", f"⚠️ Check-in: {name} ka problem me '{task['role']}' → zgjidhet tani, jo në minutën e fundit")
        S.save(st)
    return respond(job_id, task_id, None, accept=False)


# ---------------------------------------------------------------- real-time progress (started / done)

def progress(job_id: str, task_id: str, worker_id: str | None, kind: str) -> dict:
    import datetime as _dt
    company, _, _ = load_pack()
    with S.LOCK:
        st = S.load()
        job = S.job_by_id(st, job_id)
        task = next((t for t in (job or {}).get("tasks", []) if t["id"] == task_id), None)
        if not job or not task or task.get("status") != "accepted":
            return {"error": "no active task", "stale": True}
        if worker_id and task.get("worker_id") != worker_id:
            return {"error": "this task is no longer yours", "stale": True}
        name = (worker_by_id(company, task["worker_id"]) or {}).get("name", "?")
        now = _dt.datetime.now().strftime("%H:%M:%S")
        if kind == "start":
            task["started_at"] = now
            S.feed(st, "tool", f"🚗 {name} e nisi '{task['role']}' ({now[:5]}, planifikuar {task['from']})")
        else:
            task["done_at"] = now
            S.feed(st, "accepted", f"✅ {name} e përfundoi '{task['role']}' ({now[:5]}, planifikuar deri {task['to']})")
            if all(x.get("done_at") for x in job["tasks"]):
                job["status"] = "done"
                S.feed(st, "accepted", f"🏁 '{job['title']}' përfundoi. Raporti: GET /api/report")
        S.save(st)
    if notifier:
        verb = "e nisi" if kind == "start" else "e përfundoi"
        notifier.send_leader(f"{'🚗' if kind == 'start' else '✅'} {name} {verb} '{task['role']}' në {now[:5]}.")
        if kind == "done" and job.get("status") == "done":
            notifier.send_leader(f"🏁 '{job['title']}' përfundoi. Të gjitha detyrat u kryen.")
    return {"status": kind, "at": now}
