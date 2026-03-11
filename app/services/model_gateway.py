import json
from dataclasses import dataclass
from typing import Optional
from urllib import error as urllib_error
from urllib import request as urllib_request

from app.core.prompt_loader import PromptLoader
from app.core.settings import Settings

try:
    from litellm import completion
except Exception:  # pragma: no cover
    completion = None


@dataclass
class GenerationResult:
    intent: str
    confidence: float
    draft_reply: str
    provider_used: str
    model_used: str
    escalation_reason: Optional[str] = None


@dataclass
class TextGenerationResult:
    content: str
    provider_used: str
    model_used: str


class ModelGateway:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.prompt_loader = PromptLoader()
        self.model_timeout_seconds = 10.0
        self._resolved_local_model: Optional[str] = None

    def _heuristic_classification(self, subject: str, body: str) -> tuple[str, float]:
        combined = f"{subject}\n{body}".lower()
        intent = "general-inquiry"
        confidence = 0.68
        if any(word in combined for word in ("invoice", "payment", "quote", "proposal")):
            intent = "commercial-request"
            confidence = 0.78
        if any(word in combined for word in ("urgent", "asap", "today", "blocked")):
            intent = "urgent-request"
            confidence = 0.82
        return intent, confidence

    def _heuristic_fallback(self, subject: str, body: str) -> GenerationResult:
        intent, confidence = self._heuristic_classification(subject, body)

        draft = (
            "Thanks for your message. I reviewed your request and prepared a draft response. "
            "I will confirm next steps and timing shortly."
        )
        return GenerationResult(
            intent=intent,
            confidence=confidence,
            draft_reply=draft,
            provider_used="fallback-rule",
            model_used="rules-v1",
        )

    def _call_model(self, *, provider: str, model: str, prompt: str) -> Optional[GenerationResult]:
        if completion is None:
            return None

        kwargs = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "timeout": self.model_timeout_seconds,
            "request_timeout": self.model_timeout_seconds,
        }

        if provider == "local":
            kwargs["api_base"] = self.settings.ollama_base_url
        else:
            if self.settings.openrouter_api_key:
                kwargs["api_key"] = self.settings.openrouter_api_key

        try:
            response = completion(**kwargs)
            content = response.choices[0].message.content
            payload = json.loads(content)
            return GenerationResult(
                intent=str(payload["intent"]),
                confidence=float(payload["confidence"]),
                draft_reply=str(payload["draft_reply"]),
                provider_used=provider,
                model_used=model,
            )
        except Exception:
            return None

    def _ollama_request(self, *, path: str, payload: Optional[dict] = None) -> Optional[dict]:
        body = None
        headers = {}
        method = "GET"
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
            method = "POST"

        req = urllib_request.Request(
            f"{self.settings.ollama_base_url.rstrip('/')}{path}",
            data=body,
            headers=headers,
            method=method,
        )
        try:
            with urllib_request.urlopen(req, timeout=self.model_timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib_error.URLError, TimeoutError, json.JSONDecodeError, OSError):
            return None

    def _parse_json_object(self, content: str) -> Optional[dict]:
        try:
            parsed = json.loads(content)
            return parsed if isinstance(parsed, dict) else None
        except json.JSONDecodeError:
            start = content.find("{")
            end = content.rfind("}")
            if start >= 0 and end > start:
                try:
                    parsed = json.loads(content[start : end + 1])
                    return parsed if isinstance(parsed, dict) else None
                except json.JSONDecodeError:
                    return None
            return None

    def _list_local_ollama_models(self) -> list[str]:
        payload = self._ollama_request(path="/api/tags")
        if not payload:
            return []

        models: list[str] = []
        for item in payload.get("models", []):
            if item.get("remote_host"):
                continue
            name = str(item.get("name") or item.get("model") or "").strip()
            if name:
                models.append(name)
        return models

    def _resolve_local_model_name(self) -> Optional[str]:
        if self._resolved_local_model:
            return self._resolved_local_model

        available = self._list_local_ollama_models()
        if not available:
            return None

        if self.settings.local_model in available:
            self._resolved_local_model = self.settings.local_model
            return self._resolved_local_model

        preferred = [
            "qwen2.5:1.5b",
            "qwen2.5:7b-instruct-q4_K_M",
            "mistral:latest",
        ]
        for name in preferred:
            if name in available:
                self._resolved_local_model = name
                return self._resolved_local_model

        self._resolved_local_model = available[0]
        return self._resolved_local_model

    def _call_local_ollama_structured(self, *, prompt: str) -> Optional[GenerationResult]:
        model_name = self._resolve_local_model_name()
        if not model_name:
            return None

        payload = self._ollama_request(
            path="/api/generate",
            payload={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.2},
            },
        )
        if not payload:
            return None

        content = str(payload.get("response") or "").strip()
        parsed = self._parse_json_object(content)
        if not parsed:
            return None

        return GenerationResult(
            intent=str(parsed["intent"]),
            confidence=float(parsed["confidence"]),
            draft_reply=str(parsed["draft_reply"]),
            provider_used="local",
            model_used=f"ollama/{model_name}",
        )

    def _call_text_model(self, *, provider: str, model: str, prompt: str) -> Optional[TextGenerationResult]:
        if completion is None:
            return None

        kwargs = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "timeout": self.model_timeout_seconds,
            "request_timeout": self.model_timeout_seconds,
        }

        if provider == "local":
            kwargs["api_base"] = self.settings.ollama_base_url
        else:
            if self.settings.openrouter_api_key:
                kwargs["api_key"] = self.settings.openrouter_api_key

        try:
            response = completion(**kwargs)
            content = response.choices[0].message.content
            return TextGenerationResult(
                content=str(content),
                provider_used=provider,
                model_used=model,
            )
        except Exception:
            return None

    def _call_local_ollama_text(self, *, prompt: str) -> Optional[TextGenerationResult]:
        model_name = self._resolve_local_model_name()
        if not model_name:
            return None

        payload = self._ollama_request(
            path="/api/generate",
            payload={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.2},
            },
        )
        if not payload:
            return None

        content = str(payload.get("response") or "").strip()
        if not content:
            return None

        return TextGenerationResult(
            content=content,
            provider_used="local",
            model_used=f"ollama/{model_name}",
        )

    def draft_email(
        self,
        *,
        sender: str,
        subject: str,
        body: str,
        thread_context: Optional[str],
        risk_level: str,
    ) -> GenerationResult:
        prompt = self.prompt_loader.render(
            "email/email_operations_prompt.txt",
            sender=sender,
            subject=subject,
            body=body,
            thread_context=thread_context or "none",
        )
        draft_prompt = self.prompt_loader.render(
            "email/email_draft_prompt.txt",
            sender=sender,
            subject=subject,
            body=body,
            thread_context=thread_context or "none",
        )

        local_result = self._call_local_ollama_structured(prompt=prompt)
        if local_result is None:
            local_text = self._call_local_ollama_text(prompt=draft_prompt)
            if local_text is not None:
                intent, confidence = self._heuristic_classification(subject, body)
                local_result = GenerationResult(
                    intent=intent,
                    confidence=confidence,
                    draft_reply=local_text.content,
                    provider_used=local_text.provider_used,
                    model_used=local_text.model_used,
                )
        if local_result is None:
            return self._heuristic_fallback(subject, body)

        needs_cloud = (
            not self.settings.force_local_only
            and (
                local_result.confidence < self.settings.local_confidence_threshold
                or len(body) > self.settings.max_local_input_chars
                or risk_level == "high"
            )
        )

        if not needs_cloud:
            return local_result

        if not self.settings.openrouter_api_key:
            local_result.escalation_reason = "cloud_unconfigured_used_local"
            return local_result

        cloud_result = self._call_model(
            provider="cloud",
            model=f"openrouter/{self.settings.cloud_model}",
            prompt=prompt,
        )
        if cloud_result is None:
            local_result.escalation_reason = "cloud_unavailable_used_local"
            return local_result

        cloud_result.escalation_reason = "routed_to_cloud"
        return cloud_result

    def generate_text(self, *, prompt: str, fallback_content: str) -> TextGenerationResult:
        local_result = self._call_local_ollama_text(prompt=prompt)
        if local_result is not None:
            return local_result

        if not self.settings.force_local_only and self.settings.openrouter_api_key:
            cloud_result = self._call_text_model(
                provider="cloud",
                model=f"openrouter/{self.settings.cloud_model}",
                prompt=prompt,
            )
            if cloud_result is not None:
                return cloud_result

        return TextGenerationResult(
            content=fallback_content,
            provider_used="fallback-rule",
            model_used="rules-v1",
        )
