# AI Team Leader — Team Hi5

**Your leader talks to the client. The agent turns the deal into a plan and gives every person their task, in detail.**

An AI agent that works as a team leader and task delegator: it takes a job in free text, checks capacity (people, vehicles, equipment, travel, rules) in deterministic code, splits the job into tasks, assigns them, gets the leader's approval, and sends each worker a detailed task on Telegram with ACCEPT / CAN'T buttons.

**The LLM understands, plans and writes. Code checks the rules. A human approves.**

- Plan, criteria, demand, industries, stack: [`PLAN.md`](PLAN.md)
- Who does what: [`TASKS.md`](TASKS.md)

## Layout

| Folder | What |
|---|---|
| `src/engine/` | deterministic capacity check, rules, task assignment (no LLM) |
| `src/agent/` | Claude loop, tools, prompt, validators |
| `src/channels/` | Telegram bot, stage console |
| `industries/` | one config pack per industry (`events` = demo, `corporate` = next, `_template`) |
| `ui/` | management screen (offline, no CDN) |
| `tests/` | engine tests T1–T6 + expected outcomes written by hand |
| `scripts/` | scenario runner, output checker, state reset |
| `evidence/` | run outputs (JSON); every number in the deck comes from here |
| `pitch/` | presentation |
| `demo/` | demo script (written by the team), phone setup, backup video |
| `docs/` | interview notes; `archive/` = dropped ShiftRescue design |

## Run

```bash
pip install -r requirements.txt
cp .env.example .env        # ANTHROPIC_API_KEY (+ TELEGRAM_* for phones); never commit .env
python -m src.server        # http://localhost:8000  (UI from ui/, API under /api)
```

- Data: `industries/events/company.json` + `jobs.json` if present, otherwise `src/dev_data/` (fallback).
- Without Telegram the whole flow works from the UI (approve + accept/decline buttons call the API).
- Telegram: create a bot with @BotFather → `TELEGRAM_BOT_TOKEN`. Everyone sends `/start` to the bot and gets their chat_id → `TELEGRAM_IDENTITY_MAP=chat:leader,chat:w_erioni,...`
- Quick test without the server: `python -m src.agent.loop "Ditëlindje të shtunën 16:00 në Mitrovicë, bounce + maskotë"`

### API (for the UI)
| Method | Path | Body | What |
|---|---|---|---|
| GET | `/api/view` | — | job, tasks, workers, feed, blocked, existing_jobs, busy |
| POST | `/api/message` | `{"text": "..."}` | leader message → agent (async, 202; poll `/api/view`, `busy` = agent working) |
| POST | `/api/approve` | `{"job_id": null}` | human approval → tasks sent to the crew |
| POST | `/api/callback` | `{"job_id","task_id","action":"accept"\|"decline"}` | phone fallback buttons |
| POST | `/api/reset` | — | clean state before a demo |

Fictional company, synthetic data. No real names, no money amounts.
