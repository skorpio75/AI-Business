# Hybrid RAG and Review Architecture

## Purpose
Define the target architecture for:
- retrieval-augmented context across internal and client-facing agent work
- governed use of external web sources for broader market, technology, and standards context
- bounded review/gate agents in multi-agent workflows

## Goals
- improve agent context awareness for internal operating work
- improve client-facing consulting quality through grounded internal, client, and external evidence
- separate authoritative grounding from broader enrichment
- keep review and judging behavior inside explicit workflow checkpoints rather than free-form supervisor autonomy

## Hybrid Retrieval Model

### Source Classes
- `internal_corpus`: firm playbooks, prior delivery artifacts, standards, templates, internal decisions
- `client_corpus`: tenant-scoped client documents, meeting notes, architectures, SOWs, backlog context, reports
- `external_web`: public documentation, vendor sites, standards, market signals, reference material
- `shared_workspace`: current structured operational truth from platform state and entities

### Source Roles
- `shared_workspace` is the source of truth for current operational state
- `internal_corpus` and `client_corpus` provide grounded retrieval context
- `external_web` provides enrichment, comparison, and broader perspective

### Non-Negotiable Rule
External retrieval may broaden reasoning, but it must not silently become authoritative platform truth.

## Context Assembly Order

### Internal operating mode
1. workflow input
2. shared workspace
3. internal corpus retrieval
4. recent episodic events if relevant
5. optional external web enrichment

### Client delivery or client-facing consulting mode
1. workflow input or client brief
2. tenant-scoped shared workspace
3. client corpus retrieval
4. relevant internal firm knowledge
5. recent episodic events if relevant
6. optional external web enrichment

## Evidence Lanes
Outputs that use hybrid retrieval should keep evidence separated into readable lanes:
- grounded internal evidence
- grounded client evidence
- external enrichment
- recommendation or synthesis

This makes it clear which parts are based on tenant-safe/client-safe grounding and which parts are broader market or technology context.

## Retrieval Design Intent

### Shared Retrieval Service
The platform should evolve from one knowledge-specific retrieval path into a shared context-assembly layer that can be reused by:
- `Knowledge Agent`
- `CTO/CIO Agent`
- `Chief AI / Digital Strategy Agent`
- `Proposal / SOW Agent`
- later delivery authoring agents such as PMO, BA, Architect, and Documentation

### Mission Context Packs
Consulting and delivery workflows should be able to assemble bounded mission packs that combine:
- client brief
- selected client documents
- selected internal playbooks or prior examples
- recent episodic events
- optional external enrichment

This keeps consulting work focused on one engagement or problem statement instead of one flat undifferentiated corpus.

### Provenance Requirements
Every retrieval-enhanced output should preserve:
- source class
- source identifier or URL
- citation/snippet
- retrieval time for external web results when relevant

## External Web Retrieval Boundaries
- external web retrieval should be governed through normalized research tools, not ad hoc browsing inside business logic
- externally retrieved content should remain cited and distinguishable from internal or client-grounded context
- external results may inform recommendations, but state changes and client commitments must still flow through approved workflow steps
- risky or externally consequential outputs should prefer a review/gate step before human or client-facing release

## Review/Gate Agent Pattern

### Why
Multi-agent flows benefit from a bounded agent that can evaluate:
- output quality
- grounding completeness
- policy compliance
- contradiction across evidence lanes
- whether the result should be revised, approved, escalated, or sent to human review

### What It Is
A review/gate agent is a workflow step with an explicit rubric and finite outcomes such as:
- `approve`
- `revise`
- `escalate`
- `human_review`

### What It Is Not
- not a universal second-pass reviewer on every task
- not an autonomous boss agent overriding workflow control
- not a replacement for human approval on sensitive actions

## Candidate Review/Gate Families
- `QA / Review Agent` for deliverable quality and consistency checks
- `Risk / Watchdog Agent` for policy, safety, and contradiction checks
- `Mission Control Agent` for supervisor-style run visibility and escalation routing

These families should act as bounded review/gate roles only when the workflow justifies the extra control cost.

## Good First Review/Gate Targets
- client-facing advisory analyses
- proposal and SOW drafts
- architecture recommendations
- delivery steering packs and milestone summaries
- outputs that combine internal/client grounding with external web enrichment

## Overkill Cases
- simple grounded Q&A
- low-risk internal summaries
- deterministic or tool-first operational steps where no meaningful synthesis is occurring

## Rollout Guidance

### Wave 1
- define hybrid retrieval source classes and provenance rules
- add shared context assembly for current knowledge and advisory surfaces

### Wave 2
- add governed external web retrieval as enrichment for advisory families
- add mission-scoped context packs

### Wave 3
- add bounded review/gate checkpoints for consulting, proposal, and delivery-authoring workflows

## Related Docs
- `MEMORY_MODEL.md`
- `INTEGRATIONS.md`
- `AGENTS.md`
- `AGENT_LLM_ROUTING_MATRIX.md`
- `ARCHITECTURE.md`
- `ROADMAP.md`
