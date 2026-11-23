# Oracle persona

The stage oracle's persona is `.claude/agents/blind-oracle.md`, sent (frontmatter stripped) as the
entire system prompt by `tools/cold_read_oracle_stage.py` for every reader, Claude or codex. It
carries no jacket: the jacket comes from `reviews/cold-read/volume-packets.toml` with the reader's
memory. See `ORACLE.md`, "The reader at stage N".
