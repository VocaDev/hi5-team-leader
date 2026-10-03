# Runtime presentation metrics

Source: `evidence/2026-10-03_1645_run/events.jsonl` (41 parsed event objects).

> All measured values below are derived from this event file. Unavailable means the needed event or field was not recorded.

## Leader message → planning reply

Planning replies found: **1** (selected the latest by event-file order).
- Selected latest: **16.0 seconds** from `detail.duration_s` on `reply` event n=23 (status `PLAN_PROPOSED`).

This duration is the runtime's measured agent call duration. The event schema does not record a distinct timestamp for when plan generation began or completed, so it is not independently recalculated from event timestamps.

## MIRATO → all workers ACCEPT

**8 seconds**

Calculation: `16:42:35` (event n=24, approval) → `16:42:43` (event n=33, all tasks confirmed). Elapsed wall-clock time from the logged `t` values.

Event identification: approval uses `type=accepted` and text containing `✅ Lideri e miratoi`; completion uses a later `type=accepted` event whose text contains `🎉` and `konfirmuar`, matching `src/runtime.py`.

## Engine checks and blocked rules

- `check` events: **15** (count of parsed objects with `type == "check"`).
- `blocked` events: **4** (count of parsed objects with `type == "blocked"`).

These counts cover the entire source file, not only one plan, because engine check/blocked events do not consistently carry a job identifier.

## Cost per plan

Plan reply: event n=23 (`detail.status=PLAN_PROPOSED`).
Token usage recorded on the `PLAN_PROPOSED` reply:
- `input_tokens`: 8 tokens
- `output_tokens`: 1203 tokens
- `cache_read_input_tokens`: 10732 tokens
- `cache_creation_input_tokens`: 734 tokens
- Priced-category subtotal: **$0.02990840** (8 × $4/1,000,000 + 1203 × $20/1,000,000 + 10732 × $0.2/1,000,000 + 734 × $5/1,000,000).
- Total for all recorded and priced categories: **$0.02990840**.
- Prices used: input $4/1M, output $20/1M, cache write $5/1M, cache read $0.20/1M.

## Schema notes

- Runtime timestamps are local `HH:MM:SS` strings without a date or timezone offset. Elapsed time assumes the selected events belong to the same run; if the clock time rolls backward, the calculation treats it as one midnight crossing.
- Runtime usage aggregates token fields across model calls and stores them on the final reply. It does not record per-call usage or a plan/job identifier in the usage object.
- Runtime `cache_creation_input_tokens` are priced as cache writes at $5 per 1M tokens.
- Counts are file-wide. Approval and completion are paired in event order, with the latest completed pair selected.
