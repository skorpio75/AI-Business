from uuid import uuid4

from app.core.prompt_loader import PromptLoader
from app.models.schemas import ProposalGenerationRequest, ProposalGenerationResponse
from app.services.model_gateway import ModelGateway
from app.services.observability import NullObservabilityService


class ProposalWorkflowService:
    def __init__(self, model_gateway: ModelGateway, observability: NullObservabilityService | None = None) -> None:
        self.model_gateway = model_gateway
        self.prompt_loader = PromptLoader()
        self.observability = observability or getattr(model_gateway, "observability", NullObservabilityService())

    def run(self, payload: ProposalGenerationRequest) -> ProposalGenerationResponse:
        workflow_id = str(uuid4())
        with self.observability.start_span(
            name="workflow.proposal-generation.run",
            input={"workflow_id": workflow_id, "client_name": payload.client_name},
            metadata={"workflow_type": "proposal-generation"},
        ) as observation:
            desired_outcomes = payload.desired_outcomes or ["Clarify project goals", "Define a first delivery slice"]
            constraints = payload.constraints or ["Budget and delivery assumptions still need confirmation"]
            prompt = self.prompt_loader.render_composition(
                "proposal-generation.generate-draft",
                template_context={
                    "client_name": payload.client_name,
                    "opportunity_summary": payload.opportunity_summary,
                    "desired_outcomes": "\n".join(f"- {item}" for item in desired_outcomes),
                    "constraints": "\n".join(f"- {item}" for item in constraints),
                },
                injected_context={
                    "approval_policy": (
                        "Draft only. Pricing, scope commitment, and client delivery promises require CEO review."
                    ),
                    "output_schema": (
                        "proposal draft with executive summary, delivery shape, assumptions, and next steps"
                    ),
                },
            )
            fallback_draft = self._fallback_draft(payload, desired_outcomes, constraints)
            generation = self.model_gateway.generate_text(
                prompt=prompt,
                fallback_content=fallback_draft,
            )
            response = ProposalGenerationResponse(
                workflow_id=workflow_id,
                title=f"Proposal draft for {payload.client_name}",
                executive_summary=(
                    f"Prepared a baseline proposal for {payload.client_name} based on the provided opportunity summary."
                ),
                proposal_draft=generation.content,
                next_steps=[
                    "Validate scope and pricing assumptions with the client.",
                    "Confirm delivery milestones and required approvals.",
                    "Convert the baseline draft into a client-facing proposal after review.",
                ],
                provider_used=generation.provider_used,
                model_used=generation.model_used,
                local_llm_invoked=generation.local_llm_invoked,
                cloud_llm_invoked=generation.cloud_llm_invoked,
                llm_diagnostic_code=generation.llm_diagnostic_code,
                llm_diagnostic_detail=generation.llm_diagnostic_detail,
            )
            observation.update(
                output=response.model_dump(mode="json"),
                metadata={
                    "provider_used": response.provider_used,
                    "model_used": response.model_used,
                    "desired_outcome_count": len(desired_outcomes),
                    "constraint_count": len(constraints),
                },
            )
            return response

    def _fallback_draft(
        self,
        payload: ProposalGenerationRequest,
        desired_outcomes: list[str],
        constraints: list[str],
    ) -> str:
        outcomes_text = "\n".join(f"- {item}" for item in desired_outcomes)
        constraints_text = "\n".join(f"- {item}" for item in constraints)
        return (
            f"Proposal title: {payload.client_name} delivery proposal\n\n"
            f"Opportunity summary:\n{payload.opportunity_summary}\n\n"
            f"Desired outcomes:\n{outcomes_text}\n\n"
            f"Constraints and assumptions:\n{constraints_text}\n\n"
            "Recommended delivery shape:\n"
            "- Discovery and scoping\n"
            "- MVP implementation with measurable checkpoints\n"
            "- Review, handover, and next-phase recommendations\n"
        )
