#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.40", "openai-codex"]
# ///
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
import hashlib
import os
import sys

REPO = Path(__file__).resolve().parents[3]
os.chdir(REPO)
sys.path.insert(0, str(REPO / 'tools'))

import authorship_audit  # noqa: E402
import cold_read  # noqa: E402
import checkpoint_bundle  # noqa: E402

ROOT = REPO / 'reviews' / 'capture-panel' / 'horizon-book-two-current-raw'
PANEL = REPO / 'reviews' / 'capture-panel'
PERSONAS = ['romance-graduate', 'fsog-refugee', 'consent-sensitive']
MODELS = ['claude-opus-4-8', 'gpt-5.6-sol', 'gpt-5.5']
PROTOCOL = 'book-two-current-raw-horizon-v2'

REVISED_JACKET = """A Warm Reception
Book Two of With a Long Spoon

Vee has learned what it is to be wanted. This spring, she learns her appetite runs in more directions than one.

Pace's house is warmer now: drawers that remember her, meals that answer before she asks, a man whose hands keep making room for what she is brave enough to name. Across the table, Randi's attention is no safer. The lunches are dinners now. The jokes have teeth. The woman who taught Vee not to be ashamed is becoming the want Vee can no longer keep safely unnamed.

Randi and Pace chose her together. Vee knows what she wants from each of them. She does not yet know how much of that wanting has been arranged.

Warmer and more explicit than the book before it, A Warm Reception follows Vee through the spring of her own appetite: fuller, bolder, more honest in the body, and shadowed by the game still moving around her. Everything she gives is hers. Not every door has been opened. The closer she gets, the less she can see of the shape closing around her.
"""

