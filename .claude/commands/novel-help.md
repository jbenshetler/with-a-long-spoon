Show available novel assistant commands and the typical writing workflow.

Print the following help text exactly:

---

NOVEL ASSISTANT — command reference

WORKFLOW
  Start of session:   /novel-scan        check what changed
  If changes found:   /novel-sync        update the knowledge graph
  Before writing:     /novel-scene-prep  character knowledge brief
  After writing:      /novel-verify      check draft for violations
  Index new scene:    /novel-post-scene  add to graph, draft deltas
  Checkpoint:         /novel-exportdb    snapshot to knowledge-state/

COMMANDS
  /novel-scan        Scan meta/ and scenes/ for changes. No API cost.
  /novel-sync        Sync changed files. Shows diffs before writing anything.
  /novel-scene-prep  Character knowledge brief before writing a scene.
  /novel-verify      Check a draft for continuity violations.
  /novel-post-scene  Index a new scene and draft knowledge delta entries.
  /novel-exportdb    Export knowledge graph to knowledge-state/ and commit.
  /novel-importdb    Restore knowledge graph from knowledge-state/ files.
  /novel-help        Show this message.

PRIME RULE
  Never answer a factual question about the novel from memory.
  Always use research() or character_knowledge() — tools only.

COST GUIDE
  scan, character_knowledge, verify (SQL only) — free
  research, verify (with LLM)                 — ~$0.01–0.05
  sync one character file                      — ~$1–3 (Opus extraction)
  full rebuild                                 — ~$10

---
