#!/usr/bin/env python3
"""Derive auditable presentation metrics from runtime/events.jsonl."""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EVENTS = ROOT / "runtime" / "events.jsonl"
DEFAULT_OUTPUT = ROOT / "evidence" / "numbers.md"
PLAN_REPLY_STATUS = "PLAN_PROPOSED"
APPROVAL_MARKER = "✅ Lideri e miratoi"
CONFIRMED_MARKER = "🎉"
PRICE_PER_MILLION = {
    "input_tokens": 4.00,
    "output_tokens": 20.00,
    "cache_creation_input_tokens": 5.00,
    "cache_read_input_tokens": 0.20,
}
USAGE_CATEGORIES = (
    "input_tokens",
    "output_tokens",
    "cache_read_input_tokens",
    "cache_creation_input_tokens",
)


class EventFileError(Exception):
    """A source file exists but cannot be used as event data."""


def load_events(path: Path) -> list[dict[str, Any]]:
    if not path.is_file():
        raise FileNotFoundError(f"Events file not found: {path}")
    events: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as stream:
            for line_number, line in enumerate(stream, 1):
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise EventFileError(
                        f"Malformed JSON at {path}:{line_number}: {exc.msg} (column {exc.colno})"
                    ) from exc
                if not isinstance(event, dict):
                    raise EventFileError(
                        f"Invalid event at {path}:{line_number}: expected a JSON object, got {type(event).__name__}"
                    )
                events.append(event)
    except UnicodeDecodeError as exc:
        raise EventFileError(f"Events file is not valid UTF-8: {path}: {exc}") from exc
    return events


def format_number(value: float, places: int = 1) -> str:
    return f"{value:.{places}f}"


def plan_replies(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        event for event in events
        if event.get("type") == "reply"
        and isinstance(event.get("detail"), dict)
        and event["detail"].get("status") == PLAN_REPLY_STATUS
    ]


def valid_nonnegative_number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    value = float(value)
    return value if math.isfinite(value) and value >= 0 else None


def usage_report(reply: dict[str, Any]) -> tuple[str, list[str]]:
    detail = reply.get("detail")
    usage = detail.get("usage") if isinstance(detail, dict) else None
    if not isinstance(usage, dict):
        return "Unavailable: this planning reply has no `detail.usage` object.", [
            "No token categories or cost could be derived."
        ]

    present: dict[str, float] = {}
    invalid: list[str] = []
    for category in USAGE_CATEGORIES:
        if category in usage:
            parsed = valid_nonnegative_number(usage[category])
            if parsed is None:
                invalid.append(category)
            else:
                present[category] = parsed

    if not present:
        reason = "No recognized token usage categories are present."
        if invalid:
            reason += " Invalid values: " + ", ".join(invalid) + "."
        return "Unavailable: " + reason, [reason]

    lines = ["Token usage recorded on the `PLAN_PROPOSED` reply:"]
    for category, tokens in present.items():
        lines.append(f"- `{category}`: {tokens:g} tokens")
    if invalid:
        lines.append("- Invalid values ignored: " + ", ".join(f"`{x}`" for x in invalid))

    priced = {key: value for key, value in present.items() if key in PRICE_PER_MILLION}
    excluded = [key for key in present if key not in PRICE_PER_MILLION]
    if not priced:
        lines.append("- Cost: unavailable; this runtime usage contains no categories with a supplied price.")
        return "\n".join(lines), lines

    subtotal = sum(tokens * PRICE_PER_MILLION[key] / 1_000_000 for key, tokens in priced.items())
    calc = " + ".join(
        f"{tokens:g} × ${PRICE_PER_MILLION[key]:g}/1,000,000"
        for key, tokens in priced.items()
    )
    lines.append(f"- Priced-category subtotal: **${subtotal:.8f}** ({calc}).")
    if excluded:
        lines.append(
            "- Total cost: **unavailable** because these recorded categories have no supplied price: "
            + ", ".join(f"`{key}`" for key in excluded)
            + "."
        )
    elif set(priced) != set(PRICE_PER_MILLION):
        missing = sorted(set(PRICE_PER_MILLION) - set(priced))
        lines.append(
            "- Total cost: **unavailable**; only recorded and priced categories are included above. "
            "Missing priced categories: " + ", ".join(f"`{key}`" for key in missing) + "."
        )
    else:
        lines.append("- Total for all recorded and priced categories: **${:.8f}**.".format(subtotal))
    lines.append("- Prices used: input $4/1M, output $20/1M, cache write $5/1M, cache read $0.20/1M.")
    return "\n".join(lines), lines


def parse_clock(value: Any) -> datetime | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d{2}:\d{2}:\d{2}", value):
        return None
    try:
        return datetime.strptime(value, "%H:%M:%S")
    except ValueError:
        return None


def elapsed_seconds(start: dict[str, Any], end: dict[str, Any]) -> tuple[float | None, str]:
    start_t, end_t = parse_clock(start.get("t")), parse_clock(end.get("t"))
    if start_t is None or end_t is None:
        return None, "A required event has no valid `HH:MM:SS` timestamp."
    delta = end_t - start_t
    if delta.total_seconds() < 0:
        delta += timedelta(days=1)
    return delta.total_seconds(), "Elapsed wall-clock time from the logged `t` values."


