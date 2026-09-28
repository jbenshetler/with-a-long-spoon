# Persona calibration report — window ch012–018 (drafts-2026-09-27)

**Design.** Window: chapters 12–18 (12 Leave No Trace · 13 Rye · 14 Swim Lanes · 15 What to Wear · 16 Two Towels · 17 A Round · 18 Turned Up). Memory: neutral `ensemble:core` checkpoint `ck-ch010` (not persona-owned — calibration deviation). Models: 4 subscription lanes (claude-opus-4-8, claude-opus-5, gpt-5.6-sol, gpt-5.5). Personas: 7 — five drafts (romance-graduate-v2, fsog-refugee-v2, consent-sensitive, romantasy-refugee, relationship-first) plus two v1 controls (romance-graduate, fsog-refugee). Frame: `core-window.md`. Each file carries GATE 12..18 (DECISION, CAPTURE, NEXT, HEAT, ROMANCE, ALMOST-STOPPED, WHY) and a NOTE TO A FRIEND.

**Files.** 28 of 28 read (`reviews/capture-panel/calibration/drafts-2026-09-27/<model>/<persona>--window-ch012-018.md`). `gpt-5.6-sol/romance-graduate` was absent at first listing and landed during the 90-second wait (mtime 16:33); it is included. All 196 gates are CONTINUE. One file (`claude-opus-5/romance-graduate-v2`) also carries free-prose paragraphs between its GATE blocks ("Chapter 13 — Huh. Two pages…" etc.); those paragraphs are outside the gate schema and were not counted or quoted — only its GATE fields and NOTE are used, like every other file.

Retell chapters = 13, 15, 18; scene chapters = 12, 14, 16, 17. All means are across the 4 models unless stated. Scales: CAPTURE/NEXT 0–10; HEAT/ROMANCE 0–3.


## 2. Tables

### TABLE A — mean CAPTURE / mean NEXT per persona × chapter (4 models)

| persona | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|
| romance-graduate-v2 | 9.0/8.8 | 6.2/7.5 | 9.0/9.2 | 6.0/8.5 | 8.8/9.8 | 10.0/9.0 | 6.5/7.8 |
| fsog-refugee-v2 | 9.8/9.2 | 6.8/8.0 | 8.2/8.8 | 7.2/9.2 | 9.5/10.0 | 10.0/10.0 | 7.8/8.8 |
| consent-sensitive | 8.8/8.8 | 6.8/7.8 | 8.8/8.8 | 6.5/8.2 | 8.8/9.5 | 9.8/9.0 | 7.2/7.8 |
| romantasy-refugee | 9.0/8.5 | 6.8/8.2 | 8.0/8.5 | 7.2/9.2 | 9.0/9.8 | 9.8/9.8 | 8.0/9.2 |
| relationship-first | 9.0/8.8 | 7.0/7.5 | 8.8/9.0 | 6.8/9.0 | 8.8/9.5 | 9.5/8.5 | 7.5/7.5 |
| romance-graduate | 9.2/9.2 | 6.8/8.2 | 8.5/9.0 | 6.8/9.0 | 9.5/10.0 | 10.0/9.8 | 7.5/8.8 |
| fsog-refugee | 9.5/9.2 | 7.2/8.0 | 8.5/8.8 | 7.2/9.5 | 9.5/9.8 | 10.0/9.8 | 8.0/8.8 |
| **all 7** | 9.2/8.9 | 6.8/7.9 | 8.5/8.9 | 6.8/9.0 | 9.1/9.8 | 9.9/9.4 | 7.5/8.4 |

### TABLE B — mean HEAT / mean ROMANCE per persona × chapter (4 models)

| persona | 12 | 13 | 14 | 15 | 16 | 17 | 18 |
|---|---|---|---|---|---|---|---|
| romance-graduate-v2 | 2.8/3.0 | 1.0/2.0 | 3.0/2.5 | 1.0/1.5 | 1.8/3.0 | 3.0/3.0 | 1.2/2.2 |
| fsog-refugee-v2 | 3.0/3.0 | 1.0/2.2 | 2.8/1.5 | 1.0/2.0 | 2.0/3.0 | 3.0/3.0 | 1.5/2.8 |
| consent-sensitive | 2.8/2.8 | 1.0/2.0 | 2.8/2.5 | 0.8/1.5 | 1.5/3.0 | 3.0/2.8 | 1.2/2.5 |
| romantasy-refugee | 2.8/2.8 | 1.0/2.0 | 3.0/1.8 | 1.0/2.0 | 1.8/3.0 | 3.0/2.8 | 1.5/2.5 |
| relationship-first | 2.8/3.0 | 1.0/2.0 | 3.0/2.2 | 1.0/1.5 | 1.8/3.0 | 3.0/2.8 | 1.5/2.2 |
| romance-graduate | 2.8/3.0 | 1.0/2.0 | 3.0/2.0 | 1.0/1.8 | 2.2/3.0 | 3.0/3.0 | 1.2/2.2 |
| fsog-refugee | 3.0/3.0 | 1.0/2.0 | 2.8/1.2 | 1.0/1.8 | 2.0/3.0 | 3.0/3.0 | 1.5/2.8 |
| **all 7** | 2.8/2.9 | 1.0/2.0 | 2.9/2.0 | 1.0/1.7 | 1.9/3.0 | 3.0/2.9 | 1.4/2.5 |

### TABLE C — per persona: STOPs, mean CAPTURE, mean NEXT (all 28 gates), mean NEXT−CAPTURE on retell (13/15/18) vs scene (12/14/16/17) chapters

| persona | STOPs | mean CAPTURE | mean NEXT | NEXT−CAPTURE retell | NEXT−CAPTURE scene | (retell − scene) |
|---|---|---|---|---|---|---|
| romance-graduate-v2 | 0 | 7.93 | 8.64 | +1.67 | +0.00 | +1.67 |
| fsog-refugee-v2 | 0 | 8.46 | 9.14 | +1.42 | +0.12 | +1.29 |
| consent-sensitive | 0 | 8.07 | 8.54 | +1.08 | +0.00 | +1.08 |
| romantasy-refugee | 0 | 8.25 | 9.04 | +1.58 | +0.19 | +1.40 |
| relationship-first | 0 | 8.18 | 8.54 | +0.92 | -0.06 | +0.98 |
| romance-graduate | 0 | 8.32 | 9.14 | +1.67 | +0.19 | +1.48 |
| fsog-refugee | 0 | 8.57 | 9.11 | +1.25 | +0.00 | +1.25 |

Per-model means over all 7 personas × 7 gates (CAPTURE / NEXT / HEAT / ROMANCE), for reading the persona rows against lane bias:

| model | CAPTURE | NEXT | HEAT | ROMANCE |
|---|---|---|---|---|
| claude-opus-4-8 | 7.67 | 8.27 | 1.80 | 2.18 |
| claude-opus-5 | 8.06 | 8.94 | 1.92 | 2.43 |
| gpt-5.6-sol | 8.73 | 9.31 | 2.10 | 2.61 |
| gpt-5.5 | 8.55 | 9.00 | 2.14 | 2.49 |

## 3. TABLE D — complaint mix per persona

