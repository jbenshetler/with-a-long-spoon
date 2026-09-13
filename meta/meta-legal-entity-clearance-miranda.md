# Entity-name clearance — the father's company (`{{The Outlier}}`)

*Record of a name-collision check run 2026-09-13, the collision it found, and the
replacement it cleared. Written to be re-verifiable by a third party years later:
every source, method, date, and artifact is named, and the raw extracts are
committed alongside in `meta/entity-clearance/`. Companion to
`meta-plan-legal-read.md` (item [5]) and `meta-plan-lawyer.md`.*

> ## ⚠ CANON GUARD — read before quoting anything below
>
> **The father's company is `Miranda Interests, LLC` — canon, but NOT rendered in
> Volume 1's prose. The on-page tag is `MIRA`.**
>
> The name **`Miranda Holdings, LLC`** and the tag **`MIRH`** appear throughout
> this file as the **RETIRED** name and as the name of a **real, unrelated
> company**. They are not canon and must never be returned as canon.
>
> This is a legal/provenance record, not a canon source. For the company's name
> go to `meta-arch-randi.md`, `meta-arch-bible.md`, or `outlier.md`. This file is
> the only doc in `meta/*.md` that still contains the retired name, and it is
> indexed by `na.py` and matched by `rg` — hence this guard.

**Outcome, in two steps.** (1) Canon name `Miranda Holdings, LLC` →
**`Miranda Interests, LLC`**, cleared across three indexes. (2) Then, going
further: **Volume 1's prose no longer names the company at all** — the reveal
renders only `MIRANDA`, and the tag is **`MIRA`** (`MIRH` → `MIRA`). The cleared
canon name is held in the planning docs for later volumes. The retired name
survives only in this record and in `meta-plan-legal-read.md` /
`meta-plan-lawyer.md`, where it documents the collision.

---

## 1. Why this check was run

`{{The Outlier}}` shows Randi building a PPP data visualization for a stats
project, driving into her own home county, and finding the county's worst
outlier. The dot resolves to her father's holding company — named for her. The
prose puts a real federal dataset on the page, and at the time of this check it
named the company. *(For exactly what the page does and does not assert, see the
precision note below — it is narrower than this paragraph once read closely, and
the company is no longer named at all.)*

The exposure is **defamation of a business entity / trade libel by name
collision**: if a real company shares the name, a reader who searches it lands on
a real business against the novel's depiction. The 2026-08-01 per-chapter legal
scan flagged this at risk 2 (`meta-plan-legal-read.md` item [5]) with the
mitigation "run a quick entity search." This is that search, run properly.

### What the page actually depicts — stated precisely, because it bounds the risk

Recorded carefully (author correction, 2026-09-13) so this file never overstates
the novel's own conduct. An earlier draft of this record said the book "shows
that company taking PPP loans and cutting its workforce anyway." **It does not.**
That imports the planning docs' knowledge (`meta-arch-randi.md`) onto a page that
is more restrained.

**On the page:** a government PPP record showing *"the loans, several of them,
one company under another, and beside each loan the thing the loan had been for
and had not done"*, sitting over *"the worst point in the county."* Randi says
*"Cheating bastards."* Cassie — **who cannot see the screen** — says *"One
company, that size, everybody cut anyway."*

> ### Superseding mitigation — the prose no longer names the entity (2026-09-13)
>
> After the rename, the author went further: **Volume 1's prose never names the
> company, the state, or the county.** The reveal now renders only
> *"the first word of the name was MIRANDA"*; the word `LLC` no longer appears in
> the chapter, and the tag became `MIRA` (the first four letters of MIRANDA, so
> it derives from the only thing shown). No jurisdiction was ever named — "the
> state numbers", "County after county", "her county", Cassie's "flat rural
> nowhere".
>
> **Effect on the risk: the adverse statements no longer attach to any named
> entity.** An unnamed company cannot be defamed — there is no "of and
> concerning" any real business. What remains is a character's epithet about her
> own father (*"Cheating bastards"*) and a blind generalization about "one
> company, that size."
>
> `Miranda Interests, LLC` **remains canon** in the planning docs and remains
> cleared by §§2–4, so a later volume can put it on the page if wanted. Craft rule
> and rationale: `meta-note-outlier.md` § MIRA.

