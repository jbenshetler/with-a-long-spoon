export const meta = {
  name: 'graded-loop',
  description: 'General produce→evaluate→revise loop: a producer subagent drafts an artifact; one or more evaluator subagents score it against rubrics (structured pass/fail); iterate until every evaluator passes or a cap. File-logged (draft-vN.md + <key>-vN.md) and restartable. Domain-agnostic — the caller supplies the prompts, schemas, and pass fields via args.',
  phases: [
    { title: 'Draft', detail: 'producer drafts v1 from the caller inputs' },
    { title: 'Evaluate', detail: 'evaluators score the current draft in parallel' },
    { title: 'Revise', detail: 'producer applies findings; loop to the cap' },
  ],
}

// ── args contract ───────────────────────────────────────────────────────────
// args = {
//   workdir: string,                       // e.g. "/tmp/<task>-graded" (all files live here)
//   producer: {
//     draftPrompt:  string,                // role + inputs for the v1 draft
//     revisePrompt: string,                // role + inputs for each revision
//     agentType?, model?, effort?          // optional overrides
//   },
//   evaluators: [ {                         // one or more; run in parallel each round
//     key: string,                         // short slug -> label + findings filename
//     prompt: string,                      // role + rubric
//     schema: object,                      // JSON Schema; MUST include the boolean passField
//     passField: string,                   // name of the boolean the loop branches on
//     agentType?, model?, effort?
//   } ],
//   maxIters?: number,                     // default 5
// }
// Pass condition each round: every evaluator returned a verdict and verdict[passField] === true.

const A = args || {}
if (!A.workdir) throw new Error('graded-loop: args.workdir required')
if (!A.producer || !A.producer.draftPrompt || !A.producer.revisePrompt)
  throw new Error('graded-loop: args.producer.{draftPrompt, revisePrompt} required')
if (!Array.isArray(A.evaluators) || A.evaluators.length === 0)
  throw new Error('graded-loop: args.evaluators[] required (at least one)')

const WD = A.workdir
const MAX = A.maxIters || 5
const draftFile = (i) => `${WD}/draft-v${i}.md`
const findFile = (key, i) => `${WD}/${key}-v${i}.md`
const clean = (o) => { for (const k in o) if (o[k] === undefined) delete o[k]; return o }
const pOpts = (label, ph) => clean({
  label, phase: ph,
  agentType: A.producer.agentType || 'general-purpose',
  model: A.producer.model, effort: A.producer.effort,
})

phase('Draft')
await agent(
  `${A.producer.draftPrompt}\n\n--- graded-loop context ---\nWrite the complete draft to ${draftFile(1)} and return only that path. All working files live under ${WD}.`,
  pOpts('draft:v1', 'Draft'))

let final = null
for (let i = 1; i <= MAX; i++) {
  const cur = draftFile(i)
  phase('Evaluate')
  const raw = await parallel(A.evaluators.map((ev) => () =>
    agent(
      `${ev.prompt}\n\n--- graded-loop context ---\nThe draft to evaluate is ${cur}. Write your human-readable findings to ${findFile(ev.key, i)}, then return the structured verdict. Judge net of any inputs the caller told you to treat as superseded.`,
      clean({ label: `${ev.key}:v${i}`, phase: 'Evaluate', schema: ev.schema, agentType: ev.agentType || 'general-purpose', model: ev.model, effort: ev.effort }))
      .then((v) => ({ key: ev.key, passField: ev.passField, verdict: v }))
  ))
  const results = raw.filter(Boolean)
  const passed = results.length === A.evaluators.length &&
    results.every((r) => r.verdict && r.verdict[r.passField] === true)
  log(`iter ${i}: ` + results.map((r) => `${r.key}=${r.verdict ? r.verdict[r.passField] : 'null'}`).join(' '))

  if (passed) { final = { iter: i, draftPath: cur, verdicts: results, passed: true }; break }
  if (i === MAX) { final = { iter: i, draftPath: cur, verdicts: results, passed: false, hitCap: true }; break }

  phase('Revise')
  const findings = A.evaluators.map((ev) => findFile(ev.key, i)).join(', ')
  await agent(
    `${A.producer.revisePrompt}\n\n--- graded-loop context ---\nCurrent draft: ${cur}. Evaluator findings to apply: ${findings}. Write the fully revised draft to ${draftFile(i + 1)} and return only that path. Fix every issue; introduce no new issues or losses.`,
    pOpts(`revise:v${i}->${i + 1}`, 'Revise'))
}

return final
