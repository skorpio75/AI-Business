# Copyright (c) Dario Pizzolante
import unittest

import yaml
from sqlalchemy import select

from app.core.settings import ROOT
from app.db.models import ApprovalORM, WorkflowRunORM, WorkflowStateSnapshotORM
from app.knowledge.ingestion import DocumentIngestionService
from app.knowledge.retrieval import KeywordRetrievalService
from app.models.schemas import KnowledgeQueryRequest
from app.services.email_workflow import EmailWorkflowService
from app.services.knowledge_qna import KnowledgeQnAService
from app.services.model_gateway import GenerationResult, TextGenerationResult
from tests.sample_data import email_workflow_request
from tests.unit.base import TrackBSeededClientTestCase


class PortableWorkflowGateway:
    def __init__(self, tenant_id: str) -> None:
        self.tenant_id = tenant_id

    def generate_text(self, *, prompt: str, fallback_content: str, **_: object) -> TextGenerationResult:
        return TextGenerationResult(
            content=f"Tenant {self.tenant_id} grounded answer generated from seeded Track B context.",
            provider_used="local",
            model_used="stub/local-portability",
            local_llm_invoked=True,
        )

    def draft_email(
        self,
        *,
        sender: str,
        subject: str,
        body: str,
        thread_context: str | None,
        risk_level: str,
    ) -> GenerationResult:
        return GenerationResult(
            intent="general-inquiry",
            confidence=0.93,
            draft_reply=f"Reply for {self.tenant_id}: we reviewed '{subject}' and will follow up shortly.",
            provider_used="local",
            model_used="stub/local-portability",
            local_llm_invoked=True,
        )


class TrackBWorkflowPortabilityTests(TrackBSeededClientTestCase):
    def test_seeded_instances_load_isolated_track_b_settings(self) -> None:
        alpha = self.seed_track_b_client("Acme Portability Alpha", api_port=8111, postgres_port=5511, tenant_prefix="track-b-portability")
        beta = self.seed_track_b_client("Beta Portability Bravo", api_port=8112, postgres_port=5512, tenant_prefix="track-b-portability")

        alpha_settings = self.activate_seeded_client(alpha)
        beta_settings = self.activate_seeded_client(beta)

        self.assertEqual(alpha_settings.primary_track, "track_b_client")
        self.assertEqual(beta_settings.primary_track, "track_b_client")
        self.assertNotEqual(alpha_settings.tenant_id, beta_settings.tenant_id)
        self.assertNotEqual(alpha_settings.resolved_env_file, beta_settings.resolved_env_file)
        self.assertNotEqual(alpha_settings.resolved_client_documents_dir, beta_settings.resolved_client_documents_dir)
        self.assertTrue(alpha_settings.resolved_client_documents_dir.is_dir())
        self.assertTrue(beta_settings.resolved_client_documents_dir.is_dir())

    def test_implemented_workflows_run_across_seeded_clients(self) -> None:
        seeded_clients = [
            self.seed_track_b_client("Acme Workflow Portability", api_port=8121, postgres_port=5521, tenant_prefix="track-b-portability"),
            self.seed_track_b_client("Beta Workflow Portability", api_port=8122, postgres_port=5522, tenant_prefix="track-b-portability"),
        ]

        for seeded in seeded_clients:
            settings = self.activate_seeded_client(seeded)
            gateway = PortableWorkflowGateway(settings.tenant_id)

            handbook_path = settings.resolved_client_documents_dir / "delivery-handbook.md"
            handbook_path.write_text(
                (
                    f"{settings.tenant_id} delivery handbook\n"
                    "Knowledge workflow portability is validated for this client instance.\n"
                    "Email workflow portability is validated for this client instance.\n"
                ),
                encoding="utf-8",
            )
            ingested_docs = DocumentIngestionService().ingest(str(settings.resolved_client_documents_dir))
            knowledge_service = KnowledgeQnAService(
                retrieval_service=KeywordRetrievalService(ingested_docs),
                model_gateway=gateway,
            )
            knowledge_response = knowledge_service.answer(
                KnowledgeQueryRequest(question="How is workflow portability validated?", limit=2)
            )

            self.assertTrue(knowledge_response.grounded)
            self.assertEqual(knowledge_response.provider_used, "local")
            self.assertIn(settings.tenant_id, knowledge_response.answer)
            self.assertGreaterEqual(len(knowledge_response.citations), 1)
            self.assertTrue(
                knowledge_response.citations[0].source_path.startswith(
                    str(settings.resolved_client_documents_dir)
                )
            )

            email_service = EmailWorkflowService(model_gateway=gateway)
            with self.sqlite_session() as db:
                email_response = email_service.run(
                    email_workflow_request(
                        source_account_id=settings.tenant_id,
                        source_message_id=f"msg-{settings.tenant_id}",
                        source_thread_id=f"thread-{settings.tenant_id}",
                    ),
                    db=db,
                )

                workflow_runs = db.execute(select(WorkflowRunORM)).scalars().all()
                approvals = db.execute(select(ApprovalORM)).scalars().all()
                snapshots = db.execute(select(WorkflowStateSnapshotORM)).scalars().all()

            self.assertEqual(email_response.status, "pending_approval")
            self.assertEqual(email_response.send_status, "pending")
            self.assertEqual(email_response.provider_used, "local")
            self.assertIn(settings.tenant_id, email_response.draft_reply)
            self.assertEqual(len(workflow_runs), 1)
            self.assertEqual(len(approvals), 1)
            self.assertEqual(len(snapshots), 1)
            self.assertEqual(snapshots[0].workflow_type, "email-operations")

    def test_seeded_client_contracts_keep_track_b_workflow_pack_ids(self) -> None:
        seeded_clients = [
            self.seed_track_b_client("Acme Contract Portability", api_port=8131, postgres_port=5531, tenant_prefix="track-b-portability"),
            self.seed_track_b_client("Beta Contract Portability", api_port=8132, postgres_port=5532, tenant_prefix="track-b-portability"),
        ]
        base_workflows = yaml.safe_load((ROOT / "config" / "base" / "workflows.yaml").read_text(encoding="utf-8"))
        base_workflow_ids = {item["id"] for item in base_workflows["workflows"]}

        for seeded in seeded_clients:
            contract = yaml.safe_load(seeded.client_config_path.read_text(encoding="utf-8"))
            default_enabled = contract["solution_pack"]["default_enabled_workflows"]
            planned_portability = contract["solution_pack"]["planned_workflow_portability"]

            self.assertEqual(default_enabled, ["knowledge-qna", "document-intake", "reporting"])
            self.assertEqual(planned_portability, ["email-operations"])
            self.assertTrue(set(default_enabled).issubset(base_workflow_ids))
            self.assertTrue(set(planned_portability).issubset(base_workflow_ids))


if __name__ == "__main__":
    unittest.main()
