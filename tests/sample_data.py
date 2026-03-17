# Copyright (c) Dario Pizzolante
from pathlib import Path
from typing import Any

from app.models.connectors import ConnectorBootstrapStatusResponse, ProviderBootstrapStatus
from app.models.schemas import EmailWorkflowRequest


DEFAULT_EMAIL_WORKFLOW_PAYLOAD = {
    "sender": "client@example.com",
    "subject": "Need an update",
    "body": "Please confirm the next delivery checkpoint.",
}

DEFAULT_EMAIL_SOURCE_METADATA = {
    "source_account_id": "client-account",
    "source_message_id": "msg-001",
    "source_thread_id": "thread-001",
    "source_provider": "microsoft_graph",
}

DEFAULT_KNOWLEDGE_QUERY_PAYLOAD = {
    "question": "What workflow is supported?",
    "limit": 2,
}

DEFAULT_PROPOSAL_GENERATION_PAYLOAD = {
    "client_name": "Acme",
    "opportunity_summary": "The client wants a first proposal draft.",
    "desired_outcomes": ["Clarify scope"],
    "constraints": ["Budget approval pending"],
}

DEFAULT_PUBLIC_BOOKING_PAYLOAD = {
    "full_name": "Dario Pizzolante",
    "email": "dario@example.com",
    "company": "Stratevia",
    "role_title": "Managing Director",
    "service_interest": "AI strategy and roadmapping",
    "challenge_summary": "We need a practical conversation about modernization priorities and where AI can create business value.",
    "preferred_timing": "Within the next 2 weeks",
    "website_path": "/booking",
    "consent_to_contact": True,
}

DEFAULT_CTO_CIO_ANALYSIS_PAYLOAD = {
    "engagement_name": "Retail ERP Recovery",
    "problem_statement": "The client has legacy ERP and CRM fragmentation with manual handoffs.",
    "business_goal": "Reduce delivery friction and create a safer modernization path.",
    "client_context": "Leadership wants a phased roadmap without disrupting operations.",
    "engagement_history": [
        "A prior migration attempt stalled because integration scope was too broad.",
    ],
    "current_stack": ["legacy ERP", "CRM", "Excel"],
    "constraints": ["phased rollout", "limited bandwidth"],
    "desired_outcomes": ["clear roadmap", "lower integration risk"],
}

DEFAULT_CHIEF_AI_ANALYSIS_PAYLOAD = {
    "engagement_name": "Support Operations AI Review",
    "problem_statement": "Support staff spend too much time answering repetitive questions and triaging email.",
    "business_context": "Leadership wants a practical AI roadmap without unmanaged risk.",
    "client_context": "The company has scattered policy documents and approval-heavy workflows.",
    "engagement_history": [
        "A chatbot pilot failed because source content was unreliable.",
    ],
    "process_areas": ["support", "email triage"],
    "data_assets": ["policy PDFs"],
    "current_stack": ["shared mailbox", "SharePoint"],
    "delivery_constraints": ["human approval required", "8-week pilot window"],
    "desired_outcomes": ["faster response times", "better answer consistency"],
}

DEFAULT_CONNECTOR_BOOTSTRAP_PROVIDER = {
    "provider_id": "microsoft_graph",
    "inbox_selected": True,
    "calendar_selected": True,
    "access_token_present": True,
    "refresh_token_present": True,
    "client_id_present": True,
    "client_secret_present": False,
    "secret_store_path": "secrets/client-a/microsoft-graph.json",
    "refresh_supported": True,
    "status": "ready",
    "detail": "Microsoft Graph is ready.",
}


def email_workflow_payload(
    *,
    include_source_metadata: bool = True,
    **overrides: Any,
) -> dict[str, Any]:
    payload = dict(DEFAULT_EMAIL_WORKFLOW_PAYLOAD)
    if include_source_metadata:
        payload.update(DEFAULT_EMAIL_SOURCE_METADATA)
    payload.update(overrides)
    return payload


