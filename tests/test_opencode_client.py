from __future__ import annotations

import base64
import os
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from client.opencode import OpenCodeClient


class OpenCodeClientAuthTests(unittest.TestCase):
    def test_blank_password_skips_authorization_header(self) -> None:
        env = {
            "OPENCODE_BASE_URL": "http://localhost:4096",
            "OPENCODE_USERNAME": "opencode",
            "OPENCODE_PASSWORD": "",
            "OPENCODE_DIRECTORY": "/tmp/wiki",
        }
        with patch.dict(os.environ, env, clear=False):
            client = OpenCodeClient()
        self.assertEqual(client.headers, {})

    def test_password_adds_basic_auth_header(self) -> None:
        env = {
            "OPENCODE_BASE_URL": "http://localhost:4096",
            "OPENCODE_USERNAME": "alice",
            "OPENCODE_PASSWORD": "secret",
            "OPENCODE_DIRECTORY": "/tmp/wiki",
        }
        with patch.dict(os.environ, env, clear=False):
            client = OpenCodeClient()
        expected = base64.b64encode(b"alice:secret").decode("utf-8")
        self.assertEqual(client.headers, {"Authorization": f"Basic {expected}"})

    def test_send_message_uses_timeout_from_environment(self) -> None:
        env = {
            "OPENCODE_BASE_URL": "http://localhost:4096",
            "OPENCODE_USERNAME": "alice",
            "OPENCODE_PASSWORD": "",
            "OPENCODE_DIRECTORY": "/tmp/wiki",
            "OPENCODE_MESSAGE_TIMEOUT": "9999",
        }
        with patch.dict(os.environ, env, clear=False):
            client = OpenCodeClient()
            with patch.object(client, "_request") as request_mock:
                request_mock.return_value.raise_for_status.return_value = None
                request_mock.return_value.text = "{}"
                request_mock.return_value.json.return_value = {"ok": True}
                client.send_message("session-1", "hello", model_id="openai/gpt-5.4")

        self.assertEqual(request_mock.call_args.kwargs["timeout"], 9999)

    def test_wait_for_session_complete_returns_false_on_error_status(self) -> None:
        env = {
            "OPENCODE_BASE_URL": "http://localhost:4096",
            "OPENCODE_USERNAME": "opencode",
            "OPENCODE_PASSWORD": "",
            "OPENCODE_DIRECTORY": "/tmp/wiki",
        }
        with patch.dict(os.environ, env, clear=False):
            client = OpenCodeClient()
            with patch.object(client, "get_session_status", return_value={"type": "error"}):
                self.assertFalse(client.wait_for_session_complete("session-1", poll_interval=0, max_wait=1))

    def test_wait_for_session_complete_returns_true_on_completed_status(self) -> None:
        env = {
            "OPENCODE_BASE_URL": "http://localhost:4096",
            "OPENCODE_USERNAME": "opencode",
            "OPENCODE_PASSWORD": "",
            "OPENCODE_DIRECTORY": "/tmp/wiki",
        }
        with patch.dict(os.environ, env, clear=False):
            client = OpenCodeClient()
            with patch.object(client, "get_session_status", return_value={"type": "completed"}):
                self.assertTrue(client.wait_for_session_complete("session-1", poll_interval=0, max_wait=1))

    def test_wait_for_session_complete_returns_true_for_idle_session_metadata_without_runtime_fields(self) -> None:
        env = {
            "OPENCODE_BASE_URL": "http://localhost:4096",
            "OPENCODE_USERNAME": "opencode",
            "OPENCODE_PASSWORD": "",
            "OPENCODE_DIRECTORY": "/tmp/wiki",
        }
        with patch.dict(os.environ, env, clear=False):
            client = OpenCodeClient()
            with patch.object(client, "get_session_status", return_value=None), patch.object(
                client,
                "get_session_info",
                return_value={"id": "session-1", "title": "Ontic Wiki Reindex"},
            ):
                self.assertTrue(client.wait_for_session_complete("session-1", poll_interval=0, max_wait=1))

    def test_wait_for_session_complete_keeps_waiting_on_retry(self) -> None:
        env = {
            "OPENCODE_BASE_URL": "http://localhost:4096",
            "OPENCODE_USERNAME": "opencode",
            "OPENCODE_PASSWORD": "",
            "OPENCODE_DIRECTORY": "/tmp/wiki",
        }
        with patch.dict(os.environ, env, clear=False):
            client = OpenCodeClient()
            with patch.object(
                client,
                "get_session_status",
                side_effect=[{"type": "retry"}, None],
            ), patch.object(
                client,
                "get_session_info",
                return_value={"id": "session-1", "title": "Ontic Wiki Reindex"},
            ):
                self.assertTrue(client.wait_for_session_complete("session-1", poll_interval=0, max_wait=1))


if __name__ == "__main__":
    unittest.main()
