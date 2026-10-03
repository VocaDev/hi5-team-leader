# -*- coding: utf-8 -*-
"""
Understand a worker's free text ("e përfundova", "s'muj sot", "jam rrugës") and turn it into the same
actions as the buttons. The model only classifies; the runtime does the action with the usual checks.
Keyword fallback if the model call fails, so a worker is never ignored.
"""
from __future__ import annotations

import json
import re

import anthropic

from .. import runtime as R
from .. import state as S
from ..config import MODEL, load_pack

INTENTS = ["accept", "decline", "ready", "problem", "started", "done", "other"]

KEYWORDS = [
    ("done", r"p[eë]rfundo|mbaro|e kreva|kreva|u kry|done|finish|e kryva|perfundum"),
    ("started", r"e nisa|u nisa|nisem|jam rrug|fillova|kom nis|kam nis|started|on my way"),
    ("problem", r"problem|s'?mu[nj]|nuk mu[nj]|s'?vij|nuk vij|s[eë]mur|smut|s'?mundem|nuk mundem|vonohem"),
    ("decline", r"refuzoj|nuk e pranoj|s'?e pranoj"),
    ("ready", r"\bgati\b|jam gati|ready"),
    ("accept", r"\bpo\b|\bok\b|okej|pranoj|e pranoj|accept|dakord|n[eë] rregull"),
]


def _keyword(text: str) -> str:
    t = text.lower()
    for intent, rx in KEYWORDS:
        if re.search(rx, t):
            return intent
    return "other"


def _my_tasks(worker_id: str) -> tuple[dict | None, list[dict]]:
    with S.LOCK:
        st = S.load()
    job = S.current_job(st)
    if not job:
        return None, []
    return job, [t for t in job["tasks"] if t.get("worker_id") == worker_id and t.get("status") in ("sent", "accepted")]


def _classify(text: str, tasks: list[dict]) -> dict:
    tools = [{
        "name": "classify", "strict": True,
        "description": "Classify the worker's message about their tasks.",
        "input_schema": {"type": "object", "additionalProperties": False, "required": ["intent", "task_id"],
                         "properties": {"intent": {"type": "string", "enum": INTENTS},
                                        "task_id": {"type": "string", "description": "one of the task ids, or '' if unclear"}}},
    }]
    ctx = [{"task_id": t["id"], "role": t["role"], "time": f"{t['from']}-{t['to']}", "status": t["status"],
            "checkin": t.get("checkin"), "started": bool(t.get("started_at")), "done": bool(t.get("done_at"))} for t in tasks]
    msg = anthropic.Anthropic().messages.create(
        model=MODEL, max_tokens=2000, output_config={"effort": "low"}, tools=tools,
        system=("You read short messages from field workers (Albanian, Gheg or English) and classify them. "
                "accept = takes the offered task; decline = refuses an offered task; ready = answers a check-in that "
                "they are ready; problem = cannot do it / sick / late / any blocker; started = has started or is on the way; "
                "done = finished the work; other = anything else. Pick the task the message is about (if one task, that one). "
                "Always answer by calling classify."),
        messages=[{"role": "user", "content": f"Worker tasks: {json.dumps(ctx, ensure_ascii=False)}\nMessage: {text}"}],
    )
    for b in msg.content:
        if b.type == "tool_use" and b.name == "classify":
            return dict(b.input)
    raise RuntimeError("no classification")


def handle(worker_id: str, name: str, text: str) -> str:
    """Returns the reply for the worker. Logs everything to the feed; notifies the leader."""
    job, tasks = _my_tasks(worker_id)
    S.log("message", f"💬 {name}: {text}")
    if not job or not tasks:
        if R.notifier:
            R.notifier.send_leader(f"💬 {name}: {text}")
        return "E mora dhe ia kalova liderit. Për momentin s'ke detyrë aktive."
    try:
        c = _classify(text, tasks)
        how = "AI"
    except Exception:  # noqa: BLE001 — never ignore a worker
        c = {"intent": _keyword(text), "task_id": ""}
        how = "fjalë kyçe"
    intent = c.get("intent", "other")
    task = next((t for t in tasks if t["id"] == c.get("task_id")), None)
    if not task:  # pick the most relevant task for the intent
        pref = {"accept": "sent", "decline": "sent"}.get(intent)
        cands = [t for t in tasks if t["status"] == pref] if pref else [t for t in tasks if t["status"] == "accepted"]
        if intent == "done":
            cands = [t for t in cands if t.get("started_at") and not t.get("done_at")] or [t for t in cands if not t.get("done_at")]
        task = (cands or tasks)[0]
    S.log("tool", f"🧠 Kuptova ({how}): {name} → {intent} · '{task['role']}'")
    jid, tid = job["id"], task["id"]

    if intent == "accept" and any(t["status"] == "sent" for t in tasks):
        sent = [t for t in tasks if t["status"] == "sent"]
        for t in sent:  # "po / ok" means yes to everything offered to me
            R.respond(jid, t["id"], worker_id, accept=True)
        return "✅ U regjistrua: i pranove " + ", ".join(f"'{t['role']}' ({t['from']}–{t['to']})" for t in sent) + "."
    if intent in ("decline", "problem") and task["status"] == "sent":
        R.respond(jid, tid, worker_id, accept=False)
        return "U regjistrua. Detyra i kalon dikujt tjetër ose liderit."
    if intent == "problem" and task["status"] == "accepted":
        R.checkin_answer(jid, tid, worker_id, ok=False)
        return "⚠️ E njoftova liderin. Po kërkohet zgjidhje."
    if intent == "ready" and task["status"] == "accepted":
        R.checkin_answer(jid, tid, worker_id, ok=True)
        return "👍 Faleminderit, suksese!"
    if intent == "started" and task["status"] == "accepted":
        R.progress(jid, tid, worker_id, "start")
        return f"🚗 U regjistrua nisja e '{task['role']}'."
    if intent == "done" and task["status"] == "accepted":
        if not task.get("started_at"):
            R.progress(jid, tid, worker_id, "start")
        R.progress(jid, tid, worker_id, "done")
        return f"✅ U regjistrua: '{task['role']}' përfundoi. Faleminderit!"
    if R.notifier:
        R.notifier.send_leader(f"💬 {name}: {text}")
    return "E mora dhe ia kalova liderit."
