"""Prevent loss or misattribution of reviews during structural changes."""
import contextlib
import importlib.util
import io
import os
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))
import renumber_gates as gates


class MergeGateTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        cwd = os.getcwd()
        os.chdir(self.temp.name)
        self.addCleanup(os.chdir, cwd)
        self.slugs = ['opening', 'fed', 'portion', 'gone']
        self.title_map = {gates.norm(s): s for s in self.slugs}
        self.patches = [patch.object(gates, 'reader_slugs', return_value=self.slugs),
                        patch.object(gates, 'title_index', return_value=self.title_map)]
        for p in self.patches:
            p.start()
            self.addCleanup(p.stop)

    def gate(self, n, title, model='reader', persona='romance-graduate', sha='123456789abc'):
        path = Path('reviews/capture-panel') / model / 'dag' / persona / ('gate-ch%03d.md' % n)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('*protocol · gate ch%03d · prose-sha %s*\n\nGATE %d — %s\nDECISION: CONTINUE\nCAPTURE: 8\n' %
                        (n, sha, n, title))
        return str(path)

    def plan(self, **kwargs):
        return gates.build_plan(None, None, 'retire', merged=(2, 3),
                                preserve_shas=['123456789abc'], **kwargs)

    def test_merge_preserves_reviewed_gate_and_retires_both_legacy_reads(self):
        fresh = self.gate(2, 'Fed')
        fresh_bytes = Path(fresh).read_bytes()
        old = self.gate(3, 'Fed')
        later = self.gate(4, 'Portion')
        later_body = Path(later).read_text().split('\n', 1)[1]
        unreviewed = self.gate(2, 'Toenails', model='legacy')
        old_legacy = self.gate(3, 'Fed', model='legacy')
        plan, halts, _, _, _ = self.plan()
        self.assertEqual(halts, [])
        self.assertNotIn(fresh, plan)
        self.assertEqual(plan[old], gates.DELETE)
        self.assertEqual(plan[later], 3)
        retired = gates.retirement_paths(plan, 'retire', merged=(2, 3))
        self.assertEqual(gates.validate(plan, retired), [])
        gates.apply_plan(plan, retired)
        self.assertEqual(Path(fresh).read_bytes(), fresh_bytes)
        self.assertEqual(Path(later.replace('004', '003')).read_text().split('\n', 1)[1], later_body)
        self.assertIn('gate ch003', Path(later.replace('004', '003')).read_text().split('\n')[0])
        self.assertFalse(Path(unreviewed).exists())
        self.assertFalse(Path(old_legacy).exists())
        self.assertTrue(all(Path(p).exists() for p in retired.values()))

    def test_merged_title_without_reviewed_hash_halts(self):
        path = self.gate(2, 'Fed', sha='aaaaaaaaaaaa')
        before = Path(path).read_bytes()
        _, halts, _, _, _ = self.plan()
        self.assertEqual(halts[0][0], 'unverified-merged-read')
        self.assertEqual(Path(path).read_bytes(), before)

    def test_other_live_chapter_at_merge_position_halts(self):
        self.gate(3, 'Gone')
        _, halts, _, _, _ = self.plan()
        self.assertEqual(halts[0][0], 'merge-position-holds-other-live-read')

    def test_retirement_and_temporary_collisions_are_rejected(self):
        self.gate(2, 'Toenails')
        self.gate(3, 'Fed')
        later = self.gate(4, 'Portion')
        plan, halts, _, _, _ = self.plan()
        self.assertEqual(halts, [])
        retired = gates.retirement_paths(plan, 'retire', name='same.md', merged=(2, 3))
        self.assertTrue(gates.validate(plan, retired))
        retired = gates.retirement_paths(plan, 'retire', merged=(2, 3))
        Path(next(iter(retired.values()))).write_text('existing history')
        Path(later + '.renumber-tmp').write_text('unfinished operation')
        errors = gates.validate(plan, retired)
        self.assertTrue(any('retirement' in e for e in errors))
        self.assertTrue(any('temporary' in e for e in errors))

    def test_known_mistype_survives_position_change(self):
        self.gate(5, 'Sorority', model='claude-fable-5-1', persona='fsog-refugee')
        plan, halts, _, _, _ = self.plan()
        self.assertEqual(halts, [])
        gates.apply_plan(plan, {})
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(gates.verify(), 0)

    def test_already_aligned_tail_requires_explicit_opt_in(self):
        path = self.gate(4, 'Gone')
        before = Path(path).read_bytes()
        _, halts, _, _, _ = self.plan()
        self.assertTrue(halts)
        plan, halts, _, _, _ = self.plan(keep_aligned=True)
        self.assertEqual(halts, [])
        self.assertNotIn(path, plan)
        self.assertEqual(Path(path).read_bytes(), before)

    def test_aligned_tail_cannot_be_overwritten_by_a_shift(self):
        self.gate(4, 'Gone')
        self.gate(5, 'Gone')
        plan, halts, _, _, _ = self.plan(keep_aligned=True)
        self.assertEqual(halts, [])
        self.assertTrue(any('occupied' in e for e in gates.validate(plan)))

    def test_plain_removal_and_insertion_still_validate(self):
        removed = self.gate(2, 'Deleted')
        later = self.gate(3, 'Fed')
        plan, halts, _, _, _ = gates.build_plan(2, None, 'retire')
        self.assertEqual(halts, [])
        self.assertEqual(plan, {removed: gates.DELETE, later: 2})
        Path(removed).unlink()
        Path(later).unlink()
        earlier = self.gate(1, 'Opening')
        source = self.gate(2, 'Portion')
        plan, halts, _, _, _ = gates.build_plan(None, 2, 'retire')
        self.assertEqual(halts, [])
        self.assertNotIn(earlier, plan)
        self.assertEqual(plan[source], 3)

    def test_check_does_not_mutate_files(self):
        self.gate(2, 'Fed')
        self.gate(3, 'Fed')
        self.gate(4, 'Portion')
        before = {str(p): p.read_bytes() for p in Path('.').rglob('*.md')}
        args = ['renumber_gates.py', '--merged', '2', '3', '--preserve-prose-sha',
                '123456789abc', '--check']
        with patch.object(sys, 'argv', args), contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(gates.main(), 0)
        self.assertEqual(before, {str(p): p.read_bytes() for p in Path('.').rglob('*.md')})


class RetiredCaptureTests(unittest.TestCase):
    def test_default_statistics_exclude_retired_history(self):
        # Loading historical scores should not need a model SDK or provider call.
        stub = types.SimpleNamespace(capture_models=lambda **_: ('active-reader',))
        spec = importlib.util.spec_from_file_location('capture_stats_for_test', TOOLS / 'capture_stats.py')
        module = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, {'checkpoint_bundle': types.SimpleNamespace(), 'cold_read_config': stub}):
            spec.loader.exec_module(module)
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            for model in ['active-reader', 'retired-reader']:
                p = root / model / 'dag/romance-graduate/gate-ch001.md'
                p.parent.mkdir(parents=True)
                p.write_text('DECISION: CONTINUE\nCAPTURE: 8\nNEXT: 9\n')
            with patch.object(module, 'PANEL_ROOT', root):
                self.assertEqual([g.model for g in module.load()], ['active-reader'])
                self.assertEqual([g.model for g in module.load(model='retired-reader')], ['retired-reader'])


if __name__ == '__main__':
    unittest.main()
