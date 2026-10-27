import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from azbench.cli import combine_reports
from azbench.core import (
    consume_stream,
    make_prompt,
    percentile,
    summarize,
    validate_config,
)


class MetricsTests(unittest.TestCase):
    def test_combine_prefers_measured_row_without_selecting_fastest_region(self):
        with tempfile.TemporaryDirectory() as tmp:
            a = Path(tmp) / "a.json"
            b = Path(tmp) / "b.json"
            a.write_text(
                json.dumps(
                    [
                        {
                            "model": "test",
                            "deployment_type": "PTU Regional",
                            "status": "unsupported_in_region",
                            "region": "a",
                        }
                    ]
                )
            )
            b.write_text(
                json.dumps(
                    [
                        {
                            "model": "test",
                            "deployment_type": "PTU Regional",
                            "status": "measured",
                            "region": "b",
                            "e2e_avg": 2,
                        }
                    ]
                )
            )
            rows = combine_reports([str(a), str(b)])
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["region"], "b")

    def test_combine_classifies_policy_rejection(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "policy.json"
            path.write_text(
                json.dumps(
                    [
                        {
                            "model": "test",
                            "deployment_type": "PTU Regional",
                            "status": "execution_failed",
                            "error_detail": "RequestDisallowedByPolicy: denied",
                        }
                    ]
                )
            )
            self.assertEqual(combine_reports([path])[0]["status"], "blocked_by_policy")

    def test_nearest_rank_p95_and_empty(self):
        self.assertEqual(percentile(list(range(1, 21)), 0.95), 19)
        self.assertIsNone(percentile([], 0.95))

    def test_failures_are_counted_but_not_latency_samples(self):
        rows = [
            dict(
                ok=True,
                ttft_s=1.0,
                e2e_s=3.0,
                tbt_s=0.02,
                usage={
                    "prompt_tokens": 100,
                    "completion_tokens": 101,
                    "prompt_tokens_details": {
                        "cached_tokens": 20,
                        "cache_write_tokens": 60,
                    },
                },
            ),
            dict(ok=False, error="timeout"),
        ]
        s = summarize(rows)
        self.assertEqual((s["requests"], s["successes"], s["failures"]), (2, 1, 1))
        self.assertEqual(s["ttft_avg"], 1.0)
        self.assertEqual(s["read_cache_pct"], 20.0)
        self.assertEqual(s["write_cache_pct"], 60.0)

    def test_unknown_cache_writes_are_not_reported_as_zero(self):
        s = summarize(
            [
                dict(
                    ok=True,
                    ttft_s=1,
                    e2e_s=2,
                    tbt_s=0.1,
                    usage={
                        "prompt_tokens": 100,
                        "completion_tokens": 10,
                        "prompt_tokens_details": {"cached_tokens": 0},
                    },
                )
            ]
        )
        self.assertIsNone(s["write_cache_pct"])
        self.assertEqual(s["read_cache_pct"], 0.0)

    def test_weighted_cache_percentages(self):
        rows = [
            dict(
                ok=True,
                ttft_s=1,
                e2e_s=2,
                tbt_s=0.1,
                usage={
                    "prompt_tokens": n,
                    "prompt_tokens_details": {
                        "cached_tokens": c,
                        "cache_write_tokens": 0,
                    },
                },
            )
            for n, c in [(100, 100), (900, 0)]
        ]
        self.assertEqual(summarize(rows)["read_cache_pct"], 10.0)

    def test_all_failures_have_no_fake_latency(self):
        s = summarize([{"ok": False}])
        self.assertIsNone(s["e2e_95th"])
        self.assertEqual(s["failures"], 1)


class StreamTests(unittest.TestCase):
    def stream(self, objects, done=True):
        data = "".join("data: " + json.dumps(x) + "\n\n" for x in objects)
        if done:
            data += "data: [DONE]\n\n"
        return io.BytesIO(data.encode())

    def test_usage_after_finish_and_chunk_timing(self):
        objects = [
            {"type": "response.created"},
            {"type": "response.output_text.delta", "delta": "hello"},
            {"type": "response.output_text.delta", "delta": " world"},
            {
                "type": "response.completed",
                "response": {
                    "status": "completed",
                    "model": "test",
                    "usage": {"input_tokens": 10, "output_tokens": 3},
                },
            },
        ]
        with patch("azbench.core.time.perf_counter", side_effect=[11, 13, 14]):
            r = consume_stream(self.stream(objects), 10)
        self.assertEqual(r["ttft_s"], 1)
        self.assertEqual(r["tbt_s"], 1)
        self.assertEqual(r["e2e_s"], 4)
        self.assertEqual(r["usage"]["completion_tokens"], 3)

    def test_truncated_stream_is_failure(self):
        with self.assertRaises(ValueError):
            consume_stream(
                self.stream(
                    [{"type": "response.output_text.delta", "delta": "partial"}], False
                ),
                0,
            )

    def test_stream_error_is_failure(self):
        with self.assertRaises(ValueError):
            consume_stream(
                self.stream(
                    [{"type": "error", "error": {"message": "provider failed"}}]
                ),
                0,
            )


class ConfigTests(unittest.TestCase):
    def test_reject_invalid_load(self):
        for key in [
            "duration_s",
            "concurrency",
            "input_tokens",
            "output_tokens",
            "timeout_s",
        ]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_config({"benchmark": {key: 0}})

    def test_reject_literal_key(self):
        with self.assertRaises(ValueError):
            validate_config({"targets": [{"api_key": "secret"}]})

    def test_input_target_preserves_instruction(self):
        import tiktoken

        enc = tiktoken.get_encoding("o200k_base")
        text = make_prompt(
            {"input_tokens": 512, "cache_mode": "cold", "tokenizer": "o200k_base"},
            "abcdef",
        )
        self.assertEqual(len(enc.encode(text)), 512)
        self.assertIn("Continue", text)

    def test_exact_input_with_long_random_prefix(self):
        import tiktoken

        enc = tiktoken.get_encoding("o200k_base")
        for size in [512, 3006]:
            text = make_prompt(
                {"input_tokens": size, "cache_mode": "cold", "tokenizer": "o200k_base"},
                "01234567-abcd-4567-89ab-0123456789ab",
            )
            self.assertEqual(len(enc.encode(text)), size)


if __name__ == "__main__":
    unittest.main()
