# Copyright (c) Dario Pizzolante
import unittest

from app.models.specialist_contracts import ChiefAIDigitalStrategyInput, CTOCIOCounselInput
from app.services.agent_registry import AgentRegistryService
from app.services.chief_ai_panel import ChiefAIPanelService
from app.services.cto_cio_panel import CTOCIOPanelService
from app.services.model_gateway import StructuredGenerationResult, TextGenerationResult


class StubModelGateway:
    def generate_text(self, *, prompt: str, fallback_content: str, **kwargs) -> TextGenerationResult:
        del prompt, kwargs
        return TextGenerationResult(
            content=fallback_content,
            provider_used="fallback-rule",
            model_used="rules-test",
            local_llm_invoked=False,
            cloud_llm_invoked=False,
        )

    def generate_structured_json(self, *, prompt: str, fallback_payload: dict) -> StructuredGenerationResult:
        return StructuredGenerationResult(
            content=fallback_payload,
            provider_used="fallback-rule",
            model_used="rules-test",
            local_llm_invoked=False,
            cloud_llm_invoked=False,
        )


class SpecialistAdvisoryAnalysisTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = AgentRegistryService()
        gateway = StubModelGateway()
        self.cto_service = CTOCIOPanelService(model_gateway=gateway)
        self.chief_ai_service = ChiefAIPanelService(model_gateway=gateway)

    def test_cto_cio_analysis_uses_problem_context_and_history(self) -> None:
        agent = self.registry.get_agent("cto-cio-agent")
        self.assertIsNotNone(agent)

        response = self.cto_service.analyze_client_context(
            agent=agent,
            payload=CTOCIOCounselInput(
                engagement_name="Retail ERP Recovery",
                problem_statement=(
                    "The client has a legacy ERP and CRM stack with manual spreadsheet handoffs, poor delivery "
                    "visibility, and growing audit pressure."
                ),
                business_goal="Reduce delivery friction and create a safer modernization path.",
                client_context="Security review findings are open and leadership wants a phased migration.",
                engagement_history=[
                    "Two prior modernization attempts stalled because integration scope was too broad.",
                    "The PMO asked for clearer steering checkpoints and decision ownership.",
                ],
                current_stack=["legacy ERP", "CRM", "Excel", "custom APIs"],
                constraints=["phased rollout", "must satisfy audit controls", "limited internal bandwidth"],
                desired_outcomes=["clear roadmap", "better governance", "lower integration risk"],
            ),
        )

        recommended_ids = {item.service_id for item in response.recommended_services}
        upsell_ids = {item.opportunity_id for item in response.upsell_opportunities}
        signal_categories = {signal.category for signal in response.context_signals}

        self.assertIn("Retail ERP Recovery", response.analysis_summary)
        self.assertEqual(response.provider_used, "fallback-rule")
        self.assertEqual(response.model_used, "rules-test")
        self.assertEqual(response.mission_assessment.consulting_motion, "mixed")
        self.assertIn("technology-strategy-assessment", recommended_ids)
        self.assertIn("architecture-modernization-review", recommended_ids)
        self.assertIn("governance-controls-review", recommended_ids)
        self.assertIn("delivery-governance-reset", recommended_ids)
        self.assertIn("expand-integration-governance", upsell_ids)
        self.assertIn("expand-controls", upsell_ids)
        self.assertIn("expand-delivery-oversight", upsell_ids)
        self.assertIn("history", signal_categories)
        self.assertIn("constraint", signal_categories)

    def test_cto_cio_panel_uses_governed_model_route_metadata(self) -> None:
        agent = self.registry.get_agent("cto-cio-agent")
        self.assertIsNotNone(agent)

        response = self.cto_service.build_panel(agent=agent)

        self.assertEqual(response.provider_used, "fallback-rule")
        self.assertEqual(response.model_used, "rules-test")
        self.assertGreater(len(response.scope_insights), 0)
        self.assertGreater(len(response.strategy_options), 0)

    def test_chief_ai_analysis_recommends_knowledge_and_workflow_services(self) -> None:
        agent = self.registry.get_agent("chief-ai-digital-strategy-agent")
        self.assertIsNotNone(agent)

        response = self.chief_ai_service.analyze_client_context(
            agent=agent,
            payload=ChiefAIDigitalStrategyInput(
                engagement_name="Support Operations AI Review",
                problem_statement=(
                    "Support staff spend too much time answering repetitive questions, searching policies, and "
                    "triaging inbound email manually."
                ),
                business_context="Leadership wants a practical AI roadmap without creating unmanaged risk.",
                client_context="The company has scattered policy documents and approval-heavy workflows.",
                engagement_history=[
                    "A chatbot proof of concept failed because source content was unreliable.",
                    "Operations leaders still want a supervised pilot if grounding and approval rules are stronger.",
                ],
                process_areas=["support", "policy operations", "email triage"],
                data_assets=["policy PDFs"],
                current_stack=["shared mailbox", "SharePoint", "ticketing system"],
                delivery_constraints=["human approval required", "privacy review", "8-week pilot window"],
                desired_outcomes=["faster response times", "better answer consistency"],
            ),
        )

        recommended_ids = {item.service_id for item in response.recommended_services}
        opportunity_ids = {item.opportunity_id for item in response.opportunity_map}
        upsell_ids = {item.opportunity_id for item in response.upsell_opportunities}

        self.assertEqual(response.mission_assessment.consulting_motion, "mixed")
        self.assertEqual(response.provider_used, "fallback-rule")
        self.assertEqual(response.model_used, "rules-test")
        self.assertIn("ai-opportunity-assessment", recommended_ids)
        self.assertIn("knowledge-assistant-pilot", recommended_ids)
        self.assertIn("workflow-automation-pilot", recommended_ids)
        self.assertIn("data-readiness-sprint", recommended_ids)
        self.assertIn("ai-governance-setup", recommended_ids)
        self.assertIn("expand-knowledge-ops", upsell_ids)
        self.assertIn("expand-workflow-suite", upsell_ids)
        self.assertIn("expand-data-foundation", upsell_ids)
        self.assertIn("expand-ai-governance", upsell_ids)
        self.assertIn("opp-knowledge", opportunity_ids)
        self.assertIn("opp-automation", opportunity_ids)
        self.assertEqual(len(response.delivery_blueprint), 3)

    def test_chief_ai_panel_uses_governed_model_route_metadata(self) -> None:
        agent = self.registry.get_agent("chief-ai-digital-strategy-agent")
        self.assertIsNotNone(agent)

        response = self.chief_ai_service.build_panel(agent=agent)

        self.assertEqual(response.provider_used, "fallback-rule")
        self.assertEqual(response.model_used, "rules-test")
        self.assertGreater(len(response.scope_signals), 0)
        self.assertGreater(len(response.opportunity_map), 0)


if __name__ == "__main__":
    unittest.main()
