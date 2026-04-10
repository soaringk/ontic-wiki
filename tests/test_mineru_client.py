from __future__ import annotations

import io
import os
import sys
import unittest
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from client.mineru import MineruParseError, MineruPrecisionClient


class MineruPrecisionClientTests(unittest.TestCase):
    def test_requires_token(self) -> None:
        with patch.dict(os.environ, {"MINERU_API_TOKEN": ""}, clear=False):
            client = MineruPrecisionClient()
            with self.assertRaises(MineruParseError):
                _ = client.headers

    def test_parse_pdf_uses_upload_poll_and_zip_download(self) -> None:
        with TemporaryDirectory() as temp_dir:
            pdf_path = Path(temp_dir) / "paper.pdf"
            pdf_path.write_bytes(b"%PDF-1.4 fake")

            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, "w") as archive:
                archive.writestr("result/full.md", "# Parsed\n\ncontent")
            zip_bytes = zip_buffer.getvalue()

            post_response = Mock()
            post_response.json.return_value = {
                "code": 0,
                "data": {
                    "batch_id": "batch-1",
                    "file_urls": ["https://upload.example/file"],
                },
            }
            post_response.raise_for_status.return_value = None

            put_response = Mock(status_code=200)

            get_poll_response = Mock()
            get_poll_response.json.return_value = {
                "code": 0,
                "data": {
                    "extract_result": [
                        {
                            "data_id": "paper",
                            "file_name": "paper.pdf",
                            "state": "done",
                            "full_zip_url": "https://cdn.example/result.zip",
                        }
                    ]
                },
            }
            get_poll_response.raise_for_status.return_value = None

            get_zip_response = Mock()
            get_zip_response.content = zip_bytes
            get_zip_response.raise_for_status.return_value = None

            with patch.dict(
                os.environ,
                {
                    "MINERU_API_TOKEN": "token",
                    "MINERU_BASE_URL": "https://mineru.example/api/v4",
                },
                clear=False,
            ), patch("client.mineru.requests.post", return_value=post_response) as post_mock, patch(
                "client.mineru.requests.put",
                return_value=put_response,
            ) as put_mock, patch(
                "client.mineru.requests.get",
                side_effect=[get_poll_response, get_zip_response],
            ) as get_mock, patch.object(MineruPrecisionClient, "_should_enable_ocr", return_value=False), patch.object(
                MineruPrecisionClient,
                "_looks_weak",
                return_value=False,
            ):
                client = MineruPrecisionClient()
                markdown = client.parse_pdf(pdf_path, data_id="paper")

            self.assertEqual(markdown, "# Parsed\n\ncontent")
            post_mock.assert_called_once()
            put_mock.assert_called_once()
            self.assertEqual(get_mock.call_count, 2)

    def test_auto_policy_enables_ocr_for_scanned_like_pdf(self) -> None:
        with patch.dict(os.environ, {"MINERU_OCR_ENABLE": "auto", "MINERU_API_TOKEN": "token"}, clear=False):
            client = MineruPrecisionClient()
            with patch.object(client, "_should_enable_ocr", return_value=True):
                self.assertTrue(client._resolve_ocr_mode(Path("paper.pdf")))

    def test_auto_policy_retries_with_ocr_after_weak_non_ocr_output(self) -> None:
        with patch.dict(os.environ, {"MINERU_OCR_ENABLE": "auto", "MINERU_API_TOKEN": "token"}, clear=False):
            client = MineruPrecisionClient()
            with patch.object(client, "_should_enable_ocr", return_value=False), patch.object(
                client,
                "_parse_pdf_once",
                side_effect=["short", "# Strong markdown output\n\nEnough content here."],
            ) as parse_mock:
                result = client.parse_pdf(Path("paper.pdf"), data_id="paper")

        self.assertIn("Strong markdown", result)
        self.assertEqual(parse_mock.call_args_list[0].kwargs["is_ocr"], False)
        self.assertEqual(parse_mock.call_args_list[1].kwargs["is_ocr"], True)

    def test_auto_policy_retries_with_ocr_after_non_ocr_failure(self) -> None:
        with patch.dict(os.environ, {"MINERU_OCR_ENABLE": "auto", "MINERU_API_TOKEN": "token"}, clear=False):
            client = MineruPrecisionClient()
            with patch.object(client, "_should_enable_ocr", return_value=False), patch.object(
                client,
                "_parse_pdf_once",
                side_effect=[MineruParseError("failed"), "# OCR recovered markdown"],
            ) as parse_mock:
                result = client.parse_pdf(Path("paper.pdf"), data_id="paper")

        self.assertIn("OCR recovered", result)
        self.assertEqual(parse_mock.call_args_list[0].kwargs["is_ocr"], False)
        self.assertEqual(parse_mock.call_args_list[1].kwargs["is_ocr"], True)

    def test_sample_pages_uses_half_the_document_with_minimum_one(self) -> None:
        pages = list(range(7))
        sampled = MineruPrecisionClient._sample_pages(pages)
        self.assertEqual(sampled, [0, 1, 3, 5])

        short_pages = [0]
        self.assertEqual(MineruPrecisionClient._sample_pages(short_pages), [0])


if __name__ == "__main__":
    unittest.main()