**Not on the page:** any dollar amount. The word *fraud*. Any narration
confirming layoffs at this company. Cassie's line is a generalization about the
aggregate pattern that lands on Randi's father by coincidence, not an assertion
by the book about this entity.

**Inference only, never stated:** family wealth in the $10M+ range, read off
lifestyle (whim purchases of very expensive shoes; Gstaad at Christmas). That
sizes the *family*, not the loans. **No conclusion about loan size, or about
which PPP disclosure tier the fictional company would occupy, is available from
the text** — an earlier draft of this record inferred the $150k+ tier from the
"multiple millions" figure and was wrong to; that figure describes wealth, not
loans.

None of this weakens the finding in §3. The rename is required because a real
company bearing the name is findable in the dataset the scene depicts —
independent of how large the fictional loans are or how explicitly the book
characterizes them.

## 2. What was checked, and how

Three independent indexes. A name is only cleared if it is clean in all three.

### 2.1 Virginia business entity registry

- **Registry:** Virginia has **no Secretary of State business registry.** Unlike
  most states, business entities are registered with the **State Corporation
  Commission (SCC)**, through the **Clerk's Information System (CIS)** at
  <https://cis.scc.virginia.gov/>. Anyone searching "Virginia Secretary of State
  business search" will be looking in the wrong place; the SCC is the authority.
  *Verified 2026-09-13: the system self-identifies as "Clerk's Information
  System." Its search interface was not itself exercised for this record — see
  provenance below.*
- **Search performed by:** the author, against CIS, query "Miranda", exported to
  CSV and supplied on 2026-09-13. **Not independently re-run by the assistant**,
  which verified the file's contents but not the act of searching. A verifier who
  wants the check end-to-end should re-run the CIS query and compare against the
  committed export.
- **Artifact:** `meta/entity-clearance/va-cis-entity-search-miranda-20260913.csv.xz`
  (author-supplied, search on "Miranda"). sha256 of the **uncompressed** CSV as
  supplied: `3d90a696c4d70eac81045a1c9011fe578e45dd3fe1c23b7681fe3e4a1b8f5796`
  (15,175 bytes); the `.xz` wrapper's own hash is in `SHA256SUMS.txt`.
- **Result: 95 entities. 49 Active, 43 Inactive, 3 Pending Inactive.**
  Among the Active: **`Miranda Holdings, LLC`**.
- Also Active, so unavailable as suffixes: Ventures, Group, Properties, Realty,
  Capital, Investments, Partners, Management, Communications, Construction,
  Consulting, Farms, Solutions Group, and others.

> ### ⚠ A null result that is NOT clearance — record and do not repeat
>
> A search was also run at
> `https://www.scc.virginia.gov/boi/consumerinquiry/search.aspx?searchType=agent`
> for Virginia companies containing "Miranda", and returned **no hits**.
>
> **That null is meaningless.** `scc.virginia.gov/boi/` is the SCC's **Bureau of
> Insurance** consumer inquiry. Verified 2026-09-13: it searches licensed
> insurance **agents**, insurance **agencies**, insurance **companies**, and
> insurance **navigators** — never general business entities. Its own page reads
> *"Select or enter your search criteria into any or all search fields"* across
> those four databases.
>
> The correct index returned 95 hits including an Active `Miranda Holdings, LLC`
> for the same query. Same commission, different bureau, opposite answer. **Any
> future entity check must use `cis.scc.virginia.gov`, not `/boi/`.**

### 2.2 Open web

Searched each candidate as a quoted company name. Findings recorded because
absence from a state registry does not imply absence nationally:

