"""friction_check: quote verification, family mapping, stance, grouping."""
from pathlib import Path
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import friction_check as fc

PROSE = """# Test

She had been late to everything all morning and it didn't bother her a whit.

"Same numbers. Nobody touched one of them," the professor said, and tapped the board.

Randi knelt on the pale floor and held the foot to the light.
"""


class QuoteVerification(unittest.TestCase):
    def setUp(self):
        self.scene = fc.Scene(PROSE)

    def test_exact_quote_ignores_case_and_punctuation(self):
        self.assertEqual(self.scene.verify("same numbers — nobody touched ONE of them!"),
                         (5, 5, "same numbers nobody touched one of them"))

    def test_trimmed_misquote_uses_longest_run(self):
        v = self.scene.verify("Same numbers. Nobody touched one.")
        self.assertEqual(v[:2], (5, 5))

    def test_too_short_and_absent_quotes_fail(self):
        self.assertIsNone(self.scene.verify("held the foot"))          # 3 words
        self.assertIsNotNone(self.scene.verify("held the foot", min_words=3))
        self.assertIsNone(self.scene.verify("the cat sat on the mat"))

    def test_stopword_run_does_not_anchor(self):
        self.assertIsNone(self.scene.verify("and it didn't"))
        self.assertIsNone(fc.Scene("it was on the way to it").verify("it was on the", 4))


class Families(unittest.TestCase):
    def test_prefixes(self):
        cases = {"claude-opus-5-5": "Anthropic", "claude-fable-5-1": "Anthropic",
                 "gpt-5.6-sol": "OpenAI", "gemini-4-argon": "Google", "glm-5.3": "Zhipu",
                 "deepseek-v4-pro-0813": "DeepSeek", "muse-wonder": "Meta",
                 "kimi-k3": "Moonshot", "qwen-4": "Alibaba"}
        for model, fam in cases.items():
            self.assertEqual(fc.family(model), fam, model)
        self.assertIsNone(fc.family("pilot-consensus"))


class Classification(unittest.TestCase):
    def m(self, s):
        return fc.mask(s)[0]

    def test_complaint(self):
        self.assertEqual(fc.classify(self.m('"Same numbers. Nobody touched one" is the author tapping the glass.')), "complaint")
        self.assertEqual(fc.classify(self.m('The ending felt heavy-handed.')), "complaint")

    def test_praise(self):
        self.assertEqual(fc.classify(self.m('"He made it to you" is the best line in the chapter.')), "praise")

    def test_mixed(self):
        self.assertEqual(fc.classify("The shoe-store comedy runs a touch long but earns it."), "mixed")

    def test_negations(self):
        self.assertEqual(fc.classify("I felt no friction with the writing at all."), "neutral")
        self.assertEqual(fc.classify("The last line doesn't land."), "complaint")

    def test_quoted_words_are_not_cues(self):
        # "dragging" and "tidy" belong to the prose, not the reviewer
        self.assertEqual(fc.classify(self.m('She wrote "the breasts dragging across a tidy bed."')), "neutral")

    def test_weak_cue_yields_to_praise(self):
        self.assertEqual(fc.classify("I winced, and it was perfect."), "praise")
        self.assertEqual(fc.classify("I winced at that line."), "complaint")

    def test_context(self):
        self.assertEqual(fc.paragraph_context("ALMOST-STOPPED: \"x\"", ""), "complaint")
        self.assertEqual(fc.paragraph_context("Friction: the lecture.", ""), "complaint")
        self.assertEqual(fc.paragraph_context("+ LOVE: the shoes", ""), "praise")
        self.assertEqual(fc.paragraph_context("+ GRUDGE: Vee dimmed Cassie", ""), "")
        self.assertEqual(fc.classify("A plain sentence.", "complaint"), "complaint")
        self.assertEqual(fc.classify("A lovely sentence.", "complaint"), "mixed")

    def test_sentence_split_respects_quotes(self):
        masked, spans = fc.mask('He said "Stop. Go now." Then it ended. Fine.')
        self.assertEqual(len(spans), 1)
        self.assertEqual(len(fc.sentences(masked)), 3)


