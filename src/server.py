# -*- coding: utf-8 -*-
"""
One process: API for the UI + the AI Team Leader + Telegram.

    python -m src.server            -> http://localhost:8000  (UI from ui/, API under /api)

API (contract in TASKS.md):
  GET  /api/view                      everything the UI shows
  POST /api/message   {text}          leader message -> agent (async; watch /api/view)
  POST /api/approve   {job_id?}       human approval -> tasks sent to the crew
  POST /api/callback  {job_id, task_id, action: accept|decline}   panel fallback for the phones
  POST /api/checkin   {job_id?}       ask everyone who accepted "are you ready?"
  POST /api/checkin_answer {job_id, task_id, ok}   panel fallback for the check-in buttons
  POST /api/industry  {name}          switch rulebook: "events" | "it_services" (resets state)
  POST /api/reset                     clean state before a demo
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from . import runtime as R
from . import state as S
from .config import UI_DIR, load_pack
from .channels import telegram_bot

app = FastAPI(title="AI Team Leader — Hi5")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
POOL = ThreadPoolExecutor(max_workers=2)
CONSOLE_HISTORY: list = []


class Msg(BaseModel):
    text: str


class Approve(BaseModel):
    job_id: str | None = None


class Industry(BaseModel):
    name: str


class CheckinAnswer(BaseModel):
    job_id: str
    task_id: str
    ok: bool


class Callback(BaseModel):
    job_id: str
    task_id: str
    action: str


@app.get("/api/view")
def api_view():
    return S.view()


@app.get("/api/health")
def api_health():
    from .config import current_industry
    _, _, src = load_pack()
    return {"ok": True, "industry": current_industry(), "data": src, "telegram": R.notifier is not None}


def _run_console(text: str) -> None:
    global CONSOLE_HISTORY
    from .agent.loop import run
    res = run(text, history=CONSOLE_HISTORY[-12:])
    CONSOLE_HISTORY = res.get("history") or CONSOLE_HISTORY


@app.post("/api/message", status_code=202)
def api_message(m: Msg):
    if not m.text.strip():
        return JSONResponse({"error": "empty"}, status_code=400)
    if S.load().get("busy"):
        return JSONResponse({"error": "agent is busy, wait a few seconds"}, status_code=409)
    POOL.submit(_run_console, m.text.strip())
    return {"accepted": True}


@app.post("/api/approve")
def api_approve(a: Approve):
    return R.approve(a.job_id, by="paneli")


@app.post("/api/callback")
def api_callback(c: Callback):
    return R.respond(c.job_id, c.task_id, None, accept=c.action == "accept")


@app.post("/api/checkin")
def api_checkin(a: Approve):
    return R.checkin(a.job_id)


@app.post("/api/checkin_answer")
def api_checkin_answer(c: CheckinAnswer):
    return R.checkin_answer(c.job_id, c.task_id, None, ok=c.ok)


@app.post("/api/industry")
def api_industry(i: Industry):
    from .config import ROOT, set_industry
    if i.name != "events" and not (ROOT / "industries" / i.name / "company.json").exists():
        return JSONResponse({"error": f"unknown industry {i.name}"}, status_code=400)
    set_industry(i.name)
    return {**api_reset(), "industry": i.name}


@app.post("/api/reset")
def api_reset():
    global CONSOLE_HISTORY
    CONSOLE_HISTORY = []
    if R.notifier:
        R.notifier.leader_history = []
    S.reset()
    return {"ok": True}


@app.on_event("startup")
def _startup() -> None:
    S.load()
    telegram_bot.start()


if UI_DIR.exists() and (UI_DIR / "index.html").exists():
    app.mount("/", StaticFiles(directory=UI_DIR, html=True), name="ui")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
