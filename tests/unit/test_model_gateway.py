# Copyright (c) Dario Pizzolante
import io
from unittest.mock import patch
from urllib import error as urllib_error

from app.services.model_gateway import ModelGateway
from tests.unit.base import UnitTestCase


class ModelGatewayTests(UnitTestCase):
    def test_ollama_request_marks_http_404_as_endpoint_mismatch(self) -> None:
        gateway = ModelGateway(settings=self.build_settings(ollama_base_url="http://ollama:11434"))
        http_error = urllib_error.HTTPError(
            url="http://ollama:11434/api/generate",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=io.BytesIO(b'{"error":"page not found"}'),
        )

        with patch("app.services.model_gateway.urllib_request.urlopen", side_effect=http_error):
            payload, diagnostic_code, diagnostic_detail = gateway._ollama_request(
                path="/api/generate",
                payload={"model": "qwen2.5:1.5b", "prompt": "test"},
            )

        self.assertIsNone(payload)
        self.assertEqual(diagnostic_code, "local_ollama_endpoint_not_found")
        self.assertIsNotNone(diagnostic_detail)
        self.assertIn("http://ollama:11434/api/generate", diagnostic_detail)
        self.assertIn("OLLAMA_BASE_URL points to a non-Ollama service", diagnostic_detail)

    def test_generate_text_surfaces_endpoint_mismatch_in_fallback_detail(self) -> None:
        gateway = ModelGateway(
            settings=self.build_settings(
                ollama_base_url="http://ollama:11434",
                openrouter_api_key=None,
                force_local_only=False,
            )
        )
        http_error = urllib_error.HTTPError(
            url="http://ollama:11434/api/generate",
            code=404,
            msg="Not Found",
            hdrs=None,
            fp=io.BytesIO(b'{"error":"page not found"}'),
        )

        gateway._resolve_local_model_name = lambda preferred_model=None: ("qwen2.5:1.5b", None, None)  # type: ignore[method-assign]

        with patch("app.services.model_gateway.urllib_request.urlopen", side_effect=http_error):
            result = gateway.generate_text(prompt="Explain strategy posture", fallback_content="fallback")

        self.assertEqual(result.provider_used, "fallback-rule")
        self.assertEqual(result.model_used, "rules-v1")
        self.assertEqual(result.llm_diagnostic_code, "multiple_llm_failures")
        self.assertIsNotNone(result.llm_diagnostic_detail)
        self.assertIn("HTTP 404", result.llm_diagnostic_detail)
        self.assertIn("OPENROUTER_API_KEY is not configured", result.llm_diagnostic_detail)

