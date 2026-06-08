Scan meta/ and scenes/ for changes since last sync. No API calls.

Scan the novel directory for files that have changed, been added, or been deleted since the last index run.

Steps:
1. Call the `scan` MCP tool.
2. Show the full scan report.
3. If changes found: "Found [N] change(s). Run /sync to update, or tell me which files to sync first."
4. If nothing to sync: "Everything is current."
5. Always show pending items (knowledge delta gaps, stale tests, export lag) even if no file changes.
