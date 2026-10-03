# -*- coding: utf-8 -*-
"""Runtime state: one lock, atomic writes (temp file + os.replace), a live feed for the UI."""
from __future__ import annotations

import datetime as dt
import json
import os
import threading

from .config import EVENTS_FILE, STATE_FILE, current_industry, load_pack

LOCK = threading.RLock()


def _now() -> str:
    return dt.datetime.now().strftime("%H:%M:%S")


def empty_state() -> dict:
    return {"jobs": [], "feed": [], "blocked": [], "seq": 0, "busy": False}


def load() -> dict:
    with LOCK:
        if not STATE_FILE.exists():
            save(empty_state())
        return json.loads(STATE_FILE.read_text(encoding="utf-8"))


def save(state: dict) -> None:
    with LOCK:
        tmp = STATE_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        os.replace(tmp, STATE_FILE)


def reset() -> dict:
    with LOCK:
        st = empty_state()
        save(st)
        # keep events.jsonl (evidence across scenes); the UI feed starts clean
        feed(st, "system", "Gjendja u rivendos. Gati për punë të re.")
        return st


def feed(state: dict, kind: str, text: str, detail: dict | None = None) -> None:
    """Append one line to the live feed (UI) and to events.jsonl (evidence). Caller holds LOCK and saves."""
    state["seq"] = state.get("seq", 0) + 1
    item = {"n": state["seq"], "t": _now(), "type": kind, "text": text}
    state["feed"].append(item)
    state["feed"] = state["feed"][-200:]
    with EVENTS_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps({**item, "detail": detail or {}}, ensure_ascii=False) + "\n")
    save(state)


def log(kind: str, text: str, detail: dict | None = None) -> None:
    with LOCK:
        st = load()
        feed(st, kind, text, detail)


def job_by_id(state: dict, job_id: str) -> dict | None:
    return next((j for j in state["jobs"] if j["id"] == job_id), None)


def current_job(state: dict) -> dict | None:
    live = [j for j in state["jobs"] if j.get("status") != "cancelled"]
    return live[-1] if live else None


def view() -> dict:
    """The contract Erza's UI reads (TASKS.md -> view.json)."""
    company, _, _ = load_pack()
    with LOCK:
        st = load()
    job = current_job(st)
    names = {w["id"]: w["name"] for w in company["workers"]}
    res_names = {x["id"]: x["name"] for x in company.get("vehicles", []) + company.get("equipment", [])}
    assigned = {}
    for j in st["jobs"]:
        for t in j["tasks"]:
            if t.get("worker_id") and t.get("status") in ("planned", "sent", "accepted"):
                assigned[t["worker_id"]] = "assigned"
    busy_existing = {wid for ej in company.get("existing_jobs", []) for wid in ej.get("assignments", {})}
    workers = [{"id": w["id"], "name": w["name"], "skills": w.get("skills", []),
                "status": assigned.get(w["id"]) or ("busy" if w["id"] in busy_existing else "free")}
               for w in company["workers"]]
    out_job, tasks = None, []
    if job:
        out_job = {"id": job["id"], "title": job["title"], "client": job.get("client", ""), "zone": job["zone"],
                   "start": job["start"], "status": job["status"], "summary": job.get("summary", "")}
        for t in job["tasks"]:
            tasks.append({"id": t["id"], "role": t["role"], "worker": names.get(t.get("worker_id"), None),
                          "from": t["from"], "to": t["to"],
                          "bring": [res_names.get(r, r) for r in ([t.get("vehicle")] if t.get("vehicle") else []) + (t.get("equipment") or [])],
                          "status": t.get("status", "planned"), "note": t.get("note", ""),
                          "checkin": t.get("checkin"), "started_at": t.get("started_at"), "done_at": t.get("done_at")})
    return {"job": out_job, "tasks": tasks, "workers": workers, "feed": st["feed"][-60:], "blocked": st["blocked"][-10:],
            "existing_jobs": [{"title": e["title"], "zone": e["zone"], "from": e["from"], "to": e["to"],
                               "workers": [names.get(w, w) for w in e.get("assignments", {})]} for e in company.get("existing_jobs", [])],
            "busy": st.get("busy", False), "jobs_count": len(st["jobs"]),
            "industry": current_industry(), "company": company.get("company", {}).get("name", "")}
