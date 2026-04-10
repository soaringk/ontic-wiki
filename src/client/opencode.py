from __future__ import annotations

import base64
import os
import time
from pathlib import Path

import requests


ROOT_DIR = Path(__file__).resolve().parents[2]
ENV_PATH = ROOT_DIR / ".env"


def _load_env_file() -> None:
    if not ENV_PATH.exists():
        return

    for line in ENV_PATH.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip())


_load_env_file()


def message_timeout() -> int:
    return int(os.getenv("OPENCODE_MESSAGE_TIMEOUT", "3600"))


class OpenCodeClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("OPENCODE_BASE_URL", "http://localhost:4096").rstrip("/")
        self.username = os.getenv("OPENCODE_USERNAME", "opencode")
        self.password = os.getenv("OPENCODE_PASSWORD")
        directory_override = os.getenv("OPENCODE_DIRECTORY")
        self.directory = directory_override or str(ROOT_DIR)
        self.headers: dict[str, str] = {}
        if self.password:
            credentials = f"{self.username}:{self.password}"
            encoded = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
            self.headers["Authorization"] = f"Basic {encoded}"

    def _request(self, method: str, path: str, *, timeout: int, **kwargs):
        headers = dict(self.headers)
        headers.update(kwargs.pop("headers", {}))

        params = dict(kwargs.pop("params", {}))
        if self.directory:
            params.setdefault("directory", self.directory)

        return requests.request(
            method=method,
            url=f"{self.base_url}{path}",
            headers=headers,
            params=params,
            timeout=timeout,
            **kwargs,
        )

    @staticmethod
    def _is_running_status(status: str | None) -> bool:
        return (status or "").lower() in {"running", "busy", "queued", "retry"}

    @staticmethod
    def _is_success_status(status: str | None) -> bool:
        return (status or "").lower() in {"completed", "complete", "success", "succeeded", "done", "idle"}

    @staticmethod
    def _is_failure_status(status: str | None) -> bool:
        return (status or "").lower() in {"error", "failed", "failure", "cancelled", "canceled", "timeout", "timed_out"}

    def create_session(self, title: str) -> str:
        response = self._request("POST", "/session", timeout=10, json={"title": title})
        response.raise_for_status()
        return response.json()["id"]

    def send_message(
        self,
        session_id: str,
        message: str,
        *,
        model_id: str,
        provider_id: str | None = None,
        agent: str = "build",
    ):
        if provider_id is None:
            provider_id = "google"
            if "/" in model_id:
                provider_id, model_id = model_id.split("/", 1)
            elif model_id.startswith("anthropic"):
                provider_id = "anthropic"

        payload = {
            "parts": [{"type": "text", "text": message}],
            "model": {"modelID": model_id, "providerID": provider_id},
            "agent": agent,
        }
        response = self._request(
            "POST",
            f"/session/{session_id}/message",
            timeout=message_timeout(),
            json=payload,
        )
        response.raise_for_status()
        if not response.text.strip():
            return {"status": "accepted_empty_response", "session_id": session_id}
        return response.json()

    def get_session_status(self, session_id: str):
        response = self._request("GET", "/session/status", timeout=10)
        response.raise_for_status()
        return response.json().get(session_id)

    def get_session_info(self, session_id: str):
        response = self._request("GET", f"/session/{session_id}", timeout=10)
        response.raise_for_status()
        return response.json()

    def delete_session(self, session_id: str) -> None:
        response = self._request("DELETE", f"/session/{session_id}", timeout=10)
        response.raise_for_status()

    def wait_for_session_complete(
        self,
        session_id: str,
        *,
        poll_interval: int = 15,
        max_wait: int = 7200,
    ) -> bool:
        started = time.time()
        while time.time() - started < max_wait:
            status_payload = self.get_session_status(session_id)
            if status_payload is not None:
                status_type = status_payload.get("type", "")
                if self._is_running_status(status_type):
                    time.sleep(poll_interval)
                    continue
                if self._is_success_status(status_type):
                    return True
                if self._is_failure_status(status_type):
                    return False
                return False

            info = self.get_session_info(session_id)
            running = bool(info.get("running") or info.get("busy"))
            status = info.get("status")
            if running or self._is_running_status(status):
                time.sleep(poll_interval)
                continue
            # OpenCode drops idle sessions from /session/status, and /session/:id
            # may return plain session metadata without runtime fields.
            if status is None and "running" not in info and "busy" not in info:
                return True
            if self._is_success_status(status):
                return True
            if self._is_failure_status(status):
                return False
            return False
        return False
