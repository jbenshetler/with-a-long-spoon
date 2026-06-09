Flag an incorrect KB fact during writing. Suppresses it from research() immediately and queues it for triage.

Syntax:
  /novel-flag Randi's scent is wrong
  /novel-flag [PACE] five kinds of shoes by the door
  /novel-flag [RANDI] the thing about locking the door is off

Optional [CHARACTER] prefix narrows the search to one character's facts.
Without it, all entities are searched.

Steps:
1. Call flag_fact(description=<full input after /novel-flag>)
2. Present the candidates returned:
     [1] [HIGH] Randi → scent
         Current value: Gardenia and something colder underneath
         target_spec: property:12:scent
3. Ask the author: which one? (or "none of these")
4. On selection: call confirm_flag(target_spec=<chosen spec>, description=<original input>)
5. Report: "Flagged. 'Randi → scent' suppressed from research() until resolved in triage."

What happens after flagging:
- The fact is removed from active retrieval immediately
- It appears in /novel-triage with [FLAGGED BY AUTHOR] marker and HIGH priority
- Resolve via Edit (corrected value, re-activates) or Reject (permanent removal, retained for audit)

Do NOT auto-flag without author confirmation. Always present candidates and wait for the author to pick.