GAPS = {
'inversion': ('Inversion','Unwritten vignette',"At Brooke’s Standards meeting, Randi—the sister who normally helps discipline others—is placed on the docket herself. The visible case is a ledger of missed obligations and her conspicuous behavior at the mixer; the unspoken case is the house’s growing suspicion around Vee. Randi accepts attendance probation and gives up Thursday dinners rather than invite scrutiny, then closes alone in her single with the cost of concealment. Sources: meta-plan-chronology Spring/Inversion; meta-note-inversion."),
'gesso': ('Gesso','Unwritten scene',"At the delayed Saturday brunch, Vee shows Randi the photograph of her waxed, painted body; Randi names it “Gesso,” the white ground beneath paint. Their charged account of Still Life circles the one taste Pace withheld, and when Vee asks whether it is gross, Randi refuses to validate the shame. Vee flees to the restroom, unexpectedly imagines what Randi would taste like, returns certain she looks guilty, and finds Randi’s knowing smile waiting; she leaves early to avoid the goodbye kiss she wants. Sources: meta-plan-chronology Spring/Gesso; meta-condensed-gesso."),
'bricklayers-game-tbd': ('The Bricklayers Game','Unwritten scene; title provisional',"Vee sits in the bleachers with Kayla and Meg to support Cassie at a Bricklayers game. It is a warm, nonsexual floor-world outing and Vee’s only real dodge of the post-Gesso week: Cassie’s game gives her an honest reason not to see Randi. The reader understands what that ordinary refuge is sheltering her from, while the scene resets the pressure without making anyone else privy to it. Source: meta-plan-chronology Spring/The Bricklayers Game."),
'safely-held': ('Safely Held','Unwritten scene',"At the Brooks & Dunn tribute night at The Usual, Pace brings Vee into Sheri’s country-western world. Dancing progresses from floor work to lifts, but when Vee says the lifts are too heavy, he offers and waits rather than putting her in the air without a yes. That refusal to override her hesitation lets the later airborne intimacy move from shame into ease, quietly rehearsing the trust required for restraint. Sources: meta-plan-chronology Spring/Safely Held; meta-condensed-safely-held."),
'held-loosely': ('Held Loosely','Unwritten SATC scene',"At their first dinner after a week of silence, Randi turns Brooke’s “too loose and sloppy” crackdown into a warm complaint, explaining the lost Thursdays without revealing that Vee is the hidden cause. Vee is relieved it was not her, though the new once-a-week pattern makes her want more of Randi while fearing that want. They laugh away the mixer kiss, then Vee recounts the dance and a jar that finally gave way under Pace’s deliberately gentle restraint; her voice changes, and Randi learns how central tenderness is to Vee’s attachment. Sources: meta-plan-chronology Spring/Held Loosely; meta-condensed-held-loosely."),
'meg-beat-tbd': ('The Meg Beat','Unwritten scene; placement/title TBD',"After the game has established Meg as easy company, Vee tries to talk to her about sex and relationships. Meg is practical and untroubled—“it’s just sex”—and that normalization makes Vee’s experience feel too large to name. The conversation remains light and Meg remains unwounded, but Vee cannot say that what she has with Randi is not just sex without exposing what it is. Source: meta-plan-chronology Spring/The Meg Beat."),
'winter-wonderland': ('Winter Wonderland','Unwritten scene; snow-window placement unfixed',"On a snow day, Vee and Pace browse a garage sale, where he buys an old Flexible Flyer sled, then take it onto the hills above Blacksburg. The point is their clumsy warmth and laughter in the cold rather than sex: one of the light outings that earns later darkness. It may be a garage-sale/sledding diptych, but its exact position is constrained only by the winter snow window. Source: meta-plan-chronology Spring/Winter Wonderland. Underplanned beyond this."),
'grain-1-the-first-flicker': ('Grain #1 — The First Flicker','Unwritten vignette',"During an overnight ritual at Pace’s drawer, Vee notices that the scrunchie form may sit lower than it should. Her own use could explain a decline, so the anomaly is neither provable nor speakable; it folds into her larger anxiety about what Pace feels and will not name. The reader receives no certainty beyond Vee’s first half-conscious decision to watch. Source: meta-plan-chronology Spring/Grain #1."),
'grain-2-worn-in-plain-sight': ('Grain #2 — Worn in Plain Sight','Architecture complete; prose not drafted',"From March onward, Randi wears deep-green scrunchies like Vee’s, and Vee reads the sightings as an ecstatic sign that the glamorous friend is adopting her style. On the first spoken instance, Vee asks whether she has converted Randi; Randi answers, “You’ve ruined me. I used to have standards.” The common style and buyable-but-uncommon color preserve deniability, while later appearances become mere set dressing—except for one post-Restoration delay before Vee’s delight arrives. Sources: meta-plan-chronology Spring/Grain #2; meta-condensed-grain-2-scrunchies."),
'randi-social-price-2': ('Randi — Social Price #2','Unwritten vignette; slot TBD',"Randi quietly audits what months of absence have cost her: skipped events, uncollected standing, and a chapter social fabric beginning to pull away. No one confronts her; the point is the accumulated private reckoning. She still chooses the arrangement despite its price. Source: meta-plan-chronology Spring/Randi Social Price #2. Underplanned beyond this."),
'massage-table': ('Massage Table','Unwritten scene',"After Vee strains her neck at the gym, Pace buys—not builds—a massage table for her recovery. The deliberately ordinary, purchased apparatus is the anti-bench: he keeps her still because movement hurts, making restraint a medical, tender gift rather than a demand for proof. It also gives her relief from the shame of what her hands might involuntarily reveal, while introducing a restraint vocabulary that remains protective. Source: meta-plan-chronology Spring/Massage Table."),
'into-the-dark': ('Into the Dark','Unwritten scene; broad date window',"Vee and Pace take a day trip to a Virginia cavern, moving together through cool formations with the world above shut away. The outing’s closeness is the point, not a literal blindfold or a set-piece of sex. Their descent becomes a quiet thematic prefiguration of later surrender into darkness and being led where she cannot fully see. Source: meta-plan-chronology Spring/Into the Dark. Underplanned beyond this."),
'cabin-debrief-brunch': ('Cabin Debrief Brunch','Unwritten SATC scene',"After the cabin, Vee tells Randi that she let Pace watch her, naming the exposure she crossed. Randi warmly steers her away from shame or regret while privately receiving confirmation that the larger plan has reached its deepest level. Their goodbye lingers one beat too long; Vee explains the charge away, while the reader can later read the kiss as another step upward. Source: meta-plan-chronology Spring/Cabin Debrief Brunch."),
'claim': ('Claim','Unwritten scene',"After receiving Pace’s key and entering his house alone for the first time, Vee gives him green bedsheets to replace his white ones. The gift carries her private color into his most intimate room and reads as real gratitude and deepening love. Its timing also makes it a defensive claim after the kiss: she makes his bed hers just as access to him becomes most frighteningly open. Sources: meta-plan-chronology Spring/Claim; meta-note-in-her-place."),
'for-you': ('For You','Unwritten scene; placement provisional',"In Pace’s bed on white sheets, Randi and Pace move through the middle rung of their spring staircase. Randi asks what Vee’s mouth was like on his cock, laundering her desire through his pleasure; Pace gently turns the question toward whether Randi imagines Vee’s mouth on her. For one breath Randi nearly owns the wish, then wraps it back in “for Pace,” and Pace gives the concealment room rather than forcing a confession. Sources: meta-plan-chronology Spring/For You; meta-note-for-you."),
'break-set-piece-tbd': ('The Break Set-Piece','Unwritten scene; title provisional',"Separated over spring break, Vee discovers that missing Randi feels wrong in a way she cannot name. When Randi sends a topless sunbathing photo, Vee—alone in Pace’s house with his key—masturbates to it on her own green sheets. The photo strips away the usual lunch-story cover: for the first time the desired object is nakedly Randi herself. Source: meta-plan-chronology Spring/Break Set-Piece."),
'deep-end': ('The Deep End','Unwritten scene',"Pace casually calls synchronized swimming dumb, not realizing Vee did it for eight years. Offended, she brings him to a pool, demonstrates what she knows, and watches him fail completely at trying it. For once she is the expert and he the ungainly beginner; laughter dissolves the slight without requiring an apology he does not quite understand he owes. Source: meta-plan-chronology Spring/Deep End."),
'cassie-spring': ('Cassie — Spring','Unwritten vignette',"Cassie tries to reconnect, but Vee arrives only half-present. Cassie observes, “She’s really involved in your life now, isn’t she?” and Vee produces a ready explanation. The distance is named from both sides and dismissed in the same motion, leaving the reader to feel what Vee cannot admit. Source: meta-plan-chronology Spring/Cassie Spring."),
'secret-plans-the-ask': ('Secret Plans — The Ask','Architecture complete; prose not drafted',"In a quiet domestic moment, Vee makes her first act of erotic authorship: she invites Pace on an “adventure.” Shy but brave, she supplies only the premise—a space princess chased, captured, stripped, and interrogated for secret plans she will never reveal—and leaves the torture to him. She authors the wish rather than the execution, making her first time holding the pen also an act of handing herself over. Sources: meta-plan-chronology Spring/Secret Plans; meta-condensed-secret-plans; meta-note-secret-plans."),
'secret-plans-the-princess': ('Secret Plans — The Princess','Architecture complete; prose not drafted',"On a warm afternoon in full daylight, Vee runs across Pace’s private land in the costume he has made to reveal her as it tears. She is fluent in the princess fiction while he begins stiffly, then warms to her delight; when she seems to escape, her body betrays disappointment and his sudden surge reveals he has been toying with her. Capture turns the playful chase into an interrogation where hands and alien-tech devices control when relief comes, stripping away both the costume and her defiant persona until only their real dynamic remains. Sources: meta-plan-chronology Spring/Secret Plans; meta-condensed-secret-plans; meta-note-secret-plans."),
'secret-plans-brunch-retell': ('Secret Plans — Brunch Retell','Unwritten SATC scene',"Vee gives Randi her first authored retell, describing the adventure she conceived rather than merely material Randi has extracted from her. That self-authorship unsettles Randi’s usual position: she feels jealousy, lost leverage, and fascination at once, but the wound appears only in a wordless tell. The retell foregrounds how the theatrical game became real to Vee, with the clamps surviving as part of the “torture” rather than becoming the center of the story. Sources: meta-plan-chronology Spring/Secret Plans retell; meta-condensed-secret-plans; meta-note-secret-plans."),
'grain-3-the-restoration': ('Grain #3 — The Restoration','Architecture complete; prose not drafted',"Alone at the drawer, Vee sees the form has gone up: roughly four scrunchies have returned, an impossible direction in an arrangement where Pace never touches her things and she never rethreads them. She briefly wonders whether he quietly noticed she was running low, then rejects the comforting story because his respectful noninterference is precisely what the drawer means. With no outward explanation available, she concludes she must be wrong about what she saw, learning to distrust her own accurate readings. Sources: meta-plan-chronology Spring/Grain #3; meta-condensed-grain-3-restoration."),
'found-hair': ('The Found Hair','Architecture complete; prose not drafted',"Vee finds a long dark hair on Pace’s couch or in his kitchen, not in the bedroom. Her body flinches first, then she immediately files it under Sheri—the safe woman—and does not investigate whether Sheri has ever actually been in the house. The trace resolves into a warm, fond thought, showing how thoroughly Vee has learned to wave off an anomaly when an innocent story is available. Sources: meta-plan-chronology Spring/Found Hair; meta-note-the-found-hair."),
'ordinary-hang': ('Ordinary Hang','Unwritten vignette',"Randi and Vee simply spend time together—studying for anthropology finals, sharing a night in Randi’s single, or taking a walk. It is explicitly not a debrief: nothing major need be said. The reader instead feels how a friendship can be genuine and dangerous at once, with Randi’s steering invisible because the relationship has its own ordinary momentum. Source: meta-plan-chronology Spring/Ordinary Hang. Underplanned beyond this."),
'scar': ('The Scar','Architecture complete; prose not drafted',"Vee returns to the scar she first asked about on the porch, still half-looking for a vulnerability in Pace’s armor. This time he tells her, flatly and without dramatizing it, that his father tied his bike to a car and dragged it because he thought it would be funny. Vee receives the disclosure as a reason to love him more, while the account’s sealed temperature and casual cruelty leave the reader with the colder resonance. Sources: meta-plan-chronology Spring/The Scar; meta-note-scar-reveal."),
'cassie-may': ('Cassie — May','Unwritten vignette; title provisional',"Just before Cassie leaves for her nursing internship, she and Vee celebrate over lunch: each has earned a summer fieldwork or internship placement, and their friendship is briefly rendered as a mutual peer relationship. Cassie offers a small, funny dating story of her own, an ordinary invitation to reciprocal disclosure. Vee cannot match it, because her own coin is untellable; the gap remains quiet rather than accusatory. Source: meta-plan-chronology Spring/Cassie May."),
'first-taste-slot-tbd': ('First Taste','Unwritten scene; exact title/slot TBD',"Just before Vee on the Bench, Vee crosses the year-long boundary against tasting herself, and the crossing must be pleasant as well as chosen. Wearing Pace’s costly ivory chemise with pearls and no panties, she tests his whiskey/white-wine language against her own tongue after he offers her a taste; “A shot?” lets her enter through play rather than retreat. He extends her pleasure until need helps overcome the remaining resistance, then gives her release immediately, leaving the act as real liberation with an unresolved instrumental edge. Sources: meta-plan-chronology Spring/First Taste; meta-note-taste-thread."),
}

