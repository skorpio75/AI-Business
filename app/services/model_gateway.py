# Copyright (c) Dario Pizzolante
import json
import re
from dataclasses import dataclass
from typing import Optional
from urllib import error as urllib_error
from urllib import request as urllib_request

from app.core.prompt_loader import PromptLoader
from app.core.settings import Settings
from app.services.observability import LangfuseObservabilityService, NullObservabilityService

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
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None


@dataclass
class TextGenerationResult:
    content: str
    provider_used: str
    model_used: str
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None


@dataclass
class StructuredGenerationResult:
    content: dict
    provider_used: str
    model_used: str
    local_llm_invoked: bool = False
    cloud_llm_invoked: bool = False
    llm_diagnostic_code: Optional[str] = None
    llm_diagnostic_detail: Optional[str] = None


class ModelGateway:
    def __init__(
        self,
        settings: Settings,
        observability: LangfuseObservabilityService | NullObservabilityService | None = None,
    ):
        self.settings = settings
        self.prompt_loader = PromptLoader()
        self.model_timeout_seconds = settings.model_timeout_seconds
        self._resolved_local_model: Optional[str] = None
        self.observability = observability or LangfuseObservabilityService(settings=settings)

    def _heuristic_classification(self, subject: str, body: str) -> tuple[str, float]:
        combined = f"{subject}\n{body}".lower()
        intent = "general-inquiry"
        confidence = 0.84
        if any(word in combined for word in ("invoice", "payment", "quote", "proposal")):
            intent = "commercial-request"
            confidence = 0.86
        if any(word in combined for word in ("urgent", "asap", "today", "blocked")):
            intent = "urgent-request"
            confidence = 0.9
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

    def _clean_exception_message(self, exc: Exception) -> str:
        message = " ".join(str(exc).split())
        if message:
            return message[:240]
        return exc.__class__.__name__

    def _clean_response_excerpt(self, content: str) -> str:
        excerpt = " ".join(content.split())
        return excerpt[:180]

    def _normalize_email_draft_text(self, draft: str) -> str:
        text = draft.strip()
        lines = text.splitlines()
        if lines and lines[0].strip().lower().startswith("subject:"):
            lines = lines[1:]
            while lines and not lines[0].strip():
                lines = lines[1:]
        text = "\n".join(lines).strip()
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text

    def _draft_contains_unresolved_placeholders(self, draft: str) -> bool:
        if re.search(r"\[[^\]]+\]", draft):
            return True
        placeholder_markers = (
            "client's name",
            "your name",
            "specific issue",
            "related topic",
        )
        lowered = draft.lower()
        return any(marker in lowered for marker in placeholder_markers)

    def _join_focus_items(self, items: list[str]) -> str:
        if not items:
            return "the points you raised"
        if len(items) == 1:
            return items[0]
        if len(items) == 2:
            return f"{items[0]} and {items[1]}"
        return ", ".join(items[:-1]) + f", and {items[-1]}"

    def _extract_email_focus(self, *, subject: str, body: str, thread_context: str | None) -> str:
        combined = f"{subject}\n{body}".lower()
        focus_items: list[str] = []
        for keywords, focus in [
            (("checkpoint", "milestone"), "the next checkpoint"),
            (("blocked", "blocker", "issue"), "any current blockers"),
            (("plan", "timeline", "timing", "schedule"), "the updated plan and timing"),
            (("proposal", "quote", "pricing", "scope"), "scope and commercial details"),
            (("invoice", "payment"), "invoice and payment details"),
            (("review",), "the item currently under review"),
        ]:
            if any(keyword in combined for keyword in keywords) and focus not in focus_items:
                focus_items.append(focus)
        if thread_context and "dependenc" in thread_context.lower():
            focus_items.append("the dependency review noted in the thread")
        return self._join_focus_items(focus_items[:3])

    def _bounded_email_reply(
        self,
        *,
        intent: str,
        subject: str,
        body: str,
        thread_context: str | None,
    ) -> str:
        subject_ref = subject.strip() or "your message"
        focus = self._extract_email_focus(subject=subject, body=body, thread_context=thread_context)
        if intent == "urgent-request":
            return (
                f"Thanks for flagging this regarding {subject_ref}. "
                f"I am reviewing {focus} now, and I will confirm the immediate next step and timing shortly."
            )
        if intent == "commercial-request":
            return (
                f"Thanks for your note regarding {subject_ref}. "
                f"I am reviewing {focus} and will come back with a concrete response shortly."
            )
        return (
            f"Thanks for your note about {subject_ref}. "
            f"I am reviewing {focus} and will confirm the next step and timing shortly."
        )

    def _draft_appears_generic(self, draft: str) -> bool:
        lowered = draft.lower()
        generic_markers = (
            "reviewed your request",
            "prepared a draft response",
            "confirm next steps and timing shortly",
            "please let me know if you have any specific questions",
            "thank you for your email regarding",
        )
        return any(marker in lowered for marker in generic_markers)

    def _apply_email_draft_guardrails(
        self,
        *,
        result: GenerationResult,
        subject: str,
        body: str,
        thread_context: str | None,
    ) -> GenerationResult:
        normalized_draft = self._normalize_email_draft_text(result.draft_reply)
        if self._draft_contains_unresolved_placeholders(normalized_draft):
            return GenerationResult(
                intent=result.intent,
                confidence=result.confidence,
                draft_reply=self._bounded_email_reply(
                    intent=result.intent,
                    subject=subject,
                    body=body,
                    thread_context=thread_context,
                ),
                provider_used="fallback-rule",
                model_used="rules-v2-email-guardrail",
                escalation_reason=result.escalation_reason,
                local_llm_invoked=result.local_llm_invoked,
                cloud_llm_invoked=result.cloud_llm_invoked,
                llm_diagnostic_code=self._select_diagnostic_code(
                    result.llm_diagnostic_code,
                    "email_draft_placeholder_detected",
                ),
                llm_diagnostic_detail=self._join_diagnostic_details(
                    result.llm_diagnostic_detail,
                    "Generated draft contained unresolved placeholders or template markers, so a bounded rule-based draft was substituted.",
                ),
            )
        if normalized_draft != result.draft_reply:
            result.draft_reply = normalized_draft
        return result

    def _select_diagnostic_code(self, *codes: Optional[str]) -> Optional[str]:
        unique_codes = []
        for code in codes:
            if code and code not in unique_codes:
                unique_codes.append(code)
        if not unique_codes:
            return None
        if len(unique_codes) == 1:
            return unique_codes[0]
        return "multiple_llm_failures"

    def _join_diagnostic_details(self, *details: Optional[str]) -> Optional[str]:
        unique_details = []
        for detail in details:
            if detail and detail not in unique_details:
                unique_details.append(detail)
        if not unique_details:
            return None
        return " ".join(unique_details)

    def _result_metadata(self, result: GenerationResult | TextGenerationResult | StructuredGenerationResult) -> dict:
        metadata = {
            "provider_used": result.provider_used,
            "model_used": result.model_used,
            "local_llm_invoked": result.local_llm_invoked,
            "cloud_llm_invoked": result.cloud_llm_invoked,
            "llm_diagnostic_code": result.llm_diagnostic_code,
            "llm_diagnostic_detail": result.llm_diagnostic_detail,
        }
        if isinstance(result, GenerationResult):
            metadata["escalation_reason"] = result.escalation_reason
            metadata["confidence"] = result.confidence
            return metadata
        return metadata

    def _call_model(
        self, *, provider: str, model: str, prompt: str
    ) -> tuple[Optional[GenerationResult], bool, Optional[str], Optional[str]]:
        with self.observability.start_generation(
            name="model-gateway.provider-structured",
            input={"prompt": prompt},
            metadata={"provider": provider, "operation": "structured-email"},
            model=model,
            model_parameters={"temperature": 0.2, "timeout_seconds": self.model_timeout_seconds},
        ) as observation:
            if completion is None:
                diagnostic_code = "litellm_unavailable"
                diagnostic_detail = (
                    "LiteLLM is not available in this environment, so provider-backed model calls could not run."
                )
                observation.update(
                    level="ERROR",
                    status_message=diagnostic_code,
                    metadata={"diagnostic_code": diagnostic_code, "diagnostic_detail": diagnostic_detail},
                )
                return (
                    None,
                    False,
                    diagnostic_code,
                    diagnostic_detail,
                )

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
                result = GenerationResult(
                    intent=str(payload["intent"]),
                    confidence=float(payload["confidence"]),
                    draft_reply=str(payload["draft_reply"]),
                    provider_used=provider,
                    model_used=model,
                    local_llm_invoked=provider == "local",
                    cloud_llm_invoked=provider == "cloud",
                )
                observation.update(
                    output={
                        "intent": result.intent,
                        "confidence": result.confidence,
                        "draft_reply": result.draft_reply,
                    },
                    metadata=self._result_metadata(result),
                )
                return (
                    result,
                    True,
                    None,
                    None,
                )
            except Exception as exc:
                provider_label = "cloud" if provider == "cloud" else provider
                diagnostic_code = f"{provider_label}_llm_request_failed"
                diagnostic_detail = (
                    f"{provider_label.capitalize()} model request failed: {self._clean_exception_message(exc)}."
                )
                observation.update(
                    level="ERROR",
                    status_message=diagnostic_code,
                    metadata={"diagnostic_code": diagnostic_code, "diagnostic_detail": diagnostic_detail},
                )
                return (
                    None,
                    True,
                    diagnostic_code,
                    diagnostic_detail,
                )

    def _ollama_request(
        self,
        *,
        path: str,
        payload: Optional[dict] = None,
        timeout_seconds: float | None = None,
    ) -> tuple[Optional[dict], Optional[str], Optional[str]]:
        endpoint = f"{self.settings.ollama_base_url.rstrip('/')}{path}"
        body = None
        headers = {}
        method = "GET"
        if payload is not None:
            body = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
            method = "POST"

        req = urllib_request.Request(
            endpoint,
            data=body,
            headers=headers,
            method=method,
        )
        try:
            with urllib_request.urlopen(req, timeout=timeout_seconds or self.model_timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8")), None, None
        except urllib_error.HTTPError as exc:
            response_excerpt = ""
            try:
                response_excerpt = self._clean_response_excerpt(exc.read().decode("utf-8", errors="ignore"))
            except Exception:
                response_excerpt = ""

            if exc.code == 404:
                diagnostic_code = "local_ollama_endpoint_not_found"
                diagnostic_detail = (
                    f"Ollama endpoint {endpoint} responded with HTTP 404. "
                    "This usually means OLLAMA_BASE_URL points to a non-Ollama service, proxy, or wrong path."
                )
            else:
                diagnostic_code = "local_ollama_http_error"
                diagnostic_detail = (
                    f"Ollama endpoint {endpoint} responded with HTTP {exc.code}: "
                    f"{self._clean_exception_message(exc)}."
                )
            if response_excerpt:
                diagnostic_detail = f"{diagnostic_detail} Response excerpt: {response_excerpt}."
            return (
                None,
                diagnostic_code,
                diagnostic_detail,
            )
        except urllib_error.URLError as exc:
            return (
                None,
                "local_ollama_unreachable",
                f"Could not reach Ollama at {endpoint}: {self._clean_exception_message(exc)}.",
            )
        except TimeoutError as exc:
            return (
                None,
                "local_ollama_timeout",
                f"Ollama timed out while serving {path}: {self._clean_exception_message(exc)}.",
            )
        except json.JSONDecodeError:
            return (
                None,
                "local_ollama_invalid_response",
                f"Ollama returned a non-JSON response for {path}.",
            )
        except OSError as exc:
            return (
                None,
                "local_ollama_request_failed",
                f"Ollama request for {path} failed: {self._clean_exception_message(exc)}.",
            )

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

    def _list_local_ollama_models(self) -> tuple[list[str], Optional[str], Optional[str]]:
        payload, diagnostic_code, diagnostic_detail = self._ollama_request(path="/api/tags")
        if not payload:
            return [], diagnostic_code, diagnostic_detail

        models: list[str] = []
        for item in payload.get("models", []):
            if item.get("remote_host"):
                continue
            name = str(item.get("name") or item.get("model") or "").strip()
            if name:
                models.append(name)
        return models, None, None

    def _resolve_local_model_name(
        self,
        preferred_model: str | None = None,
    ) -> tuple[Optional[str], Optional[str], Optional[str]]:
        if preferred_model:
            return preferred_model, None, None
        if self._resolved_local_model:
            return self._resolved_local_model, None, None

        available, diagnostic_code, diagnostic_detail = self._list_local_ollama_models()
        if diagnostic_code:
            return None, diagnostic_code, diagnostic_detail
        if not available:
            return (
                None,
                "local_model_unavailable",
                "Ollama is reachable, but no local models are installed for the configured gateway.",
            )

        if self.settings.local_model in available:
            self._resolved_local_model = self.settings.local_model
            return self._resolved_local_model, None, None

        preferred = [
            "qwen2.5:1.5b",
            "qwen2.5:7b-instruct-q4_K_M",
            "mistral:latest",
        ]
        for name in preferred:
            if name in available:
                self._resolved_local_model = name
                return self._resolved_local_model, None, None

        self._resolved_local_model = available[0]
        return self._resolved_local_model, None, None

    def _call_local_ollama_structured(
        self,
        *,
        prompt: str,
        local_model_override: str | None = None,
        timeout_seconds: float | None = None,
    ) -> tuple[Optional[GenerationResult], bool, Optional[str], Optional[str]]:
        model_name, diagnostic_code, diagnostic_detail = self._resolve_local_model_name(
            preferred_model=local_model_override
        )
        if not model_name:
            return None, False, diagnostic_code, diagnostic_detail

        with self.observability.start_generation(
            name="model-gateway.local-ollama-structured",
            input={"prompt": prompt},
            metadata={"provider": "local", "operation": "structured-email"},
            model=f"ollama/{model_name}",
            model_parameters={
                "temperature": 0.2,
                "format": "json",
                "timeout_seconds": timeout_seconds or self.model_timeout_seconds,
            },
        ) as observation:
            payload, request_code, request_detail = self._ollama_request(
                path="/api/generate",
                payload={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "options": {"temperature": 0.2},
                },
                timeout_seconds=timeout_seconds,
            )
            if not payload:
                observation.update(
                    level="ERROR",
                    status_message=request_code,
                    metadata={"diagnostic_code": request_code, "diagnostic_detail": request_detail},
                )
                return None, True, request_code, request_detail

            content = str(payload.get("response") or "").strip()
            parsed = self._parse_json_object(content)
            if not parsed:
                diagnostic_code = "local_llm_invalid_json"
                diagnostic_detail = (
                    f"Local model ollama/{model_name} returned content that could not be parsed as structured JSON."
                )
                observation.update(
                    level="ERROR",
                    status_message=diagnostic_code,
                    metadata={"diagnostic_code": diagnostic_code, "diagnostic_detail": diagnostic_detail},
                )
                return (
                    None,
                    True,
                    diagnostic_code,
                    diagnostic_detail,
                )
            try:
                intent = str(parsed["intent"])
                confidence = float(parsed["confidence"])
                draft_reply = str(parsed["draft_reply"])
            except (KeyError, TypeError, ValueError):
                diagnostic_code = "local_llm_invalid_schema"
                diagnostic_detail = (
                    f"Local model ollama/{model_name} returned JSON, but it did not include the expected email drafting fields."
                )
                observation.update(
                    level="ERROR",
                    status_message=diagnostic_code,
                    metadata={"diagnostic_code": diagnostic_code, "diagnostic_detail": diagnostic_detail},
                )
                return (
                    None,
                    True,
                    diagnostic_code,
                    diagnostic_detail,
                )

            result = GenerationResult(
                intent=intent,
                confidence=confidence,
                draft_reply=draft_reply,
                provider_used="local",
                model_used=f"ollama/{model_name}",
                local_llm_invoked=True,
            )
            observation.update(
                output={
                    "intent": result.intent,
                    "confidence": result.confidence,
                    "draft_reply": result.draft_reply,
                },
                metadata=self._result_metadata(result),
            )
            return (
                result,
                True,
                None,
                None,
            )

    def _call_text_model(
        self,
        *,
        provider: str,
        model: str,
        prompt: str,
        max_tokens: int | None = None,
    ) -> tuple[Optional[TextGenerationResult], bool, Optional[str], Optional[str]]:
        with self.observability.start_generation(
            name="model-gateway.provider-text",
            input={"prompt": prompt},
            metadata={"provider": provider, "operation": "text"},
            model=model,
            model_parameters={"temperature": 0.2, "timeout_seconds": self.model_timeout_seconds},
        ) as observation:
            if completion is None:
                diagnostic_code = "litellm_unavailable"
                diagnostic_detail = (
                    "LiteLLM is not available in this environment, so provider-backed text generation could not run."
                )
                observation.update(
                    level="ERROR",
                    status_message=diagnostic_code,
                    metadata={"diagnostic_code": diagnostic_code, "diagnostic_detail": diagnostic_detail},
                )
                return (
                    None,
                    False,
                    diagnostic_code,
                    diagnostic_detail,
                )

            kwargs = {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
                "timeout": self.model_timeout_seconds,
                "request_timeout": self.model_timeout_seconds,
            }
            if max_tokens is not None:
                kwargs["max_tokens"] = max_tokens

            if provider == "local":
                kwargs["api_base"] = self.settings.ollama_base_url
            else:
                if self.settings.openrouter_api_key:
                    kwargs["api_key"] = self.settings.openrouter_api_key

            try:
                response = completion(**kwargs)
                content = response.choices[0].message.content
                result = TextGenerationResult(
                    content=str(content),
                    provider_used=provider,
                    model_used=model,
                    local_llm_invoked=provider == "local",
                    cloud_llm_invoked=provider == "cloud",
                )
                observation.update(
                    output={"content": result.content},
                    metadata=self._result_metadata(result),
                )
                return (
                    result,
                    True,
                    None,
                    None,
                )
            except Exception as exc:
                provider_label = "cloud" if provider == "cloud" else provider
                diagnostic_code = f"{provider_label}_llm_request_failed"
                diagnostic_detail = (
                    f"{provider_label.capitalize()} text generation failed: {self._clean_exception_message(exc)}."
                )
                observation.update(
                    level="ERROR",
                    status_message=diagnostic_code,
                    metadata={"diagnostic_code": diagnostic_code, "diagnostic_detail": diagnostic_detail},
                )
                return (
                    None,
                    True,
                    diagnostic_code,
                    diagnostic_detail,
                )

    def _call_local_ollama_text(
        self,
        *,
        prompt: str,
        num_predict: int | None = None,
        timeout_seconds: float | None = None,
        local_model_override: str | None = None,
    ) -> tuple[Optional[TextGenerationResult], bool, Optional[str], Optional[str]]:
        model_name, diagnostic_code, diagnostic_detail = self._resolve_local_model_name(
            preferred_model=local_model_override
        )
        if not model_name:
            return None, False, diagnostic_code, diagnostic_detail

        options = {"temperature": 0.2}
        if num_predict is not None:
            options["num_predict"] = num_predict

        with self.observability.start_generation(
            name="model-gateway.local-ollama-text",
            input={"prompt": prompt},
            metadata={"provider": "local", "operation": "text"},
            model=f"ollama/{model_name}",
            model_parameters={
                "temperature": 0.2,
                "num_predict": num_predict,
                "timeout_seconds": timeout_seconds or self.model_timeout_seconds,
            },
        ) as observation:
            payload, request_code, request_detail = self._ollama_request(
                path="/api/generate",
                payload={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": options,
                },
                timeout_seconds=timeout_seconds,
            )
            if not payload:
                observation.update(
                    level="ERROR",
                    status_message=request_code,
                    metadata={"diagnostic_code": request_code, "diagnostic_detail": request_detail},
                )
                return None, True, request_code, request_detail

            content = str(payload.get("response") or "").strip()
            if not content:
                diagnostic_code = "local_llm_empty_response"
                diagnostic_detail = f"Local model ollama/{model_name} returned an empty text response."
                observation.update(
                    level="ERROR",
                    status_message=diagnostic_code,
                    metadata={"diagnostic_code": diagnostic_code, "diagnostic_detail": diagnostic_detail},
                )
                return (
                    None,
                    True,
                    diagnostic_code,
                    diagnostic_detail,
                )

            result = TextGenerationResult(
                content=content,
                provider_used="local",
                model_used=f"ollama/{model_name}",
                local_llm_invoked=True,
            )
            observation.update(
                output={"content": result.content},
                metadata=self._result_metadata(result),
            )
            return (
                result,
                True,
                None,
                None,
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
        with self.observability.start_span(
            name="model-gateway.draft-email",
            input={
                "sender": sender,
                "subject": subject,
                "body_length": len(body),
                "thread_context_present": thread_context is not None,
                "risk_level": risk_level,
            },
            metadata={"workflow_id": "email-operations", "operation": "draft-email"},
        ) as observation:
            thread_summary = thread_context.strip() if thread_context else "No prior thread context was provided."
            state_summary = (
                f"risk={risk_level}\n"
                f"body_length={len(body)}\n"
                "goal=address request directly, propose next step, avoid overcommitment"
            )
            draft_prompt = self.prompt_loader.render_composition(
                "email-operations.draft-reply",
                template_context={
                    "sender": sender,
                    "subject": subject,
                    "body": body,
                    "thread_context": thread_context or "none",
                    "risk_level": risk_level,
                },
                injected_context={
                    "tenant_context": f"tenant={self.settings.tenant_id}; solo consulting CEO support",
                    "track": self.settings.primary_track,
                    "operating_mode": "internal_operating",
                    "approval_policy": "draft only; outbound send requires approval",
                    "autonomy_policy": f"risk={risk_level}; keep bounded and specific",
                    "tool_profile": "use email body + thread only",
                    "state_summary": state_summary,
                    "memory_context": thread_summary,
                },
            )
            intent, confidence = self._heuristic_classification(subject, body)

            local_text, local_llm_invoked, local_text_code, local_text_detail = self._call_local_ollama_text(
                prompt=draft_prompt,
                num_predict=self.settings.email_local_text_num_predict,
                timeout_seconds=self.settings.email_local_timeout_seconds,
                local_model_override=self.settings.email_local_model,
            )
            local_result: GenerationResult | None = None
            if local_text is not None:
                local_result = GenerationResult(
                    intent=intent,
                    confidence=confidence,
                    draft_reply=local_text.content,
                    provider_used=local_text.provider_used,
                    model_used=local_text.model_used,
                    local_llm_invoked=local_llm_invoked,
                    cloud_llm_invoked=local_text.cloud_llm_invoked,
                    llm_diagnostic_code=local_text_code,
                    llm_diagnostic_detail=local_text_detail,
                )
                if (
                    self.settings.email_upgrade_on_weak_draft
                    and self.settings.email_strong_local_model
                    and self.settings.email_strong_local_model != self.settings.email_local_model
                    and (
                        self._draft_contains_unresolved_placeholders(local_result.draft_reply)
                        or self._draft_appears_generic(local_result.draft_reply)
                    )
                ):
                    stronger_prompt = (
                        f"{draft_prompt}\n\n"
                        "Revision pass:\n"
                        "- avoid placeholders and template markers\n"
                        "- avoid generic filler\n"
                        "- mention the concrete request and next step\n"
                        "- do not invent names, dates, or meetings"
                    )
                    stronger_text, stronger_invoked, stronger_code, stronger_detail = self._call_local_ollama_text(
                        prompt=stronger_prompt,
                        num_predict=self.settings.email_strong_local_text_num_predict,
                        timeout_seconds=self.settings.email_strong_local_timeout_seconds,
                        local_model_override=self.settings.email_strong_local_model,
                    )
                    local_llm_invoked = local_llm_invoked or stronger_invoked
                    if stronger_text is not None:
                        local_result = GenerationResult(
                            intent=intent,
                            confidence=confidence,
                            draft_reply=stronger_text.content,
                            provider_used=stronger_text.provider_used,
                            model_used=stronger_text.model_used,
                            local_llm_invoked=local_llm_invoked,
                            cloud_llm_invoked=stronger_text.cloud_llm_invoked,
                            escalation_reason="routed_to_stronger_local",
                            llm_diagnostic_code=self._select_diagnostic_code(
                                local_text_code,
                                "email_draft_quality_retry",
                            ),
                            llm_diagnostic_detail=self._join_diagnostic_details(
                                local_text_detail,
                                "A stronger local email model was used because the first draft looked weak or template-like.",
                            ),
                        )
                    else:
                        local_result.llm_diagnostic_code = self._select_diagnostic_code(
                            local_result.llm_diagnostic_code,
                            stronger_code,
                        )
                        local_result.llm_diagnostic_detail = self._join_diagnostic_details(
                            local_result.llm_diagnostic_detail,
                            stronger_detail,
                            "The stronger local retry did not produce a usable draft.",
                        )
                local_result = self._apply_email_draft_guardrails(
                    result=local_result,
                    subject=subject,
                    body=body,
                    thread_context=thread_context,
                )

            if local_result is None:
                fallback_local_text = None
                fallback_local_code = None
                fallback_local_detail = None
                if (
                    self.settings.email_strong_local_model
                    and self.settings.email_strong_local_model != self.settings.email_local_model
                ):
                    fallback_local_text, fallback_local_invoked, fallback_local_code, fallback_local_detail = (
                        self._call_local_ollama_text(
                            prompt=draft_prompt,
                            num_predict=self.settings.email_strong_local_text_num_predict,
                            timeout_seconds=self.settings.email_strong_local_timeout_seconds,
                            local_model_override=self.settings.email_strong_local_model,
                        )
                    )
                    local_llm_invoked = local_llm_invoked or fallback_local_invoked
                    if fallback_local_text is not None:
                        fallback_local_result = GenerationResult(
                            intent=intent,
                            confidence=confidence,
                            draft_reply=fallback_local_text.content,
                            provider_used=fallback_local_text.provider_used,
                            model_used=fallback_local_text.model_used,
                            local_llm_invoked=local_llm_invoked,
                            cloud_llm_invoked=fallback_local_text.cloud_llm_invoked,
                            escalation_reason="routed_to_fallback_local",
                            llm_diagnostic_code=self._select_diagnostic_code(
                                local_text_code,
                                "email_fallback_local_used",
                            ),
                            llm_diagnostic_detail=self._join_diagnostic_details(
                                local_text_detail,
                                "Fallback local email model produced the final draft after the primary local model failed.",
                            ),
                        )
                        fallback_local_result = self._apply_email_draft_guardrails(
                            result=fallback_local_result,
                            subject=subject,
                            body=body,
                            thread_context=thread_context,
                        )
                        observation.update(
                            output={"intent": fallback_local_result.intent, "draft_reply": fallback_local_result.draft_reply},
                            metadata=self._result_metadata(fallback_local_result),
                        )
                        return fallback_local_result

                cloud_llm_invoked = False
                cloud_code = None
                cloud_detail = None
                if not self.settings.force_local_only and self.settings.openrouter_api_key:
                    cloud_text, cloud_llm_invoked, cloud_code, cloud_detail = self._call_text_model(
                        provider="cloud",
                        model=f"openrouter/{self.settings.cloud_model}",
                        prompt=draft_prompt,
                        max_tokens=self.settings.email_cloud_max_tokens,
                    )
                    if cloud_text is not None:
                        cloud_result = GenerationResult(
                            intent=intent,
                            confidence=confidence,
                            draft_reply=cloud_text.content,
                            provider_used=cloud_text.provider_used,
                            model_used=cloud_text.model_used,
                            local_llm_invoked=local_llm_invoked,
                            cloud_llm_invoked=cloud_llm_invoked or cloud_text.cloud_llm_invoked,
                            llm_diagnostic_code=self._select_diagnostic_code(
                                local_text_code,
                                fallback_local_code,
                            ),
                            llm_diagnostic_detail=self._join_diagnostic_details(
                                local_text_detail,
                                fallback_local_detail,
                                "Cloud text generation produced the final draft after the local path failed.",
                            ),
                        )
                        cloud_result = self._apply_email_draft_guardrails(
                            result=cloud_result,
                            subject=subject,
                            body=body,
                            thread_context=thread_context,
                        )
                        observation.update(
                            output={"intent": cloud_result.intent, "draft_reply": cloud_result.draft_reply},
                            metadata=self._result_metadata(cloud_result),
                        )
                        return cloud_result
                elif self.settings.force_local_only:
                    cloud_code = "force_local_only_enabled"
                    cloud_detail = "Cloud fallback was skipped because force_local_only is enabled."
                else:
                    cloud_code = "cloud_unconfigured"
                    cloud_detail = "Cloud fallback was skipped because OPENROUTER_API_KEY is not configured."

                fallback_result = self._heuristic_fallback(subject, body)
                fallback_result.local_llm_invoked = local_llm_invoked
                fallback_result.cloud_llm_invoked = cloud_llm_invoked
                fallback_result.llm_diagnostic_code = self._select_diagnostic_code(
                    local_text_code,
                    fallback_local_code,
                    cloud_code,
                )
                fallback_result.llm_diagnostic_detail = self._join_diagnostic_details(
                    local_text_detail,
                    fallback_local_detail,
                    cloud_detail,
                    "Rule-based fallback was used because local email drafting did not produce a usable result.",
                )
                observation.update(
                    output={"intent": fallback_result.intent, "draft_reply": fallback_result.draft_reply},
                    metadata=self._result_metadata(fallback_result),
                )
                return fallback_result

            needs_cloud = (
                not self.settings.force_local_only
                and (
                    local_result.confidence < self.settings.local_confidence_threshold
                    or len(body) > self.settings.max_local_input_chars
                    or risk_level == "high"
                )
            )

            if not needs_cloud:
                local_result.local_llm_invoked = local_llm_invoked or local_result.local_llm_invoked
                observation.update(
                    output={"intent": local_result.intent, "draft_reply": local_result.draft_reply},
                    metadata=self._result_metadata(local_result),
                )
                return local_result

            if not self.settings.openrouter_api_key:
                local_result.local_llm_invoked = local_llm_invoked or local_result.local_llm_invoked
                local_result.escalation_reason = "cloud_unconfigured_used_local"
                local_result.llm_diagnostic_code = self._select_diagnostic_code(
                    local_result.llm_diagnostic_code,
                    "cloud_unconfigured",
                )
                local_result.llm_diagnostic_detail = self._join_diagnostic_details(
                    local_result.llm_diagnostic_detail,
                    "Cloud escalation was skipped because OPENROUTER_API_KEY is not configured.",
                )
                observation.update(
                    output={"intent": local_result.intent, "draft_reply": local_result.draft_reply},
                    metadata=self._result_metadata(local_result),
                )
                return local_result

            cloud_text, cloud_llm_invoked, cloud_code, cloud_detail = self._call_text_model(
                provider="cloud",
                model=f"openrouter/{self.settings.cloud_model}",
                prompt=draft_prompt,
                max_tokens=self.settings.email_cloud_max_tokens,
            )
            if cloud_text is None:
                local_result.local_llm_invoked = local_llm_invoked or local_result.local_llm_invoked
                local_result.cloud_llm_invoked = cloud_llm_invoked
                local_result.escalation_reason = "cloud_unavailable_used_local"
                local_result.llm_diagnostic_code = self._select_diagnostic_code(
                    local_result.llm_diagnostic_code,
                    cloud_code,
                )
                local_result.llm_diagnostic_detail = self._join_diagnostic_details(
                    local_result.llm_diagnostic_detail,
                    cloud_detail,
                    "The workflow kept the local draft because cloud escalation did not produce a usable result.",
                )
                observation.update(
                    output={"intent": local_result.intent, "draft_reply": local_result.draft_reply},
                    metadata=self._result_metadata(local_result),
                )
                return local_result

            cloud_result = GenerationResult(
                intent=intent,
                confidence=confidence,
                draft_reply=cloud_text.content,
                provider_used=cloud_text.provider_used,
                model_used=cloud_text.model_used,
                local_llm_invoked=local_llm_invoked,
                cloud_llm_invoked=cloud_llm_invoked or cloud_text.cloud_llm_invoked,
                escalation_reason="routed_to_cloud",
                llm_diagnostic_code=local_result.llm_diagnostic_code,
                llm_diagnostic_detail=local_result.llm_diagnostic_detail,
            )
            cloud_result.local_llm_invoked = local_llm_invoked
            cloud_result = self._apply_email_draft_guardrails(
                result=cloud_result,
                subject=subject,
                body=body,
                thread_context=thread_context,
            )
            observation.update(
                output={"intent": cloud_result.intent, "draft_reply": cloud_result.draft_reply},
                metadata=self._result_metadata(cloud_result),
            )
            return cloud_result

    def generate_text(
        self,
        *,
        prompt: str,
        fallback_content: str,
        local_num_predict: int | None = None,
        local_timeout_seconds: float | None = None,
        local_model_override: str | None = None,
    ) -> TextGenerationResult:
        with self.observability.start_span(
            name="model-gateway.generate-text",
            input={
                "prompt_length": len(prompt),
                "local_num_predict": local_num_predict,
                "local_timeout_seconds": local_timeout_seconds,
                "local_model_override": local_model_override,
            },
            metadata={"operation": "text"},
        ) as observation:
            local_result, local_llm_invoked, local_code, local_detail = self._call_local_ollama_text(
                prompt=prompt,
                num_predict=local_num_predict,
                timeout_seconds=local_timeout_seconds,
                local_model_override=local_model_override,
            )
            if local_result is not None:
                local_result.local_llm_invoked = local_llm_invoked or local_result.local_llm_invoked
                observation.update(
                    output={"content": local_result.content},
                    metadata=self._result_metadata(local_result),
                )
                return local_result

            cloud_llm_invoked = False
            cloud_code = None
            cloud_detail = None
            if not self.settings.force_local_only and self.settings.openrouter_api_key:
                cloud_result, cloud_llm_invoked, cloud_code, cloud_detail = self._call_text_model(
                    provider="cloud",
                    model=f"openrouter/{self.settings.cloud_model}",
                    prompt=prompt,
                )
                if cloud_result is not None:
                    cloud_result.local_llm_invoked = local_llm_invoked
                    cloud_result.cloud_llm_invoked = cloud_llm_invoked or cloud_result.cloud_llm_invoked
                    cloud_result.llm_diagnostic_code = local_code
                    cloud_result.llm_diagnostic_detail = self._join_diagnostic_details(
                        local_detail,
                        "Cloud text generation produced the final output after the local path failed.",
                    )
                    observation.update(
                        output={"content": cloud_result.content},
                        metadata=self._result_metadata(cloud_result),
                    )
                    return cloud_result
            elif self.settings.force_local_only:
                cloud_code = "force_local_only_enabled"
                cloud_detail = "Cloud fallback was skipped because force_local_only is enabled."
            else:
                cloud_code = "cloud_unconfigured"
                cloud_detail = "Cloud fallback was skipped because OPENROUTER_API_KEY is not configured."

            fallback_result = TextGenerationResult(
                content=fallback_content,
                provider_used="fallback-rule",
                model_used="rules-v1",
                local_llm_invoked=local_llm_invoked,
                cloud_llm_invoked=cloud_llm_invoked,
                llm_diagnostic_code=self._select_diagnostic_code(local_code, cloud_code),
                llm_diagnostic_detail=self._join_diagnostic_details(
                    local_detail,
                    cloud_detail,
                    "Rule-based fallback content was returned because no LLM path produced a usable result.",
                ),
            )
            observation.update(
                output={"content": fallback_result.content},
                metadata=self._result_metadata(fallback_result),
            )
            return fallback_result

    def generate_structured_json(
        self,
        *,
        prompt: str,
        fallback_payload: dict,
        allow_local_text_recovery: bool = True,
        local_num_predict: int | None = None,
        local_timeout_seconds: float | None = None,
        local_model_override: str | None = None,
    ) -> StructuredGenerationResult:
        with self.observability.start_span(
            name="model-gateway.generate-structured-json",
            input={
                "prompt_length": len(prompt),
                "allow_local_text_recovery": allow_local_text_recovery,
                "local_num_predict": local_num_predict,
                "local_timeout_seconds": local_timeout_seconds,
                "local_model_override": local_model_override,
            },
            metadata={"operation": "structured-json"},
        ) as observation:
            local_structured, local_llm_invoked, local_structured_code, local_structured_detail = (
                self._call_local_ollama_structured_json(
                    prompt=prompt,
                    num_predict=local_num_predict,
                    timeout_seconds=local_timeout_seconds,
                    local_model_override=local_model_override,
                )
            )
            if local_structured is not None:
                local_structured.local_llm_invoked = local_llm_invoked or local_structured.local_llm_invoked
                observation.update(
                    output=local_structured.content,
                    metadata=self._result_metadata(local_structured),
                )
                return local_structured

            local_text_code = None
            local_text_detail = None
            if allow_local_text_recovery and local_structured_code != "local_ollama_timeout":
                local_text, local_text_invoked, local_text_code, local_text_detail = self._call_local_ollama_text(
                    prompt=prompt,
                    num_predict=local_num_predict,
                    timeout_seconds=local_timeout_seconds,
                    local_model_override=local_model_override,
                )
                local_llm_invoked = local_llm_invoked or local_text_invoked
                if local_text is not None:
                    parsed = self._parse_json_object(local_text.content)
                    if parsed is not None:
                        recovered_result = StructuredGenerationResult(
                            content=parsed,
                            provider_used=local_text.provider_used,
                            model_used=local_text.model_used,
                            local_llm_invoked=local_llm_invoked or local_text.local_llm_invoked,
                            cloud_llm_invoked=local_text.cloud_llm_invoked,
                            llm_diagnostic_code=local_structured_code,
                            llm_diagnostic_detail=self._join_diagnostic_details(
                                local_structured_detail,
                                "Structured JSON mode failed, but the gateway recovered by parsing the local text response.",
                            ),
                        )
                        observation.update(
                            output=recovered_result.content,
                            metadata=self._result_metadata(recovered_result),
                        )
                        return recovered_result
                    local_text_code = "local_llm_invalid_json"
                    local_text_detail = (
                        f"Local model {local_text.model_used} returned text, but it was not valid JSON for a structured response."
                    )

            cloud_llm_invoked = False
            cloud_code = None
            cloud_detail = None
            if not self.settings.force_local_only and self.settings.openrouter_api_key:
                cloud_text, cloud_llm_invoked, cloud_code, cloud_detail = self._call_text_model(
                    provider="cloud",
                    model=f"openrouter/{self.settings.cloud_model}",
                    prompt=prompt,
                )
                if cloud_text is not None:
                    parsed = self._parse_json_object(cloud_text.content)
                    if parsed is not None:
                        cloud_result = StructuredGenerationResult(
                            content=parsed,
                            provider_used=cloud_text.provider_used,
                            model_used=cloud_text.model_used,
                            local_llm_invoked=local_llm_invoked,
                            cloud_llm_invoked=cloud_llm_invoked or cloud_text.cloud_llm_invoked,
                            llm_diagnostic_code=self._select_diagnostic_code(
                                local_structured_code,
                                local_text_code,
                            ),
                            llm_diagnostic_detail=self._join_diagnostic_details(
                                local_structured_detail,
                                local_text_detail,
                                "Cloud model produced the final structured output after local attempts failed.",
                            ),
                        )
                        observation.update(
                            output=cloud_result.content,
                            metadata=self._result_metadata(cloud_result),
                        )
                        return cloud_result
                    cloud_code = "cloud_llm_invalid_json"
                    cloud_detail = (
                        f"Cloud model {cloud_text.model_used} returned text, but it was not valid JSON for a structured response."
                    )
            elif self.settings.force_local_only:
                cloud_code = "force_local_only_enabled"
                cloud_detail = "Cloud fallback was skipped because force_local_only is enabled."
            else:
                cloud_code = "cloud_unconfigured"
                cloud_detail = "Cloud fallback was skipped because OPENROUTER_API_KEY is not configured."

            fallback_result = StructuredGenerationResult(
                content=fallback_payload,
                provider_used="fallback-rule",
                model_used="rules-v1",
                local_llm_invoked=local_llm_invoked,
                cloud_llm_invoked=cloud_llm_invoked,
                llm_diagnostic_code=self._select_diagnostic_code(
                    local_structured_code,
                    local_text_code,
                    cloud_code,
                ),
                llm_diagnostic_detail=self._join_diagnostic_details(
                    local_structured_detail,
                    local_text_detail,
                    cloud_detail,
                    "Rule-based structured fallback was returned because no LLM path produced valid JSON.",
                ),
            )
            observation.update(
                output=fallback_result.content,
                metadata=self._result_metadata(fallback_result),
            )
            return fallback_result

    def _call_local_ollama_structured_json(
        self,
        *,
        prompt: str,
        num_predict: int | None = None,
        timeout_seconds: float | None = None,
        local_model_override: str | None = None,
    ) -> tuple[Optional[StructuredGenerationResult], bool, Optional[str], Optional[str]]:
        model_name, diagnostic_code, diagnostic_detail = self._resolve_local_model_name(
            preferred_model=local_model_override
        )
        if not model_name:
            return None, False, diagnostic_code, diagnostic_detail

        options = {"temperature": 0.2}
        if num_predict is not None:
            options["num_predict"] = num_predict

        with self.observability.start_generation(
            name="model-gateway.local-ollama-structured-json",
            input={"prompt": prompt},
            metadata={"provider": "local", "operation": "structured-json"},
            model=f"ollama/{model_name}",
            model_parameters={
                "temperature": 0.2,
                "num_predict": num_predict,
                "timeout_seconds": timeout_seconds or self.model_timeout_seconds,
                "format": "json",
            },
        ) as observation:
            payload, request_code, request_detail = self._ollama_request(
                path="/api/generate",
                payload={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "format": "json",
                    "options": options,
                },
                timeout_seconds=timeout_seconds,
            )
            if not payload:
                observation.update(
                    level="ERROR",
                    status_message=request_code,
                    metadata={"diagnostic_code": request_code, "diagnostic_detail": request_detail},
                )
                return None, True, request_code, request_detail

            content = str(payload.get("response") or "").strip()
            parsed = self._parse_json_object(content)
            if parsed is None:
                diagnostic_code = "local_llm_invalid_json"
                diagnostic_detail = (
                    f"Local model ollama/{model_name} returned content that was not valid JSON for structured output."
                )
                observation.update(
                    level="ERROR",
                    status_message=diagnostic_code,
                    metadata={"diagnostic_code": diagnostic_code, "diagnostic_detail": diagnostic_detail},
                )
                return (
                    None,
                    True,
                    diagnostic_code,
                    diagnostic_detail,
                )

            result = StructuredGenerationResult(
                content=parsed,
                provider_used="local",
                model_used=f"ollama/{model_name}",
                local_llm_invoked=True,
            )
            observation.update(
                output=result.content,
                metadata=self._result_metadata(result),
            )
            return (
                result,
                True,
                None,
                None,
            )
