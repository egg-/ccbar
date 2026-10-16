---
description: Point Claude Code's status line at ccbar. Writes the statusLine entry in ~/.claude/settings.json.
disable-model-invocation: true
---

Set up ccbar as the user's status line.

1. Copy `${CLAUDE_PLUGIN_ROOT}/ccbar.py` to `${CLAUDE_PLUGIN_DATA}/ccbar.py`, creating the
   directory if needed. A SessionStart hook repeats this copy on every new session so plugin
   updates reach the status line, but it has not run yet if the plugin was installed in this
   session.
2. Read `~/.claude/settings.json`. If it already has a `statusLine` whose `command` is not
   the one below, show the user the current value and ask before replacing it.
3. Set `statusLine` to exactly this, leaving every other key untouched:

   ```json
   {
     "type": "command",
     "command": "python3 \"${CLAUDE_PLUGIN_DATA}/ccbar.py\"",
     "refreshInterval": 10
   }
   ```

4. Check it renders: `echo '{"model":{"display_name":"Opus"},"cost":{"total_cost_usd":1.5}}' | python3 "${CLAUDE_PLUGIN_DATA}/ccbar.py"`
   should print a line with `Opus` and `$1.50`.
5. Tell the user the bar appears on the next status line refresh, and that uninstalling the
   plugin deletes the copied file, so they should remove the `statusLine` entry at the same time.
