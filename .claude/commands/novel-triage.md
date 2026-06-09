Work through the human review queue. Optionally filter by character name or set batch size.

The review queue contains facts the quality loop expected to find in the knowledge graph but
couldn't. Approving an item writes the fact directly into entity properties or behavioral_states.

CLI (run from novel-assistant/ directory):
  POSTGRES_HOST=localhost POSTGRES_PORT=5433 uv run python scripts/triage_queue.py <command>

Steps:
1. Run `stats` — report pending count and breakdown by character.
   "N items pending. Breakdown: Vee: X, Randi: Y, Pace: Z, Cassie: W"

2. Ask: filter by character? batch size? (defaults: all characters, 10 per batch)
   If the user typed a character name after /novel-triage, use that as the filter.
   If they typed a number, use that as the batch size.

3. Run `fetch [--character NAME] [--limit N]` — show the batch.
   Present each item compactly:
     [1/10]  id=265
     Q:        What is Randi's signature scent?
     Expected: Randi wears a perfume of gardenia with something colder underneath.

4. For each item, ask: Approve / Reject / Edit / Skip / Temporal
   - Approve  → `approve <id>`                      — LLM classifies and writes to entity.properties or behavioral_states
   - Reject   → `reject <id>`                       — marks dismissed, nothing written
   - Edit     → `approve <id> --value "new text"`   — writes corrected value instead
   - Skip     → leave unreviewed, move to next
   - Temporal → `temporal <id> [--after "event"] [--before "event"]`
                Writes to temporal_states for facts only true within a chapter window.
                Prompt the author for after/before event bounds before running.
                Example: "Vee and Randi have known each other ~1 week"
                  → after="Vee and Randi first meet" before="one month into their friendship"

5. After the batch: show progress ("5 approved, 3 rejected, 2 skipped — 381 remaining")
   Offer to continue with next batch.

Handling facts that are grounded but not objectively true:
  False belief   → E to reframe: "Vee believes X" rather than "X is true"
  Performed lie  → A as-is; behavioral_state classification captures the performance
  Retconned doc  → R, the source is no longer authoritative

What gets written on approve:
  Stable facts (scent, name, rule, appearance) → entity.properties[key]
  Triggered patterns (when X → character does Y) → behavioral_states row
  The LLM classifies automatically; use --value if the expected answer needs correction.

After triage session:
  Note how many items were approved.
  Offer to re-run quality loop to see the pass rate improvement.
