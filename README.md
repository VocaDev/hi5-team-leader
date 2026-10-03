# AI Team Leader — Team Hi5

**Your leader talks to the client. The agent turns the deal into a plan and gives every person their task, in detail.**

An AI agent that works as a team leader and task delegator: it takes a job in free text, checks capacity (people, vehicles, equipment, travel, rules) in deterministic code, splits the job into tasks, assigns them, gets the leader's approval, and sends each worker a detailed task on Telegram with ACCEPT / CAN'T buttons.

**The LLM understands, plans and writes. Code checks the rules. A human approves.**

- Plan, criteria, demand, industries, stack: [`PLAN.md`](PLAN.md)

## Layout

| Folder | What |
|---|---|
| `src/engine/` | deterministic planner, rules, impact chain, recovery check (no LLM) |
| `src/agent/` | Claude loop, tools, prompt, validators |
| `src/channels/` | Telegram bot, stage console |
| `industries/` | one config pack per industry (`events` = demo, `corporate` = next, `_template`) |
| `ui/` | management screen (offline, no CDN) |
| `tests/` | engine tests T1–T6 + expected outcomes written by hand |
| `scripts/` | scenario runner, output checker, state reset |
| `evidence/` | run outputs (JSON); every number in the deck comes from here |
| `pitch/` | presentation |
| `demo/` | demo script (written by the team), phone setup, backup video |
| `docs/` | architecture, interview notes |

## Run (once the code exists)

```bash
pip install -r requirements.txt
cp .env.example .env   # fill in locally, never commit
python -m src.server
```

Fictional company, synthetic data. No real names, no money amounts.
