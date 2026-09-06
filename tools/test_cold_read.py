"""Focused unit tests for Codex subscription cold-reader authentication."""
from __future__ import annotations

import hashlib
import json
import importlib
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))


class _UsageTotal:
    input_tokens = 11
    output_tokens = 17
    reasoning_output_tokens = 3
    total_tokens = 28
    cached_input_tokens = 2


class _Result:
    final_response = "### Reader reaction\n\nFine\n\n### Carry-forward state\n\nRemembered"
    id = "turn-1"
    error = None
    status = "completed"
    duration_ms = 25
    usage = types.SimpleNamespace(total=_UsageTotal())


class _Thread:
    def __init__(self, calls):
        self.calls = calls

    def run(self, prompt, **kwargs):
        self.calls.append(("run", prompt, kwargs))
        return _Result()


class _Codex:
    last = None

    def __init__(self):
        self.calls = []
        self.closed = False
        _Codex.last = self

    def thread_start(self, **kwargs):
        self.calls.append(("thread_start", kwargs))
        return _Thread(self.calls)

    def account(self, *, refresh_token=False):
        return types.SimpleNamespace(account=object(), requires_openai_auth=False)

    def close(self):
        self.closed = True


import cold_read_batch


class _Sandbox:
    read_only = "read-only"

class _Responses:
    def create(self, **kwargs):
        self.kwargs = kwargs
        usage = types.SimpleNamespace(
            input_tokens=10,
            output_tokens=20,
            total_tokens=30,
            output_tokens_details=None,
        )
        return types.SimpleNamespace(
            output_text="### Reader reaction\n\nFine\n\n### Carry-forward state\n\nRemembered",
            usage=usage,
            status="completed",
            id="response-1",
        )




class _ChatCompletions:
    def create(self, **kwargs):
        self.kwargs = kwargs
        usage = types.SimpleNamespace(prompt_tokens=10, completion_tokens=20, total_tokens=30)
        choice = types.SimpleNamespace(
            message=types.SimpleNamespace(content="### Reader reaction\n\nFine\n\n### Carry-forward state\n\nRemembered"),
            finish_reason="stop",
        )
        return types.SimpleNamespace(id="chat-1", usage=usage, choices=[choice])


class _Chat:
    def __init__(self):
        self.completions = _ChatCompletions()
class _OpenAI:
    last = None

    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.responses = _Responses()
        self.chat = _Chat()
        _OpenAI.last = self


class CodexAdapterTests(unittest.TestCase):
    def setUp(self):
        self.module = importlib.import_module("cold_read")

    def test_subscription_adapter_isolated_and_reports_unknown_cost(self):
        fake_sdk = types.SimpleNamespace(Codex=_Codex, Sandbox=_Sandbox)
        with patch.dict(sys.modules, {"openai_codex": fake_sdk}):
            agent_fn, close = self.module.make_codex_agent_fn(
                system_prompt="blind-reader instructions",
                effort="low",
            )
            result = agent_fn(prompt="chapter text", model="codex-model", label="label")
            thread_call = _Codex.last.calls[0]
            run_call = _Codex.last.calls[1]

            self.assertEqual(thread_call[0], "thread_start")
            self.assertEqual(thread_call[1]["developer_instructions"], "blind-reader instructions")
            self.assertEqual(thread_call[1]["sandbox"], _Sandbox.read_only)
            self.assertNotEqual(Path(thread_call[1]["cwd"]).resolve(), self.module.REPO)
            self.assertEqual(run_call[2]["sandbox"], _Sandbox.read_only)
            self.assertEqual(result["output"], _Result.final_response)
            self.assertIsNone(result["usage"]["cost"])
            self.assertEqual(result["usage"]["totalTokens"], 28)
            close()
            self.assertTrue(_Codex.last.closed)

    def test_retention_does_not_require_unintroduced_principals(self):
        principals = {"cassie": ["cassie"], "vee's mother": ["vee's mother"]}
        self.assertEqual(
            cold_read_batch.check_retention("", "### Who's who\n\n- **Pace**", principals),
            [],
        )
        self.assertEqual(
            cold_read_batch.check_retention("Cassie", "### Who's who\n\n- **Pace**", principals),
            ["dropped PRINCIPAL: cassie"],
        )

    def test_openrouter_uses_compatible_endpoint_and_token_cap(self):
        fake_openai = types.SimpleNamespace(OpenAI=_OpenAI)
        with patch.dict(sys.modules, {"openai": fake_openai}):
            agent_fn = self.module.make_openrouter_agent_fn(
                system_prompt="blind-reader instructions",
                effort="none",
                timeout=30,
                max_output_tokens=4000,
                api_key="router-token",
            )
            result = agent_fn(prompt="chapter text", model="anthropic/claude-sonnet-4", label="label")
            self.assertEqual(_OpenAI.last.kwargs["base_url"], "https://openrouter.ai/api/v1")
            self.assertEqual(_OpenAI.last.kwargs["api_key"], "router-token")
            self.assertEqual(_OpenAI.last.chat.completions.kwargs["max_tokens"], 4000)
            self.assertIsNone(result["usage"]["cost"])

    def test_provider_completion_rejects_truncation_signals(self):
        grounded = importlib.import_module("cold_read_grounded")
        grounded.validate_provider_completion({"finishReason": "stop", "incomplete": False})
        grounded.validate_provider_completion({})
        with self.assertRaisesRegex(RuntimeError, "finish reason"):
            grounded.validate_provider_completion({"finishReason": "length"})
        with self.assertRaisesRegex(RuntimeError, "incomplete"):
            grounded.validate_provider_completion(
                {"finishReason": "stop", "incomplete": True}
            )




