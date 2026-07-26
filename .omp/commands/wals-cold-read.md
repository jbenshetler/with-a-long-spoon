---
description: OMP cold-read wrapper — follows Claude command source with OMP model/agent resolution
argument-hint: "[--model <omp-model-id>] [none | fall | spring | summer | <slug> | <slug-a>..<slug-b> | <slug>..] [--fresh]"
---

Run the cold-read workflow by **reading and following** `.claude/commands/cold-read.md`, with the OMP-specific overrides below. This wrapper exists so the Claude command remains the workflow source of truth while OMP uses its own `blind-reader` agent and model configuration.

## Required source-read

Before executing, read `.claude/commands/cold-read.md` and follow its current workflow unless an override below conflicts. The Claude command may change; those changes should flow through automatically via this source-read.

## OMP overrides

1. **Agent definition:** use the OMP task agent `blind-reader` from `.omp/agents/blind-reader.md`, not `.claude/agents/blind-reader.md`.
2. **Model selection:** OMP does not use Claude Code's `model: opus|sonnet|haiku` tier mapping. Delete that mapping mentally.
3. **Effective default reader model:** when `--model` is omitted, the `blind-reader` model is resolved by OMP task-agent configuration, in this order:
   - `task.agentModelOverrides.blind-reader` in effective OMP config;
   - otherwise the `model:` frontmatter in `.omp/agents/blind-reader.md`;
   - otherwise the current OMP default task model.
4. **`--model <id>` semantics in OMP:** `<id>` is an OMP model selector, not a Claude tier. It names both the runtime reader model and the output directory key. If omitted, use the effective default reader model selector as `<id>`.
5. **Spawning:** spawn `blind-reader` as an OMP task agent using the runtime model selector from step 4. If the task tool cannot carry a per-spawn model override, use the eval bridge's `agent(prompt, agent="blind-reader", model="<id>")` helper for each reader turn. Do not pass a Claude `model: opus|sonnet|haiku` tier.
6. **Prompt starvation and carry-forward:** keep the Claude command's starvation rules, but format every reader prompt exactly like this so the prior state is unmissable:

   ```text
   TITLE:
   <display title>

   PRIOR READER-STATE (authoritative memory from every earlier chapter):
   <prior carry-forward, or "empty — opening chapter">

   OUTPUT PRIORITY:
   Keep `### Reader reaction` concise. Always complete `### Carry-forward state`
   in full; if space is tight, shorten the reaction, never the carry-forward.

   CHAPTER TEXT:
   <clean prose>
   ```

   Do not pass file paths, slug, chronology, meta, model name, or framing of what the scene does. Before each spawn after the opener, assert that the prior carry-forward is non-empty and came from the immediately preceding review file in this model's directory.
7. **Output validation:** the reader output must include both `### Reader reaction` and `### Carry-forward state`. If either heading is missing, or if the carry-forward section is empty, discard that run, retry once with a format reminder, and stop rather than writing a broken chain if the retry still fails.
8. **Blindness tripwire:** keep the Claude command's hard stop. A clean reader uses zero tools. If the OMP task/eval result reports any tool use, do not write the review and stop.

All other behavior — manifest resolution, target selection, carry-forward chaining, output file layout, synthesis, stale downstream warnings, and non-destructive write policy — comes from the current `.claude/commands/cold-read.md`.
