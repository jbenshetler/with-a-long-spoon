Sync changed files identified by the last scan. Presents diffs for approval before writing anything.

Sync changed files into the knowledge graph.

Steps:
1. Call `scan` MCP tool if no scan result is cached from this session.
2. Show the suggested sync order with estimated costs.
3. Ask: "Proceed with all? Or specify which files to sync first."
4. On approval: call `sync` MCP tool.
5. For each file being synced, present the diff for approval before writing to the database.
6. After all files synced: show sync summary and git commit hash.
7. Note any quality loop results and review queue items.

If the human specifies a subset (e.g. "just Vivienne for now"):
call sync with that file only, leave others for later.
