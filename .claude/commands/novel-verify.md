Check a draft or the current scene for continuity violations.

Verify text against the knowledge graph for continuity violations.

Steps:
1. If text was provided after the command (e.g. /verify [pasted text]): use that text as the draft.
2. If no text provided: ask "Paste the text to verify, or tell me which scene file to check."
3. If a file path is provided: read the file content.
4. Call `verify_draft` MCP tool with the text and current chapter.
5. Show violations with severity, the offending passage, and the rule violated.
6. If clean: "No violations found."
7. Do NOT suggest rewrites unless asked. Violations only.
