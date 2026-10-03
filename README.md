# AI Team Leader — Team Hi5

**Your leader talks to the client. The agent turns the deal into a plan and gives every person their task, in detail.**

An AI agent that works as a team leader and task delegator. It takes a job in free text, checks capacity (people, vehicles, equipment, travel, rules) in deterministic code, splits the job into tasks, assigns them, waits for the leader's approval, and then sends each worker a detailed task on Telegram with ACCEPT / CAN'T buttons. After that it follows the job through: check-ins, started/done progress, reassignment when someone drops out, and escalation to the leader when no safe replacement exists.

**The LLM understands, plans and writes. Code checks the rules. A human approves.**

Built at the Genpact AI Hackathon Kosovo 2026 (Agentic AI for Businesses), 3 October 2026. Real user: **Magic Events**, interviewed with permission (`docs/interview/notes.md`).

- Plan, criteria, industries, stack: [`PLAN.md`](PLAN.md)
- Who does what: [`TASKS.md`](TASKS.md)
- Problem evidence: [`docs/demand.md`](docs/demand.md) · competitors: [`docs/competitors.md`](docs/competitors.md)

## Rules the engine enforces

Rules live in `src/engine/planner.py`. They can't be overridden by the agent or the leader. Every rejection comes back as a sentence with the arithmetic (e.g. *"at 'J1' until 17:00; + 20 min travel = 17:20 > 14:20"*).

| Rule | What it checks |
|---|---|
| R1 | Worker has every skill the task needs |
| R2 | No overlap, travel time included |
| R3 | Max working hours per day |
| R4 | Nobody is booked without ACCEPT (enforced by the runtime) |
| R5 | Not unavailable, hasn't declined this task |
| R6 | Vehicles and equipment never double-booked |
| R7 | Four-eyes: reviewer can't be the person who did the work |

## Layout

| Folder | What |
|---|---|
| `src/engine/` | deterministic capacity check, rules, task assignment (no LLM) |
| `src/agent/` | Claude loop (`loop.py`), worker free-text intent (`worker_intent.py`) |
| `src/channels/` | Telegram bot |
| `src/dev_data/` | **demo data used on stage** (events company: Erza, Flutura, Dritoni, Blerta; vans, bounce castles, mascot) |
| `industries/` | config packs: `construction` and `it_services` have data; `events`, `corporate`, `_template` are README-only |
| `ui/` | management screen (offline, no CDN) |
| `tests/` | `expected.md`: hand-written expected outcomes for the engine (automated tests not written yet) |
| `scripts/` | `numbers.py`: derives the pitch metrics from an evidence run |
| `evidence/` | run outputs; every number in the deck comes from here |
| `pitch/` | deck, architecture figure, brief |
| `demo/` | demo script and pre-demo checklist |
| `docs/` | demand, competitors, interview notes; `archive/` = dropped ShiftRescue design |

## Run

```bash
pip install -r requirements.txt
cp .env.example .env        # ANTHROPIC_API_KEY (+ TELEGRAM_* for phones); never commit .env
python -m src.server        # http://localhost:8000  (UI from ui/, API under /api)
```

- **Data:** `INDUSTRY=events` (default) loads `industries/events/` if it has `company.json` + `jobs.json`; it doesn't yet, so it falls back to `src/dev_data/`. `INDUSTRY=construction` or `it_services` loads that pack. The UI can switch with `POST /api/industry`.
- **Without Telegram** the whole flow works from the UI (approve, accept/decline, check-in and progress buttons call the API).
- **Telegram:** create a bot with @BotFather → `TELEGRAM_BOT_TOKEN`. Everyone sends `/start` to the bot to get their chat_id, then map it: `TELEGRAM_IDENTITY_MAP=<chat_id>:leader,<chat_id>:w_erza,<chat_id>:w_flutura`.
- **Quick test without the server:** `python -m src.agent.loop "Birthday on Saturday 16:00 in Mitrovicë, bounce + mascot"`
- **Metrics from a run:** `python scripts/numbers.py` (reads `runtime/events.jsonl`)

Config in `.env`: `MODEL` (default `claude-opus-5-5`), `EFFORT` (default `medium`), `INDUSTRY`.

### API (for the UI)

| Method | Path | Body | What |
|---|---|---|---|
| GET | `/api/view` | — | job, tasks, workers, feed, blocked, existing jobs, `busy` |
| GET | `/api/health` | — | industry, data files in use, Telegram on/off |
| POST | `/api/message` | `{"text"}` | leader message → agent (async, 202; poll `/api/view`) |
| POST | `/api/approve` | `{"job_id": null}` | human approval → tasks sent to the crew |
| POST | `/api/callback` | `{"job_id","task_id","action":"accept"\|"decline"}` | worker accept/decline (phone fallback) |
| POST | `/api/checkin` | `{"job_id": null}` | ask every worker "Are you ready?" |
| POST | `/api/checkin_answer` | `{"job_id","task_id","ok"}` | ready / problem → reassign or escalate |
| POST | `/api/progress` | `{"job_id","task_id","kind":"start"\|"done"}` | started / finished |
| POST | `/api/worker_message` | `{"worker","text"}` | worker free text → same actions as the buttons |
| GET | `/api/report` | — | hours per person, overtime risk, late starts, problems |
| POST | `/api/industry` | `{"name"}` | switch industry pack (resets state) |
| POST | `/api/reset` | — | clean state before a demo (evidence log is kept) |

## Evidence (full run, 3 Oct 2026 16:45)

| Metric | Value |
|---|---|
| Leader message → plan proposed | **16 s** |
| Approval → all workers ACCEPT | **8 s** |
| Model cost for the plan | **~$0.03** |

Details: [`evidence/README.md`](evidence/README.md). The world is simulated; the workflow and the agent's behaviour are live.

## Known gaps

- No automated engine tests yet (`tests/test_engine.py` planned; cases in `tests/expected.md`).
- `industries/events/` has no data; the demo runs on `src/dev_data/`.
- State is a JSON file under `runtime/` with a lock: fine for a demo, not for multiple users.

Fictional company, synthetic data. No real customer data, no money amounts.