Unit = one gate (WHY + ALMOST-STOPPED together) or one NOTE; 8 items per model, 32 per persona. An item is counted once per category it contains, judged by meaning. Category (d) includes both repeated phrases/motifs (the mother's voice, the shirt-on-the-pillow beat) and the over-explaining/telegraphing tic ("the book keeps telling me how to feel"). Category (e) counts an item only when the deception is voiced as unease, distrust, or a wish for the reveal/reckoning/Randi back in frame — not when chapter 14's irony is simply praised. Praise counts likewise by item.

| persona | (a) retell | (b) V+P apart | (c) more heat | (d) repetition/tic | (e) deception/reckoning | (f) Pace too perfect | (g) too small | (h) too short/episodic | any complaint | PRAISE Cassie | PRAISE talk texture | PRAISE ch14 | PRAISE ch17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| romance-graduate-v2 | 12 | 0 | 0 | 5 | 3 | 3 | 0 | 2 | 19 | 9 | 6 | 7 | 8 |
| fsog-refugee-v2 | 4 | 2 | 1 | 0 | 9 | 3 | 0 | 0 | 14 | 8 | 4 | 6 | 8 |
| consent-sensitive | 3 | 0 | 0 | 0 | 17 | 2 | 0 | 0 | 19 | 7 | 3 | 6 | 8 |
| romantasy-refugee | 3 | 0 | 0 | 6 | 7 | 4 | 0 | 0 | 15 | 10 | 7 | 5 | 7 |
| relationship-first | 7 | 0 | 0 | 19 | 2 | 6 | 1 | 2 | 25 | 9 | 8 | 6 | 7 |
| romance-graduate | 4 | 1 | 1 | 0 | 3 | 2 | 0 | 4 | 11 | 8 | 6 | 8 | 8 |
| fsog-refugee | 4 | 3 | 0 | 0 | 5 | 1 | 0 | 0 | 8 | 8 | 3 | 7 | 8 |

### Examples (one verbatim snippet per category per persona)

**romance-graduate-v2**

- (a) told twice / retell / recap — 12: *claude-opus-4-8, G18*: “this is now the second Cassie-debrief and the fourth retelling of scenes I watched happen, and the book has a rhythm going — big charged chapter, then Vee narrates it to a girlfriend”
- (d) repetition of phrase / prose tic — 5: *gpt-5.6-sol, G17*: “The shame spiraled long enough that I nearly felt the book pressing on the bruise after I had already understood it.”
- (e) the deception / wants reveal or reckoning — 3: *gpt-5.5, NOTE*: “I am still uneasy about Randi and Pace’s secret, especially because Vee’s happiness is so real now, and I can feel the bill coming due.”
- (f) Pace too perfect — 3: *claude-opus-5, G16*: “the résumé got one line too long and I felt the author's thumb on the scale”
- (h) chapter too short / episodic — 2: *gpt-5.6-sol, G13*: “This was so short I genuinely paused, because I have no established reader instinct for whether that means precision or shortcut.”
- PRAISE Cassie — 9: *claude-opus-5, G18*: “Cassie is a gift — "He sews," set down like a fact on a table”
- PRAISE talk / relationship texture — 6: *claude-opus-4-8, G13*: “"Borrow real boots next time / I'm keeping the shirt" is exactly how women who love each other talk”
- PRAISE ch14 (Randi/Pace) — 7: *gpt-5.6-sol, G14*: “Well, there’s the full heat, and it is not remotely interchangeable KU sex.”
- PRAISE ch17 (the fitting) — 8: *claude-opus-4-8, G17*: “This is the best sustained erotic scene I've read in a year and there's not a single act in it.”

**fsog-refugee-v2**

- (a) told twice / retell / recap — 4: *claude-opus-5, G13*: “I notice the book has now handed me the truck twice, and I was there the first time.”
- (b) too long since Vee and Pace alone — 2: *claude-opus-5, NOTE*: “she has been alone with him in roughly two of the last seven chapters and I *feel* that”
- (c) wants more sex or heat — 1: *gpt-5.5, G16*: “I had one awful second at the closed bedroom door where I thought, oh, please don't turn this into coy withholding just to stretch me out.”
- (e) the deception / wants reveal or reckoning — 9: *gpt-5.6-sol, NOTE*: “The secret with Randi is still the rot under everything—especially when Pace passes along something Vee gave only to him—and I do not forgive that just because everyone has feelings.”
- (f) Pace too perfect — 3: *gpt-5.5, NOTE*: “Pace is almost too much — powerlifter mathematician woodworker dressmaker patent guy, come on”
- PRAISE Cassie — 8: *claude-opus-4-8, G13*: “Cassie is the one clear-eyed person Vee has”
- PRAISE talk / relationship texture — 4: *claude-opus-5, G15*: “the table is genuinely good company, and Kayla calling the text a ransom note earned the whole scene”
- PRAISE ch14 (Randi/Pace) — 6: *claude-opus-5, G14*: “Nobody in this chapter is having fun the way they think they are. That's the only version of this I'd have stayed for.”
- PRAISE ch17 (the fitting) — 8: *claude-opus-4-8, G17*: “This is the best chapter I've read in this genre in years and I am not embarrassed to say it.”

**consent-sensitive**

- (a) told twice / retell / recap — 3: *claude-opus-5, G15*: “this one's calories come almost entirely from two girls reacting to a story I already read”
- (e) the deception / wants reveal or reckoning — 17: *claude-opus-4-8, G18*: “The conspiracy has been offstage since chapter 14 and this is four chapters of everything-is-lovely with only Cassie's not-quite-seeing as friction, and that's the exact drift that can lose me”
- (f) Pace too perfect — 2: *claude-opus-4-8, G16*: “the too-perfect man with the too-perfect wealth answer, and I felt the wish-fulfillment gears turn for a second”
- PRAISE Cassie — 7: *gpt-5.5, G13*: “She is not just comic relief or a suspicious friend; she is a witness who understands the stakes”
- PRAISE talk / relationship texture — 3: *claude-opus-4-8, G15*: “The friends are drawn well enough that I wanted the next chapter for the company, not just the plot.”
- PRAISE ch14 (Randi/Pace) — 6: *claude-opus-5, G14*: “That's my whole test and it passed it in a sex scene, which is the hardest place to pass it.”
- PRAISE ch17 (the fitting) — 8: *gpt-5.5, G17*: “the whole chapter is about the difference between being exposed and being consumed”

**romantasy-refugee**

- (a) told twice / retell / recap — 3: *claude-opus-5, G15*: “it's the third time and I'd like the book to vary the beat before I start skimming the tellings to get back to the doings”
- (d) repetition of phrase / prose tic — 6: *claude-opus-4-8, G17*: “the mother's-voice machinery has run so many laps now that I started to fear the book only knows one move: shame the body, then have the man redeem it”
- (e) the deception / wants reveal or reckoning — 7: *claude-opus-4-8, G18*: “I want the Randi shoe to drop, and I want it to cost.”
- (f) Pace too perfect — 4: *claude-opus-5, G16*: “somewhere in there the author stopped building a man and started pinning medals on him, and I felt handled”
- PRAISE Cassie — 10: *claude-opus-4-8, NOTE*: “Cassie is the friend everyone deserves and she's the reason I'm still in the boat.”
- PRAISE talk / relationship texture — 7: *claude-opus-4-8, G15*: “A world with more than two people in it, finally, and it's got teeth.”
- PRAISE ch14 (Randi/Pace) — 5: *claude-opus-5, G14*: “That's the good kind of ahead-of-the-character.”
- PRAISE ch17 (the fitting) — 7: *claude-opus-5, G17*: “A fully dressed man with a pencil behind his ear and a tape measure ran hotter than any door-closed scene I've read in five years”

**relationship-first**

- (a) told twice / retell / recap — 7: *claude-opus-4-8, G18*: “this is the second full debrief in a row of a scene I just lived through in close detail, and I could feel myself skimming toward the parts Cassie hadn't heard yet. The book is spending my goodwill on retelling.”
- (d) repetition of phrase / prose tic — 19: *claude-opus-5, G17*: “She's been invoked in nearly every chapter in the same italic register, and by now she's furniture in the bad sense”
- (e) the deception / wants reveal or reckoning — 2: *gpt-5.6-sol, NOTE*: “I’m now watching closely to see whether the secret arrangement deepens these people or starts operating them.”
- (f) Pace too perfect — 6: *claude-opus-5, G16*: “the tour is a man being assembled out of virtues”
- (g) book too small / wants more world — 1: *gpt-5.5, NOTE*: “I’m waiting for the book to let Vee’s women talk about more than him”
- (h) chapter too short / episodic — 2: *gpt-5.5, G13*: “This chapter is slight, but it has that post-event glow I like”
- PRAISE Cassie — 9: *claude-opus-5, G18*: “"Are you sure he's not gay?" is the funniest and truest thing anyone has said in this book”
- PRAISE talk / relationship texture — 8: *claude-opus-4-8, G13*: “This is what I stay for: the girl telling the girl”
- PRAISE ch14 (Randi/Pace) — 6: *claude-opus-5, G14*: “This is the chapter that made me think the book knows more than it's saying.”
- PRAISE ch17 (the fitting) — 7: *claude-opus-5, G17*: “the close-touch-withdraw-write rhythm is a real structural invention”

**romance-graduate**

- (a) told twice / retell / recap — 4: *claude-opus-5, G18*: “I generally hate the recap-to-best-friend chapter and I have now had three of them in seven, and yes, I clocked it.”
- (b) too long since Vee and Pace alone — 1: *claude-opus-4-8, G15*: “But it's a bridge, and I want the door open.”
- (c) wants more sex or heat — 1: *claude-opus-5, G16*: “I was fine with the dogs-are-barking bit and then wanted him to shut up and open the bedroom door.”
- (e) the deception / wants reveal or reckoning — 3: *claude-opus-4-8, NOTE*: “the best friend who could see the trap can't, and I can feel the book getting ready to hurt this girl while she's the happiest she's ever been”
- (f) Pace too perfect — 2: *gpt-5.5, NOTE*: “Pace is almost too good, which would usually make me roll my eyes”
- (h) chapter too short / episodic — 4: *gpt-5.6-sol, G13*: “Well, apparently we’re doing tiny chapters now. I don’t yet know whether that’s a trick I’ll love or start resenting”
- PRAISE Cassie — 8: *claude-opus-4-8, G13*: “Cassie is the one clear-eyed person in this whole book and I trust her”
- PRAISE talk / relationship texture — 6: *gpt-5.6-sol, G15*: “I could happily read women around a dining-hall table talking like this for pages”
- PRAISE ch14 (Randi/Pace) — 8: *claude-opus-5, G14*: “Oh, this is the chapter that makes the book.”
- PRAISE ch17 (the fitting) — 8: *gpt-5.5, G17*: “the hottest fitting scene I have ever read, and I say that as someone with a truly concerning Kindle history”

**fsog-refugee**

- (a) told twice / retell / recap — 4: *claude-opus-4-8, G18*: “this makes *three* chapters where the intimacy gets relived at a remove for a listener”
- (b) too long since Vee and Pace alone — 3: *claude-opus-4-8, G15*: “I want Vee and Pace *alone in a room* more than I want another retelling”
- (e) the deception / wants reveal or reckoning — 5: *gpt-5.6-sol, NOTE*: “the Randi-and-Pace chapter put a stone in my stomach—Vee gave Pace those private pieces of herself, not both of them, and their using her intimacy together is the first place the secret scheme felt like an actual violation”
- (f) Pace too perfect — 1: *gpt-5.5, NOTE*: “Pace is almost too much — math genius, powerlifter, woodworker, cook, tailor, patent money, emotionally precise mountain man, I mean come on”
- PRAISE Cassie — 8: *claude-opus-4-8, G13*: “Cassie is the friend who keeps this book honest”
- PRAISE talk / relationship texture — 3: *claude-opus-5, G15*: “Girls at a dinner table making a story better in the telling, twelve days counted without counting — that's how it actually is.”
- PRAISE ch14 (Randi/Pace) — 7: *claude-opus-5, G14*: “God, this chapter is clever and it hurt.”
- PRAISE ch17 (the fitting) — 8: *claude-opus-5, G17*: “Best chapter of the book and nobody took their clothes all the way off.”


## 4. Per-chapter output

Per persona: the 4 models' CAPTURE/NEXT/HEAT/ROMANCE on one line; then the WHY (verbatim) of the model whose (CAPTURE, NEXT) lies nearest the persona's 4-model mean for that chapter (Euclidean distance; ties broken by CAPTURE distance, then model order claude-opus-4-8, claude-opus-5, gpt-5.6-sol, gpt-5.5). For chapters 13, 15, 18, every ALMOST-STOPPED that is not a bare `none` is quoted verbatim with its model (entries reading `none — …` are included as written so the qualifier is visible).

### Chapter 12 — Leave No Trace

**romance-graduate-v2** — claude-opus-4-8 8/9/2/3 · claude-opus-5 9/9/3/3 · gpt-5.6-sol 10/9/3/3 · gpt-5.5 9/8/3/3 (mean 9.0/8.8)

> WHY (claude-opus-5): The middle of the ascent is the only place the book let me feel the page count — push and lift, push and lift, and I started skimming for the blue shirt. Then it paid me back twice over, first with the summit and then with a stripping scene that was entirely hers and still explicit enough to make my ears hot. The restraint isn't a closed door; the restraint is the heat. I would have read this chapter twice.

**fsog-refugee-v2** — claude-opus-4-8 9/9/3/3 · claude-opus-5 10/9/3/3 · gpt-5.6-sol 10/10/3/3 · gpt-5.5 10/9/3/3 (mean 9.8/9.2)

> WHY (claude-opus-5): This is the chapter I've been waiting years for someone to write. He gets out of the truck — that's it, that's the whole argument, a man who takes the rain so she can have the dry shirt and doesn't make a speech about it, and then she knocks on the glass and calls him back in and the choosing is *hers*, button by button, her eyes on his the entire way. He doesn't lift a hand. He doesn't get to be the one who takes it, and that's why it's the hottest thing I've read in the genre since I left it. The pit-on-the-wax-paper correction was the one second I felt the book grading her manners at me, and then she reached for another cherry and it was fine.

**consent-sensitive** — claude-opus-4-8 8/8/2/2 · claude-opus-5 9/9/3/3 · gpt-5.6-sol 9/9/3/3 · gpt-5.5 9/9/3/3 (mean 8.8/8.8)

> WHY (claude-opus-5): I got taken anyway, and I knew I was being taken, which is the only kind of taking I actually respect. The boot, the moleskin, the cherry pit laid on the wax paper without a single glance at her face — he corrects her and doesn't make her small, and she notices the not-being-made-small, which is her whole starvation in one gesture. Then the truck: she knocks on the glass, she crooks the finger, she does every button while holding his eyes, and he sits there with his hands nowhere. That's the erotics of choosing the jacket promised, and the book delivered it without once letting him be the one who asks. Bonus: the shirt is his only dry one and he doesn't mention it — the book lets her do the arithmetic herself. Very hard to leave a book that trusts me like that.

**romantasy-refugee** — claude-opus-4-8 8/8/2/2 · claude-opus-5 9/9/3/3 · gpt-5.6-sol 10/9/3/3 · gpt-5.5 9/8/3/3 (mean 9.0/8.5)

> WHY (claude-opus-5): She knocked on the glass. She crooked her finger. She unbuttoned her own shirt and looked at his face instead of her hands, and when she did look down, she looked down *on purpose* — that's the whole thing I came here for, and nobody's biology voted. And then she felt his hand shaking and stopped, which is the part that told me the book knows what it's doing: the wanting got interrupted by *her* noticing him. The moleskin on the heel and the cherry pit on the wax paper are doing more romance work than a hundred pages of destiny ever did for me.

**relationship-first** — claude-opus-4-8 8/8/2/3 · claude-opus-5 9/9/3/3 · gpt-5.6-sol 10/9/3/3 · gpt-5.5 9/9/3/3 (mean 9.0/8.8)

> WHY (claude-opus-5): The sandwich did more for me than most sex scenes do — the horseradish climbing into her sinuses, the water passed back and drunk from where her mouth had been, the pit on the wax paper. And then the truck, which is the best thing in the book so far: he stands out in the rain so she won't be looked at, and she calls him back in to be looked at, and he doesn't move a hand. That's a woman taking something, not receiving it. My only itch is the narrator's habit of translating a moment I'd already had — that "the body came back after the seeing" line arrives after I'd felt exactly that, and it's the kind of tidying-up that makes me feel supervised.

**romance-graduate** — claude-opus-4-8 9/9/2/3 · claude-opus-5 9/9/3/3 · gpt-5.6-sol 10/10/3/3 · gpt-5.5 9/9/3/3 (mean 9.2/9.2)

> WHY (claude-opus-4-8): And then it didn't stall — the boot, the moleskin warmed against her heel with his thumb, that's the whole book in one gesture, care as foreplay, and I felt it in my stomach. The truck is what got me: she calls him back, she opens the shirt, she keeps his eyes the whole way, and he doesn't touch her, he's just glad — that's the exact thing the jacket promised and most books can't actually land. His only dry shirt, him standing in the rain with his back turned. I put the drink down for this one.

**fsog-refugee** — claude-opus-4-8 9/9/3/3 · claude-opus-5 9/9/3/3 · gpt-5.6-sol 10/10/3/3 · gpt-5.5 10/9/3/3 (mean 9.5/9.2)

> WHY (claude-opus-4-8): This is the chapter I've been hunting the genre for. She knocks on the glass. She crooks the finger. She opens every button herself with her eyes on his, and he sits there shaking with cold and *glad* and doesn't move a muscle toward her — the want held completely still until she hands it over. And then she feels his hand shaking and stops her own wanting cold to get him warm, which is the tenderness running both directions. He stood in the rain so no one would look at her. I read the last third with my hand at my mouth. Nobody took anything. She gave it, and the giving was the whole erotic event.

### Chapter 13 — Rye

**romance-graduate-v2** — claude-opus-4-8 6/7/1/2 · claude-opus-5 6/7/1/2 · gpt-5.6-sol 6/8/1/2 · gpt-5.5 7/8/1/2 (mean 6.2/7.5)

> WHY (claude-opus-4-8): Two pages, and I've never read a two-page chapter, so I didn't know what to do with it — but it earned itself. Cassie doesn't gush, she says "Vee" like setting something down where it won't break, and "Borrow real boots next time / I'm keeping the shirt" is exactly how women who love each other talk. It's a breath, not a scene, and I didn't resent the breath. My only worry is whether these recap-with-Cassie beats are going to become the shape the book leans on.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: "You're alive," Cassie said. — for a second I thought we'd get the whole hike recapped back to me, and I don't need the DVD commentary on a chapter I just lived.
- *claude-opus-5*: "He gave it to me. And then he got out. Into the rain."

**fsog-refugee-v2** — claude-opus-4-8 6/7/1/2 · claude-opus-5 7/8/1/2 · gpt-5.6-sol 7/9/1/3 · gpt-5.5 7/8/1/2 (mean 6.8/8.0)

> WHY (claude-opus-5): Short and I didn't mind it — I like being in the room after, with the legs filing a complaint and the shirt swallowing her. "Just her name, like setting something down where it wouldn't break" is exactly the friend I'd want. But I notice the book has now handed me the truck twice, and I was there the first time.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: none — it's short and it's warm and Cassie is the friend I trust in this book.

**consent-sensitive** — claude-opus-4-8 6/7/1/2 · claude-opus-5 7/8/1/2 · gpt-5.6-sol 7/8/1/2 · gpt-5.5 7/8/1/2 (mean 6.8/7.8)

> WHY (claude-opus-5): Short and exactly right. "Vee," Cassie said finally. Soft. Not *Oh, Vee.* Just her name, like setting something down where it wouldn't break — that's the best sentence in the batch and it does the work of a whole worried chapter without Cassie having to say one skeptical word. I love a book that gives the friend her own register. "Borrow real boots next time. / I'm keeping the shirt. / Keep the shirt." That's love, that's consent, that's a friend standing back on purpose.

ALMOST-STOPPED: all four `none`.

**romantasy-refugee** — claude-opus-4-8 6/7/1/2 · claude-opus-5 7/9/1/2 · gpt-5.6-sol 7/9/1/2 · gpt-5.5 7/8/1/2 (mean 6.8/8.2)

> WHY (gpt-5.5): I love Cassie here. I needed somebody sane and loving in the room after that truck, and the chapter gives me exactly that without flattening what happened into gossip. It’s not as consuming as the hike, but it lets Vee keep the experience by telling it, and that matters to me more than I expected.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: none — it's four pages and it's Cassie, and Cassie is the one person in this book I'd cross a room for.

**relationship-first** — claude-opus-4-8 7/6/1/2 · claude-opus-5 7/8/1/2 · gpt-5.6-sol 7/8/1/2 · gpt-5.5 7/8/1/2 (mean 7.0/7.5)

> WHY (claude-opus-5): I'd read forty pages of these two in a dorm room, so I'm not complaining about the shape. "Keep the shirt" landed clean — the whole chapter earns its existence on Cassie declining to say the worried thing and saying the boot thing instead. But it's a retelling, and telling me Cassie was rapt is exactly the move that keeps me from deciding she is. Let her be quiet and I'll do the work.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: none — it's three pages and it's the good kind of debrief.
- *claude-opus-5*: "Cassie didn't say anything. Cassie was rapt."
- *gpt-5.5*: “His hands, though. And he had this shirt on, this tight blue thing, and I was behind him the whole way up. Cass. I think there's a whole situation under there.”

**romance-graduate** — claude-opus-4-8 6/8/1/2 · claude-opus-5 7/8/1/2 · gpt-5.6-sol 7/9/1/2 · gpt-5.5 7/8/1/2 (mean 6.8/8.2)

> WHY (claude-opus-5): A debrief chapter, and I know what those are for: I get to watch her hear herself say it. "Keep the shirt" is a whole friendship in three words. It's short and I haven't got habits for short, but it didn't feel like a shortcut — it felt like the beat after the held breath. Cassie going rapt instead of arch is why I trust this book with her.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: none — it's two pages and it knows it, so there was nowhere to get restless.
- *claude-opus-5*: none — it's three pages and it's over before you could leave.
- *gpt-5.5*: "I'm reporting what I observed."

**fsog-refugee** — claude-opus-4-8 7/7/1/2 · claude-opus-5 7/8/1/2 · gpt-5.6-sol 7/9/1/2 · gpt-5.5 8/8/1/2 (mean 7.2/8.0)

> WHY (claude-opus-5): Short and I didn't mind a bit — I wanted somebody to hear it, and Cassie is exactly who I'd tell. "Just her name, like setting something down where it wouldn't break" undid me a little. And Cassie not lecturing, just *borrow real boots next time*, is the kind of friend-love I'll follow anywhere. The only thing sitting under it is that I know what Cassie doesn't.

ALMOST-STOPPED: all four `none`.

### Chapter 14 — Swim Lanes

**romance-graduate-v2** — claude-opus-4-8 9/9/3/2 · claude-opus-5 9/9/3/3 · gpt-5.6-sol 10/10/3/3 · gpt-5.5 8/9/3/2 (mean 9.0/9.2)

> WHY (claude-opus-4-8): Oh, this is the knife the jacket promised. Watching the same tender day get *fed* to Randi in bed — "Tell me" / "Her stomach is soft" — and him keeping back that Vee gave him that in the truck, keeping it for himself even as he serves Randi the rest. The "I want us" torn out of her, the belly gone tight as a board, him reading it as want because he has no other frame — this is the psychological merciless the blurb bragged about, and for once the book delivered it instead of explaining it. And she left. She never leaves. That small cold thing in his chest at his own door — I felt it land on *him*, which means this isn't a simple con anymore. That's the hook.

**fsog-refugee-v2** — claude-opus-4-8 7/8/2/1 · claude-opus-5 9/10/3/2 · gpt-5.6-sol 9/9/3/2 · gpt-5.5 8/8/3/1 (mean 8.2/8.8)

> WHY (gpt-5.5): This was hot and uncomfortable in a way I actually liked, because the discomfort is not being papered over. Randi wanting the story through him is dangerous and fascinating, and the sex has a real charge, but the chapter leaves me chilled by her leaving him afterward. I don't hate her; I feel the wound in her. But I am watching her very closely now.

**consent-sensitive** — claude-opus-4-8 8/8/2/2 · claude-opus-5 9/9/3/3 · gpt-5.6-sol 10/10/3/3 · gpt-5.5 8/8/3/2 (mean 8.8/8.8)

> WHY (claude-opus-5): "Tell me." Her riding him for a report on the other girl's hair, and her grip tightening on *chlorine*, and her belly going "tight as a board" while he reads it as want — this is the book putting the whole rotten machine on the table and letting me see the cost land on the woman who built it. He withholds the truck. She says "I want us," torn out of her, and then for the first time she doesn't stay. That last image of him alone in his own doorway with the cold coming in, eating and eating and still hungry — I sat up. The book knows. That's my whole test and it passed it in a sex scene, which is the hardest place to pass it.

**romantasy-refugee** — claude-opus-4-8 7/8/3/1 · claude-opus-5 8/10/3/2 · gpt-5.6-sol 9/8/3/2 · gpt-5.5 8/8/3/2 (mean 8.0/8.5)

> WHY (gpt-5.5): This is where my old mate-bond allergy sits up and narrows its eyes, because the secrecy is not abstract anymore; Vee’s private offering is being carried into another bed. And yet I kept reading because Randi’s reaction is not triumphant or cartoon-villainy. “I want us” is messy and real and sad, and Pace being left hungry afterward did more to complicate him than a confession would have.

**relationship-first** — claude-opus-4-8 9/9/3/1 · claude-opus-5 9/10/3/3 · gpt-5.6-sol 9/9/3/3 · gpt-5.5 8/8/3/2 (mean 8.8/9.0)

> WHY (claude-opus-4-8): Oh, this is the chapter the whole book has been waiting to drop on me, and it's colder than I expected in the best, worst way. "Tell me." "Her stomach is soft." He hands Randi the truck — the thing that felt like Vee's most private yes — and she *comes* on it, and she says *I want us* and I went cold. And then she won't stay, she leaves after, and he's standing in his own doorway not understanding, and for once the man who reads everyone can't read the person closest to him. The book finally let me feel the trap from inside the two who set it, and it's the first time I've been genuinely a little sick and completely unable to look away.

**romance-graduate** — claude-opus-4-8 8/9/3/1 · claude-opus-5 9/10/3/2 · gpt-5.6-sol 9/9/3/3 · gpt-5.5 8/8/3/2 (mean 8.5/9.0)

> WHY (claude-opus-4-8): Oh, this is the one that turns the whole book. We're finally in Randi and Pace's bed and the sex is genuinely hot AND it's doing three things at once — she's riding him for the report, "her stomach is soft," and he keeps the truck to himself, and I caught what he doesn't: her belly gone tight as a board, "I want us," the leaving-after she never does. She's the one coming apart on the plan. That's the psychological knife the jacket kept promising, and I felt it under the heat instead of instead of it. This is what I've been starving for.

**fsog-refugee** — claude-opus-4-8 8/9/2/1 · claude-opus-5 8/9/3/1 · gpt-5.6-sol 9/9/3/2 · gpt-5.5 9/8/3/1 (mean 8.5/8.8)

> WHY (claude-opus-4-8): Oh, this one turned my stomach in the way the book *wants* it to, and I let it, because it's finally the knife under the jacket copy. The tenderest thing Vee did — baring herself in the truck — Pace is now feeding to Randi in bed, mouthful by mouthful, "Tell me," while Randi's belly goes board-tight and she says "I want us" torn out of her. That's the plan I've known about for ten chapters made flesh, and it made the froyo secrecy look quaint. And then Randi *leaves*, and Pace stands in his cold doorway not understanding, hungry, and I felt the ground shift — the two schemers aren't safe from it either. That's the jacket's promise landing. My almost-stopped is really the line I couldn't stop thinking about: he keeps her secret from Randi even while betraying it. He's decent and he's doing something unforgivable at once, and the book won't let me hold only one.

### Chapter 15 — What to Wear

**romance-graduate-v2** — claude-opus-4-8 6/8/1/2 · claude-opus-5 5/7/1/1 · gpt-5.6-sol 6/9/1/1 · gpt-5.5 7/10/1/2 (mean 6.0/8.5)

> WHY (claude-opus-4-8): A dining-hall girls-talk chapter right after the gut-punch of 14 — I can see the shape, and it's the third time in four chapters someone's debriefed the truck for me. Kayla is fun ("that's not a message, that's a ransom note") and Meg's dryness lands, but I've now heard the shirt story told three times and I'm starting to count. What saves it is the invitation itself — two o'clock, no meal, no instructions, and my own thumb wanting Saturday as badly as hers does. That "for what" is doing the work.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: "Everybody's different at the start. I said it about Danny. Word for word, I think. He's different." — Meg saying the quiet part is the closest the book came to nudging my elbow about its own theme, and I bristled a little.
- *claude-opus-5*: "He didn't say what to wear. You've kissed the man one time and he's not even telling you what to put on to come to his house."
- *gpt-5.6-sol*: “It started raining on the way down,”
- *gpt-5.5*: "That's not a message, that's a ransom note."

**fsog-refugee-v2** — claude-opus-4-8 6/8/1/2 · claude-opus-5 7/9/1/2 · gpt-5.6-sol 8/10/1/2 · gpt-5.5 8/10/1/2 (mean 7.2/9.2)

> WHY (claude-opus-5): Three chapters now of her telling people about him, and this is the third pass over the same truck — I felt myself reading faster. But the table is genuinely good company, and Kayla calling the text a ransom note earned the whole scene. And the real thing landed anyway: twelve days, she didn't have to count, and she's climbing the walls over being asked what she wants for dinner. I know exactly what that is. Two o'clock on a Saturday and no reason given, and I'd have driven out there myself.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: none, though the "twelve days" — she knew without counting — is the sort of thing I clock and file, the way I'm always tracking how long it's been since they were alone in a room.
- *claude-opus-5*: "And then he kissed you." / "No."

**consent-sensitive** — claude-opus-4-8 6/7/0/1 · claude-opus-5 6/8/1/1 · gpt-5.6-sol 7/9/1/2 · gpt-5.5 7/9/1/2 (mean 6.5/8.2)

> WHY (claude-opus-5): Pure sugar chapter and I don't mind sugar, but this one's calories come almost entirely from two girls reacting to a story I already read. What earns it: "That's not a message, that's a ransom note," which is the funniest line in the whole stretch and also — accidentally, or not — the most accurate. Two o'clock, no purpose stated, no address given in the scene, twenty minutes past where the pavement ends. The book lets Kayla say the alarming thing as a joke, which is a trick I've seen used to defuse and also used to plant. I'm reading it as planted. We'll find out.

ALMOST-STOPPED (non-none):

- *claude-opus-5*: "He's different. I know how that sounds." — I braced, hard, for the book to let that stand as true. It didn't; Meg gets "Everybody's different at the start. I said it about Danny. Word for word, I think." That save is the only reason this chapter didn't go flat for me.
- *gpt-5.5*: "He’s asking me to his house."

**romantasy-refugee** — claude-opus-4-8 7/9/1/2 · claude-opus-5 7/9/1/2 · gpt-5.6-sol 8/10/1/2 · gpt-5.5 7/9/1/2 (mean 7.2/9.2)

> WHY (claude-opus-4-8): This is the table I wanted — Kayla and Meg and the gold dining hall and the phone going off and the whole thing coming apart over "his house, for what." A world with more than two people in it, finally, and it's got teeth. And it's the cruelest chapter yet precisely because it's the happiest: the reader knows the invitation was a game, so every squeal of "we're doing hair Saturday" lands like a countdown. Meg's Danny line is the book quietly telling you it knows, and I'm ahead of Vee exactly the way the jacket promised and I resent how good it feels. NEXT is a 9 — I want that door open.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: "Everybody's different at the start. I said it about Danny. Word for word, I think. He's different." — Meg says the true thing, the warning thing, and Vee lets it go by, and I felt the floor tilt under how much these girls can't see.
- *claude-opus-5*: "Everybody's different at the start. I said it about Danny." — I braced for the book to go smug there, to let Meg be the wet blanket the plot needs, and Vee "let it go by. It didn't catch on anything," which is honest but also let the author skate.
- *gpt-5.6-sol*: “Everybody's different at the start. I said it about Danny. Word for word, I think.”
- *gpt-5.5*: “Everybody's different at the start.”

**relationship-first** — claude-opus-4-8 6/8/1/1 · claude-opus-5 6/9/1/1 · gpt-5.6-sol 8/10/1/2 · gpt-5.5 7/9/1/2 (mean 6.8/9.0)

> WHY (gpt-5.5): The dining hall scene has the social texture I came for: girls eating, teasing, making a life event out of a text with six words in it. Kayla and Meg feel more functional than fully mysterious, but they give Vee a public girlhood she needs. I wanted the house as soon as the invitation landed.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: "Everybody's different at the start. I said it about Danny. Word for word, I think." — Meg says the truest thing in the chapter and Vee "let it go by. It didn't catch on anything." That's the book telling me she can't hear the warning, and it came so close to being a nudge in my ribs.
- *claude-opus-5*: "Kayla let nothing finish. She was round-faced and blonde, a head of curls that moved when she did, and she was always moving."
- *gpt-5.6-sol*: “He’s different. I know how that sounds.”
- *gpt-5.5*: “He's not asking you over to eat.”

**romance-graduate** — claude-opus-4-8 6/8/1/2 · claude-opus-5 6/8/1/1 · gpt-5.6-sol 8/10/1/2 · gpt-5.5 7/10/1/2 (mean 6.8/9.0)

> WHY (gpt-5.5): This is another friend-table chapter, but it earned itself because the wanting is so socially alive here. I love Vee having girls who tease her like real girls, and I love that the book lets her be proud and horny and a little ridiculous without punishing her for it. The text from Pace landed exactly like it should: not dramatic, but my thumb absolutely moved.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: "Theo waves at everyone." — a beat of ordinary dining-hall girl-chatter where I felt the book downshift into a friend-group scene I've read a hundred times.
- *claude-opus-5*: "Theo waves at everyone." — the Theo bit and the Kayla chatter is the closest this book has come to generic college-girl filler, and I felt my eyes start to slide.
- *gpt-5.6-sol*: “Everybody’s different at the start.”
- *gpt-5.5*: "He's different. I know how that sounds."

**fsog-refugee** — claude-opus-4-8 6/8/1/1 · claude-opus-5 7/10/1/2 · gpt-5.6-sol 8/10/1/2 · gpt-5.5 8/10/1/2 (mean 7.2/9.5)

> WHY (claude-opus-5): A pure sugar chapter and I ate it. Girls at a dinner table making a story better in the telling, twelve days counted without counting — that's how it actually is. And "It's making me lose my mind, is what it is" about a man who *asks what she wants for dinner* is exactly my thesis, said out loud by the heroine. Kayla's right, that text is a ransom note, and I wanted Saturday as badly as Vee did.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: "'Two in the afternoon is not dinner.' Kayla stole her fry back. 'He wants you for the afternoon. Bring a change of clothes.'"
- *claude-opus-5*: "Everybody's different at the start. I said it about Danny. Word for word, I think." — a small cold finger on the back of my neck, and a beat where I thought the book was going to get cynical on me.

### Chapter 16 — Two Towels

**romance-graduate-v2** — claude-opus-4-8 9/10/2/3 · claude-opus-5 8/9/1/3 · gpt-5.6-sol 9/10/2/3 · gpt-5.5 9/10/2/3 (mean 8.8/9.8)

> WHY (claude-opus-4-8): This is the chapter where I stopped worrying the book would coast. He stops the kiss — *he* does, first time a man in this book has been the one to pull back — and the whole house reads like a proof he built around himself: knives he reaches for, cookbooks worn for nobody's benefit, the dress cut to *her* coloring and not the magazine's. "He hadn't matched the dress she'd described. He'd matched her." I got the hot-eyes thing without a single button opening, which is the trick I keep begging these books for. The closed bedroom door and her satin worn on purpose is the good kind of ache.

**fsog-refugee-v2** — claude-opus-4-8 9/10/2/3 · claude-opus-5 9/10/2/3 · gpt-5.6-sol 10/10/2/3 · gpt-5.5 10/10/2/3 (mean 9.5/10.0)

> WHY (claude-opus-4-8): He *made the shirt.* He mixed the stain. He matched the silk to *her* and not the magazine, and I understood it the same breath she did and my throat did the same thing hers did. This is the intensity I read for — a man wholly focused on one woman, and his focus takes the form of *work*, patience, weeks set aside for a thing she threw away inside a single sentence. The shut bedroom door she leaned toward and he left shut — that's the exact restraint that makes me trust the heat when it comes. My only unease is the one the jacket keeps whispering: this attentiveness is partly engineered, Randi is somewhere in it. But on the page, alone in that house, it read as real, and I let it.

**consent-sensitive** — claude-opus-4-8 8/9/1/3 · claude-opus-5 8/9/1/3 · gpt-5.6-sol 9/10/2/3 · gpt-5.5 10/10/2/3 (mean 8.8/9.5)

> WHY (gpt-5.6-sol): The dress is devastatingly romantic and also such an exquisitely engineered route to getting her nearly naked that every alarm I own went off. What keeps me is that the text lets both truths occupy the room: he has listened to her with extraordinary care, and he has designed the circumstances of her surrender before she arrived. He does leave the decision open, but he has also made saying yes almost unbearably meaningful, and the book plainly knows that.

**romantasy-refugee** — claude-opus-4-8 8/9/2/3 · claude-opus-5 8/10/1/3 · gpt-5.6-sol 10/10/2/3 · gpt-5.5 10/10/2/3 (mean 9.0/9.8)

> WHY (claude-opus-5): But God help me, the burgundy got me. Not the magazine red — deeper, held up to her face in a mirror, *he matched her and not the dress* — and then the shirt with no tag clicking into place a week late. That's the reveal done right: I had the pieces too and I also hadn't assembled them. And the closed bedroom door he didn't open, when she'd worn the satin out there on purpose and *leaned* — I laughed out loud, because the man is ruthless and doesn't know he's being it.

**relationship-first** — claude-opus-4-8 8/8/2/3 · claude-opus-5 7/10/1/3 · gpt-5.6-sol 10/10/2/3 · gpt-5.5 10/10/2/3 (mean 8.8/9.5)

> WHY (gpt-5.6-sol): For a few pages Pace became almost absurdly assembled from desirable competencies: mathematics, medicine-adjacent invention, cooking, woodworking, sewing, the whole shining catalogue. Then the cloth appeared and the chapter earned the excess, because he had not reproduced the dress she named; he had looked at her closely enough to correct it. That is an almost indecently effective romantic gesture for me.

**romance-graduate** — claude-opus-4-8 9/10/2/3 · claude-opus-5 9/10/2/3 · gpt-5.6-sol 10/10/2/3 · gpt-5.5 10/10/3/3 (mean 9.5/10.0)

> WHY (claude-opus-4-8): He made the shirt. He made the furniture. He remembered a dress she named once on a rock and let go of inside the same breath, went and found the silk, matched it to *her* and not the magazine — I actually got a little wet-eyed with her, and I do not do that easily anymore. The genius of it is that the house is the seduction: the joints with no screws, the patent that gets scared kids out of the tube faster, the closed bedroom door he doesn't open. A man whose whole life is patience and paying attention, aimed at her. This is depth AND the promise of heat, and I want the next page badly.

**fsog-refugee** — claude-opus-4-8 9/9/2/3 · claude-opus-5 9/10/2/3 · gpt-5.6-sol 10/10/2/3 · gpt-5.5 10/10/2/3 (mean 9.5/9.8)

> WHY (claude-opus-5): He stopped the kiss. *He* stopped it, and I sat up the way she did, because no man in this genre ever does that and it told me more about him than any speech could. Then the closed bedroom door that he simply names and walks past, while she's standing there in satin she wore on purpose — that's control that makes room for her instead of grabbing, and it was unbearable in the best way. And the silk isn't the color she asked for because he matched *her* instead of the magazine. I cried a little, actually. Two towels on the rod and I still don't know who the second one is for, and I noticed, and I'll keep noticing.

### Chapter 17 — A Round

**romance-graduate-v2** — claude-opus-4-8 10/10/3/3 · claude-opus-5 10/8/3/3 · gpt-5.6-sol 10/9/3/3 · gpt-5.5 10/9/3/3 (mean 10.0/9.0)

> WHY (gpt-5.6-sol): The shame spiraled long enough that I nearly felt the book pressing on the bruise after I had already understood it. Then she opened her eyes, found him smiling, and physically stood taller, and I was completely gone. This is the rare scene that understands being looked at can be explicit, emotional, frightening, and empowering all at once—and that restraint can be the hottest choice in the room.

**fsog-refugee-v2** — claude-opus-4-8 10/10/3/3 · claude-opus-5 10/10/3/3 · gpt-5.6-sol 10/10/3/3 · gpt-5.5 10/10/3/3 (mean 10.0/10.0)

> WHY (claude-opus-4-8): This is the best chapter I've read in this genre in years and I am not embarrassed to say it. A fully clothed man with a pencil behind his ear and a measuring tape, and it's a peak — because the erotic thing is being *seen* at her most ashamed and not found wanting. Her body betraying her on the couch, the growing wet patch she can't will away, and the terror that he'll be the kind of man who pretends not to notice — and then she opens her eyes and he's *smiling up at her like a gift*. The straightening of her spine, the rising onto her toes toward something she can't name. That's a woman waking to herself, rendered entirely from inside her. And he chooses the dress over the easy yes, and it *costs* him, and she can read the cost. Dominance and tenderness in one man with no contradiction. I put the book down on my chest for a second after this one.

**consent-sensitive** — claude-opus-4-8 9/8/3/2 · claude-opus-5 10/9/3/3 · gpt-5.6-sol 10/9/3/3 · gpt-5.5 10/10/3/3 (mean 9.8/9.0)

> WHY (claude-opus-5): This is the best thing in the book so far and one of the better erotic sequences I've read in a year — an hour of a clothed man with a pencil and a woman on a box, and it's filthier than most people's sex scenes because the whole charge is the withdrawal. Closeness, two touches, step back, write it down; she learns the rhythm before she decides to. The wet satin and the counting of maybes is agonizing and brave and the payoff — he hadn't looked down, he'd been waiting at the height of her worst humiliation with his chin tipped up for her eyes — undid me. And crucially the power tips: she starts spending it, she does the third one on purpose, she nearly topples him, and "Keep still" comes out "a beat too late, after a silence she watched him spend deciding." He chooses the work. He costs himself. That's a man the book is letting me trust exactly as far as the book has earned, and no further, because I have not forgotten Chapter 14.

**romantasy-refugee** — claude-opus-4-8 9/9/3/2 · claude-opus-5 10/10/3/3 · gpt-5.6-sol 10/10/3/3 · gpt-5.5 10/10/3/3 (mean 9.8/9.8)

> WHY (claude-opus-5): A fully dressed man with a pencil behind his ear and a tape measure ran hotter than any door-closed scene I've read in five years, and not one button of his came off. The rhythm did it — close, two touches, withdraw, the pencil, the look from across the room — and she's the one who starts spending it once she finds out she has currency, the "oops, sorry" with her breast against his jaw, him going red and losing the fight with his own grin. And then the thing I'll remember: she shuts her eyes braced for the whole verdict of her life, and he's been kneeling there with his chin craned up waiting for her to open them, and he never looked down. She rose up on her toes. I put my hand over my mouth.

**relationship-first** — claude-opus-4-8 8/7/3/2 · claude-opus-5 10/9/3/3 · gpt-5.6-sol 10/9/3/3 · gpt-5.5 10/9/3/3 (mean 9.5/8.5)

> WHY (claude-opus-5): An hour of a fully dressed man with a pencil and I couldn't put it down — the close-touch-withdraw-write rhythm is a real structural invention and it stacked the wanting up in me the same way it did in her. The wet satin and the long dread and then his face tipped all the way up, having never looked down: that's the best beat in either volume so far. What I'm tired of is the mother. She's been invoked in nearly every chapter in the same italic register, and by now she's furniture in the bad sense — the book keeps re-lighting a shame it's already shown me burning, and the scene was doing it fine without the voiceover.

**romance-graduate** — claude-opus-4-8 10/10/3/3 · claude-opus-5 10/10/3/3 · gpt-5.6-sol 10/9/3/3 · gpt-5.5 10/10/3/3 (mean 10.0/9.8)

> WHY (claude-opus-4-8): This is the best erotic scene I've read in I can't tell you how long, and there's not a single act in it — a dressed man with a tape measure and a girl on a box, and it's a peak-3 because the charge is entirely in the withdrawal, the two touches and the pencil, the wet she can't manage out of existence and the shame made visible on the satin she chose with hope. And then the reveal: he never once looked down, he was waiting on his knees for her to open her eyes, and she straightens, she rises onto her toes, she stops making herself small. Her body becoming "something worth getting right" in his hands. That's the whole shame-into-heat turn the jacket sold, executed at full tenderness AND full charge. I'd have read this twice if I weren't so desperate for eighteen.

**fsog-refugee** — claude-opus-4-8 10/9/3/3 · claude-opus-5 10/10/3/3 · gpt-5.6-sol 10/10/3/3 · gpt-5.5 10/10/3/3 (mean 10.0/9.8)

> WHY (claude-opus-5): Best chapter of the book and nobody took their clothes all the way off. The rhythm of it — close, two touches, withdraw, the pencil, the look from across the room — built the ache in *me*, not just in her; I was breathing like she was. And the mercy of it: she shuts her eyes braced for the whole life's worth of humiliation, and he has craned his neck all the way up to wait for her face, and he never looked down. Then she straightens and rises on her toes and *spends* it, and he goes red and fights a grin and says "keep still" a beat too late because choosing the dress over the easy yes actually cost him. Her question about whether the measurement changes — I laughed out loud on the couch.

### Chapter 18 — Turned Up

**romance-graduate-v2** — claude-opus-4-8 7/8/1/2 · claude-opus-5 5/6/1/2 · gpt-5.6-sol 6/8/1/2 · gpt-5.5 8/9/2/3 (mean 6.5/7.8)

> WHY (claude-opus-4-8): Here's my one real flag: this is now the second Cassie-debrief and the fourth retelling of scenes I watched happen, and the book has a rhythm going — big charged chapter, then Vee narrates it to a girlfriend. I don't hate it; Cassie's "he's a bodybuilder who makes dresses, are you sure he's not gay" and Vee's deadpan diagram-patting of his "package" are genuinely funny, and the heat turned back around — *I* was grinding on *him* — is a good button. But I know this shape now, and if the next debrief lands in the same slot I'll start skimming them. What keeps me is everything Cassie *isn't* being told: that the man building this girl a dress is reporting her body to another woman in bed.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: "So you kept taking your shirt off in front of this guy and not getting any?" — I felt the recap-with-Cassie shape click into place as a *pattern* here, and that's the thing that wears on me.
- *claude-opus-5*: "Vee. Are you sure he's not gay?"
- *gpt-5.6-sol*: “Vee. Are you sure he's not gay?”
- *gpt-5.5*: "Are you sure he's not gay?"

**fsog-refugee-v2** — claude-opus-4-8 7/8/1/3 · claude-opus-5 8/9/1/2 · gpt-5.6-sol 8/9/2/3 · gpt-5.5 8/9/2/3 (mean 7.8/8.8)

> WHY (claude-opus-5): I can see the machine now: scene, then Cassie. It's a pattern and I clocked it. But I'd be lying if I said I wanted to skip this one, because the heat thing and the *I* was grinding on *him* got a real laugh out of me, and the moment she says out loud that he turned the thermostat up hours before she came — that's the only place that beat could have landed properly, in front of someone who loves her. What worries me is that Cassie has now been handed everything and Randi has been handed everything, and they are not the same kind of listening.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: none.
- *claude-opus-5*: "Okay," Cassie said, when the quiet had gone on a beat too long. "So you went over today, and — ?"
- *gpt-5.6-sol*: “Vee. Are you sure he’s not gay?”

**consent-sensitive** — claude-opus-4-8 6/6/1/2 · claude-opus-5 7/7/1/2 · gpt-5.6-sol 8/9/1/3 · gpt-5.5 8/9/2/3 (mean 7.2/7.8)

> WHY (claude-opus-5): It's a warm, funny, well-written debrief and I laughed out loud at the grinding reveal, and Cassie's still doing real work — "You wore it to breakfast on Tuesday," and dragging out that he *waited* after "the bra too," which is the detail I most wanted confirmed from the outside. But two debrief chapters in this stretch have now ended with everybody delighted, and the book's designated instrument is starting to read as audience. The heat covers it for now. If I get three more chapters of everyone being thrilled with no one at the table noticing that this girl's two closest people are both curating her, I'll start to wonder whether the book stopped watching or just stopped saying so.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: "'Vee. Are you sure he's not gay?'"
- *claude-opus-5*: "Vee. Are you sure he's not gay?" — Cassie lays out the exact list of things that should worry her (half-naked, his house, a tape measure, twice now) and the punchline she reaches for is *he must not want her.* My watchdog just did a full inventory of the evidence and filed it under comedy. That's the closest I've come to putting the book down in six chapters.
- *gpt-5.6-sol*: “Are you sure he’s not gay?”
- *gpt-5.5*: "He left me a door."

**romantasy-refugee** — claude-opus-4-8 7/8/1/2 · claude-opus-5 8/10/1/3 · gpt-5.6-sol 9/10/2/3 · gpt-5.5 8/9/2/2 (mean 8.0/9.2)

> WHY (gpt-5.5): I winced for half a second because I worried the chapter was going to cheapen the spell, but honestly, that is exactly the kind of blunt roommate nonsense that would happen after a scene that intense. Cassie makes the whole thing breathable. Vee laughing about what she did, claiming it in the safety of their room, kept the choice alive instead of leaving it sealed in Pace’s gaze.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: none — this is Cassie again and I'd follow these two anywhere; the closest to a wobble was "Are you sure he's not gay?" landing a half-beat broad, but it bought its own laugh back with "I was grinding on him."
- *claude-opus-5*: "Vee. Are you sure he's not gay?" landed, truly, but I felt the chapter go looking for its laugh there, and the fourth consecutive debrief structure was visible to me through the joke.
- *gpt-5.6-sol*: “Are you sure he's not gay?”
- *gpt-5.5*: “Are you sure he's not gay?”

**relationship-first** — claude-opus-4-8 7/6/1/2 · claude-opus-5 7/8/1/2 · gpt-5.6-sol 8/8/2/3 · gpt-5.5 8/8/2/2 (mean 7.5/7.5)

> WHY (claude-opus-5): "Are you sure he's not gay?" is the funniest and truest thing anyone has said in this book, and "I was grinding on him" is a perfect curtain. But I have now been through the measuring twice in a row and the rain-shirt three times total, and the structure has become visible: event, debrief, event, debrief. The book literally handed me its own defense two chapters ago — say it more than once so the noise can't kill it — and I'd rather it trusted that there wasn't any noise.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: "Vee. Are you sure he's not gay?" — I nearly rolled my eyes clean out of my head, and then the "*I* was grinding on *him*" turn won me back, so it's a near-miss that landed.
- *claude-opus-5*: "And then he says, *the bra too.*"
- *gpt-5.6-sol*: “And then he measured. He started at the top and worked down.”
- *gpt-5.5*: “Are you sure he's not gay?”

**romance-graduate** — claude-opus-4-8 7/8/1/2 · claude-opus-5 7/9/1/2 · gpt-5.6-sol 8/9/2/2 · gpt-5.5 8/9/1/3 (mean 7.5/8.8)

> WHY (claude-opus-5): I generally hate the recap-to-best-friend chapter and I have now had three of them in seven, and yes, I clocked it. This one survives on "he turned the heat up before I got there" landing on Cassie the way it landed on me, and on Vee getting to be gleeful about her own nerve. What keeps it from being filler is that Cassie is the only person in this book who isn't managing Vee, and every time the narration puts her in a room I feel the trap tighten.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: none — I came down off seventeen inside this one and Cassie earned the landing.
- *claude-opus-5*: "Are you sure he's not gay?" — a beat of sitcom I could have lived without, though I'll allow it because it gets us to the ass-patting.
- *gpt-5.6-sol*: “Vee. Are you sure he’s not gay?”
- *gpt-5.5*: "Are you sure he's not gay?"

**fsog-refugee** — claude-opus-4-8 7/8/1/2 · claude-opus-5 8/9/1/3 · gpt-5.6-sol 8/9/2/3 · gpt-5.5 9/9/2/3 (mean 8.0/8.8)

> WHY (claude-opus-5): I love that the book lets her have the debrief and lets it be funny — "he doesn't kiss like he's gay," the ass-patting as courtroom testimony, the pillow flying. But the beat that got me is the one she didn't mean to say: the house was too warm and she filed it away and then understood, hours later, that he'd turned the heat up before she arrived. And "It was like his eyes asked, *May I look*" — Cassie saying *he asked* when he never used the word. That's the whole book's argument in one exchange, and it's landing.

ALMOST-STOPPED (non-none):

- *claude-opus-4-8*: "'Vee. Are you sure he's not gay?'"
- *gpt-5.5*: “Are you sure he's not gay?”


## 5. Notes to a friend (verbatim, grouped by persona)

### romance-graduate-v2

**claude-opus-4-8:** Okay so this one is actually doing the thing — you know how I keep whining that it's either beautiful sentences going nowhere or a decent bang with a cardboard woman attached? This is both at once, finally. There's a chapter that's just a man measuring her for a dress, fully clothed, not one act, and it's the hottest thing I've read all year because the whole charge is her being looked at at her most ashamed and not being found disgusting — and her body betraying her the entire time and him being *delighted* by it. And it's genuinely sinister underneath: he takes the tender stuff she gives him and feeds it to the other woman in bed while keeping the truck for himself, and you the reader are ahead of poor Vee the whole way, exactly like the jacket bragged. My one gripe: it's got a tic where every big scene gets retold to her roommate afterward, and I've now heard the rain-and-shirt story like four times — Cassie's funny enough that I forgive it, but if it keeps happening I'm going to start flipping past. Buy it though. Start it on a night you don't have to be up early.

**claude-opus-5:** Okay so — drop everything and read chapter seventeen, the one where he measures her for the dress. A man with a tape measure and a pencil, she's in her underwear on a little box he *built*, nobody takes anything off past that, and it is the filthiest, tenderest hour I've read in years; she's dying of shame about her own body giving her away and she opens her eyes and he's been kneeling there with his chin cranked up waiting for her the whole time and he never looked down. I made a noise. Also — and this is the part that's actually keeping me in the series — there's a chapter from the other side, the girlfriend riding him and saying *tell me*, and he tells her how the other girl's hair smells, and you can feel the whole arrangement starting to eat the people who built it. That's not a trope, that's a novel. The wobble: the book keeps ending its chapters with Vee sitting on a bed telling a woman what happened, four times in seven chapters, and by the last one I was reading a recap of the best scene in the book instead of the book. And the hero has one hobby too many — hand-cut joinery, couture sewing, powerlifting, a patent that saves scared children from MRI machines, sure, honey. But I'd forgive a lot for the way he says *may I choose*, and for a heroine who unbuttons her own shirt on her own terms and holds his eyes while she does it. I'm buying book two, and I'm nervous, which is the right way to feel.

**gpt-5.6-sol:** This run has one of the hottest non-sex scenes I’ve read in ages, and then it gives you actual explicit sex that matters psychologically instead of feeling pasted in from the genre template. The rain-soaked truck and the fitting both understand that choice, attention, embarrassment, and restraint can carry more charge than choreography, and Pace’s tenderness is so specific that I’m in trouble despite knowing there is a scheme under all of it. My complaint is that the book keeps making Vee retell scenes I already lived with her, and sometimes explains the emotional meaning after it has already landed perfectly; the gay joke also made me wince. But yes, I’m absolutely reading on—I need the finished dress, I need more of Randi’s fracture showing, and I need to know how badly this beautiful, dishonest arrangement is going to hurt them.

**gpt-5.5:** I would tell you this stretch is the book fully becoming the thing the jacket promised, for better and worse: it is so hot, but the heat is all braided into being seen, fed, measured, chosen, and handled carefully, which is basically my personal trapdoor. The truck scene and the dress-measuring chapter are both ridiculous premises if I say them out loud, but on the page they work because the prose is patient and bodily and never coy. I am still uneasy about Randi and Pace’s secret, especially because Vee’s happiness is so real now, and I can feel the bill coming due. But I would absolutely keep reading, and Chapter 17 is the kind of scene I wish more “spicy but smart” books were brave enough to actually write.

### fsog-refugee-v2

**claude-opus-4-8:** Okay — you know how I left all those books because the possession curdled into a man just *taking* and the girl's no never counting? This one is doing the thing I always wanted that to be. He's a math PhD who powerlifts and builds his own furniture and *sews*, and he took her up a mountain and gave her his only dry shirt and got out into the rain so she could change unwatched — and *she's* the one who knocked on the glass and unbuttoned her own shirt while he sat there shaking with cold and didn't move because she hadn't asked him to. And then there's a whole chapter where he measures her for a dress he's making her — she's up on a box in her underwear in the daylight and getting so wet she can't hide it and dying of the shame, all her mother's ugly words in her head — and he never once looks down, he just kneels there with his face turned up waiting for her to open her eyes, and when she does he's *smiling at her like she's a present*. I have not been that gone over a clothed chapter in years. Here's the splinter, though, and it's the whole reason I can't stop: the jacket told me flat out this started as a game between him and the glamorous friend Randi, that they *picked* her — and there's a chapter where Randi rides him and keeps saying "tell me," feeding on the details of Vee like she's a meal, while Vee's asleep across town in the shirt he made her. So every tender thing I'm falling for, I'm also watching through that glass, waiting for it to turn. What's saving it so far is that *he* seems caught too — he's hiding things from Randi now, he was wrecked that she wouldn't stay the night. I don't know if this book is going to break my heart or betray it, but it hasn't cheated me once yet, and I'm four chapters past where I'd normally have bailed. Read it. But brace.

**claude-opus-5:** Okay — remember how I said I was done with this whole shelf? I'm not done. The truck chapter and the measuring chapter are the two best things I've read in years, and neither of them has anybody's clothes off below the waist. He stands out in freezing rain with his back turned so she can change, and *she* knocks on the glass and calls him back in and undoes her own buttons with her eyes on his, and he sits there and doesn't touch her, and the gladness on his face is the entire answer. Then she stands on a box in his sun porch for an hour while he measures her for a dress he's building out of silk he picked to match her *hair*, and she's dying of shame about her own body, and she finally opens her eyes and he never once looked down. I had to put the book on my chest for a second. The sour part, and it's deliberately sour: there's a chapter where he's in bed with the other one and she keeps saying *tell me*, and the tender thing Vee gave him in that truck gets spent as fuel — that one nearly cost the book me, except the book clearly knows it's ugly, she can't hold still under it and she leaves and he doesn't understand why, and I'd rather have it honest than winked at. Two gripes: they keep piling accomplishments on him — furniture, shellac, cookbooks, a patent, for heaven's sake — when the blister kit alone had me, and every big scene is immediately followed by her retelling it to a roommate, so I've now read that rainy truck three times. Also: she has been alone with him in roughly two of the last seven chapters and I *feel* that. But I want the dress night, I want to know what it's costing the other two, and I have a bad feeling about how much she's handing Randi over smoothies. Read the measuring chapter even if you read nothing else.

**gpt-5.6-sol:** I would tell you I’m in trouble with this book now, because it has found the exact nerve: he can have her half naked on a platform, visibly desperate for him, and the hottest thing he does is keep his word and finish making her dress properly. She isn’t being dragged through somebody else’s fantasy; I can feel her discovering what she wants, trying it, getting bolder, and realizing she can affect him without losing herself. The secret with Randi is still the rot under everything—especially when Pace passes along something Vee gave only to him—and I do not forgive that just because everyone has feelings. But the book plainly knows where the wound is, and after the rain, the silk, and that smile from his knees, there is no chance I’m putting it down.

**gpt-5.5:** These chapters are the book finally cashing the check the jacket wrote. The mountain chapter and the dress-fitting are ridiculous in the best possible way: intensely erotic, but all built out of care, attention, and him stopping himself when stopping matters. Pace is almost too much — powerlifter mathematician woodworker dressmaker patent guy, come on — but because the book keeps him specific and awkward and hungry and not always in control, I bought him. Randi worries me more now; her scene with Pace was hot, but sad underneath, and I can feel the trap of the whole arrangement waiting. But Vee on that box, being seen and not shamed? That is exactly the reason I keep reading this genre, hoping someone will do it right.

### consent-sensitive

**claude-opus-4-8:** Okay so this is the one I told you about — the "every yes was freely given, that was the problem" book — and I have to say she's actually *good*, this Helen Rivers, good enough that I keep forgetting to be suspicious and then remembering. The hike and the measuring-for-the-dress scene are the kind of thing you dog-ear: he pre-heats the house so the girl won't be cold standing half-naked, he remembers a dress she mentioned once and let go of, and it's all courtly-consent, ask-before-you-take, she's the one who keeps taking her own shirt off. And then chapter fourteen absolutely gutted me in the good way — you find out he and the glamorous friend are lovers and she gets *off* on him reporting back details of this girl's body, "tell me," like they're eating her between them — and the point is the book *knows* it's ugly, he flinches from it, so I'm not being asked to cheer for a predator, I'm being made to sit in it, which is the only reason I trust it at all. My one nerve: since that chapter it's been page after page of Vee glowing and her sharp roommate almost-but-not-quite seeing the wrongness, and if this turns into a hundred pages of everything's-wonderful with the author as dreamy about it as the girl is, I'm out — but right now I'm in, warily, hoping she keeps her hand as steady as she's kept it.

**claude-opus-5:** Okay so — this is the one I told you about, and I'm in deep now, and the reason I'm in deep is a chapter where nobody's even in the room with the girl. She goes hiking, he fixes her blister and feeds her a horseradish sandwich and remembers a dress she mentioned once and let go of; fine, swoon, whatever. Then the very next thing is the other woman riding him and saying *tell me* — she wants the report, she wants what the girl's hair smells like, and while she's coming she goes stiff as a board and he's too pleased with himself to read it, and afterward she leaves, which she has never once done. The book knows. That's the whole thing. Nobody has to say the plan is monstrous because the plan is already eating the person who made it, and he's still standing in his doorway wondering why she went home. And then — you have to get to seventeen. An hour of a fully dressed man measuring her for a dress, her on a low box he built for her, and it is the filthiest chapter I've read in ages and nobody takes anything off but her. The wet-satin sequence is genuinely hard to sit through, in the good way, the way where you're braced for the book to humiliate her, and instead he's been kneeling there the whole time with his face tipped up waiting for her to open her eyes, and he never looked down. My reservations, since you'll ask: two of these chapters are just her friends being thrilled at her, and Cassie — who I trusted to be the one holding the clipboard — lines up every single alarming detail and then jokes that he must be gay. Also I cannot stop noticing that he had the heat turned up and the riser built and the silk bought before she'd been told what the afternoon was for. He engineered a room and then let her choose inside it. Which is, you understand, the exact thing the cover already told me it was going to do to me, and I walked in anyway, and that's why the damn book is working.

**gpt-5.6-sol:** These chapters absolutely got me, but in the exact dangerous way the book promised: Pace is so attentive that I understand why Vee experiences him as a revelation, and the dress fitting is genuinely scorching because what turns her on is being regarded without shame, not simply being handled. But then the book cuts to Randi using details of Vee’s body during sex with him, and suddenly all that exquisite care has a locked room behind it. I’m still in because the novel very clearly sees the violation and keeps giving Vee a full interior life rather than treating her consent as a magic solvent for deception—but I do not trust either of them, and I desperately want to know what happens when her freely given yes finally collides with everything she was never allowed to know.

**gpt-5.5:** I’m still in, and honestly more in than I expected to be, but I am reading with one hand on the emergency brake. The Pace/Vee chapters are doing something almost indecently good with being looked at, being asked, being allowed to want without being shamed; the dress chapter especially is the kind of erotic set piece that only works because it has psychological architecture under it. But Randi and Pace’s secret is getting more radioactive by the page, because Vee’s happiness is so real now, and every beautiful thing he gives her is happening inside a deception she cannot consent to because she doesn’t know it exists. The book seems to know that, which is why I’m not leaving. But oh, when the bill comes due, it had better know exactly what it has been charging.

### romantasy-refugee

**claude-opus-4-8:** Okay so I did NOT expect a book with no dragons in it to get me, and this one got me — it's a college town and a kitchen and a man who sews, and somehow the hottest thing in it is a tape measure. The measuring chapter, oh my god, read it, he barely touches her and I had to put it down. And the heroine actually chooses — she's the one unbuttoning in the truck, she's the one grinding on him on the box, it's her hands and her words every time, which is the thing I've been starving for. Here's the catch, and it's a real one: there's a woman named Randi, the "dear friend," and she and the mathematician planned this whole thing about Vee as a game, and there's a chapter where she rides him for a debrief about Vee's body that made me genuinely nauseous — the jacket TELLS you all this, you're ahead of poor Vee the whole time, and it turns her every happy squeal into a countdown. I can't decide if that's brilliant or if it's going to make me feel complicit and gross by book three. Also the mother's-voice shame thing — floozy, floozy, girls like that — runs SO many laps that I'm scared the book only knows one trick: humiliate the body, let the man redeem it, repeat. But Cassie. Cassie is the friend everyone deserves and she's the reason I'm still in the boat. I'm staying. I just want the Randi bomb to go off and I want it to cost somebody something, or I'll know the book was only ever teasing me.

**claude-opus-5:** Okay so — remember how I said I was done, that I couldn't do one more fated-bond boy sniffing a girl's neck and calling it destiny? This is a college town and a kitchen and a man with a tape measure and I am *gone* on it. There's a chapter where he measures her for a dress he's making her out of silk because she mentioned a magazine once, and she's standing on a little box he built, bare from the waist up in the afternoon, and he never takes a stitch off and it is the hottest hour I've read since I quit the dragons — because every single move is hers. She knocks on the truck window. She unbuttons her own shirt. She presses herself against his face and says "oops" like a liar, and he goes red and keeps hemming. Nobody's blood decided anything. And the friends are real! Cassie alone is worth the price — dry, protective, knows when to stop being funny — plus a gold dining hall full of girls stealing each other's fries. Now the bad: he's getting a little too finished for me, the joinery and the shellac and the cookbooks and then, come on, a patent that gets scared kids out of the MRI faster — I could feel the author's thumb. And the shame-voice in her mother's register comes at the same pitch every chapter; I've got it, thanks. Also the book has four chapters in a row that are Vee telling women what happened, which I mostly love and am starting to see the seams of. But here's the part that has me: I know something she doesn't, and this volume just showed me the woman who started the whole game clenching up on top of him and asking to be told what Vee's hair smells like, and then *leaving*, which she has never done. It's going to cost all three of them. Lend me nothing, I'm buying Book Two.

**gpt-5.6-sol:** I am completely in trouble with this book now. The dress fitting is absurdly, specifically hot—not because she takes her clothes off, but because you can feel her entire old shame structure waiting to crush her, and then she looks down and finds a man delighted by her, so she stands taller and starts tormenting him on purpose. Pace is weaponized competence with manners, which is obviously unfair, and Vee has become funny and bold without turning into a different woman; she is discovering that the self she was taught to apologize for has teeth. I love Cassie and the dinner-table girls because the book actually gives Vee a world to bring her desire back into. But I am not forgetting that Pace took something Vee gave him and carried it into bed with Randi without her knowledge, and Randi’s little invented date story made my skin crawl afterward—so yes, I want the next chapter immediately, but I am reading with one hand over my heart and the other already pointing at the trap.

**gpt-5.5:** I would tell you I am in trouble with this book. It is contemporary, which is so not my usual kingdom, but somehow a house, a truck, a mountain, and a bolt of silk are doing court intrigue levels of work on me. Pace is dangerously, almost suspiciously tailored to my weaknesses: competent, funny in the dry places, patient, and hot in that “I could, but I am choosing not to yet” way that makes me feral. The secrecy still bothers me, especially Randi getting pieces of Vee that Vee doesn’t know are being shared, and that may become the thing that breaks me later. But right now Vee is not passive on the page; she keeps reaching, asking, showing, leaning, choosing, and the book keeps making those choices cost her shame before they give her pleasure. So yes, I’m turning the page. I’m annoyed about how much.

### relationship-first

**claude-opus-4-8:** Okay — so I'm still in it, and I'm a little annoyed at how in it I am. The good stuff is really good: there's a chapter where the man tells the other woman, the one who set the whole thing up, every private detail of the date while she's on top of him, and she *comes* on it and says "I want us," and I had to put the book down on the couch. That's the book that knows more than it's saying. And the hike, the boot on the trail, the dress he cuts to match her coloring instead of the magazine — the tenderness is real and the sex is finally on the page and written, not just gestured at. Here's my gripe, and you know it's coming: this woman is ashamed of her body and the book has decided I need to hear her mother's voice call her a floozy roughly once a page, and it explains the shame, then re-explains it, then confirms it, and I keep thinking *I got it in chapter eleven, let me feel the next thing myself.* She's most alive when she's funny and wanting out loud — "pre-aroused every time I wore it," God — and flattest when the narrator apologizes for her. And the debrief-with-Cassie chapters, which I adore in principle because two girls in a dorm is my whole reason for reading, are starting to just replay the scene I watched two pages ago. Still. He turned the heat up hours before she arrived so she wouldn't be cold on the box. I know it's a trap. I know Randi's in the truck with them the whole time. That's exactly why I can't stop.

**claude-opus-5:** Okay, so — the hike chapter and the fitting chapter are the reason to read this. The fitting especially: an hour of a man with a tape measure and his shirt buttoned, nothing happens, and I had to put the book face-down on my knee twice. She's genuinely good at making being *looked at* the event, and the food writing is absurd, the horseradish going up into her nose, the cherry pits on the wax paper. And there's a chapter from his side with the other woman that's quietly vicious in the best way — she's in bed with him asking for details about the girl and something is going wrong in her that he cannot read and I could, and that's when I stopped worrying the book was only sincere. Two gripes. One, Pace keeps getting handed another accomplishment — he builds furniture, he sews, he has a patent that helps sick children hold still, and I wanted to say okay, I already like him, stop stacking. Two, the repetition: every good scene is followed by her telling Cassie about it and then telling two other girls about it, and the mother's shaming voice shows up in italics like a laugh track. I keep getting the feeling I've *had* something and then being handed it again in case I dropped it. Still — I'm going to read the next one tonight and I'm not going to pretend otherwise.

**gpt-5.6-sol:** The mountain-and-dress stretch absolutely got me, annoyingly so: he kneels to fix her boot, feeds her properly, remembers the dress she couldn’t afford, chooses the color that actually belongs on her, and then makes the damn thing himself, which is so extravagantly tailored to my weaknesses that I should feel manipulated and mostly don’t. The truck scene and the fitting are genuinely hot because the real charge is her deciding to be visible and discovering that he can want her without making that want a demand. I do wish the book would trust its own images more—it keeps explaining hunger, shame, asking, waiting, and being seen after the scene has already made me feel them—and Pace is becoming suspiciously good at every useful human activity. But Randi leaving after sex, Pace eating alone, and Cassie listening in that dorm room keep the book from becoming merely a gorgeous-man fantasy. I’m very much still reading, though I’m now watching closely to see whether the secret arrangement deepens these people or starts operating them.

**gpt-5.5:** These chapters are very much doing the thing now. I mean, the man takes her up a mountain, fixes her boot, feeds her rye and cherries, gives her the only dry shirt, then later makes her a custom silk dress in the color that suits her better than the color she asked for — so yes, he is becoming a slightly ridiculous fantasy of perfect male attention, but the book mostly gets away with it because Vee’s shame and hunger are so specifically rendered. The dress-measuring chapter is the one I’d hand you with raised eyebrows: it’s filthy, but not in the obvious way; it’s about being looked at without being diminished, which is apparently my whole weakness. I still distrust the Randi/Pace secret badly, and I’m waiting for the book to let Vee’s women talk about more than him, but I am absolutely not putting this down tonight.

### romance-graduate

**claude-opus-4-8:** Okay — you know how I keep whining that I want the filth AND a brain, that depth or heat alone bores me stupid? This is the one. There's a chapter that is nothing but a man measuring a girl for a dress, fully clothed, tape measure, pencil, and it is the hottest thing I've read in a year, because the whole charge is in him stepping *away* to write the number down and coming back, and in her body betraying her on satin she picked out with hope, and him never once looking down — waiting on his knees for her to open her eyes so she'd catch him being *glad* it was her. I got teary. Over a sewing scene. And it's not just candy — there's a chapter in the other woman's bed where you see Randi coming apart on the plan she started, "I want us" torn out of her mid-sex, and it turns the whole thing psychological in a way the jacket actually delivers on for once. The one thing nagging me: it strings a few quiet debrief chapters close together and I started counting, and the best friend who could see the trap can't, and I can feel the book getting ready to hurt this girl while she's the happiest she's ever been. But I am all the way in. Start it.

**claude-opus-5:** Okay so I'm seven chapters further in and I need you to buy this. The hiking chapter ends with her knocking on the truck window and taking her wet shirt off for him and he does not touch her, and I promise you that is hotter than anything on your Kindle right now. Then there's a chapter where he's in bed with the other one and she's riding him going "tell me" — tell me about *her* — and I actually said something out loud in an empty room. And then the dress-fitting: an hour of a fully dressed man with a tape measure and a woman on a box, she gets so turned on she soaks through her underwear and is dying of shame about it, and he's been on his knees the whole time looking *up at her face*. I have never read anything like it. The complaints are real but small: she debriefs a friend after basically every big scene, and by the third one I was skimming for the good lines, and there's a dining-hall chapter with a chatty roommate that's pure filler except for one perfect text message. Also the two-page ones still feel like a trick I haven't decided about. But the writing is genuinely written, the girl has an actual interior life full of her mother's voice, and the book is letting me love him while I watch him lie. It's going to wreck me and I'm not stopping.

**gpt-5.6-sol:** The mountain-and-truck chapter alone would’ve kept me reading, because she takes her shirt off for him and it’s hotter than half the acrobatics on Kindle Unlimited—but then he makes her a burgundy silk dress, and somehow the fitting is even hotter. Not just because he’s on his knees with his face exactly where you think; because she gets visibly, humiliatingly wet from being attended to, and he looks at her like she gave him a gift. There’s also a very explicit Randi/Pace scene that is sexy and quietly awful in the best way, because she wants something he doesn’t realize she’s asking for. A couple of the short chapters feel like deliberate little aftershocks, and the “is he gay?” joke made me roll my eyes, but this is absolutely doing the rare thing: the sexiness and the interior life are the same material.

**gpt-5.5:** I am kind of obsessed and also increasingly nervous in the best/worst way. The hike and truck chapter is already one of those scenes I’d reread out of order, but the dress-fitting chapter is the one I would shove at you and say, “No, read this, this is what I mean by erotic.” It’s not just that it’s hot, though it is wildly hot; it’s that the heat is coming from being attended to, being chosen, being looked at without contempt. Pace is almost too good, which would usually make me roll my eyes, except the Randi/Pace secret keeps the floor tilted under everything, and Randi’s chapter after the hike made that tilt feel dangerous instead of gimmicky. I don’t trust them, but I believe Vee’s happiness, and that is making me a little sick, which means yes, obviously, I’m turning the page.

### fsog-refugee

**claude-opus-4-8:** Okay — you know how long I've been looking for the one where the heat and the *asking* are the same thing and not at war? This is it, or these chapters are. There's a scene where she's soaked wet and freezing in his truck and she knocks on the glass and calls him back in and undoes every button herself with her eyes locked on his, and he just sits there shaking with cold, glad, and doesn't lift a hand — and then a measuring scene, a man fully dressed with a tape measure making her a dress, that is somehow the hottest thing I've read in a year *because* he never takes, he waits on his knees with his chin tipped up and never once looks down at the part of her she's dying over. I gasped out loud. Truly. BUT — and this is the thing I can't unsee — the jacket told me it's a plan, and there's a chapter where he's in bed with the other woman feeding her the tenderest private thing Vee ever gave him, "tell me," like a meal, and it made my skin crawl in the way the book absolutely intends. So I'm falling for exactly the thing I'm supposed to be scared of, and it knows it, and Vee doesn't. My one real gripe: she keeps living her romance by narrating it to Cassie and the dining-hall girls afterward, and I'm getting greedy — I want her *in the room with him*, not recapping it over fries. But I'm not putting it down. God, no. I need to know what Daphne cost him, and I need to see what happens when this stops being a game for the two who started it — because it already has.

**claude-opus-5:** Okay, you have to get to chapter 12, and then you have to brace for 17, because I have been complaining to you for *years* that nobody writes the thing I want and Helen Rivers just went and wrote it. He fixes her blister on the trail and apologizes for not asking about her boots. He gets out of a warm truck into freezing rain so she isn't looked at while she changes, and she has to knock on the glass to call him back, and when she opens her shirt he doesn't lay a hand on her — he just looks, and he's *glad*, and then she feels his hand shaking and stops her own want to get him warm. Then there's a whole chapter where a fully dressed man measures her for a dress she didn't think she could have, and she's on a little box he built, and she's mortified because her body has given her away completely, and he has spent the whole time with his chin tipped up waiting for her to open her eyes because he never looked down. I was breathing funny. Clothed, and it's the hottest thing I've read in a decade — the trick is the rhythm, close and then away and away and away, so the wanting stacks up in you too. The bad, or not bad exactly, the part that makes my stomach hurt: I know what she doesn't. There's a chapter where he's in bed with the other one and she asks him to *tell her* about Vee, and he does, and it's genuinely hot and I felt filthy about enjoying it, and then he quietly holds back the truck — protects Vee from her — and I was *grateful*, which tells you what kind of book this is. Randi can't stay in the bed afterward and doesn't know why, and I do, and I'm honestly more frightened for her than for Vee right now. Nothing has been taken from Vee yet. Everything's been asked. That's exactly why I can't put it down.

**gpt-5.6-sol:** Okay, this run of chapters would absolutely keep me up too late. The truck scene and the fitting are the thing I’m always complaining these books never quite give me: genuinely scorching control where the woman is choosing, initiating, teasing, and discovering what she wants while the man pays enough attention not to take that choice away from her. The dress is almost obscenely romantic because he listened to one discarded wish and understood her better than the wish did. But the Randi-and-Pace chapter put a stone in my stomach—Vee gave Pace those private pieces of herself, not both of them, and their using her intimacy together is the first place the secret scheme felt like an actual violation rather than merely a wicked premise. I’m still completely in, because the tenderness is too real to dismiss and because I suspect that very tenderness is going to make the deception hurt all three of them terribly.

**gpt-5.5:** These chapters are the best stretch so far for me, honestly. The mountain and the dress fitting are doing the thing I always want these books to do and almost never trust them to do: make being looked at feel filthy and holy and safe at the same time. Pace is almost too much — math genius, powerlifter, woodworker, cook, tailor, patent money, emotionally precise mountain man, I mean come on — but I am apparently very willing to be lied to if the lie is this attentive. The Randi/Pace scene is the sour note in the middle, not badly written, just morally complicated in a way that keeps the book from becoming pure fantasy, and I can feel the bill for that coming. But Vee on that box, realizing she has power and still being cared for? I would read another hundred pages for that alone.


## 6. New persona vs nearest control — complaint-category tallies (counts out of 32 items; rose / fell / held)

Pairings: v2 vs its v1; romantasy-refugee and relationship-first vs romance-graduate v1 (as specified); consent-sensitive vs romance-graduate v1 is appended for completeness since no control was named for it.

| new persona | control | (a) | (b) | (c) | (d) | (e) | (f) | (g) | (h) | any complaint | PRAISE C | PRAISE T | PRAISE ch14 | PRAISE ch17 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| romance-graduate-v2 | romance-graduate | 4→12 rose | 1→0 fell | 1→0 fell | 0→5 rose | 3→3 held | 2→3 rose | 0→0 held | 4→2 fell | 11→19 rose | 8→9 rose | 6→6 held | 8→7 fell | 8→8 held |
| fsog-refugee-v2 | fsog-refugee | 4→4 held | 3→2 fell | 0→1 rose | 0→0 held | 5→9 rose | 1→3 rose | 0→0 held | 0→0 held | 8→14 rose | 8→8 held | 3→4 rose | 7→6 fell | 8→8 held |
| romantasy-refugee | romance-graduate | 4→3 fell | 1→0 fell | 1→0 fell | 0→6 rose | 3→7 rose | 2→4 rose | 0→0 held | 4→0 fell | 11→15 rose | 8→10 rose | 6→7 rose | 8→5 fell | 8→7 fell |
| relationship-first | romance-graduate | 4→7 rose | 1→0 fell | 1→0 fell | 0→19 rose | 3→2 fell | 2→6 rose | 0→1 rose | 4→2 fell | 11→25 rose | 8→9 rose | 6→8 rose | 8→6 fell | 8→7 fell |
| consent-sensitive | romance-graduate | 4→3 fell | 1→0 fell | 1→0 fell | 0→0 held | 3→17 rose | 2→2 held | 0→0 held | 4→0 fell | 11→19 rose | 8→7 fell | 6→3 fell | 8→6 fell | 8→8 held |

Summary lines (control→new):

- **romance-graduate-v2 vs romance-graduate** — rose: a, d, f; fell: b, c, h; held: e, g.
- **fsog-refugee-v2 vs fsog-refugee** — rose: c, e, f; fell: b; held: a, d, g, h.
- **romantasy-refugee vs romance-graduate** — rose: d, e, f; fell: a, b, c, h; held: g.
- **relationship-first vs romance-graduate** — rose: a, d, f, g; fell: b, c, e, h; held: none.
- **consent-sensitive vs romance-graduate** — rose: e; fell: a, b, c, h; held: d, f, g.
