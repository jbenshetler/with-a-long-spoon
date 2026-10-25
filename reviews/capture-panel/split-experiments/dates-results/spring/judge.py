import sys, json, re, glob, os, concurrent.futures as cf
sys.path.insert(0, '/home/jeff/clients/wals/one/tools')
import cold_read
B = '/tmp/dates-blind-spring'
MODEL = 'google/gemini-4-argon'
TRUTH = open(f'{B}/TRUE-DATES.txt').read()
FACTS = """Additional true facts: Pace and Randi first met Saturday, August 8. Fall semester begins Mon Aug 31. Thanksgiving break Sat Nov 21 - Sun Nov 29 (Thanksgiving Thu Nov 26). Finals Mon Dec 14 - Fri Dec 18. Christmas break Sat Dec 19 - Mon Jan 18. Spring semester begins Tue Jan 19. Spring break Sat Mar 6 - Sun Mar 14. Valentine's Day is Sunday Feb 14 (the "Valentine's Saturday" dance is Sat Feb 13; no drafted chapter covers it). In TRUE DATES, an indented line under a chapter is a later day that begins at the section opening with the quoted words."""
SYSTEM = "You are a blind, even-handed judge of TIMELINE ACCURACY in readers' writing about a novel. Lanes are labeled only L###; do not speculate about which condition any lane belongs to. Apply the same standard to every lane. Output only the requested JSON inside one ```json fenced block, then nothing else."
GATES = """Below are sentences extracted from readers' per-chapter reactions, each prefixed "L### chNNN:" (the reader lane and the chapter they had just read), extracted because they contain temporal language.

Classify every snippet's temporal claim(s): CORRECT, WRONG (contradicts the truth: wrong date/weekday, elapsed time off by more than a day or two, wrong order, relationship age badly off), VAGUE (unverifiable), UNSURE (the reader says they're unsure/confused about when or how much time passed), or NOT-TEMPORAL (the matched word isn't a time claim, e.g. "the Sunday dress", a quoted title). Also flag any snippet that comments on how the book presents dates/time (e.g. dates at chapter heads, a sense of a log or schedule) as META, quoting it.

Return JSON: {"L###": {"correct": n, "wrong": n, "vague": n, "unsure": n, "not_temporal": n, "errors": ["chNNN <quote> — <truth>"], "unsure_quotes": ["chNNN <quote>"], "meta": ["chNNN <quote>"]}, ...} covering every lane that appears."""
MINTS = """Below are each reader lane's carry-forward memory notes written after chapter {b} (one file per lane).

For EACH lane, find every TEMPORAL claim: a calendar date, weekday, month/season, elapsed time ("two weeks in", "six days later", "the next morning", "a month"), duration of a relationship, or the ordering of events in time. Classify each:
- CORRECT: consistent with the true dates.
- WRONG: contradicts them (wrong date/weekday/month, elapsed time off by more than a day or two, wrong order, a relationship's age badly off).
- VAGUE: temporal language too loose to check ("recently", "soon").
- UNSURE: the reader states uncertainty about when something happened.

Return JSON: {{"L###": {{"correct": n, "wrong": n, "vague": n, "unsure": n, "precise_dates": n, "errors": ["<quote> — <truth>"]}}, ...}} where precise_dates counts claims naming a specific weekday or calendar date. Cover all lanes."""
fn = cold_read.make_openrouter_agent_fn(system_prompt=SYSTEM, api_key=os.environ['OPENROUTER_API_KEY'],
                                        policy='judge', max_output_tokens=48000)
def head(task): return f"TRUE DATES (chapter number, volume, slug, true in-story date):\n{TRUTH}\n\n{FACTS}\n\n{task}\n\n"
jobs = {}
snip = open(f'{B}/gate-time-snippets.txt').read().splitlines()
for name, lo, hi in (('gates-a', 25, 50), ('gates-b', 51, 75)):
    part = [l for l in snip if lo <= int(re.search(r' ch(\d+):', l).group(1)) <= hi]
    jobs[name] = head(GATES) + "SNIPPETS:\n" + '\n'.join(part)
for b in (30, 40, 50, 60, 70):
    body = ''.join(f"\n===== {os.path.basename(os.path.dirname(f))} =====\n{open(f).read()}" for f in sorted(glob.glob(f'{B}/files/*/ck-ch0{b}.md')))
    jobs[f'mints-{b}'] = head(MINTS.format(b=b)) + body
if '--dry' in sys.argv:
    for k, v in jobs.items(): print(k, len(v), 'chars')
    sys.exit()
def run(name):
    out = f'{B}/out-{name}.json'
    if os.path.exists(out): return name, 'cached'
    for attempt in range(3):
        try:
            r = fn(prompt=jobs[name], model=MODEL, label=name)
            t = re.sub(r'^```(?:json)?\s*', '', r['output'].strip())
            t = re.sub(r'\s*```\s*$', '', t)
            data = json.loads(t)
            json.dump({'result': data, 'usage': r['usage']}, open(out, 'w'), indent=1)
            return name, r['usage'].get('cost')
        except Exception as e:
            open(f'{B}/err-{name}-{attempt}.txt', 'w').write(repr(e) + '\n' + (locals().get('r') or {}).get('output', ''))
    return name, 'FAILED'
with cf.ThreadPoolExecutor(7) as ex:
    for name, cost in ex.map(run, jobs): print(name, cost, flush=True)
