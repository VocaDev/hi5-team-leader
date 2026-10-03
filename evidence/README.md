# evidence

Every number in the deck comes from here or from the Magic Events interview (`docs/interview/notes.md`). Agent replies are never edited by hand.

## Full run, 3 Oct 2026 16:45 (`2026-10-03_1645_run/`)
| Metric | Value | Source |
|---|---|---|
| Leader message → plan proposed | **16 s** | `numbers.md`, `detail.duration_s` on the `PLAN_PROPOSED` reply |
| MIRATO → all workers ACCEPT | **8 s** | `numbers.md`, event timestamps (approval → "🎉 … konfirmuar") |
| Model cost for the measured plan | **~$0.03** | `numbers.md`, token usage × Opus 5.5 prices (cache-read price ❓ to confirm) |
| Engine checks / blocked rules in the run | 15 / 4 | `numbers.md` |

41 runtime events, derived with `scripts/numbers.py` (Devlete). Pitch [X] = **16 seconds**.
Files: `events.jsonl` (every step), `state.json` (final state), `numbers.md` (derived metrics).

The world (company, people, jobs) is simulated; the workflow and the agent's behaviour are real and live.
