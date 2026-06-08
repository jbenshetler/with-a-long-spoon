Export the current knowledge graph to knowledge-state/ and commit to git.

Export the current novel knowledge state to the knowledge-state/ directory and commit it to the novel git repository.

Steps:
1. Call the `export_knowledge_state` MCP tool.
   If an optional message was provided after the command (e.g. /exportdb before rewriting act two), pass it as the `message` argument.
2. Show the list of files written and the git commit hash.
3. Show a one-line summary: how many entities, chapters, deltas exported.
4. If nothing changed since the last export, say so clearly — do not make an empty commit.

After export, confirm: "knowledge-state/ is current as of [timestamp] (commit [hash])"
