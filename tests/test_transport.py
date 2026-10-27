import json
import os
import threading
import time
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from unittest.mock import patch

from azbench.cli import verify
from azbench.core import request, run_target, validate_config


class TransportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.received = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                payload = json.loads(
                    self.rfile.read(int(self.headers["Content-Length"]))
                )
                cls.received.append((self.path, payload, self.headers.get("api-key")))
                self.send_response(200)
                self.send_header("Content-Type", "text/event-stream")
                self.end_headers()
                for data in [
                    {"type": "response.output_text.delta", "delta": "hello"},
                    {"type": "response.output_text.delta", "delta": " world"},
                    {
                        "type": "response.completed",
                        "response": {
                            "status": "completed",
                            "model": "actual-version",
                            "usage": {
                                "input_tokens": 512,
                                "output_tokens": 10,
                                "input_tokens_details": {"cached_tokens": 0},
                            },
                        },
                    },
                ]:
                    self.wfile.write(("data: " + json.dumps(data) + "\n\n").encode())
                    self.wfile.flush()
                    time.sleep(0.005)

            def log_message(self, *a):
                pass

        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def target(self):
        return dict(
            endpoint=f"http://127.0.0.1:{self.server.server_port}",
            deployment="test",
            auth="api_key",
            api_key_env="BENCH_TEST_KEY",
        )

    def test_responses_endpoint_and_store_false(self):
        b = validate_config({"benchmark": {"input_tokens": 512}})
        r = request(self.target(), b, "test-secret", 0)
        self.assertTrue(r["ok"])
        path, body, key = self.received[-1]
        self.assertEqual(path, "/openai/v1/responses")
        self.assertFalse(body["store"])
        self.assertNotIn("messages", body)
        self.assertEqual(key, "test-secret")
        self.assertEqual(r["actual_model"], "actual-version")
        self.assertNotIn("hello", json.dumps(r))

    def test_concurrency_mode_obeys_request_cap_and_excludes_warmup(self):
        b = validate_config(
            {
                "benchmark": {
                    "duration_s": 1,
                    "input_tokens": 512,
                    "max_requests": 3,
                    "warmup_requests": 1,
                    "load_mode": "concurrency",
                    "concurrency": 2,
                }
            }
        )
        records = []
        with patch.dict(os.environ, {"BENCH_TEST_KEY": "secret"}):
            result = run_target(self.target(), b, records.append)
        self.assertEqual(result["requests"], 3)
        self.assertEqual(result["successes"], 3)
        self.assertEqual(len([x for x in records if x.get("warmup")]), 1)

    def test_ptu_mismatch_is_rejected(self):
        target = dict(
            subscription="s", resource_group="g", account="a", deployment="d", ptus=30
        )
        with patch(
            "azbench.cli.az",
            return_value={
                "sku": {"name": "DataZoneProvisionedManaged", "capacity": 15},
                "properties": {"model": {"name": "test", "version": "1"}},
            },
        ):
            with self.assertRaisesRegex(ValueError, "PTUs"):
                verify(target)


if __name__ == "__main__":
    unittest.main()
