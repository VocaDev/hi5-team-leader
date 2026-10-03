# -*- coding: utf-8 -*-
"""Real-time supervision report: who is where in their work, hours per person (overtime risk), what went wrong."""
from __future__ import annotations

import datetime as dt

from . import state as S
from .config import load_pack
from .engine.planner import DEFAULT_MAX_HOURS, to_min


def _late(planned: str, actual: str | None) -> int:
    if not actual:
        return 0
    return max(0, to_min(actual[:5]) - to_min(planned))


def build() -> dict:
    company, _, _ = load_pack()
    with S.LOCK:
        st = S.load()
    names = {w["id"]: w["name"] for w in company["workers"]}
    minutes = {w["id"]: 0 for w in company["workers"]}
    for ej in company.get("existing_jobs", []):
        for wid in ej.get("assignments", {}):
            minutes[wid] = minutes.get(wid, 0) + to_min(ej["to"]) - to_min(ej["from"])
    same_day = company.get("company", {}).get("date") == dt.date.today().isoformat()  # late = only on the real day
    tasks_out, counts = [], {"accepted": 0, "declined": 0, "checkin_problems": 0, "started": 0, "done": 0, "late_starts": 0}
    for j in st["jobs"]:
        for t in j["tasks"]:
            if t.get("worker_id") and t.get("status") in ("sent", "accepted"):
                minutes[t["worker_id"]] = minutes.get(t["worker_id"], 0) + t["to_min"] - t["from_min"]
            counts["accepted"] += t.get("status") == "accepted"
            counts["declined"] += len(t.get("declined_by", []))
            counts["checkin_problems"] += t.get("checkin") == "problem"
            counts["started"] += bool(t.get("started_at"))
            counts["done"] += bool(t.get("done_at"))
            late = _late(t["from"], t.get("started_at")) if same_day else 0
            counts["late_starts"] += late > 0
            tasks_out.append({"job": j["title"], "task": t["role"], "worker": names.get(t.get("worker_id")),
                              "planned": f"{t['from']}–{t['to']}", "status": t.get("status"),
                              "started_at": t.get("started_at"), "done_at": t.get("done_at"),
                              "late_min": late, "checkin": t.get("checkin")})
    people = []
    for w in company["workers"]:
        m = minutes.get(w["id"], 0)
        mx = w.get("max_hours", DEFAULT_MAX_HOURS) * 60
        people.append({"name": w["name"], "hours_today": round(m / 60, 1), "max_hours": mx // 60,
                       "load_pct": round(100 * m / mx) if mx else 0,
                       "overtime_risk": m > 0.8 * mx})
    return {"generated_at": dt.datetime.now().strftime("%H:%M:%S"), "counts": counts,
            "people": people, "tasks": tasks_out, "blocked": st["blocked"][-10:]}
