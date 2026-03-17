# Copyright (c) Dario Pizzolante
from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy.orm import Session

from app.db.repository import insert_public_lead_submission
from app.models.schemas import PublicLeadCaptureRequest, PublicLeadCaptureResponse
from app.services.agent_run_logger import record_agent_run, subject_from_identity
from app.services.audit_event_logger import actor, record_audit_event


class PublicLeadIntakeService:
    def capture_booking_request(
        self,
        payload: PublicLeadCaptureRequest,
        *,
        db: Session,
    ) -> PublicLeadCaptureResponse:
        received_at = datetime.now(timezone.utc)
        submission_id = f"leadsub-{uuid4().hex[:12]}"
        lead_id = f"lead-{uuid4().hex[:12]}"

        response = PublicLeadCaptureResponse(
            submission_id=submission_id,
            lead_id=lead_id,
            received_at=received_at,
            message="Your request has been received and routed into the private intake workflow.",
        )
        payload_json = payload.model_dump(mode="json")
        insert_public_lead_submission(db, response, payload_json)

        lead_intake_subject = subject_from_identity(
            agent_id="lead-intake-agent",
            agent_family="lead-intake",
            mode="internal_operating",
            autonomy_class="supervised_executor",
            approval_class="bounded",
        )
        agent_run = record_agent_run(
            db,
            subject=lead_intake_subject,
            status="completed",
            started_at=received_at,
            ended_at=received_at,
            run_id=submission_id,
            trigger_event_name="lead.signal.detected",
            input_ref=f"public.booking:{submission_id}",
            output_ref=f"public_lead_submissions/{submission_id}",
        )

        record_audit_event(
            db,
            event_name="agent.run.started",
            entity_type="lead_submission",
            entity_id=submission_id,
            event_actor=actor(actor_type="workflow_system", actor_id="public-booking-endpoint"),
            status="started",
            run_id=submission_id,
            agent_run_id=agent_run.agent_run_id,
            approval_class="bounded",
            autonomy_class="supervised_executor",
            payload_ref_or_inline={
                "normalized_event_name": "lead.signal.detected",
                "source_class": response.source_class,
                "submission_kind": response.submission_kind,
                "website_path": payload.website_path,
            },
        )
        record_audit_event(
            db,
            event_name="agent.run.completed",
            entity_type="lead_submission",
            entity_id=submission_id,
            event_actor=actor(actor_type="agent", actor_id="lead-intake-agent"),
            status="completed",
            run_id=submission_id,
            agent_run_id=agent_run.agent_run_id,
            approval_class="bounded",
            autonomy_class="supervised_executor",
            payload_ref_or_inline={
                "normalized_event_names": [
                    "lead.materialized",
                    "lead.received",
                ],
                "lead_id": lead_id,
                "materialization_status": response.materialization_status,
                "lead_status": response.status,
            },
        )
        return response