- `Miranda Holdings LLC` — real, Houston TX (Dun & Bradstreet listing).
- `Miranda Enterprises LLC` — real and active: Turlock CA (trucking, DOT
  #3076576) and Linden NJ (consulting); plus a dissolved FL entity.
- `Miranda Industries, LLC` — real, active FL LLC (Miramar), plus an FMCSA
  carrier.
- `Miranda and Associates` — historical family CPA firm, antecedent of Miranda
  Investment Partners.
- `Miranda Interests LLC` — **no match found anywhere.**
- `Miranda Affiliates` / `Miranda Consolidated` — no match found.

### 2.3 SBA PPP loan-level FOIA data — the decisive index

This is the dataset the scene actually depicts, so a hit here is materially worse
than a registry hit: it is a name match *and* a conduct match in the same public
record.

- **Source:** <https://data.sba.gov/dataset/ppp-foia> — "loan-level data on all
  disbursed PPP loans", U.S. Small Business Administration, public domain.
- **Release scanned:** the `240930` (2024-09-30) release, 13 CSVs —
  `public_150k_plus_240930.csv` plus `public_up_to_150k_1..12_240930.csv`,
  ~5.2 GB total.
- **Downloaded:** 2026-09-13. Files were **streamed and filtered, never stored**.
- **Source fingerprints** (byte length, ETag, Last-Modified for all 13 files, as
  served on 2026-09-13): `meta/entity-clearance/ppp-source-manifest-20260913.csv`.
  All 13 carry `Last-Modified: Fri, 26 Jun 2026`. These stand in for checksums of
  files that were never written to disk, and let a later verifier confirm they
  fetched the same bytes.
- **Two passes were run**, deliberately kept separate:
  1. **Byte-oriented `grep`** over candidate suffixes —
     `meta/entity-clearance/ppp-grep-20260913.sh`. Output (full source rows, 10
     loans): `ppp-miranda-namehits-20260913.csv.xz`.
  2. **Parsed extract** of every borrower whose name begins with the token
     MIRANDA — `meta/entity-clearance/ppp-filter-20260913.py`. Output (1,231
     loans, 884 distinct names; columns BorrowerName, BorrowerCity,
     BorrowerState, CurrentApprovalAmount):
     `ppp-miranda-extract-20260913.csv.xz`.
- **Column layout** of the source as served: `ppp-columns-150k-plus.txt`.
- **Integrity:** `meta/entity-clearance/SHA256SUMS.txt` covers every artifact.

### 2.4 Why the artifacts are compressed

Deliberate (author ruling 2026-09-13), and **not** for space — the extracts are
46 KB and 4.6 KB raw. They are *evidence*, opened only to prove due diligence,
and must not behave like working material: `.xz` keeps them out of `rg`/`grep`
results and out of any future search over the corpus, so a name-collision
worksheet can never surface as if it were canon. `na.py` already ignores them on
two counts — it globs `meta/*.md` **non-recursively**, so neither this
subdirectory nor non-`.md` files are indexed. They are far too small for
git-LFS, which would add indirection and a clone-time dependency to manage
kilobytes; the repo already tracks 10 MB cover PNGs in plain git. Leave them
here, compressed, uncompressed only when a question is actually asked.

> **Reproduction warning, learned the hard way.** The SBA CSVs are **latin-1, not
> UTF-8.** A Python reader using the default encoding raises `UnicodeDecodeError`
> on the first non-ASCII byte of each file and *silently truncates the scan* —
> the first attempt at pass 2 returned **2 rows instead of 1,231** and looked
> like a clean result. The committed filter sets
> `sys.stdin.reconfigure(encoding='latin-1', errors='replace')`. Pass 1 was
> unaffected because `grep` does not decode. Anyone re-running this must confirm
> the row count, not just the absence of hits.

## 3. What the PPP scan found

**The collision — `MIRANDA HOLDINGS INC`, North Boston, NY, $885,600, Paid in
Full.** A real company bearing the fictional company's name, in the very dataset
the novel depicts, against a scene in which a company of that name appears as a
county's worst PPP outlier whose loans did not do what they were for, and is
called "cheating" by a character. `Inc` vs `LLC` is no protection; a reader
searching "Miranda Holdings PPP" reaches it immediately.

Mitigating but not exculpatory: the real borrower is a **single sub-$1M loan** in
upstate New York, where the fictional entity is *"several [loans], one company
under another."* Structurally different on inspection — but the search still
lands, and the book's own characterization ("cheating," a loan that "had not
done" what it was for) is adverse enough that a name match is worth removing
rather than defending.

**`Miranda Enterprises` independently disqualified** — real PPP borrowers in
Delaware (two loans, Ocean View) and Oklahoma (Pryor).

**`Miranda AND Associates LLC`** appears in the data, disqualifying *Associates*.

## 4. Candidate matrix (all three indexes)

*The **Tag** column records selection-time reasoning only. It became moot when the
prose stopped naming the company — the on-page tag is now `MIRA`, derived from
`MIRANDA`, whatever the suffix. See §5 item 3.*

| Suffix | VA registry | Open web | PPP data | Tag | Verdict |
|---|---|---|---|---|---|
| **Interests** | clean | clean | clean | `MIRI` | **SELECTED** |
| Consolidated | clean | clean | clean | `MIRC` inert | viable fallback |
| Affiliates | clean | clean | clean | `MIRA` = "look" | rejected — tag is a tell |
| Holdings | **ACTIVE** | Houston TX | **$885,600 NY** | `MIRH` | **disqualified** |
| Enterprises | clean | CA, NJ active | **DE, OK loans** | `MIRE` | disqualified |
| Associates | clean | CPA firm | **`MIRANDA AND ASSOCIATES LLC`** | `MIRA` | disqualified |
| Industries | clean | active FL LLC | clean | `MIRI` | disqualified |
| Capital / Properties / Investments | **in VA list** | — | mixed | — | disqualified |
| Ventures / Group / Realty / Partners / Management | **in VA list** | — | **taken** | — | disqualified |

Clean in VA + PPP but never web-checked, so **not cleared**: Equities, Estates,
Concerns, Assets, Companies, Trust.

## 5. Why `Miranda Interests, LLC`

1. **Clean in all three indexes** — the only candidate returning nothing
   anywhere, including no web match at all.
2. **"Miranda" is preserved, and it is load-bearing.** The father named the fraud
   company after his daughter; the reveal *is* the given name. Only the suffix
   was ever available to change. It also rhymes, unstated, with the name her
   parents wrote on her (`meta-arch-randi.md`: *"twice her family wrote on her
   name without asking"*).
3. ~~**The tag stays inert.**~~ **Selection-time reasoning, now MOOT — recorded
   because it drove the choice and must not be re-applied.** At selection the tag
   was derived from the *company name*, so the suffix determined it: `Interests`
   → `MIRI`, and candidates yielding `MIRA` (*Affiliates*, *Associates*) were
   rejected on the ground that `MIRA` reads as "look" in a novel about watching.
   **The subsequent prose change dissolved this criterion entirely.** With the
   company never named, the tag is derived from `MIRANDA` itself — so it is
   `MIRA` regardless of suffix, and the earlier objection is withdrawn as
   overstated: a tell gives away plot, and *mira* gives away none. Reasons 1, 2
   and 4–6 below are what actually carry the selection now.
4. **Rhythm holds.** *Interests* is stress-initial like *Holdings*, so the reveal
   line lands the same: *"and the name was Miranda Interests, LLC."*
5. **Plausible form.** "X Interests, LLC" is a standard holding-company
   construction for an operator with several businesses.
6. **It gains a resonance.** *Interests* = a financial stake, the interest a
   father takes in his daughter, and what a debt accrues — inside a book whose
   anthropology lectures run on reciprocity and gifts as debts *"you lay on
   someone whether they wanted it or not"* ({{Coming Due}}).

## 6. How to run a Virginia registered-name search properly

*Verified 2026-09-13. Reusable procedure for any future entity name in the novel.*

1. **Use the right system.** Virginia has **no Secretary of State** business
   registry — entities are registered with the **State Corporation Commission**,
   via the **Clerk's Information System**:
   <https://cis.scc.virginia.gov/EntitySearch/Index>. Free, no login.
   **Not** `scc.virginia.gov/boi/` (Bureau of Insurance — see §2.1 warning), and
   not a "Virginia Secretary of State" search, which does not exist.
2. **Expect a browser.** The search URL 302-redirects to `/Cookie/CookieConsent`,
   and the gate cannot be cleared with a cookie jar — `curl -b/-c` lands back at
   the consent page, and an automated fetch sees only the cookie banner. There is
   **no public REST API.** Verified 2026-09-13. The legacy endpoint
   `appspre.scc.virginia.gov/clk/bussrch.aspx`, still cited by third-party
   guides, is **404/dead**.
3. **Search the distinctive token, never the full candidate name.** Querying
   `Miranda Interests` returns nothing and *looks like clearance*; querying
   `Miranda` returns 95 entities including the Active `Miranda Holdings, LLC`.
   This is the same failure mode as the Bureau-of-Insurance null: a confident
   zero produced by too narrow a query. Use the broadest query that still bounds
   the result set.
4. **Include inactive entities.** A dissolved name can be re-registered, and a
   reader's web search surfaces dead companies as readily as live ones. Report
   the status breakdown, not just the active count.
5. **One field at a time** — CIS asks for this. Results carry entity name, SCC
   ID, status, entity type, formation date, registered agent, and filing history.
6. **Export the result** (CIS "Download Reports") and commit it. Capture the
   exact query string, the date, and the total with its status breakdown. That is
   what makes a later "did you check?" answerable.

**Know what this search does and does not answer.** A registry search answers
*"can this name be registered in Virginia."* The question here is *"will a reader
who searches this name find a real company"* — and readers use search engines,
not state registries. Virginia is therefore **one of three indexes and not the
decisive one**: `Miranda Enterprises` passed Virginia cleanly and was still
disqualified by real companies in CA, NJ, DE and OK. Always pair the registry
with §2.2 (open web) and §2.3 (the PPP data the scene depicts).

## 7. Standing guidance

- **This clearance is dated.** It reflects the registry as supplied, the web as
  of 2026-09-13, and the PPP `240930` release. Re-run before publication;
  registries change and the SBA reissues.
- **Re-run all three indexes** for any future entity name in the novel, and use
  `cis.scc.virginia.gov` — never `/boi/` (§2.1).
- **Verify row counts, not just hit counts**, when re-running the PPP scan (§2.2
  reproduction warning).
- **Item [5] does NOT close on this record.** The rename is *mitigation*; the
  item is **retained for the legal consult** by author ruling 2026-09-13, which
  judges the PPP-outlier scene the riskiest item in the book. An assistant
  recommendation to close it here was overruled. **The reason: this is the most
  adverse characterization in the book of anything even tangentially tied to a
  real legal entity** — a *named LLC*, of a real registrable type, described as
  having taken loans that "had not done" what they were for and called
  "cheating." Entities can sue for trade libel; nothing else in the sheet
  attaches adverse conduct to a named business. Reasoning and the questions for
  counsel: `meta-plan-lawyer.md` § [5]. *(A withdrawn earlier rationale — that
  the scene's reproducible research method was itself the risk — is recorded
  there as superseded: a research procedure is not actionable by anyone.)*
- **This record is the due-diligence exhibit** for that consult, together with
  `meta/entity-clearance/`. Keep both intact and dated; do not prune the
  superseded claims in §1, which show the analysis being corrected rather than
  quietly revised.
