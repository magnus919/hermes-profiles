#!/usr/bin/env python3
"""
SLO Burn Rate Calculator

Calculates error budget burn rate from SLI data.

Usage:
    python3 slo-burn-rate.py --slo-target 99.9 --window 1h --good-events 99500 --total-events 100000
    python3 slo-burn-rate.py --slo-target 99.99 --window 7d --error-rate 0.001
    python3 slo-burn-rate.py --slo-target 99.95 --window 30d --good-events 998500 --total-events 1000000
    cat sli_data.json | python3 slo-burn-rate.py --slo-target 99.9 --window 1h
"""

import argparse
import json
import sys
import math
from datetime import timedelta

# ---------------------------------------------------------------------------
# Window parsing
# ---------------------------------------------------------------------------

WINDOW_SECONDS = {
    "1h": 3600,
    "6h": 21600,
    "24h": 86400,
    "7d": 604800,
    "30d": 2592000,
}


def parse_window(window_str: str) -> int:
    """Convert a window string like '1h', '24h', '7d', '30d' to seconds."""
    window_str = window_str.strip().lower()
    if window_str in WINDOW_SECONDS:
        return WINDOW_SECONDS[window_str]

    # Fallback: try to parse programmatically
    if window_str.endswith("h"):
        hours = int(window_str[:-1])
        return hours * 3600
    elif window_str.endswith("d"):
        days = int(window_str[:-1])
        return days * 86400
    elif window_str.endswith("m"):
        minutes = int(window_str[:-1])
        return minutes * 60
    elif window_str.endswith("s"):
        return int(window_str[:-1])
    else:
        raise ValueError(
            f"Unrecognized window format: '{window_str}'. "
            f"Use e.g. 1h, 6h, 24h, 7d, 30d."
        )


