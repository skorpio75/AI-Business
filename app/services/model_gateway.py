import json
from dataclasses import dataclass
from typing import Optional

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


class ModelGateway:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.prompt_loader = PromptLoader()

    def _heuristic_fallback(self, subject: str, body: str) -> GenerationResult:
        combined = f"{subject}\n{body}".lower()
        intent = "general-inquiry"
        confidence = 0.68
        if any(word in combined for word in ("invoice", "payment", "quote", "proposal")):
            intent = "commercial-request"
            confidence = 0.78
        if any(word in combined for word in ("urgent", "asap", "today", "blocked")):
            intent = "urgent-request"
            confidence = 0.82

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

        local_result = self._call_model(
            provider="local",
            model=f"ollama/{self.settings.local_model}",
            prompt=prompt,
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