BOOK2_ORDER = [
('draft','missed-a-spot'),('draft','back'),('draft','unpacking'),('draft','across'),('draft','covering'),('draft','among-friends'),('draft','clean-plate'),('draft','reach'),('draft','my-pleasure'),('draft','another-round'),('draft','hangover'),('draft','barely-stings'),('draft','still-life'),('draft','on-her-floor'),('draft','boyfriend'),('draft','coming-due'),('draft','some-of-mine'),('gap','inversion'),('gap','gesso'),('gap','bricklayers-game-tbd'),('gap','safely-held'),('gap','held-loosely'),('gap','meg-beat-tbd'),('gap','winter-wonderland'),('gap','grain-1-the-first-flicker'),('gap','grain-2-worn-in-plain-sight'),('gap','randi-social-price-2'),('draft','burn'),('gap','massage-table'),('gap','into-the-dark'),('draft','grace'),('gap','cabin-debrief-brunch'),('gap','claim'),('gap','for-you'),('gap','break-set-piece-tbd'),('gap','deep-end'),('gap','cassie-spring'),('gap','secret-plans-the-ask'),('gap','secret-plans-the-princess'),('gap','secret-plans-brunch-retell'),('draft','in-her-place'),('gap','grain-3-the-restoration'),('gap','found-hair'),('gap','ordinary-hang'),('gap','scar'),('gap','cassie-may'),('gap','first-taste-slot-tbd'),('draft','vee-on-the-bench')]