def email_workflow_request(
    *,
    include_source_metadata: bool = True,
    **overrides: Any,
) -> EmailWorkflowRequest:
    return EmailWorkflowRequest(
        **email_workflow_payload(
            include_source_metadata=include_source_metadata,
            **overrides,
        )
    )


def approval_decision_payload(decision: str = "approve", **overrides: Any) -> dict[str, Any]:
    defaults = {
        "approve": {"decision": "approve", "note": "Looks good"},
        "reject": {"decision": "reject", "note": "Do not send"},
        "edit": {"decision": "edit", "note": "Revise it"},
    }
    payload = dict(defaults.get(decision, {"decision": decision}))
    payload.update(overrides)
    return payload


def knowledge_query_payload(**overrides: Any) -> dict[str, Any]:
    payload = dict(DEFAULT_KNOWLEDGE_QUERY_PAYLOAD)
    payload.update(overrides)
    return payload


def proposal_generation_payload(**overrides: Any) -> dict[str, Any]:
    payload = dict(DEFAULT_PROPOSAL_GENERATION_PAYLOAD)
    payload.update(overrides)
    return payload


def public_booking_payload(**overrides: Any) -> dict[str, Any]:
    payload = dict(DEFAULT_PUBLIC_BOOKING_PAYLOAD)
    payload.update(overrides)
    return payload


def cto_cio_analysis_payload(**overrides: Any) -> dict[str, Any]:
    payload = dict(DEFAULT_CTO_CIO_ANALYSIS_PAYLOAD)
    payload.update(overrides)
    return payload


def chief_ai_analysis_payload(**overrides: Any) -> dict[str, Any]:
    payload = dict(DEFAULT_CHIEF_AI_ANALYSIS_PAYLOAD)
    payload.update(overrides)
    return payload


def connector_bootstrap_status_response(
    **provider_overrides: Any,
) -> ConnectorBootstrapStatusResponse:
    provider_payload = dict(DEFAULT_CONNECTOR_BOOTSTRAP_PROVIDER)
    provider_payload.update(provider_overrides)
    return ConnectorBootstrapStatusResponse(
        providers=[ProviderBootstrapStatus(**provider_payload)]
    )


def track_b_runtime_paths(root: Path, tenant_id: str) -> dict[str, Path]:
    data_root = root / "data" / "clients" / tenant_id
    prompt_root = root / "prompts" / "clients" / tenant_id
    secret_root = root / "secrets" / tenant_id
    return {
        "env_path": root / "config" / "clients" / f"{tenant_id}.env",
        "data_root": data_root,
        "prompt_root": prompt_root,
        "secret_root": secret_root,
        "documents_dir": data_root / "documents",
        "logs_dir": data_root / "logs",
        "exports_dir": data_root / "exports",
        "vector_dir": data_root / "vector",
        "google_secret_path": secret_root / "google-oauth.json",
        "microsoft_secret_path": secret_root / "microsoft-graph.json",
    }


def track_b_settings_kwargs(
    root: Path,
    tenant_id: str,
    **overrides: Any,
) -> dict[str, Any]:
    paths = track_b_runtime_paths(root, tenant_id)
    settings_kwargs = {
        "primary_track": "track_b_client",
        "tenant_id": tenant_id,
        "runtime_env_file": str(paths["env_path"]),
        "client_documents_dir": str(paths["documents_dir"]),
        "client_logs_dir": str(paths["logs_dir"]),
        "client_exports_dir": str(paths["exports_dir"]),
        "client_vector_dir": str(paths["vector_dir"]),
        "client_prompt_override_dir": str(paths["prompt_root"]),
        "google_secrets_path": str(paths["google_secret_path"]),
        "microsoft_graph_secrets_path": str(paths["microsoft_secret_path"]),
    }
    settings_kwargs.update(overrides)
    return settings_kwargs
