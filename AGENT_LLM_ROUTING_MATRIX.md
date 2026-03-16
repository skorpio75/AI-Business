# Agent LLM Routing Matrix

## Purpose
Define which agent families should primarily use:
- compact direct-Ollama local-first execution
- compact direct-Ollama with stronger drafting guardrails
- richer governed `ModelGateway` reasoning
- deterministic or tool-first hybrid execution

This matrix is a planning and governance artifact. It does not mean every listed family is already implemented.

Current implementation truth still lives in:
- `ROADMAP.md`
- `TODO.md`
- service code under `app/services/`

## Approach Glossary
- `DO-C`: compact direct-Ollama local-first. Best for bounded internal reasoning, short grounded answers, section-assembled summaries, and typed reconstruction.
- `DO-G`: compact direct-Ollama local-first with stronger output guardrails. Best for drafts that may become external-facing after review, such as outreach, proposal, reminder, or contract-support text.
- `GW-R`: richer governed `ModelGateway` reasoning. Best for larger client briefs, richer consulting analysis, or outputs where local compact prompting would likely over-compress the reasoning.
- `DT-H`: deterministic or tool-first hybrid. Best for workflows where rules, retrieval, extraction, validation, or operational tools should dominate and LLMs should remain optional or secondary.

## Working Rules
- Prefer `DO-C` for bounded internal panels, grounded question answering, and sectionable summaries.
- Prefer `DO-G` for externally consequential drafts that still benefit from local-first speed, but need explicit review and validation layers.
- Prefer `GW-R` for richer client-facing or cross-domain reasoning where output quality depends on more context and looser synthesis.
- Prefer `DT-H` where business state changes, extraction, policy checks, or operational correctness matter more than narrative generation.
- Track A and Track B variants are separate instances even when they share the same family. Routing posture may be similar, but runtime assumptions must not be shared implicitly.

## Planned Agent Activity Label Mapping
- `DO-C` should read in Mission Control as direct `Ollama` / compact local-first.
- `DO-G` should read in Mission Control as direct `Ollama` with guarded drafting or approval-sensitive local-first behavior.
- `GW-R` should read in Mission Control as governed `LiteLLM` / `ModelGateway` reasoning.
- `DT-H` should read in Mission Control as descriptive/tool-first or deterministic hybrid execution.
- Agent Activity should combine these route labels with registry metadata such as pod, family, mode, and autonomy so operators can read the agent's operating model in one place.

## Current Live Examples
- `CTO/CIO Agent` internal panel: `DO-C`
- `Chief AI / Digital Strategy Agent` internal panel: `DO-C`
- `Knowledge Agent` current service implementation: standard `ModelGateway` text generation today, target `DO-C`
- `Proposal / SOW Agent` current service implementation: standard `ModelGateway` text generation today, target `DO-G`
- `Email Agent` current service implementation: standard `ModelGateway` drafting today, target `DO-G`
- `Finance / CFO` panel current implementation: `DT-H`

## Matrix

### Growth Pod
| Family / Agent | Typical Modes | Recommended Primary | Secondary | Current Planning Status |
|---|---|---|---|---|
| `Lead Intake Agent` | `internal_operating`, later `client_delivery` | `DT-H` | `DO-C` for concise intake summaries | Later candidate |
| `Account Research Agent` | `internal_operating`, `client_delivery` | `DO-C` | `GW-R` for richer account briefs | Candidate |
| `Qualification Agent` | `internal_operating`, `client_delivery` | `DO-C` | `DT-H` scoring guardrails | Candidate |
| `Outreach Draft Agent` | `internal_operating`, `client_delivery` | `DO-G` | `GW-R` for higher-context campaigns | Candidate |
| `Proposal / SOW Agent` | `internal_operating`, `client_delivery` | `DO-G` | `GW-R` for richer client-specific proposal synthesis | Near-term candidate |
| `CRM Hygiene Agent` | `internal_operating`, later `client_delivery` | `DT-H` | `DO-C` for notes/summaries only | Mostly deterministic |

### Delivery Pod
| Family / Agent | Typical Modes | Recommended Primary | Secondary | Current Planning Status |
|---|---|---|---|---|
| `PMO / Project Control Agent` | `internal_operating`, `client_delivery`, `client_facing_service` | `DO-C` | `DO-G` for client-facing steering packs | Broader candidate |
| `Project Management / Delivery Coordination Agent` | `internal_operating`, `client_delivery`, `client_facing_service` | `DO-C` | `DO-G` for client-ready status drafts | Broader candidate |
| `BA / Requirements Agent` | `internal_operating`, `client_delivery` | `DO-C` | `GW-R` for larger requirements packs | Broader candidate |
| `Architect Agent` | `internal_operating`, `client_delivery` | `DO-C` | `GW-R` for richer architecture reasoning | Broader candidate |
| `Build / Automation Agent` | `internal_operating`, `client_delivery` | `DT-H` | `DO-C` for change summaries | Mostly deterministic |
| `QA / Review Agent` | `internal_operating`, `client_delivery` | `DT-H` | `DO-C` for review narratives and summaries | Broader candidate |
| `Documentation Agent` | `internal_operating`, `client_delivery` | `DO-C` | `DO-G` for client handover packs | Broader candidate |

