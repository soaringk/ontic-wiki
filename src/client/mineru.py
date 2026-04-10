from __future__ import annotations

import io
import json
import math
import os
import time
import zipfile
from pathlib import Path

import requests
from pypdf import PdfReader


class MineruParseError(RuntimeError):
    """Raised when MinerU Precision Extract parsing fails."""


class MineruPrecisionClient:
    def __init__(self) -> None:
        self.base_url = os.getenv("MINERU_BASE_URL", "https://mineru.net/api/v4").rstrip("/")
        self.api_token = os.getenv("MINERU_API_TOKEN", "").strip()
        self.model_version = os.getenv("MINERU_MODEL_VERSION", "vlm")
        self.language = os.getenv("MINERU_LANGUAGE", "ch")
        self.enable_table = os.getenv("MINERU_ENABLE_TABLE", "true").lower() == "true"
        self.enable_formula = os.getenv("MINERU_ENABLE_FORMULA", "true").lower() == "true"
        self.ocr_enable = os.getenv("MINERU_OCR_ENABLE", "auto").strip().lower() or "auto"
        self.timeout = int(os.getenv("MINERU_TIMEOUT", "900"))
        self.poll_interval = int(os.getenv("MINERU_POLL_INTERVAL", "5"))

    @property
    def headers(self) -> dict[str, str]:
        if not self.api_token:
            raise MineruParseError("MINERU_API_TOKEN is not set")
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    @staticmethod
    def _format_response_payload(response: requests.Response) -> str:
        try:
            body = response.json()
        except ValueError:
            text = response.text.strip()
            return text or "<empty body>"
        return json.dumps(body, ensure_ascii=False, sort_keys=True)

    def _raise_for_status_with_body(self, response: requests.Response, context: str) -> None:
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            payload = self._format_response_payload(response)
            raise MineruParseError(
                f"{context}: HTTP {response.status_code}, response={payload}"
            ) from exc

    def parse_pdf(self, file_path: Path, *, data_id: str) -> str:
        file_path = Path(file_path)
        use_ocr = self._resolve_ocr_mode(file_path)
        try:
            markdown = self._parse_pdf_once(file_path, data_id=data_id, is_ocr=use_ocr)
        except MineruParseError:
            if self.ocr_enable == "auto" and not use_ocr:
                return self._parse_pdf_once(file_path, data_id=data_id, is_ocr=True)
            raise

        if self.ocr_enable == "auto" and not use_ocr and self._looks_weak(markdown):
            return self._parse_pdf_once(file_path, data_id=data_id, is_ocr=True)
        return markdown

    def _parse_pdf_once(self, file_path: Path, *, data_id: str, is_ocr: bool) -> str:
        batch_id, upload_url = self._request_upload_url(file_path, data_id=data_id, is_ocr=is_ocr)
        self._upload_file(upload_url, file_path)
        full_zip_url = self._wait_for_result(batch_id, file_name=file_path.name, data_id=data_id)
        return self._download_full_markdown(full_zip_url)

    def _resolve_ocr_mode(self, file_path: Path) -> bool:
        if self.ocr_enable in {"true", "1", "yes", "on"}:
            return True
        if self.ocr_enable in {"false", "0", "no", "off"}:
            return False
        if self.ocr_enable != "auto":
            raise MineruParseError(f"Unsupported MINERU_OCR_ENABLE value: {self.ocr_enable}")
        return self._should_enable_ocr(file_path)

    def _should_enable_ocr(self, file_path: Path) -> bool:
        try:
            reader = PdfReader(str(file_path))
        except Exception:
            return False

        sampled_pages = self._sample_pages(reader.pages)
        if not sampled_pages:
            return False

        extracted_pages = 0
        extracted_chars = 0
        for page in sampled_pages:
            try:
                text = (page.extract_text() or "").strip()
            except Exception:
                text = ""
            if text:
                extracted_pages += 1
                extracted_chars += len(text)

        if extracted_pages == 0:
            return True
        average_chars = extracted_chars / len(sampled_pages)
        coverage = extracted_pages / len(sampled_pages)
        return coverage < 0.5 or average_chars < 80

    @staticmethod
    def _sample_pages(pages) -> list:
        total_pages = len(pages)
        sample_count = max(1, math.ceil(total_pages / 2))
        if sample_count >= total_pages:
            return list(pages)

        indices: list[int] = []
        for i in range(sample_count):
            index = min(total_pages - 1, math.floor(i * total_pages / sample_count))
            if not indices or index != indices[-1]:
                indices.append(index)
        return [pages[index] for index in indices]

    @staticmethod
    def _looks_weak(markdown: str) -> bool:
        stripped = markdown.strip()
        if not stripped:
            return True
        return len(stripped) < 200

    def _request_upload_url(self, file_path: Path, *, data_id: str, is_ocr: bool) -> tuple[str, str]:
        payload = {
            "enable_formula": self.enable_formula,
            "enable_table": self.enable_table,
            "language": self.language,
            "model_version": self.model_version,
            "files": [
                {
                    "name": file_path.name,
                    "is_ocr": is_ocr,
                    "data_id": data_id,
                }
            ],
        }
        response = requests.post(f"{self.base_url}/file-urls/batch", json=payload, headers=self.headers, timeout=30)
        self._raise_for_status_with_body(response, "MinerU upload-url request failed")
        body = response.json()
        if body.get("code") != 0:
            raise MineruParseError(
                f"MinerU upload-url request failed: response={json.dumps(body, ensure_ascii=False, sort_keys=True)}"
            )

        batch_id = body["data"]["batch_id"]
        file_urls = body["data"].get("file_urls") or body["data"].get("files") or []
        if not file_urls:
            raise MineruParseError(
                f"MinerU upload-url request succeeded without file_urls: response={json.dumps(body, ensure_ascii=False, sort_keys=True)}"
            )
        return batch_id, file_urls[0]

    def _upload_file(self, upload_url: str, file_path: Path) -> None:
        with file_path.open("rb") as handle:
            response = requests.put(upload_url, data=handle, timeout=300)
        if response.status_code not in {200, 201}:
            payload = self._format_response_payload(response)
            raise MineruParseError(
                f"MinerU file upload failed: HTTP {response.status_code}, response={payload}"
            )

    def _wait_for_result(self, batch_id: str, *, file_name: str, data_id: str) -> str:
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            response = requests.get(
                f"{self.base_url}/extract-results/batch/{batch_id}",
                headers=self.headers,
                timeout=30,
            )
            self._raise_for_status_with_body(response, "MinerU poll failed")
            body = response.json()
            if body.get("code") != 0:
                raise MineruParseError(
                    f"MinerU poll failed: response={json.dumps(body, ensure_ascii=False, sort_keys=True)}"
                )

            result = self._match_result(body["data"].get("extract_result", []), file_name=file_name, data_id=data_id)
            if result is None:
                time.sleep(self.poll_interval)
                continue

            state = result.get("state")
            if state == "done":
                full_zip_url = result.get("full_zip_url")
                if not full_zip_url:
                    raise MineruParseError(
                        f"MinerU result completed without full_zip_url: response={json.dumps(result, ensure_ascii=False, sort_keys=True)}"
                    )
                return full_zip_url
            if state == "failed":
                raise MineruParseError(
                    f"MinerU parse failed: response={json.dumps(result, ensure_ascii=False, sort_keys=True)}"
                )

            time.sleep(self.poll_interval)

        raise MineruParseError(f"MinerU parse timed out after {self.timeout}s")

    def _download_full_markdown(self, full_zip_url: str) -> str:
        response = requests.get(full_zip_url, timeout=120)
        self._raise_for_status_with_body(response, "MinerU result download failed")
        with zipfile.ZipFile(io.BytesIO(response.content)) as archive:
            full_md_name = next((name for name in archive.namelist() if name.endswith("/full.md")), None)
            if full_md_name is None:
                full_md_name = next((name for name in archive.namelist() if name.endswith("full.md")), None)
            if full_md_name is None:
                raise MineruParseError(
                    f"MinerU result zip does not contain full.md: entries={archive.namelist()}"
                )
            return archive.read(full_md_name).decode("utf-8", errors="ignore")

    @staticmethod
    def _match_result(extract_result: list[dict], *, file_name: str, data_id: str) -> dict | None:
        for item in extract_result:
            if item.get("data_id") == data_id:
                return item
        for item in extract_result:
            if item.get("file_name") == file_name:
                return item
        return None
