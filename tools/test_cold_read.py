"""Focused unit tests for Codex subscription cold-reader authentication."""
from __future__ import annotations

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

    def test_temporal_merge_retires_state_and_carries_event(self):
        prior = {
            "boundary": 40,
            "claims": [
                {"id": "old-state", "type": "state", "superseded_at": None},
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
            prior_path.write_text("{}")
            with patch.object(self.ensemble, "REPO", Path(td)), patch.object(
                self.ensemble, "previous_ledger", return_value=(prior_path, prior)
            ):
                merged, lineage = self.ensemble.merge_temporal_ledger(
                    current, name="core", boundary=50
                )
        self.assertEqual({claim["id"] for claim in merged["claims"]}, {"new-state", "event"})
        self.assertEqual(merged["history"][0]["superseded_at"], 50)
        self.assertEqual(lineage["boundary"], 40)

class HarnessParsingTests(unittest.TestCase):
    def test_bold_checkpoint_headings_normalize(self):
        extractor = importlib.import_module("checkpoint_extract")
        text = "**Who's who**\n\nBody\n\n**Relationships**\n\nBody"
        normalized = extractor.normalize_section_headings(
            text, ("Who's who", "Relationships")
        )
        self.assertIn("### Who's who", normalized)
        self.assertIn("### Relationships", normalized)

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
        self.assertEqual(set(qa._active_panel_models()), expected)
        self.assertIn("qwen3.8-max-0902", qa.discover_models(None, "read"))
        self.assertNotIn("claude-sonnet-5", qa.discover_models(None, "read"))

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
