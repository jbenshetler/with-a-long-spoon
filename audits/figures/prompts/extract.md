Below is part of one chapter of a novel (`{{SLUG}}`). Each line starts with its line number and a tab.

List EVERY figure of speech in it. A figure is any place where the prose describes one thing in terms of another:
- similes ("like…", "as if…", "as though…", "the way you…");
- metaphors with no signal word ("the conversation was a locked room", "they were climbing the same hill");
- figurative verbs and stock body-idioms that carry a picture, even worn ones ("her heart sank", "the ground tilted under him", "his face fell"). Worn figures count: readers still notice a repeated one.
- figures inside dialogue count too.

Do NOT list literal description: a real staircase someone climbs, a real lamp in the room, actual sunlight. If you cannot tell whether something is literal, include it with "literal_maybe": true.

Be exhaustive. A long passage may hold dozens of figures. Missing a figure is worse than including a borderline one.

For each figure return an object:
- "line": the line number it is on;
- "quote": the shortest exact span from that line that contains the figure, copied character for character (at most 25 words);
- "picture": the image the figure borrows, in 1–4 plain words (e.g. "a struck match", "a tide going out", "deep water", "a held breath");
- "vehicles": EVERY concrete noun the figure borrows, singular, lowercase, as a list (e.g. "she ran out of road" -> ["road"]; "he tied his worry to a kite string" -> ["kite", "string"]; "his voice came on like a radio" -> ["radio"]). Name the borrowed thing even when the sentence implies it without naming it;
- "feeling": what the figure renders, in 2–6 plain words (e.g. "sudden lurch of wrongness", "attention turned on someone", "relief after strain");
- "sensation": the bodily sensation the figure evokes, chosen from this list exactly: "drop or lurch", "rising or lifting", "sinking or heaviness", "floating or weightless", "warmth spreading", "heat or burning", "cold or chill", "light coming on", "glow from within", "darkness or shadow", "being seen or exposed", "opening", "closing or shutting", "tightening", "loosening or release", "pressure or weight", "hollow or emptiness", "flooding or overflow", "melting or softening", "breaking or cracking", "sharpness or cutting", "jolt or shock", "hum or vibration", "suspension or held breath", "being held or supported", "being pulled or drawn", "settling or landing", "movement or travel", "none" (use "none" when the figure evokes no bodily sensation);
- "applies_to": who or what the figure describes (a character's name, or "the room", "the dress", "the evening"…);
- "pov": whose narration or speech it is in (a character's name, or "narrator");
- "kind": one of "simile", "metaphor", "verb", "idiom";
- "literal_maybe": true or false.

Reply with a JSON array of these objects and nothing else. If there are no figures, reply [].

TEXT:
{{TEXT}}
