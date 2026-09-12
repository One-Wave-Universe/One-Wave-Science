#!/usr/bin/env python3

import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest import mock

import gateway
import mudl


class GatewayTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.paths = mock.patch.multiple(
            mudl,
            QUEUE=root,
            PENDING=root / "pending",
            PROCESSING=root / "processing",
            RESULTS=root / "results",
            DONE=root / "done",
        )
        self.paths.start()
        mudl.ensure_dirs()
        self.server = gateway.GatewayServer(("127.0.0.1", 0), ["test-token"])
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.paths.stop()
        self.temp.cleanup()

    def request(self, path, *, method="GET", body=None, token="test-token"):
        data = json.dumps(body).encode() if body is not None else None
        headers = {"Authorization": f"Bearer {token}"}
        request = Request(self.base + path, data=data, headers=headers, method=method)
        with urlopen(request) as response:
            return response.status, json.loads(response.read())

    def test_requires_authentication(self):
        with self.assertRaises(HTTPError) as caught:
            self.request("/v1/health", token="wrong")
        self.assertEqual(caught.exception.code, 401)

    def test_enqueues_and_returns_named_action(self):
        status, queued = self.request("/v1/jobs", method="POST", body={"action": "health"})
        self.assertEqual(status, 202)
        request_path = mudl.PENDING / f'{queued["id"]}.json'
        claimed = mudl.PROCESSING / request_path.name
        request_path.replace(claimed)
        mudl.execute(claimed)
        status, result = self.request(f'/v1/jobs/{queued["id"]}')
        self.assertEqual(status, 200)
        self.assertEqual(result["action"], "health")
        self.assertEqual(result["exit_code"], 0)

    def test_rejects_raw_command_payload(self):
        with self.assertRaises(HTTPError) as caught:
            self.request("/v1/jobs", method="POST", body={"action": "health", "command": "id"})
        self.assertEqual(caught.exception.code, 400)


if __name__ == "__main__":
    unittest.main()

