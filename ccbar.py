#!/usr/bin/env python3
"""ccbar — a one-file status line for Claude Code.

Claude Code pipes a JSON blob to the statusLine command on stdin and prints
whatever comes back on stdout. Everything shown below is already in that blob,
so this needs no daemon, no cache, no network, and no dependencies.

Wire it up in ~/.claude/settings.json:

    "statusLine": {
      "type": "command",
      "command": "/path/to/ccbar.py",
      "refreshInterval": 10
    }
"""
import json
import sys
import time

# ponytail: thresholds are module constants, not a config file — edit and go.
WARN, CRIT = 60, 85
BAR_WIDTH = 5

FIVE_HOUR = 5 * 3600
SEVEN_DAY = 7 * 86400

RESET = "\033[0m"
DIM = "\033[2m"
GREEN, YELLOW, RED = "\033[32m", "\033[33m", "\033[31m"


def severity(pct):
    return RED if pct >= CRIT else YELLOW if pct >= WARN else GREEN


def bar(pct, width=BAR_WIDTH):
    """Block bar, at least one block once anything is used."""
    pct = max(0, min(100, pct))
    filled = round(pct / 100 * width)
    if pct > 0:
        filled = max(1, filled)
    return "█" * filled + "░" * (width - filled)


def until(epoch, now=None):
    """Compact time-remaining: 3d04h, 2h23m, 14m, or 'now'."""
    if not epoch:
        return ""
    secs = int(epoch - (time.time() if now is None else now))
    if secs <= 0:
        return "now"
    d, rem = divmod(secs, 86400)
    h, rem = divmod(rem, 3600)
    m = rem // 60
    if d:
        return f"{d}d{h:02d}h"
    if h:
        return f"{h}h{m:02d}m"
    return f"{m}m"


def project(pct, resets_at, window, now=None):
    """Usage at window close if the current burn rate holds.

    Claude Code sends when the window resets but not when it opened, so the
    start is resets_at - window. Early in a window a couple of calls look like
    an infinite rate, so hold off until enough of it has elapsed to mean
    anything.
    """
    if not resets_at or not pct:
        return None
    now = time.time() if now is None else now
    elapsed = now - (resets_at - window)
    frac = elapsed / window
    if frac < 0.1 or frac > 1:
        return None
    return min(999, round(pct / frac))


def quota(label, d, window):
    """One quota segment, or None when Claude Code sent no rate limits."""
    if not d:
        return None
    pct = d.get("used_percentage")
    if pct is None:
        return None
    resets_at = d.get("resets_at")
    c = severity(pct)
    left = until(resets_at)
    tail = f" {DIM}{left}{RESET}" if left else ""
    eta = project(pct, resets_at, window)
    fore = f" {severity(eta)}→{eta}%{RESET}" if eta is not None else ""
    return f"{DIM}{label}{RESET} {c}{bar(pct)} {pct:>3.0f}%{RESET}{fore}{tail}"


def render(d):
    seg = []

    limits = d.get("rate_limits") or {}
    seg += [s for s in (quota("5h", limits.get("five_hour"), FIVE_HOUR),
                        quota("7d", limits.get("seven_day"), SEVEN_DAY)) if s]

    ctx = d.get("context_window") or {}
    name = (d.get("model") or {}).get("display_name")
    if name:
        used = ctx.get("used_percentage")
        if used is None:
            seg.append(name)
        else:
            seg.append(f"{name} {severity(used)}{used:.0f}%{RESET}")

    cost = (d.get("cost") or {}).get("total_cost_usd")
    if cost is not None:
        seg.append(f"{DIM}${cost:.2f}{RESET}")

    return f" {DIM}│{RESET} ".join(seg)


def selftest():
    assert bar(0) == "░" * 5, bar(0)
    assert bar(1) == "█" + "░" * 4, bar(1)          # never round a live bar to empty
    assert bar(100) == "█" * 5, bar(100)
    assert bar(50) == "██░░░" or bar(50) == "███░░", bar(50)

    assert severity(0) == GREEN and severity(WARN) == YELLOW and severity(CRIT) == RED

    now = 1_000_000
    assert until(now, now) == "now"
    assert until(now + 59, now) == "0m"
    assert until(now + 3600 * 2 + 60 * 23, now) == "2h23m"
    assert until(now + 86400 * 3 + 3600 * 4, now) == "3d04h"
    assert until(None) == ""

    # Projection: half a window gone with 30% used lands at 60%.
    half = now + FIVE_HOUR / 2
    assert project(30, half, FIVE_HOUR, now) == 60
    assert project(80, half, FIVE_HOUR, now) == 160          # over cap is worth saying
    # Too early in the window to extrapolate, and no window in progress.
    assert project(5, now + FIVE_HOUR * 0.95, FIVE_HOUR, now) is None
    assert project(50, None, FIVE_HOUR, now) is None
    assert project(0, half, FIVE_HOUR, now) is None

    # A blob missing every optional key must still render, not crash.
    assert render({}) == ""
    assert "Opus 5" in render({"model": {"display_name": "Opus 5"}})
    out = render({"rate_limits": {"five_hour": {"used_percentage": 35,
                                               "resets_at": time.time() + 3600}},
                  "context_window": {"used_percentage": 11},
                  "model": {"display_name": "Opus 5"},
                  "cost": {"total_cost_usd": 4.2783}})
    assert "35%" in out and "11%" in out and "$4.28" in out, out
    print("ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit(0)
    try:
        blob = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)  # ponytail: a bad tick prints nothing rather than garbage
    print(render(blob))