VOLUME_THREE_ENDING_PACKET = """This is authorial/planning disclosure, not jacket copy and not drafted prose. It gives the intended ending shape so you can judge whether the delayed reveal/reckoning is structurally tolerable.

1. The series is designed as three continuous volumes. Book Two is escalation, not payoff. Book Three carries the frame/deed/reveal/reckoning.
2. The reveal remains late in Book Three. The planned climactic encounter is a threesome Vee agrees to under clean surface terms: she asks for a woman, a blindfold, surprise/binding terms. The consent structure is clean on its face but materially deceived because she does not know the woman is Randi or that Pace/Randi built the path together.
3. Recognition comes through the kiss, then sight. It is not a whodunit. The sequence is kiss, recognition, sight; then recognition, retroactive reconstruction, physical awareness, shame, anger, and friendship betrayal. The reveal is meant to reorganize the year behind her.
4. The ending is not a compressed forgiveness or reconciliation. The plan says there is no road back. The door is quietly and permanently shut. Nobody gets resolution; everybody gets the truth.
5. Vee does not stay for a repair conversation. She integrates rather than breaks down, frees herself, removes the blindfold, ignores Pace and Randi, and leaves looking at the objects rather than the people. She gives Pace and Randi nothing.
6. Vee leaves hurt but ascendant: full knowledge, full anger, full ownership of her transformation. The appetite does not turn off, but she keeps the no. Her forward motion carries grief, watchfulness, and hunger, not romantic repair.
7. The material ending object is anti-reunion: something left in Pace's house remains an artifact, unfinished and unfixable, not a promise she returns.
8. The final scene is the Cassie debrief weeks later. Vee returns to campus and tells Cassie everything. This is the thesis-delivery scene, not a romantic reconciliation. Vee can recount what happened, but the cost stays partly beyond words. Cassie may still say the experience sounds worth signing up for; the point is not to resolve their disagreement, but to show that the cost cannot be known until lived.
"""

