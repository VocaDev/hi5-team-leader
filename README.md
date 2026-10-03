# ShiftRescue — Team Hi5

**One person goes missing. Your operation doesn't have to.**

An AI agent for businesses that run on people, schedules and fixed-time jobs. When someone can't come, it asks *"if I move this person, what breaks next?"*, finds the smallest safe change, offers the job on Telegram, books only after ACCEPT, verifies recovery, and escalates to the owner with options when there is no safe plan.

**The LLM understands and talks. Deterministic code decides.**

- Plan, criteria, scaling, stack, split: [`PLAN.md`](PLAN.md)
- Technical design: [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

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
