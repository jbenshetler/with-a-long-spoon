Restore the knowledge graph from knowledge-state/ files. Optionally restore from a specific git commit.

Restore the novel knowledge state from knowledge-state/ files into the database.

Steps:
1. Check whether a git commit hash or partial hash was provided after the command
   (e.g. /importdb a3f2c1 or /importdb for current files).

2. If a commit hash was provided:
   - Show what that commit contains: git show --stat [hash] -- knowledge-state/
   - Show the commit message and timestamp
   - Confirm: "Restore from commit [hash]: '[message]' ([date])? [y/N]"
   - Wait for confirmation before proceeding.

3. If no hash (restore from current files):
   - Show the manifest: how many entities, chapters, deltas are in the current knowledge-state/ files
   - Show when those files were last modified
   - Confirm: "Restore from current knowledge-state/ files? [y/N]"
   - Wait for confirmation before proceeding.

4. On confirmation: call `restore_knowledge_state` MCP tool with the commit hash if provided, or None for current files.

5. Show restore summary: entities, chapters, knowledge deltas, inversion tests restored.

6. Remind: "Run /exportdb to verify the restored state matches the source files, or run the quality loop to re-validate."

SAFETY: Restore replaces all extracted knowledge in the database. It does NOT touch meta/ or scenes/ files. It is fully reversible by running /importdb again with the previous commit hash.