### Ops Pod
| Family / Agent | Typical Modes | Recommended Primary | Secondary | Current Planning Status |
|---|---|---|---|---|
| `Finance Ops Agent` | `internal_operating` | `DT-H` | `DO-C` for summaries/explanations | Decision needed |
| `Invoice / Receivables Agent` | `internal_operating` | `DT-H` | `DO-G` for reminder drafting | Later guarded candidate |
| `Vendor / Procurement Agent` | `internal_operating` | `DT-H` | `DO-G` for vendor/procurement drafts | Later guarded candidate |
| `Admin / HR Ops Agent` | `internal_operating` | `DT-H` | `DO-C` for internal summaries | Mostly deterministic |
| `Company Reporting Agent` | `internal_operating`, later `client_delivery` | `DO-C` | `GW-R` for broad business synthesis | Broader candidate |

### Executive Pod
| Family / Agent | Typical Modes | Recommended Primary | Secondary | Current Planning Status |
|---|---|---|---|---|
| `CEO Briefing Agent` | `internal_operating` | `DO-C` | `GW-R` for wider strategic briefings | Broader candidate |
| `Strategy / Opportunity Agent` | `internal_operating`, later `client_facing_service` | `DO-C` | `GW-R` for richer strategy synthesis | Broader candidate |
| `Risk / Watchdog Agent` | `internal_operating`, `client_delivery` | `DT-H` | `DO-C` for escalation narratives | Broader candidate |
| `Mission Control Agent` | `internal_operating`, `client_delivery` | `DT-H` | `DO-C` for operator briefings | Mostly deterministic supervisor |

### Corporate Function Agents
| Family / Agent | Typical Modes | Recommended Primary | Secondary | Current Planning Status |
|---|---|---|---|---|
| `Email Agent` | `internal_operating` | `DO-G` | `GW-R` for harder threads | Near-term candidate |
| `Personal Assistant Agent` | `internal_operating` | `DO-C` | `DO-G` for draft replies | Later candidate |
| `Billing Agent` | `internal_operating` | `DT-H` | `DO-G` for invoice/reminder language | Later guarded candidate |
| `Accountant Agent` | `internal_operating` | `DT-H` | `DO-C` for close explanations and summaries | Broader candidate |
| `CFO Agent` | `internal_operating` | `DO-C` | `GW-R` for richer strategy scenarios | Decision and design candidate |
| `Finance Agent` | `internal_operating` | `DO-C` | `DT-H` for metric production | Broader candidate |
| `Procurement (PO) Agent` | `internal_operating` | `DT-H` | `DO-G` for request drafts | Later guarded candidate |
| `Reporting Agent` | `internal_operating`, later `client_delivery` | `DO-C` | `GW-R` for broad synthesis | Broader candidate |
| `Compliance / Contract Agent` | `internal_operating` | `DO-G` | `GW-R` for richer non-binding analysis | Later guarded candidate |
| `CTO/CIO Agent` | `internal_operating`, `client_delivery`, `client_facing_service` | `DO-C` for internal panels | `GW-R` for client analysis | Internal panel live; client analysis later candidate |
| `Chief AI / Digital Strategy Agent` | `internal_operating`, `client_delivery`, `client_facing_service` | `DO-C` for internal panels | `GW-R` for client analysis | Internal panel live; client analysis later candidate |
| `Document Agent` | `internal_operating`, `client_delivery`, `client_facing_service` | `DT-H` | `DO-C` for classification summaries | Separate service candidate |

### Service Delivery Agents and Legacy Labels
| Family / Agent | Typical Modes | Recommended Primary | Secondary | Current Planning Status |
|---|---|---|---|---|
| `Knowledge Agent` | `internal_operating`, `client_delivery`, `client_facing_service` | `DO-C` | `DT-H` for strict retrieval behavior | Near-term candidate |
| `Project Management Agent` | legacy label for delivery coordination | `DO-C` | `DO-G` for client-ready reports | Follows PM / Delivery Coordination |
| `Delivery Agent` | `internal_operating`, `client_delivery` | `DT-H` | `DO-C` for milestone summaries | Broader candidate |
| `Quality Management Agent` | `internal_operating`, `client_delivery` | `DT-H` | `DO-C` for gate explanations | Broader candidate |
| `Consulting Support Agent` | `internal_operating`, `client_delivery`, `client_facing_service` | `DO-C` | `GW-R` for richer advisory synthesis | Broader candidate |
| `Documentation Agent` | `internal_operating`, `client_delivery` | `DO-C` | `DO-G` for client handover materials | Follows Documentation family |
| `Testing / QA Agent` | `internal_operating`, `client_delivery` | `DT-H` | `DO-C` for release-readiness summaries | Follows QA / Review family |
| `Ops Agent` | `internal_operating` | `DT-H` | `DO-C` for runbook summaries | Mostly deterministic |

## Rollout Waves
- `Wave 1`: bounded internal and grounded outputs. Examples: `Knowledge Agent`, `Proposal / SOW Agent`, `Email Agent`, internal `CEO Briefing`, internal `Reporting`, internal `Finance`.
- `Wave 2`: internal synthesis and delivery authoring. Examples: `PMO`, `Project Management / Delivery Coordination`, `BA`, `Documentation`, `Consulting Support`, `Risk / Watchdog`.
- `Wave 3`: richer delivery and advisory authoring. Examples: `Architect`, broader delivery packs, client-delivery documentation and steering artifacts.
- `Wave 4`: externally consequential or richer client-facing consulting surfaces. Examples: client `CTO/CIO`, client `Chief AI / Digital Strategy`, `Compliance / Contract`, guarded finance/advisory surfaces.

## Notes
- Multi-agent suitability and LLM routing are related but not identical decisions.
- A family can be high-suitability for bounded multi-agent runtime use while still preferring `DT-H` or `GW-R` instead of compact direct-Ollama.
- The matrix should be revisited whenever a family becomes a real backend endpoint, panel, workflow step, or client-facing service.