class DonorMemoryTests(unittest.TestCase):
    def setUp(self):
        self.config = importlib.import_module("cold_read_config")
        self.grounded = importlib.import_module("cold_read_grounded")

    def test_donor_reader_resolves_ensemble_and_cannot_mint(self):
        path = self.config.checkpoint_path("qwen3.8-max-0902", 50)
        self.assertEqual(
            path.relative_to(self.config.REPO).as_posix(),
            "reviews/cold-read/checkpoint-ensembles/core/checkpoints/ck-ch050.md",
        )
        self.assertFalse(self.config.can_mint_checkpoint("qwen3.8-max-0902"))
        self.assertFalse(self.config.can_mint_checkpoint("qwen/qwen3.8-max-0902"))
        self.assertRegex(
            self.grounded.memory_line("qwen3.8-max-0902", 59, 50),
            r"ensemble core ck-ch050@[0-9a-f]{12} \+ raw ch051\.\.ch058",
        )

    def test_donor_resume_requires_current_memory_header(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "review.md"
            expected = self.grounded.memory_line("qwen3.8-max-0902", 59, 50)
            path.write_text(
                f"# Cold read\\n\\n*scene: x · model: q · memory: {expected} · reader-protocol: v3*\\n\\n"
                "## Reader reaction\\n\\nBody\\n",
                encoding="utf-8",
            )
            self.assertTrue(
                self.grounded.review_memory_is_current("qwen3.8-max-0902", 59, 50, path)
            )
            path.write_text(path.read_text().replace(expected, "donor claude-fable-5 ck-ch050"))
            self.assertFalse(
                self.grounded.review_memory_is_current("qwen3.8-max-0902", 59, 50, path)
            )

    def test_stale_donor_checkpoint_rejected_when_loaded(self):
        ensemble = importlib.import_module("checkpoint_ensemble")
        with tempfile.TemporaryDirectory() as td:
            checkpoint = Path(td) / "ck-ch050.md"
            checkpoint.write_text("# Checkpoint\n\n---\n\nBody\n", encoding="utf-8")
            with patch.object(
                self.config, "checkpoint_path", return_value=checkpoint
            ), patch.object(
                ensemble, "check", side_effect=SystemExit("ensemble check failed")
            ):
                with self.assertRaisesRegex(SystemExit, "ensemble check failed"):
                    self.grounded.load_checkpoint("qwen3.8-max-0902", 50)

    def test_check_mode_rejects_stale_donor_before_reader_launch(self):
        cold_read = importlib.import_module("cold_read")
        with tempfile.TemporaryDirectory() as td:
            checkpoint = Path(td) / "ck-ch050.md"
            checkpoint.write_text("# stale\n", encoding="utf-8")
            argv = [
                "cold_read_grounded.py",
                "--model",
                "qwen/qwen3.8-max-0902",
                "--model-id",
                "qwen3.8-max-0902",
                "--from",
                "51",
                "--to",
                "51",
                "--check",
            ]
            with patch.object(sys, "argv", argv), patch.object(
                self.grounded, "checkpoint_path", return_value=checkpoint
            ), patch.object(
                self.grounded,
                "load_checkpoint",
                side_effect=SystemExit("ensemble check failed: stale source"),
            ) as validate, patch.object(
                cold_read, "make_codex_agent_fn"
            ) as launch:
                with self.assertRaisesRegex(SystemExit, "stale source"):
                    self.grounded.main()
        validate.assert_called_once_with("qwen3.8-max-0902", 50)
        launch.assert_not_called()

    def test_checkpoint_packet_uses_cross_volume_reader_bundle(self):
        with tempfile.TemporaryDirectory() as td:
            packet_dir = Path(td)
            fingerprints = {
                "source_sha256": "s",
                "bundle_sha256": "b",
                "cleaner_version": 1,
                "extractor_sha256": "e",
            }
            with patch.object(
                self.grounded.checkpoint_bundle,
                "build_reader_bundle",
                return_value="cross-volume bundle",
            ) as build_bundle, patch.object(
                self.grounded.checkpoint_bundle,
                "source_fingerprints",
                return_value=fingerprints,
            ), patch.object(
                self.grounded.checkpoint_bundle,
                "validate_seed_lineage",
                return_value="current",
            ), patch.object(
                self.grounded,
                "_write_chunked_packet",
                return_value=("token", packet_dir, ["part-001"]),
            ):
                self.grounded.emit_bundle_packet(60, "claude-fable-5")
        self.assertEqual(build_bundle.call_count, 2)
        build_bundle.assert_any_call(60)
        build_bundle.assert_any_call(60, start=51)


class CheckpointPolicyTests(unittest.TestCase):
    def setUp(self):
        self.bundle = importlib.import_module("checkpoint_bundle")

    def test_checkpoint_seed_policy_is_explicit(self):
        self.assertEqual(self.bundle.checkpoint_plan(50), (None, 1))
        self.assertEqual(self.bundle.checkpoint_plan(60), (50, 51))
        with self.assertRaisesRegex(ValueError, "no explicit checkpoint seed policy"):
            self.bundle.checkpoint_plan(70)

    def test_checkpoint_metadata_reads_first_and_middle_fields(self):
        raw = (
            "# Checkpoint — through Chapter 50\n\n"
            "*model: gpt-5.6-sol · span: ch001–ch050 · "
            "source-sha256: abc123 · grounded*\n\n---\n\nBody"
        )
        self.assertEqual(
            self.bundle.checkpoint_metadata(raw, "model"), "gpt-5.6-sol"
        )
        self.assertEqual(
            self.bundle.checkpoint_metadata(raw, "source-sha256"), "abc123"
        )

    def test_seed_lineage_validates_boundary_model_and_optional_source(self):
        current = (
            "# Checkpoint — through Chapter 50\n\n"
            "*model: gpt-5.6-sol · source-sha256: current*\n\n---\n\nBody"
        )
        legacy = (
            "# Checkpoint — through Chapter 50\n\n"
            "*model: moonshotai/kimi-k3*\n\n---\n\nBody"
        )
        with patch.object(
            self.bundle, "build_reader_bundle", return_value="bundle"
        ), patch.object(
            self.bundle,
            "source_fingerprints",
            return_value={"source_sha256": "current"},
        ):
            self.assertEqual(
                self.bundle.validate_seed_lineage(
                    current,
                    expected_boundary=50,
                    expected_model="gpt-5.6-sol",
                    extractor_prompt="prompt",
                ),
                "current",
            )
            self.assertEqual(
                self.bundle.validate_seed_lineage(
                    legacy,
                    expected_boundary=50,
                    expected_model="moonshotai/kimi-k3",
                    extractor_prompt="prompt",
                ),
                "unknown",
            )
            with self.assertRaisesRegex(ValueError, "seed model"):
                self.bundle.validate_seed_lineage(
                    current,
                    expected_boundary=50,
                    expected_model="gpt-5.5",
                    extractor_prompt="prompt",
                )


class EnsembleValidationTests(unittest.TestCase):
    def setUp(self):
        self.ensemble = importlib.import_module("checkpoint_ensemble")
        shared = "The checkpoint remembers this exact relationship statement."
        self.sources = [
            {"model_id": "claude-fable-5", "vendor": "anthropic", "body": shared},
            {"model_id": "gpt-5.5", "vendor": "openai", "body": shared},
        ]
        self.claim = {
            "section": "Relationships",
            "type": "state",
            "slot": "relationship:pair:status",
            "text": "Their relationship is current at this boundary.",
            "valid_from": 1,
            "superseded_at": None,
            "support": [
                {"model": "claude-fable-5", "quote": shared},
                {"model": "gpt-5.5", "quote": shared},
            ],
            "scene_evidence": [
                {"slug": "scene", "quote": "They kissed and stayed together."}
            ],
        }

    def test_cross_vendor_quote_backed_claim_passes(self):
        with patch.object(
            self.ensemble, "scene_map", return_value={"scene": "They kissed and stayed together."}
        ):
            ledger = self.ensemble.validate_claims(
                {"claims": [self.claim]}, name="core", boundary=50, sources=self.sources
            )
        self.assertEqual(len(ledger["claims"]), 1)
        self.assertEqual(ledger["claims"][0]["type"], "state")

    def test_same_vendor_quorum_fails(self):
        sources = [dict(source, vendor="anthropic") for source in self.sources]
        with patch.object(
            self.ensemble, "scene_map", return_value={"scene": "They kissed and stayed together."}
        ):
            with self.assertRaisesRegex(ValueError, "cross-vendor"):
                self.ensemble.validate_claims(
                    {"claims": [self.claim]}, name="core", boundary=50, sources=sources
                )

    def test_admission_preserves_prior_ledger_hash(self):
        settings = {
            "quorum": 2,
            "cross_vendor": True,
            "minimum_claims": 1,
            "required_sections": ["Relationships"],
        }
        payload = {"claims": [self.claim], "prior_ledger_sha256": "abc123"}
        with patch.object(
            self.ensemble, "scene_map", return_value={"scene": "They kissed and stayed together."}
        ), patch.object(
            self.ensemble.cold_read_config,
            "ensemble_settings",
            return_value=settings,
        ):
            ledger, rejected, _coverage = self.ensemble.admit_candidate_claims(
                payload, name="core", boundary=50, sources=self.sources
            )
        self.assertEqual(ledger["prior_ledger_sha256"], "abc123")
        self.assertEqual(rejected, [])

    def test_duplicate_temporal_slot_is_rejected(self):
        second = dict(self.claim, text="A conflicting current state.")
        with patch.object(
            self.ensemble, "scene_map", return_value={"scene": "They kissed and stayed together."}
        ):
            with self.assertRaisesRegex(ValueError, "has 2 active claims"):
                self.ensemble.validate_claims(
                    {"claims": [self.claim, second]},
                    name="core",
                    boundary=50,
                    sources=self.sources,
                )

    def test_one_source_entity_requires_narrow_matching_subtype(self):
        entity = dict(
            self.claim,
            section="Who's who",
            type="entity",
            slot="entity:pace:role",
            text="Pace is present in the scene.",
            support=[self.claim["support"][0]],
        )
        with patch.object(
            self.ensemble, "scene_map", return_value={"scene": "They kissed and stayed together."}
        ):
            with self.assertRaisesRegex(ValueError, "one-source entity exception"):
                self.ensemble.validate_claims(
                    {"claims": [entity]}, name="core", boundary=50, sources=self.sources
                )
            entity["entity_subtype"] = "role"
            ledger = self.ensemble.validate_claims(
                {"claims": [entity]}, name="core", boundary=50, sources=self.sources
            )
        self.assertEqual(ledger["claims"][0]["entity_subtype"], "role")

    def test_temporal_merge_replaces_same_slot_and_carries_immutable(self):
        prior = {
            "boundary": 40,
            "claims": [
                {
                    "id": "old-state",
                    "type": "state",
                    "section": "Relationships",
                    "slot": "relationship:pair:status",
                    "text": "The old state.",
                    "valid_from": 40,
                    "superseded_at": None,
                },
                {
                    "id": "event",
                    "type": "event",
                    "section": "Story so far",
                    "slot": "",
                    "text": "An immutable milestone happened.",
                    "valid_from": 10,
                    "superseded_at": None,
                },
            ],
            "history": [],
        }
        current = {
            "boundary": 50,
            "claims": [
                {
                    "id": "new-state",
                    "type": "state",
                    "section": "Relationships",
                    "slot": "relationship:pair:status",
                    "text": "The current state.",
                    "valid_from": 50,
                    "superseded_at": None,
                }
            ],
            "history": [],
        }
        with tempfile.TemporaryDirectory() as td:
            prior_path = Path(td) / "ck-ch040.json"
            prior_path.write_text("{}", encoding="utf-8")
            current["prior_ledger_sha256"] = hashlib.sha256(b"{}").hexdigest()
            with patch.object(self.ensemble, "REPO", Path(td)), patch.object(
                self.ensemble, "previous_ledger", return_value=(prior_path, prior)
            ):
                merged, lineage = self.ensemble.merge_temporal_ledger(
                    current, name="core", boundary=50
                )
        self.assertEqual({claim["id"] for claim in merged["claims"]}, {"new-state", "event"})
        self.assertEqual(merged["history"][0]["superseded_at"], 50)
        self.assertEqual(lineage["boundary"], 40)

    def test_immutable_slot_change_fails_even_when_old_claim_repeats(self):
        old = {
            "id": "old-entity",
            "type": "entity",
            "section": "Who's who",
            "slot": "entity:pace:identity",
            "text": "Pace is Pace.",
            "valid_from": 1,
            "superseded_at": None,
        }
        changed = dict(old, id="changed-entity", text="Pace is somebody else.")
        prior = {"boundary": 40, "claims": [old], "history": []}
        current = {"boundary": 50, "claims": [old, changed], "history": []}
        with tempfile.TemporaryDirectory() as td:
            prior_path = Path(td) / "ck-ch040.json"
            prior_path.write_text("{}", encoding="utf-8")
            current["prior_ledger_sha256"] = hashlib.sha256(b"{}").hexdigest()
            with patch.object(self.ensemble, "REPO", Path(td)), patch.object(
                self.ensemble, "previous_ledger", return_value=(prior_path, prior)
            ):
                with self.assertRaisesRegex(ValueError, "immutable slot"):
                    self.ensemble.merge_temporal_ledger(
                        current, name="core", boundary=50
                    )

    def test_temporal_omission_carries_unresolved_claim(self):
        prior_claim = {
            "id": "old-state",
            "type": "state",
            "section": "Relationships",
            "slot": "relationship:pair:status",
            "text": "The old state.",
            "valid_from": 40,
            "superseded_at": None,
        }
        prior = {"boundary": 40, "claims": [prior_claim], "history": []}
        current = {"boundary": 50, "claims": [], "history": []}
        with tempfile.TemporaryDirectory() as td:
            prior_path = Path(td) / "ck-ch040.json"
            prior_path.write_text("{}", encoding="utf-8")
            current["prior_ledger_sha256"] = hashlib.sha256(b"{}").hexdigest()
            with patch.object(self.ensemble, "REPO", Path(td)), patch.object(
                self.ensemble, "previous_ledger", return_value=(prior_path, prior)
            ):
                merged, _lineage = self.ensemble.merge_temporal_ledger(
                    current, name="core", boundary=50
                )
        self.assertEqual([claim["id"] for claim in merged["claims"]], ["old-state"])
        self.assertEqual(merged["claims"][0]["carried_from_boundary"], 40)
        self.assertEqual(merged["history"], [])

class HarnessParsingTests(unittest.TestCase):
    def test_bold_checkpoint_headings_normalize(self):
        extractor = importlib.import_module("checkpoint_extract")
        text = "**Who's who**\n\nBody\n\n**Relationships**\n\nBody"
        normalized = extractor.normalize_section_headings(
            text, ("Who's who", "Relationships")
        )
        self.assertIn("### Who's who", normalized)
        self.assertIn("### Relationships", normalized)

    def test_checkpoint_heading_normalizes_smart_apostrophe(self):
        extractor = importlib.import_module("checkpoint_extract")
        normalized = extractor.normalize_section_headings(
            "### What I know that they don’t\n\nBody",
            ("What I know that they don't",),
        )
        self.assertIn("### What I know that they don't", normalized)

    def test_truncated_reader_reaction_is_rejected(self):
        grounded = importlib.import_module("cold_read_grounded")
        truncated = (
            "A substantial felt read. " * 20
            + "\n\n**Heat:** 3 — hot\n\n**Romance:** 2 — tender\n"
        )
        with self.assertRaisesRegex(RuntimeError, "missing structured fields"):
            grounded.validate_reaction(truncated)

    def test_complete_reader_reaction_is_accepted(self):
        grounded = importlib.import_module("cold_read_grounded")
        reaction = "A substantial felt read. " * 20
        for label in grounded.REQUIRED_REACTION_LABELS:
            reaction += f"\n\n**{label}:** complete"
        grounded.validate_reaction(reaction)

    def test_checkpoint_plan_uses_one_prior_volume_seed(self):
        bundle = importlib.import_module("checkpoint_bundle")
        self.assertEqual(bundle.checkpoint_plan(50), (None, 1))
        self.assertEqual(bundle.checkpoint_plan(60), (50, 51))

    def test_seeded_checkpoint_source_strips_persisted_header(self):
        bundle = importlib.import_module("checkpoint_bundle")
        source = bundle.build_seeded_source(
            "# Checkpoint\n\n*metadata*\n\n---\n\n### Story so far\nOld memory\n",
            50,
            51,
            60,
            "===== CHAPTER 51: Next =====\n\nNew prose\n",
        )
        self.assertIn("PRIOR CHECKPOINT THROUGH CHAPTER 50", source)
        self.assertIn("### Story so far\nOld memory", source)
        self.assertNotIn("*metadata*", source)
        self.assertIn("RAW CURRENT-VOLUME SPAN: CHAPTERS 51 THROUGH 60", source)

    def test_grounded_mint_args_require_frozen_seed_after_volume_one(self):
        grounded = importlib.import_module("cold_read_grounded")
        args = grounded.checkpoint_extract_args(
            "gpt-5.6-sol", "gpt-5.6-sol", 60
        )
        self.assertEqual(args[:6], ["--model", "gpt-5.6-sol", "--from", "51", "--to", "60"])
        self.assertIn("--reader-sequence", args)
        seed_index = args.index("--seed-checkpoint") + 1
        self.assertTrue(args[seed_index].endswith("/gpt-5.6-sol/checkpoints/ck-ch050.md"))

    def test_chronology_consumers_load_exact_active_panel(self):
        html = importlib.import_module("chronology_html")
        qa = importlib.import_module("checkpoint_qa")
        augment = importlib.import_module("chronology_augment")
        expected = {
            "claude-fable-5",
            "claude-opus-4-8",
            "gpt-5.6-sol",
            "gpt-5.5",
            "kimi-k3",
            "glm-5.3-flash",
            "qwen3.8-max-0902",
            "deepseek-v4-pro-0813",
        }
        self.assertEqual(html.PANEL_MODELS, expected)
        self.assertEqual(augment.PANEL_MODELS, expected)
        active, _sources = qa._panel_config()
        self.assertEqual(set(active), expected)
        self.assertIn("qwen3.8-max-0902", qa.discover_models(None, "read"))
        self.assertNotIn("claude-sonnet-5", qa.discover_models(None, "read"))
        checkpoint_models = qa.discover_models(None, "checkpoint")
        self.assertEqual(checkpoint_models.count("ensemble:core"), 1)
        self.assertNotIn("qwen3.8-max-0902", checkpoint_models)
        self.assertNotIn("deepseek-v4-pro-0813", checkpoint_models)

    def test_matcher_attempt_persists_raw_output_and_usage(self):
        ensemble = importlib.import_module("checkpoint_ensemble")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            with patch.object(ensemble, "paths_for", return_value={"root": root}):
                path = ensemble.persist_matcher_attempt(
                    "core",
                    50,
                    model="gpt-5.6-terra",
                    result={
                        "id": "response-1",
                        "usage": {"totalTokens": 321},
                        "output": "{broken json",
                    },
                )
            payload = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(payload["raw_output"], "{broken json")
        self.assertEqual(payload["usage"]["totalTokens"], 321)

    def test_prior_ledger_excludes_current_and_future_boundaries(self):
        ensemble = importlib.import_module("checkpoint_ensemble")
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            claims = root / "claims"
            claims.mkdir()
            for boundary in (40, 50, 60):
                (claims / f"ck-ch{boundary:03d}.json").write_text(
                    f'{{"boundary": {boundary}}}', encoding="utf-8"
                )
            with patch.object(ensemble, "paths_for", return_value={"root": root}):
                path, payload = ensemble.previous_ledger("core", 50)
        self.assertEqual(path.name, "ck-ch040.json")
        self.assertEqual(payload["boundary"], 40)
if __name__ == "__main__":
    unittest.main()