def format_duration(seconds: int) -> str:
    """Format a duration in seconds to a human-readable string."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m"
    elif seconds < 86400:
        hours = seconds // 3600
        remainder = seconds % 3600
        if remainder == 0:
            return f"{hours}h"
        return f"{hours}h{remainder // 60}m"
    else:
        days = seconds // 86400
        remainder = seconds % 86400
        if remainder == 0:
            return f"{days}d"
        return f"{days}d{remainder // 3600}h"


# ---------------------------------------------------------------------------
# Core calculation
# ---------------------------------------------------------------------------


def calculate_burn_rate(
    slo_target: float,
    window_seconds: int,
    good_events: int | None = None,
    total_events: int | None = None,
    error_rate: float | None = None,
) -> dict:
    """
    Calculate error budget burn rate and related metrics.

    Parameters
    ----------
    slo_target : float
        Target availability percentage (e.g. 99.9 for 99.9%).
    window_seconds : int
        Analysis window in seconds.
    good_events : int, optional
        Number of successful events.
    total_events : int, optional
        Total number of events.
    error_rate : float, optional
        Direct error rate (e.g. 0.001 for 0.1% error rate).

    Returns
    -------
    dict with keys:
        sli_target, window, window_seconds, good_events, total_events,
        error_rate, measured_availability, burn_rate,
        budget_remaining_pct, time_to_exhaustion, status
    """
    slo_threshold = slo_target / 100.0  # e.g. 99.9 -> 0.999
    allowed_error_rate = 1.0 - slo_threshold  # e.g. 0.001

    if error_rate is not None:
        # Direct error rate provided
        measured_error_rate = error_rate
        measured_availability = 1.0 - measured_error_rate
        if good_events is None and total_events is None:
            good_events = None
            total_events = None
        elif good_events is not None and total_events is not None:
            pass  # keep both
        else:
            # Can't derive the missing one
            good_events = None
            total_events = None
    elif good_events is not None and total_events is not None:
        if total_events == 0:
            return {
                "error": "total_events must be greater than 0",
                "slo_target": slo_target,
                "window": format_duration(window_seconds),
            }
        measured_availability = good_events / total_events
        measured_error_rate = 1.0 - measured_availability
    else:
        return {
            "error": (
                "Provide either --good-events + --total-events, "
                "or --error-rate directly."
            ),
            "slo_target": slo_target,
            "window": format_duration(window_seconds),
        }

    # Burn rate
    if allowed_error_rate == 0:
        burn_rate = float("inf") if measured_error_rate > 0 else 0.0
    else:
        burn_rate = measured_error_rate / allowed_error_rate

    # Budget remaining
    if total_events is not None and total_events > 0:
        total_budget = allowed_error_rate * total_events
        consumed = total_events - good_events if good_events is not None else measured_error_rate * total_events
        budget_remaining = max(0.0, total_budget - consumed)
        budget_remaining_pct = (
            (budget_remaining / total_budget * 100.0) if total_budget > 0 else 0.0
        )
    else:
        # Without event counts, use the error rate as a proxy
        # Budget remaining = (allowed_error_rate - measured_error_rate) / allowed_error_rate
        if allowed_error_rate > 0:
            budget_remaining_pct = max(
                0.0,
                ((allowed_error_rate - measured_error_rate) / allowed_error_rate) * 100.0,
            )
        else:
            budget_remaining_pct = 0.0 if measured_error_rate > 0 else 100.0

    # Time to exhaustion
    if burn_rate > 0:
        # How long until the remaining budget burns at the current rate?
        window_error_budget = allowed_error_rate  # per-unit budget for the window
        remaining_fraction = max(0.0, 1.0 - (measured_error_rate / allowed_error_rate)) if allowed_error_rate > 0 else 0.0

        if burn_rate > 0 and remaining_fraction > 0:
            time_to_exhaustion_secs = (remaining_fraction / burn_rate) * window_seconds
        elif remaining_fraction <= 0:
            time_to_exhaustion_secs = 0
        else:
            time_to_exhaustion_secs = float("inf")
    else:
        time_to_exhaustion_secs = float("inf")

    # Status determination
    if burn_rate == 0 and measured_error_rate == 0:
        status = "healthy"
    elif budget_remaining_pct <= 0 or measured_error_rate >= allowed_error_rate:
        status = "exhausted"
    elif budget_remaining_pct < 30 and burn_rate > 3:
        status = "burning"
    elif budget_remaining_pct < 70 and burn_rate > 1:
        status = "warning"
    elif burn_rate > 1:
        # Elevated but budget still healthy
        status = "warning"
    else:
        status = "healthy"

    if budget_remaining_pct < 5:
        status = "exhausted"
    elif budget_remaining_pct < 30:
        # Re-check; might be "burning" if rate is really high
        if burn_rate >= 10:
            status = "burning"
        elif status != "burning":
            status = "warning"
    elif budget_remaining_pct < 70:
        if burn_rate >= 3:
            status = "burning"
        elif burn_rate > 1:
            status = "warning"

    # Format time to exhaustion
    if time_to_exhaustion_secs == float("inf"):
        formatted_ttl = "infinite"
    elif time_to_exhaustion_secs <= 0:
        formatted_ttl = "exhausted"
    else:
        formatted_ttl = format_duration(int(time_to_exhaustion_secs))

    return {
        "slo_target": slo_target,
        "window": format_duration(window_seconds),
        "window_seconds": window_seconds,
        "good_events": good_events,
        "total_events": total_events,
        "error_rate": round(measured_error_rate, 6),
        "measured_availability": round(measured_availability * 100.0, 4),
        "burn_rate": round(burn_rate, 4),
        "budget_remaining_pct": round(budget_remaining_pct, 2),
        "budget_remaining": round(budget_remaining_pct, 2),
        "time_to_exhaustion": formatted_ttl,
        "time_to_exhaustion_seconds": (
            int(time_to_exhaustion_secs)
            if time_to_exhaustion_secs not in (float("inf"), float("-inf"))
            else None
        ),
        "status": status,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Calculate SLO error budget burn rate.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "--slo-target",
        type=float,
        required=True,
        help="SLO target as a percentage (e.g. 99.9 for 99.9%%).",
    )
    parser.add_argument(
        "--window",
        type=str,
        default="1h",
        help=(
            "Analysis window. Supports: 1h, 6h, 24h, 7d, 30d "
            "or custom like 90m, 2h30m, 14d. Default: 1h."
        ),
    )
    parser.add_argument(
        "--good-events",
        type=int,
        default=None,
        help="Number of successful (good) events.",
    )
    parser.add_argument(
        "--total-events",
        type=int,
        default=None,
        help="Total number of events.",
    )
    parser.add_argument(
        "--error-rate",
        type=float,
        default=None,
        help="Direct error rate (e.g. 0.001 for 0.1%% error rate).",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        default=False,
        help="Pretty-print JSON output with indentation.",
    )
    parser.add_argument(
        "--color",
        action="store_true",
        default=False,
        help="Add terminal color codes to the JSON output for readability.",
    )
    return parser.parse_args(argv)


def _color_status(status: str) -> str:
    colors = {
        "healthy": "\033[32m",    # green
        "warning": "\033[33m",    # yellow
        "burning": "\033[31m",    # red
        "exhausted": "\033[1;31m",  # bold red
    }
    reset = "\033[0m"
    return f"{colors.get(status, '')}{status}{reset}"


def main() -> None:
    args = parse_args()

    # If reading from stdin, look for JSON data
    if not sys.stdin.isatty():
        try:
            stdin_data = sys.stdin.read().strip()
            if stdin_data:
                input_data = json.loads(stdin_data)
                # Merge stdin data with CLI args, CLI takes precedence
                if args.good_events is None and "good_events" in input_data:
                    args.good_events = input_data["good_events"]
                if args.total_events is None and "total_events" in input_data:
                    args.total_events = input_data["total_events"]
                if args.error_rate is None and "error_rate" in input_data:
                    args.error_rate = input_data["error_rate"]
                if args.window == "1h" and "window" in input_data:
                    # Only override if default hasn't been changed
                    pass  # keep explicit CLI
        except (json.JSONDecodeError, Exception):
            pass  # If stdin isn't valid JSON, just use CLI args

    try:
        window_seconds = parse_window(args.window)
    except ValueError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    result = calculate_burn_rate(
        slo_target=args.slo_target,
        window_seconds=window_seconds,
        good_events=args.good_events,
        total_events=args.total_events,
        error_rate=args.error_rate,
    )

    indent = 2 if args.pretty else None

    if args.color:
        # Color only the status field for terminal readability
        status_colorized = _color_status(result.get("status", ""))
        json_str = json.dumps(result, indent=indent)
        # Replace the plain status string with colorized version in the JSON
        plain_status = result.get("status", "")
        safe_status = json.dumps(plain_status)
        color_status_with_quotes = json.dumps(plain_status.replace(plain_status, status_colorized))
        # Simple approach: just replace the status value
        # But this can be fragile. Let's just print JSON clean and add color on top.
        print(json_str, file=sys.stderr)
        print(f"Status: {_color_status(result.get('status', ''))}")
    else:
        print(json.dumps(result, indent=indent))

    # Exit code indicates health
    status = result.get("status", "")
    if status == "healthy":
        sys.exit(0)
    elif status in ("warning", "burning"):
        sys.exit(1)
    elif status == "exhausted":
        sys.exit(2)
    elif "error" in result:
        sys.exit(3)


if __name__ == "__main__":
    main()