ARM_A_QUESTIONS = """Answer in your persona. Label A1 through A5.
A1 — Jacket only: does this revised Book Two jacket fairly prepare you for Book Two as escalation-without-reckoning, or would you still feel misled if Book Two ends with the hidden arrangement unresolved?
A2 — Based only on this jacket and your Volume One experience, do you buy Book Two? What are you expecting it to pay, and what are you willing to let it defer?
A3 — Does the jacket make the hidden arrangement feel like a live wound/coming bill, or merely sexy complication/flavor?
A4 — What one jacket sentence or promise is most important to keeping your trust?
A5 — What jacket move would make you not buy Book Two?
"""
ARM_B_QUESTIONS = """Now answer after reading the current Book Two raw-prose + sourced-gap-summary packet. Label B1 through B7.
B1 — Does this current material earn Book Three if Book Two ends warm, with Vee naming wanting Randi, but with the full Pace/Randi truth still hidden from her?
B2 — Is your anger productive hunger, or has it crossed into distrust? What exact material decides that?
B3 — Do the drafted pages already show enough dread/cost/counter-voice around the concealment, or do they mostly make the lie more comfortable to live inside?
B4 — Which drafted scene/beat most keeps your trust? Which most threatens it?
B5 — What must the remaining gap-summary scenes do, short of reveal, to preserve your trust?
B6 — What is your concrete DNF line entering Book Three after this Book Two?
B7 — If you do buy Book Three, are you buying because you trust the book, because you are trapped by investment, or both?
"""
ARM_C_QUESTIONS = """Now answer after seeing the intended Volume Three reveal/fallout ending packet. Label C1 through C6.
C1 — Does this ending packet change your answer about whether the trilogy can hold the reveal until late Book Three?
C2 — Does late reveal followed by no-road-back crash-out, Vee gives them nothing, and Cassie debrief answer your fear of Pace/Randi getting away with it, or is the delay still too long?
C3 — Is the delayed reveal tolerable as retrospective contamination if the ending is terminal/ascendant rather than reparative?
C4 — What must Book Two do so this ending feels earned rather than like the book used Vee’s uninformed desire for too long?
C5 — What must Book Three do before the reveal, if anything, to avoid losing you before the planned crash-out?
C6 — Final commercial verdict after this jacket + current Book Two packet + ending packet: do you keep reading through Book Three? yes/no/only-if. State the condition or breaking point in one sentence.
"""


def clean(text: str) -> str:
    return '\n'.join(line.rstrip() for line in text.strip().splitlines()) + '\n'

def digest(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:12]