class Grouping(unittest.TestCase):
    def hit(self, a, b):
        r = fc.Read("claude-opus-5-5", "cold", "cold", Path("x.md"))
        return fc.Hit(r, (a, b), "q", "complaint", "s", 1)

    def test_same_and_overlapping_lines_merge(self):
        groups = fc.group([self.hit(5, 5), self.hit(9, 9), self.hit(5, 7), self.hit(7, 9),
                           self.hit(12, 12)])
        self.assertEqual([sorted({h.lines for h in g}) for g in groups],
                         [[(5, 5), (5, 7), (7, 9), (9, 9)], [(12, 12)]])

    def test_stance_union(self):
        r = fc.Read("gpt-5.6-sol", "cold", "cold", Path("x.md"))
        mk = lambda s: fc.Hit(r, (1, 1), "q", s, "s", 1)
        self.assertEqual(fc.stance_of([mk("complaint"), mk("neutral")]), "complaint")
        self.assertEqual(fc.stance_of([mk("complaint"), mk("praise")]), "mixed")
        self.assertEqual(fc.stance_of([mk("neutral")]), "neutral")


class Verdicts(unittest.TestCase):
    """End to end on a synthetic chapter and corpus."""

    def read(self, d, model, text, persona="cold"):
        p = Path(d) / f"{model}-{persona}.md"
        p.write_text(text)
        return fc.Read(model, "cold" if persona == "cold" else "dag", persona, p)

    def test_real_taste_noise(self):
        lines = ["The hike had made her hungry first, that was the trick.",
                 "The siren squawked one short electronic bark over the rain.",
                 "She ate the soup slowly in the warm kitchen light.",
                 "The bench stood under the window like a promise kept.",
                 "Cassie made her bed tight every single morning.",
                 "The garment bag hung zipped and safe in the closet."]
        scene = fc.Scene("# T\n\n" + "\n\n".join(lines) + "\n")
        q = lambda i: '"' + " ".join(lines[i].split()[:6]) + '"'
        with tempfile.TemporaryDirectory() as d:
            reads = [
                # line 3: three Anthropic reads + OpenAI -> REAL
                self.read(d, "claude-opus-5-5", f"Friction: {q(0)} is on the nose.\n"),
                self.read(d, "claude-sonnet-5-5", f"{q(0)} telegraphs.\n"),
                self.read(d, "claude-fable-5-1", f"{q(0)} is heavy-handed.\n"),
                self.read(d, "gpt-5.6-sol", f"{q(0)} is heavy-handed.\n"),
                # line 5: three Anthropic reads only -> TASTE
                self.read(d, "claude-fable-5-1", f"ALMOST-STOPPED: {q(1)}\n", "fsog"),
                self.read(d, "claude-opus-5-5", f"ALMOST-STOPPED: {q(1)}\n", "fsog"),
                self.read(d, "claude-sonnet-5-5", f"ALMOST-STOPPED: {q(1)}\n", "fsog"),
                # lines 7-13: one Anthropic read each -> NOISE
                self.read(d, "claude-opus-4-8", f"{q(2)} felt like filler. {q(3)} felt like filler.\n"),
                self.read(d, "claude-opus-5-5", f"{q(4)} is tedious. {q(5)} is tedious.\n", "rg"),
                # line 9 also praised by two families -> CONTESTED
                self.read(d, "glm-5.3", f"{q(3)} is perfect.\n"),
                self.read(d, "gemini-4-argon", f"{q(3)} is the best line.\n"),
            ]
            root = fc.ROOT
            fc.ROOT = Path(d)
            try:
                res = fc.score("t", reads, scene)
            finally:
                fc.ROOT = root
        v = {p["scene"]: p["verdict"] for p in res["passages"]}
        self.assertEqual(res["anthropic_base_rate"], 1.67)
        self.assertEqual(v, {"scenes/t.md:3": "REAL", "scenes/t.md:5": "TASTE",
                             "scenes/t.md:7": "NOISE", "scenes/t.md:9": "CONTESTED",
                             "scenes/t.md:11": "NOISE", "scenes/t.md:13": "NOISE"})
        self.assertEqual([p["verdict"] for p in res["passages"]][:2], ["REAL", "TASTE"])


if __name__ == "__main__":
    unittest.main()
