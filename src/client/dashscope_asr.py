from __future__ import annotations

import json
import time
from dataclasses import dataclass
from typing import Any

import requests


class DashScopeTranscriptionError(RuntimeError):
    """Raised when DashScope Filetrans transcription fails."""


@dataclass(frozen=True)
class DashScopeFiletransConfig:
    api_key: str
    api_base: str
    model: str
    timeout_seconds: int
    poll_interval_seconds: int = 5


def is_fun_asr_model(model: str) -> bool:
    return model.startswith("fun-asr")


def build_filetrans_payload(*, model: str, file_url: str) -> dict[str, Any]:
    if is_fun_asr_model(model):
        return {
            "model": model,
            "input": {"file_urls": [file_url]},
            "parameters": {
                "channel_id": [0],
                "diarization_enabled": True,
            },
        }

    return {
        "model": model,
        "input": {"file_url": file_url},
        "parameters": {
            "channel_id": [0],
            "language": "",
            "enable_itn": False,
            "enable_words": False,
        },
    }


def extract_transcript_text(result: Any, model: str) -> str:
    if not isinstance(result, dict):
        return ""

    transcripts = result.get("transcripts")
    if transcripts is None:
        output = result.get("output")
        if isinstance(output, dict):
            output_result = output.get("result")
            if isinstance(output_result, dict):
                transcripts = output_result.get("transcripts")
    if not isinstance(transcripts, list):
        transcripts = []

    sentence_texts: list[str] = []
    fallback_texts: list[str] = []
    has_speaker_info = False

    for transcript in transcripts:
        if not isinstance(transcript, dict):
            continue
        sentences = transcript.get("sentences")
        if isinstance(sentences, list):
            normalized_sentences: list[dict[str, Any]] = []
            for sentence in sentences:
                if not isinstance(sentence, dict):
                    continue
                text = str(sentence.get("text") or "").strip()
                if not text:
                    continue
                normalized = {"text": text}
                if "begin_time" in sentence:
                    normalized["begin_time"] = sentence["begin_time"]
                if "end_time" in sentence:
                    normalized["end_time"] = sentence["end_time"]
                if "speaker_id" in sentence:
                    normalized["speaker_id"] = sentence["speaker_id"]
                    has_speaker_info = True
                normalized_sentences.append(normalized)

            if has_speaker_info and any("begin_time" in sentence for sentence in normalized_sentences):
                normalized_sentences.sort(key=lambda sentence: int(sentence.get("begin_time") or 0))

            if has_speaker_info and is_fun_asr_model(model):
                for sentence in normalized_sentences:
                    timestamp = ""
                    if "begin_time" in sentence:
                        timestamp = f"[{format_timestamp(int(sentence['begin_time']))}] "
                    speaker = ""
                    if "speaker_id" in sentence:
                        speaker = f"Speaker {int(sentence['speaker_id']) + 1}: "
                    sentence_texts.append(f"{timestamp}{speaker}{sentence['text']}")
            else:
                sentence_texts.extend(str(sentence["text"]) for sentence in normalized_sentences)

        text = str(transcript.get("text") or "").strip()
        if text:
            fallback_texts.append(text)

    return "\n\n".join(sentence_texts or fallback_texts).strip()


def format_timestamp(milliseconds: int) -> str:
    seconds = milliseconds // 1000
    minutes = seconds // 60
    secs = seconds % 60
    return f"{minutes:02d}:{secs:02d}"


class DashScopeFiletransClient:
    def __init__(self, config: DashScopeFiletransConfig) -> None:
        self.config = config

    def transcribe(self, file_url: str) -> Any:
        task_id = self.submit(file_url)
        transcription_url = self.poll(task_id)
        return self.download_result(transcription_url)

    def submit(self, file_url: str) -> str:
        if not self.config.api_key:
            raise DashScopeTranscriptionError("DASHSCOPE_API_KEY is required for video transcription")
        response = requests.post(
            f"{self.config.api_base.rstrip('/')}/services/audio/asr/transcription",
            headers=self.headers,
            json=build_filetrans_payload(model=self.config.model, file_url=file_url),
            timeout=30,
        )
        payload = self._json_response(response, "DashScope Filetrans submit")
        task_id = task_id_from_submit_response(payload)
        if not task_id:
            raise DashScopeTranscriptionError(
                f"DashScope Filetrans submit returned no task id: {json.dumps(payload, ensure_ascii=False)[:1000]}"
            )
        return task_id

    def poll(self, task_id: str) -> str:
        deadline = time.time() + self.config.timeout_seconds
        while time.time() < deadline:
            response = requests.get(
                f"{self.config.api_base.rstrip('/')}/tasks/{task_id}",
                headers=self.headers,
                timeout=30,
            )
            payload = self._json_response(response, "DashScope Filetrans poll")
            status = task_status(payload)
            if status == "SUCCEEDED":
                transcription_url = transcription_url_from_task(payload, self.config.model)
                if not transcription_url:
                    raise DashScopeTranscriptionError(f"DashScope task {task_id} succeeded without transcription_url")
                return transcription_url
            if status in {"FAILED", "CANCELED"}:
                raise DashScopeTranscriptionError(
                    f"DashScope task {task_id} ended with status {status}: {json.dumps(payload, ensure_ascii=False)[:1000]}"
                )
            time.sleep(self.config.poll_interval_seconds)
        raise DashScopeTranscriptionError(f"DashScope task {task_id} timed out after {self.config.timeout_seconds}s")

    def download_result(self, transcription_url: str) -> Any:
        response = requests.get(transcription_url, timeout=120)
        return self._json_response(response, "DashScope transcription result download")

    @property
    def headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json",
            "X-DashScope-Async": "enable",
        }

    @staticmethod
    def _json_response(response: requests.Response, context: str) -> Any:
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise DashScopeTranscriptionError(f"{context} failed: HTTP {response.status_code}, response={response.text[:1000]}") from exc
        try:
            return response.json()
        except ValueError as exc:
            raise DashScopeTranscriptionError(f"{context} returned invalid JSON: {response.text[:1000]}") from exc


def task_id_from_submit_response(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    output = payload.get("output")
    if isinstance(output, dict) and output.get("task_id"):
        return str(output["task_id"])
    return str(payload.get("task_id") or "")


def task_status(payload: Any) -> str:
    if not isinstance(payload, dict):
        return ""
    output = payload.get("output")
    if isinstance(output, dict) and output.get("task_status"):
        return str(output["task_status"])
    return str(payload.get("task_status") or "")


def transcription_url_from_task(payload: Any, model: str) -> str:
    if not isinstance(payload, dict):
        return ""
    output = payload.get("output")
    if not isinstance(output, dict):
        return ""
    if is_fun_asr_model(model):
        results = output.get("results")
        if isinstance(results, list) and results:
            first = results[0]
            if isinstance(first, dict):
                return str(first.get("transcription_url") or "")
        return ""
    result = output.get("result")
    if isinstance(result, dict):
        return str(result.get("transcription_url") or "")
    return ""

