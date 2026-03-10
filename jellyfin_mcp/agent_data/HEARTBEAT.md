# Heartbeat — Periodic Self-Check

You are running a scheduled heartbeat. Perform these checks and report results concisely.

## Checks

1. **Tool Availability** — Call `list_tools` or equivalent to verify your MCP tools are reachable. Report any connection failures.
2. **Memory Review** — Read `MEMORY.md` and check for any pending follow-up tasks or action items. List any that are overdue.
3. **Cron Log** — Read `CRON_LOG.md` and check for recent errors (❌). Summarize any failures from the last 24 hours.
4. **Peer Agents** — Read `AGENTS.md` and note if any registered peers need attention.
5. **Domain-Specific Checks**:
   - **Server Health / Logs**: Check server health status and scan recent server logs for critical errors using available tools.
   - **Playback Health**: Check for active transcodes or playback errors.
   - **New Media**: Summarize recently added movies or shows.
6. **Self-Diagnostics** — Report your current model, available tool count, and any anomalies.

## Response Format

If everything is healthy:
```
HEARTBEAT_OK — All systems nominal. [tool_count] tools available. No pending actions.
```

If issues found:
```
HEARTBEAT_ALERT — [summary of issues found]
- Issue 1: ...
- Issue 2: ...
- Action needed: ...
```