def latest_approval_confirmation(events: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    pairs: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for index, event in enumerate(events):
        if event.get("type") != "accepted" or APPROVAL_MARKER not in str(event.get("text", "")):
            continue
        confirmation = next(
            (
                later for later in events[index + 1:]
                if later.get("type") == "accepted"
                and CONFIRMED_MARKER in str(later.get("text", ""))
                and "konfirmuar" in str(later.get("text", "")).casefold()
            ),
            None,
        )
        if confirmation is not None:
            pairs.append((event, confirmation))
    if pairs:
        return pairs[-1]
    return None, None


def metric_elapsed(events: list[dict[str, Any]]) -> str:
    approvals = [
        event for event in events
        if event.get("type") == "accepted" and APPROVAL_MARKER in str(event.get("text", ""))
    ]
    confirmations = [
        event for event in events
        if event.get("type") == "accepted"
        and CONFIRMED_MARKER in str(event.get("text", ""))
        and "konfirmuar" in str(event.get("text", "")).casefold()
    ]
    start, end = latest_approval_confirmation(events)
    if not approvals or not confirmations or start is None or end is None:
        missing = []
        if not approvals:
            missing.append("approval event `type=accepted` containing `✅ Lideri e miratoi`")
        if not confirmations:
            missing.append("confirmation event `type=accepted` containing `🎉` and `konfirmuar`")
        if approvals and confirmations and (start is None or end is None):
            missing.append("a confirmation event after an approval")
        return "Unavailable: missing " + ", ".join(missing) + "."
    seconds, reason = elapsed_seconds(start, end)
    if seconds is None:
        return "Unavailable: " + reason
    return (
        f"**{seconds:g} seconds**\n\n"
        f"Calculation: `{start.get('t')}` (event n={start.get('n', 'not recorded')}, approval) "
        f"→ `{end.get('t')}` (event n={end.get('n', 'not recorded')}, all tasks confirmed). {reason}"
    )


def build_report(events: list[dict[str, Any]], source: Path) -> str:
    replies = plan_replies(events)
    checks = sum(event.get("type") == "check" for event in events)
    blocked = sum(event.get("type") == "blocked" for event in events)

    parts = [
        "# Runtime presentation metrics",
        "",
        f"Source: `{source.as_posix()}` ({len(events)} parsed event objects).",
        "",
        "> All measured values below are derived from this event file. Unavailable means the needed event or field was not recorded.",
        "",
        "## Leader message → planning reply",
        "",
    ]
    if not replies:
        parts.append(
            "**Unavailable:** no `type=reply` event has `detail.status == \"PLAN_PROPOSED\"`. "
            "This status is the runtime's signal that the model proposed a plan; other reply statuses may be clarifications or errors."
        )
    else:
        parts.append(f"Planning replies found: **{len(replies)}** (selected the latest by event-file order).")
        for index, reply in enumerate(replies, 1):
            detail = reply.get("detail") or {}
            duration = valid_nonnegative_number(detail.get("duration_s"))
            label = "Selected latest" if index == len(replies) else f"Planning reply {index}"
            if duration is None:
                parts.append(f"- {label}: unavailable; event n={reply.get('n', 'not recorded')} has no valid `detail.duration_s`.")
            else:
                parts.append(
                    f"- {label}: **{format_number(duration)} seconds** from `detail.duration_s` "
                    f"on `reply` event n={reply.get('n', 'not recorded')} (status `PLAN_PROPOSED`)."
                )
        parts.extend([
            "",
            "This duration is the runtime's measured agent call duration. The event schema does not record a distinct timestamp for when plan generation began or completed, so it is not independently recalculated from event timestamps.",
        ])

    parts.extend([
        "",
        "## MIRATO → all workers ACCEPT",
        "",
        metric_elapsed(events),
        "",
        "Event identification: approval uses `type=accepted` and text containing `✅ Lideri e miratoi`; completion uses a later `type=accepted` event whose text contains `🎉` and `konfirmuar`, matching `src/runtime.py`.",
        "",
        "## Engine checks and blocked rules",
        "",
        f"- `check` events: **{checks}** (count of parsed objects with `type == \"check\"`).",
        f"- `blocked` events: **{blocked}** (count of parsed objects with `type == \"blocked\"`).",
        "",
        "These counts cover the entire source file, not only one plan, because engine check/blocked events do not consistently carry a job identifier.",
        "",
        "## Cost per plan",
        "",
    ])
    if replies:
        selected = replies[-1]
        parts.append(f"Plan reply: event n={selected.get('n', 'not recorded')} (`detail.status=PLAN_PROPOSED`).")
        parts.append(usage_report(selected)[0])
    else:
        parts.append("**Unavailable:** there is no planning reply to associate with token usage.")

    parts.extend([
        "",
        "## Schema notes",
        "",
        "- Runtime timestamps are local `HH:MM:SS` strings without a date or timezone offset. Elapsed time assumes the selected events belong to the same run; if the clock time rolls backward, the calculation treats it as one midnight crossing.",
        "- Runtime usage aggregates token fields across model calls and stores them on the final reply. It does not record per-call usage or a plan/job identifier in the usage object.",
        "- Runtime `cache_creation_input_tokens` are priced as cache writes at $5 per 1M tokens.",
        "- Counts are file-wide. Approval and completion are paired in event order, with the latest completed pair selected.",
        "",
    ])
    return "\n".join(parts)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--events", type=Path, default=DEFAULT_EVENTS, help=f"JSONL source (default: {DEFAULT_EVENTS})")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help=f"Markdown output (default: {DEFAULT_OUTPUT})")
    args = parser.parse_args(argv)
    try:
        events = load_events(args.events)
        report = build_report(events, args.events.relative_to(ROOT) if args.events.is_relative_to(ROOT) else args.events)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    except (EventFileError, FileNotFoundError, OSError, ValueError) as exc:
        print(f"numbers.py: error: {exc}", file=sys.stderr)
        return 2
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
