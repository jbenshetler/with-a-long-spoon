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
4. On selection, ask what to do with it:

     Fix    — correct it now (no triage needed)
     Reject — it's wrong, remove it permanently (retained for audit)
     Triage — suppress it and send to /novel-triage for later

   For Fix: ask what the correction is:
     - Wrong character? "Move to [NAME]" → fix_fact(target_spec, corrected_character="Name")
     - Wrong value?    "The correct value is X" → fix_fact(target_spec, corrected_value="X")

   For Reject: call reject_fact(target_spec, description=<original input>)

   For Triage: call confirm_flag(target_spec, description=<original input>)

5. Report what happened.

What happens in each case:
  Fix    — fact is corrected or moved in KB immediately, no queue entry
  Reject — fact is removed from research() immediately; audit record written (won't appear in triage)
  Triage — fact suppressed from research(); appears in /novel-triage with [FLAGGED BY AUTHOR] HIGH priority

Do NOT apply any action without author confirmation of both the target AND the action.
