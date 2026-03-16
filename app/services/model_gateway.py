import json
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

    def _clean_exception_message(self, exc: Exception) -> str:
        message = " ".join(str(exc).split())
        if message:
            return message[:240]
        return exc.__class__.__name__

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
            with urllib_request.urlopen(req, timeout=timeout_seconds or self.model_timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8")), None, None
        except urllib_error.URLError as exc:
            return (
                None,
                "local_ollama_unreachable",
                f"Could not reach Ollama at {self.settings.ollama_base_url.rstrip('/')}{path}: {self._clean_exception_message(exc)}.",
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
        self, *, prompt: str
    ) -> tuple[Optional[GenerationResult], bool, Optional[str], Optional[str]]:
        model_name, diagnostic_code, diagnostic_detail = self._resolve_local_model_name()
        if not model_name:
            return None, False, diagnostic_code, diagnostic_detail

        with self.observability.start_generation(
            name="model-gateway.local-ollama-structured",
            input={"prompt": prompt},
            metadata={"provider": "local", "operation": "structured-email"},
            model=f"ollama/{model_name}",
            model_parameters={"temperature": 0.2, "format": "json"},
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
        self, *, provider: str, model: str, prompt: str
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
            prompt = self.prompt_loader.render_composition(
                "email-operations.classify-email",
                template_context={
                    "sender": sender,
                    "subject": subject,
                    "body": body,
                    "thread_context": thread_context or "none",
                },
                injected_context={
                    "approval_policy": "External send remains approval-gated for MVP email operations.",
                    "output_schema": "JSON object with intent, confidence, and draft_reply",
                    "tool_profile": "email.read + memory.search + approval.request",
                },
            )
            draft_prompt = self.prompt_loader.render_composition(
                "email-operations.draft-reply",
                template_context={
                    "subject": subject,
                    "body": body,
                },
                injected_context={
                    "approval_policy": "Reply draft only. No outbound send without recorded approval.",
                    "autonomy_policy": (
                        f"Risk level is {risk_level}. Keep the draft bounded and avoid unsupported commitments."
                    ),
                },
            )

            local_result, local_structured_invoked, local_structured_code, local_structured_detail = (
                self._call_local_ollama_structured(prompt=prompt)
            )
            local_llm_invoked = local_structured_invoked
            if local_result is None:
                local_text, local_text_invoked, local_text_code, local_text_detail = self._call_local_ollama_text(
                    prompt=draft_prompt
                )
                local_llm_invoked = local_llm_invoked or local_text_invoked
                if local_text is not None:
                    intent, confidence = self._heuristic_classification(subject, body)
                    local_result = GenerationResult(
                        intent=intent,
                        confidence=confidence,
                        draft_reply=local_text.content,
                        provider_used=local_text.provider_used,
                        model_used=local_text.model_used,
                        local_llm_invoked=local_llm_invoked,
                        cloud_llm_invoked=local_text.cloud_llm_invoked,
                        llm_diagnostic_code=local_structured_code,
                        llm_diagnostic_detail=self._join_diagnostic_details(
                            local_structured_detail,
                            "Structured email classification failed, so the gateway reused local plain-text output for the draft.",
                        ),
                    )
            else:
                local_text_code = None
                local_text_detail = None

            if local_result is None:
                fallback_result = self._heuristic_fallback(subject, body)
                fallback_result.local_llm_invoked = local_llm_invoked
                fallback_result.llm_diagnostic_code = self._select_diagnostic_code(
                    local_structured_code,
                    local_text_code,
                )
                fallback_result.llm_diagnostic_detail = self._join_diagnostic_details(
                    local_structured_detail,
                    local_text_detail,
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

            cloud_result, cloud_llm_invoked, cloud_code, cloud_detail = self._call_model(
                provider="cloud",
                model=f"openrouter/{self.settings.cloud_model}",
                prompt=prompt,
            )
            if cloud_result is None:
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

            cloud_result.local_llm_invoked = local_llm_invoked
            cloud_result.cloud_llm_invoked = cloud_llm_invoked or cloud_result.cloud_llm_invoked
            cloud_result.escalation_reason = "routed_to_cloud"
            cloud_result.llm_diagnostic_code = local_result.llm_diagnostic_code
            cloud_result.llm_diagnostic_detail = local_result.llm_diagnostic_detail
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
