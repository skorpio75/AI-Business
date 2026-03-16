import unittest

from pydantic import ValidationError

from app.models.audit import AgentRunRecord, AuditEventRecord


class AuditContractAlignmentTests(unittest.TestCase):
    def test_agent_run_record_requires_normalized_trigger_event_name(self) -> None:
        record = AgentRunRecord(
            agent_run_id="run-1",
            tenant_id="internal",
            track="track_a_internal",
            agent_id="email-agent",
            agent_family="email",
            mode="internal_operating",
            status="completed",
            started_at="2026-03-16T10:00:00Z",
            trigger_event_name="contract.signed",
            approval_class="ceo_required",
            autonomy_class="assistant",
        )

        self.assertEqual(record.trigger_event_name, "contract.signed")

    def test_agent_run_record_rejects_unknown_trigger_event_name(self) -> None:
        with self.assertRaises(ValidationError):
            AgentRunRecord(
                agent_run_id="run-1",
                tenant_id="internal",
                track="track_a_internal",
                agent_id="email-agent",
                agent_family="email",
                mode="internal_operating",
                status="completed",
                started_at="2026-03-16T10:00:00Z",
                trigger_event_name="nonexistent.trigger",
            )

    def test_audit_event_record_requires_normalized_tool_id_and_audit_event_name(self) -> None:
        record = AuditEventRecord(
            audit_event_id="evt-1",
            tenant_id="internal",
            track="track_a_internal",
            occurred_at="2026-03-16T10:00:00Z",
            event_name="tool.call.completed",
            entity_type="tool_call",
            entity_id="approval-1:email.send_external",
            actor_type="connector",
            actor_id="microsoft_graph",
            status="completed",
            tool_id="email.send_external",
            approval_class="ceo_required",
            autonomy_class="assistant",
        )

        self.assertEqual(record.event_name, "tool.call.completed")
        self.assertEqual(record.tool_id, "email.send_external")

    def test_audit_event_record_rejects_unknown_tool_id(self) -> None:
        with self.assertRaises(ValidationError):
            AuditEventRecord(
                audit_event_id="evt-1",
                tenant_id="internal",
                track="track_a_internal",
                occurred_at="2026-03-16T10:00:00Z",
                event_name="tool.call.completed",
                entity_type="tool_call",
                entity_id="bad-tool-call",
                actor_type="connector",
                actor_id="microsoft_graph",
                status="completed",
                tool_id="connector.raw_send",
            )

    def test_audit_event_record_rejects_unknown_audit_event_name(self) -> None:
        with self.assertRaises(ValidationError):
            AuditEventRecord(
                audit_event_id="evt-1",
                tenant_id="internal",
                track="track_a_internal",
                occurred_at="2026-03-16T10:00:00Z",
                event_name="workflow.custom.event",
                entity_type="workflow",
                entity_id="workflow-1",
                actor_type="workflow_system",
                actor_id="email-workflow",
                status="completed",
            )


if __name__ == "__main__":
    unittest.main()
