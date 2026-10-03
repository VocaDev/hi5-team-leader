# -*- coding: utf-8 -*-
"""Paths, .env and the industry pack (company + job templates)."""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:  # noqa: BLE001
    pass

INDUSTRY = os.getenv("INDUSTRY", "events").strip() or "events"
MODEL = os.getenv("MODEL", "claude-opus-5-5").strip() or "claude-opus-5-5"
RUNTIME = ROOT / "runtime"
RUNTIME.mkdir(exist_ok=True)
STATE_FILE = RUNTIME / "state.json"
EVENTS_FILE = RUNTIME / "events.jsonl"
UI_DIR = ROOT / "ui"


def _pack_file(name: str) -> Path:
    """Flutura's pack in industries/<INDUSTRY>/ wins; src/dev_data/ is the fallback until it lands."""
    real = ROOT / "industries" / INDUSTRY / name
    return real if real.exists() else Path(__file__).resolve().parent / "dev_data" / name


def load_pack() -> tuple[dict, dict, dict]:
    company_path, jobs_path = _pack_file("company.json"), _pack_file("jobs.json")
    company = json.loads(company_path.read_text(encoding="utf-8"))
    jobs = json.loads(jobs_path.read_text(encoding="utf-8"))
    return company, jobs, {"company": str(company_path.relative_to(ROOT)), "jobs": str(jobs_path.relative_to(ROOT))}
