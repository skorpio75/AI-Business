# Copyright (c) Dario Pizzolante
import unittest

from app.services.email_workflow import EmailWorkflowService
from app.services.model_gateway import GenerationResult, ModelGateway
from app.services.observability import LangfuseObservabilityService
from tests.sample_data import email_workflow_request
from tests.unit.base import UnitTestCase


class RecordingObservation:
    def __init__(self, sink: list[dict], event: dict) -> None:
        self.sink = sink
        self.event = event

    def __enter__(self):
        self.sink.append(self.event)
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def update(self, **kwargs) -> None:
        self.event.setdefault("updates", []).append(kwargs)


class RecordingLangfuseClient:
    def __init__(self) -> None:
        self.events: list[dict] = []
        self.flushed = False

    def start_as_current_observation(self, **kwargs):
        return RecordingObservation(self.events, dict(kwargs))

    def flush(self) -> None:
        self.flushed = True


class StaticEmailGateway:
    def __init__(self, observability: LangfuseObservabilityService) -> None:
        self.observability = observability

    def draft_email(self, **kwargs) -> GenerationResult:
        return GenerationResult(
            intent="general-inquiry",
            confidence=0.91,
            draft_reply=f"Reply prepared for {kwargs['sender']}",
            provider_used="local",
            model_used="stub/local",
            local_llm_invoked=True,
        )


class LangfuseObservabilityTests(UnitTestCase):
    def test_observability_service_is_safe_when_unconfigured(self) -> None:
        service = LangfuseObservabilityService(settings=self.build_settings(langfuse_enabled=False))

        with service.start_span(name="test-span", input={"ok": True}) as observation:
            observation.update(output={"status": "ok"})

        service.flush()
        self.assertFalse(service.enabled)

    def test_model_gateway_records_span_and_generation_events(self) -> None:
        client = RecordingLangfuseClient()
        observability = LangfuseObservabilityService(
            settings=self.build_settings(langfuse_enabled=True, langfuse_public_key="pk", langfuse_secret_key="sk"),
            client=client,
        )
        gateway = ModelGateway(settings=self.build_settings(), observability=observability)
        gateway._resolve_local_model_name = lambda preferred_model=None: ("qwen2.5:1.5b", None, None)  # type: ignore[method-assign]
        gateway._ollama_request = lambda **kwargs: ({"response": "local traced output"}, None, None)  # type: ignore[method-assign]

        result = gateway.generate_text(prompt="Explain observability", fallback_content="fallback")

        self.assertEqual(result.provider_used, "local")
        event_names = [event["name"] for event in client.events]
        self.assertIn("model-gateway.generate-text", event_names)
        self.assertIn("model-gateway.local-ollama-text", event_names)
        generation_event = next(event for event in client.events if event["name"] == "model-gateway.local-ollama-text")
        self.assertEqual(generation_event["as_type"], "generation")
        self.assertEqual(generation_event["model"], "ollama/qwen2.5:1.5b")

    def test_email_workflow_records_workflow_span(self) -> None:
        client = RecordingLangfuseClient()
        observability = LangfuseObservabilityService(
            settings=self.build_settings(langfuse_enabled=True, langfuse_public_key="pk", langfuse_secret_key="sk"),
            client=client,
        )
        gateway = StaticEmailGateway(observability=observability)
        service = EmailWorkflowService(model_gateway=gateway)

        with self.sqlite_session() as db:
            response = service.run(
                email_workflow_request(include_source_metadata=False),
                db=db,
            )

        self.assertEqual(response.status, "pending_approval")
        workflow_event = next(event for event in client.events if event["name"] == "workflow.email-operations.run")
        self.assertEqual(workflow_event["as_type"], "span")
        self.assertEqual(workflow_event["metadata"]["workflow_type"], "email-operations")
        update_payloads = workflow_event.get("updates", [])
        self.assertTrue(any(update.get("metadata", {}).get("workflow_status") == "pending_approval" for update in update_payloads))


if __name__ == "__main__":
    unittest.main()
