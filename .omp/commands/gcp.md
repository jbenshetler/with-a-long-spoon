---
description: Stage all changes, auto-generate a commit message, commit, and push
argument-hint: [optional context for the commit message]
---

Commit and push the current repository changes.

Use `$ARGUMENTS` only as optional context for the generated commit message; do
not treat it as a literal commit message. The commit message must come from the
actual staged diff.

## Rules

- Do not ask for confirmation for the normal path. This command means: stage all
  changes, commit, and push.
- Include all working-tree changes, including untracked files: use `git add -A`.
- Do not invent or omit changes. If the working tree is clean, report that there
  is nothing to commit and do not push.
- If the push is rejected or requires a merge/rebase/force push, stop and report
  the exact blocker. Do not force-push unless the user explicitly asks in that
  turn.
- If a check fails, fix the source problem when it is safe and obvious; otherwise
  stop with the failing command and output.

## Workflow

1. Inspect the working tree with `git status --short`.
2. Run repo-specific generated-artifact checks before the commit:
   - If `meta/meta-plan-chronology.md` changed, run `tools/chronology_html.py` and
     include the regenerated `chronology.html` in the commit.
   - If any `meta/*.md` file changed, run `python3 tools/lint_titles.py --all`.
3. Stage everything with `git add -A`.
4. Inspect the staged change shape using `git diff --cached --stat` and
   `git diff --cached --name-status`. Read the staged diff only as much as needed
   to produce an accurate concise message.
5. Generate a conventional, imperative, present-tense commit message from the
   staged diff. Prefer one line. Use a body only if the diff has multiple
   unrelated bullets that need preserving.
6. Commit with the generated message.
7. Push the current branch with `git push`.
8. Report:
   - commit hash
   - commit message
   - push result
   - any repo-specific checks run

## Message style

Examples:

```text
Mark All Told as reviewed
Add chronology HTML rebuild skill
Update SATC chronology title refs
```

Keep the subject specific and boring. Do not mention `/gcp`, automation, or the
assistant.