def volume_two_packet() -> str:
    parts = ['This packet is chronology-ordered. DRAFTED sections contain current raw cleaned prose. UNWRITTEN sections contain substantive summaries from live chronology/companion notes. Treat gap summaries as intended remainder, not executed prose.\n']
    for idx, (kind, slug) in enumerate(BOOK2_ORDER, 1):
        if kind == 'draft':
            title = checkpoint_bundle.display_title(slug)
            parts.append(f'===== BOOK TWO ITEM {idx}: {title} — DRAFTED RAW PROSE ({slug}.md) =====\n\n{checkpoint_bundle.clean_scene_text(slug)}\n')
        else:
            title, status, summary = GAPS[slug]
            parts.append(f'===== BOOK TWO ITEM {idx}: {title} — {status} ({slug}) =====\n\n{summary}\n')
    parts.append('===== BOOK TWO CURTAIN / LIVE STATUS NOTE =====\n\nThe current drafted Vee on the Bench ends in reciprocal aftercare/sleep. The planned act-three revision adds Vee naming to Pace, with her own mouth, that she wants Randi. The intended Book Two endpoint is warm: the want named, the deed unframed, and the full Pace/Randi truth still hidden from Vee.\n')
    return '\n'.join(parts)

def persona_system(persona: str) -> str:
    core = (PANEL / 'prompts' / 'core.md').read_text(encoding='utf-8')
    pers = (PANEL / 'personas' / f'{persona}.md').read_text(encoding='utf-8')
    attention = core.split('You will be given up to four chapters', 1)[0].rstrip()
    return attention + '\n\n' + pers.strip() + '\n\nYou are answering a continuation/horizon interview as this reader after Volume One. Stay in persona. Be candid about purchase, trust, anger, and DNF lines. Do not be patient out of politeness. Do not raise contraception, STI, pregnancy, or safer-sex logistics.\n'

def prior_path(model: str, persona: str) -> Path:
    return PANEL / model / f'{persona}--volume-dag-interview.md'

def output_path(model: str, persona: str, arm: str) -> Path:
    return ROOT / model / f'{persona}--{arm}.md'

def write_output(model: str, persona: str, arm: str, system_sha: str, prompt_sha: str, source: str, answer: str) -> None:
    out = output_path(model, persona, arm)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(f'# Book Two current raw horizon — {persona} · {arm}\n\n*model: {model} · persona: {persona} · arm: {arm} · protocol: {PROTOCOL} · source: {source} · system-sha: {system_sha} · prompt-sha: {prompt_sha} · run: {date.today().isoformat()}*\n\n{clean(answer)}', encoding='utf-8')

def validate(arm: str, answer: str, label: str) -> str:
    text = clean(answer)
    if len(text) < 600:
        raise RuntimeError(f'suspiciously short {label}: {len(text)} chars')
    need = {'arm-a-jacket': 'A5', 'arm-b-current-raw-gap': 'B7', 'arm-c-ending-disclosure': 'C6'}[arm]
    if need not in text:
        raise RuntimeError(f'malformed {label}: missing {need}')
    return text

def call_model(model: str, system: str, prompt: str, label: str, codex_fn=None) -> str:
    if model.startswith('claude-'):
        return authorship_audit.run_claude(model, system, prompt, label)
    if codex_fn is None:
        raise RuntimeError('codex_fn required')
    return (codex_fn(prompt=prompt, model=model, label=label).get('output') or '')

def arm_a_prompt(model: str, persona: str) -> str:
    prior = prior_path(model, persona)
    return f'===== YOUR PRIOR VOLUME ONE INTERVIEW =====\nsource: {prior.relative_to(REPO)}\n\n{prior.read_text(encoding="utf-8")}\n===== END PRIOR INTERVIEW =====\n\n===== REVISED BOOK TWO JACKET COPY =====\n\n{REVISED_JACKET}\n===== END JACKET =====\n\n{ARM_A_QUESTIONS}'

def arm_b_prompt(answer_a: str, packet: str) -> str:
    return f'===== YOUR ARM A ANSWER =====\n\n{answer_a}\n===== END ARM A =====\n\n===== REVISED BOOK TWO JACKET COPY =====\n\n{REVISED_JACKET}\n===== END JACKET =====\n\n===== CURRENT BOOK TWO RAW-PROSE + SOURCED-GAP-SUMMARY PACKET =====\n\n{packet}\n===== END BOOK TWO PACKET =====\n\n{ARM_B_QUESTIONS}'

