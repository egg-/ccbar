# ccbar

A one-file status line for Claude Code. No daemon, no cache, no network, no dependencies.

```
5h ██░░░  35% 3h22m │ 7d ███░░  62% 2d19h │ Opus 5 20% │ $11.82
```

## Why

Claude Code already pipes everything a status line needs to its `statusLine`
command on stdin — quota usage and reset times, context window, cost, model,
cache state. Reading that blob and printing one line is the whole job.

So ccbar is 130 lines of stdlib Python in a single file. It spawns per tick,
prints, and exits. Nothing stays resident.

| | ccbar | a daemon-backed bar |
|---|---|---|
| resident processes | 0 | 3+ |
| install size | 5 KB | ~28 MB |
| per tick | ~22 ms | ~86 ms |
| dependencies | none | Python runtime bundle |

## Install

Drop the file somewhere and point Claude Code at it:

```bash
curl -fsSL https://raw.githubusercontent.com/egg-/ccbar/main/ccbar.py -o ~/.local/bin/ccbar
chmod +x ~/.local/bin/ccbar
```

Then in `~/.claude/settings.json`:

```json
{
  "statusLine": {
    "type": "command",
    "command": "/Users/you/.local/bin/ccbar",
    "refreshInterval": 10
  }
}
```

Restart Claude Code once. That's the install — there is nothing to uninstall
but the file and those four lines.

`refreshInterval` is in seconds. At 10s a 22 ms tick costs about 0.2% of one
core; at 1s it costs 2%. Quota percentages do not move fast enough to be worth
the difference.

## Configure

Edit the constants at the top of the file:

```python
WARN, CRIT = 60, 85   # percentages where green turns yellow, then red
BAR_WIDTH = 5
```

There is no config file, and that is deliberate. Editing two numbers in a
script you already own is less machinery than a config format, a parser, and a
`config set` subcommand.

## What it shows

Every segment is dropped when Claude Code did not send its data, so the line
degrades instead of erroring — on a third-party relay or Bedrock/Vertex, where
no quota exists, the quota segments simply disappear.

| segment | source field |
|---|---|
| `5h` / `7d` bars | `rate_limits.{five_hour,seven_day}` |
| model + context % | `model.display_name`, `context_window.used_percentage` |
| cost | `cost.total_cost_usd` |

The stdin blob carries more than this — `prompt_cache`, `effort`,
`session_name`, `thinking`, lines added/removed. Add a segment by reading the
field and appending to `seg` in `render()`.

## Test

```bash
python3 ccbar.py --selftest
```

Render against a real payload:

```bash
echo '{"model":{"display_name":"Opus 5"},"cost":{"total_cost_usd":1.5}}' | python3 ccbar.py
```

## Prior art

[leeguooooo/claude-code-usage-bar](https://github.com/leeguooooo/claude-code-usage-bar)
(MIT) is the fuller take on this idea — themes, styles, a desktop HUD, a
daemon render path. Reach for it if you want those. ccbar shares no code with
it and exists because the stdin contract makes the minimal version this small.

## License

MIT
