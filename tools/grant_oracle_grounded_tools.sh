#!/usr/bin/env bash
# One-shot: grant the blind-oracle-grounded agent the sandboxed packet tools
# (list_packet / read_packet / write_output) — the frontmatter edit the safety
# classifier won't let Claude self-apply. Idempotent.
set -euo pipefail
cd "$(dirname "$0")/.."   # repo root

p=".claude/agents/blind-oracle-grounded.md"
if grep -q "mcp__packet__read_packet" "$p"; then
    echo "already granted: $p"
else
    sed -i 's/^tools: \[\]/tools: [mcp__packet__list_packet, mcp__packet__read_packet, mcp__packet__write_output]/' "$p"
    echo "updated: $p"
fi
echo "=== tools line ==="
grep -n '^tools:' "$p"