def arm_c_prompt(answer_b: str) -> str:
    return f'===== YOUR ARM B ANSWER =====\n\n{answer_b}\n===== END ARM B =====\n\n===== VOLUME THREE REVEAL / FALLOUT ENDING PACKET =====\n\n{VOLUME_THREE_ENDING_PACKET}\n===== END ENDING PACKET =====\n\n{ARM_C_QUESTIONS}'

def run_lane(model: str, persona: str, packet: str, codex_fn=None) -> str:
    system = persona_system(persona)
    s_sha = digest(system)
    pa = arm_a_prompt(model, persona)
    ans_a = validate('arm-a-jacket', call_model(model, system, pa, f'horizon-raw-v2-{model}-{persona}-A', codex_fn), f'{model}·{persona}·A')
    write_output(model, persona, 'arm-a-jacket', s_sha, digest(pa), str(prior_path(model, persona).relative_to(REPO)), ans_a)
    pb = arm_b_prompt(ans_a, packet)
    ans_b = validate('arm-b-current-raw-gap', call_model(model, system, pb, f'horizon-raw-v2-{model}-{persona}-B', codex_fn), f'{model}·{persona}·B')
    write_output(model, persona, 'arm-b-current-raw-gap', s_sha, digest(pb), str(output_path(model, persona, 'arm-a-jacket').relative_to(REPO)), ans_b)
    pc = arm_c_prompt(ans_b)
    ans_c = validate('arm-c-ending-disclosure', call_model(model, system, pc, f'horizon-raw-v2-{model}-{persona}-C', codex_fn), f'{model}·{persona}·C')
    write_output(model, persona, 'arm-c-ending-disclosure', s_sha, digest(pc), str(output_path(model, persona, 'arm-b-current-raw-gap').relative_to(REPO)), ans_c)
    return f'ok {model} {persona}'

def run_codex_model(model: str, packet: str) -> list[str]:
    def one(persona: str) -> str:
        system = persona_system(persona)
        fn, close = cold_read.make_codex_agent_fn(system_prompt=system, effort='low')
        try:
            return run_lane(model, persona, packet, codex_fn=fn)
        finally:
            close()
    out = []
    with ThreadPoolExecutor(max_workers=2) as pool:
        for fut in as_completed([pool.submit(one, p) for p in PERSONAS]):
            out.append(fut.result())
    return out

def write_records(packet: str) -> None:
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / 'VOLUME_TWO_RAW_GAP_PACKET.md').write_text(packet, encoding='utf-8')
    record = f'# Book Two current raw horizon instrument\n\nprotocol: {PROTOCOL}\nmodels: {", ".join(MODELS)}\npersonas: {", ".join(PERSONAS)}\nauth: subscription only; no OpenRouter\n\n## Arm labels\n\n- arm-a-jacket: revised Book Two jacket only, after prior Volume One interview.\n- arm-b-current-raw-gap: same jacket plus chronology-ordered Book Two packet: drafted scenes as raw cleaned prose; undrafted slots as substantive sourced gap summaries.\n- arm-c-ending-disclosure: same lane after actual Volume Three reveal/fallout planning disclosure.\n\n## Revised Book Two jacket\n\n{REVISED_JACKET}\n## Volume Three ending/reveal/fallout packet\n\n{VOLUME_THREE_ENDING_PACKET}\n## Arm A questions\n\n{ARM_A_QUESTIONS}\n## Arm B questions\n\n{ARM_B_QUESTIONS}\n## Arm C questions\n\n{ARM_C_QUESTIONS}\n'
    (ROOT / 'INSTRUMENT.md').write_text(record, encoding='utf-8')

def main() -> None:
    packet = volume_two_packet()
    write_records(packet)
    failures = []
    results = []
    with ThreadPoolExecutor(max_workers=3) as pool:
        futs = [pool.submit(run_lane, 'claude-opus-4-8', p, packet) for p in PERSONAS]
        futs += [pool.submit(run_codex_model, m, packet) for m in ['gpt-5.6-sol', 'gpt-5.5']]
        for fut in as_completed(futs):
            try:
                res = fut.result()
                if isinstance(res, list):
                    results.extend(res); print(res, flush=True)
                else:
                    results.append(res); print(res, flush=True)
            except Exception as e:
                failures.append(str(e)); print('FAIL', e, flush=True)
    print('\nfinished', len(results), 'lanes ok')
    if failures:
        print('failures:')
        for f in failures:
            print(' ', f)
        sys.exit(1)

if __name__ == '__main__':
    main()
