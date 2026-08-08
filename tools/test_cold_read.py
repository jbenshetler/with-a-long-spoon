"""Focused unit tests for Codex subscription cold-reader authentication."""
from __future__ import annotations

import importlib
import sys
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



if __name__ == "__main__":
    unittest.main()
