<!-- Copyright (c) Dario Pizzolante -->
# Memory Model

## Purpose
Define the shared brain, workspace, and memory behavior of the platform so agents remain consistent across processes, tasks, and contexts.

## Principle
There is no single opaque "agent brain".
The platform uses structured memory layers with explicit ownership, storage, and promotion rules.

## Memory Layers

### 1. Working Memory
Purpose:
- hold the active state of a workflow run
- pass step outputs between nodes
- support resumable execution and approval checkpoints

Characteristics:
- short-lived
- scoped to one workflow run
- mutable during execution
- persisted for recovery and audit

Storage:
- PostgreSQL workflow state tables
- LangGraph state when workflow engine is introduced

Examples:
- current email classification
- draft reply under review
- current approval status
- current delivery risk summary

### 2. Episodic Memory
Purpose:
- store what happened in past runs
- allow agents and the CEO to learn from prior outcomes
- support audit, traceability, and operational continuity

Characteristics:
- medium to long-lived
- event-oriented
- append-heavy
- queryable by client, project, workflow, agent, and time

Storage:
- PostgreSQL
- Langfuse traces for model/run inspection

Examples:
- past approvals and rejections
- prior proposal drafts
- previous delivery incidents
- historical model routing decisions

### 3. Semantic Memory
Purpose:
- store reusable knowledge and facts
- provide grounded context to agents
- enable retrieval across workflows

Characteristics:
- long-lived
- document and fact oriented
- shared within one company instance
- retrieval-based, not blindly appended to prompts

Storage:
- source documents in file/object storage
- embeddings and metadata in pgvector/PostgreSQL

Examples:
- contracts and SOWs
- client context
- delivery standards
- accounting policies
- architecture notes
- playbooks and templates

### 4. Shared Workspace
Purpose:
- act as the canonical structured operating context for the company
- expose current truth for entities that multiple agents must coordinate around

Characteristics:
- structured, not free-form chat memory
- shared by all agents inside one company instance
- updated through workflows and approved actions
- source of truth for operational coordination

Storage:
- PostgreSQL relational tables

Canonical entities:
- clients
- projects
- opportunities
- tasks
- invoices
- purchase orders
- reports
- deliverables
- approvals
- improvement backlog items

Examples:
- current project status
- invoice payment state
- open delivery risks
- prioritized CEO action list
- CTO/CIO improvement backlog

### 5. Agent Scratchpad
Purpose:
- hold temporary reasoning artifacts for one agent during one task
- support decomposition and intermediate notes without polluting shared memory

Characteristics:
- private to the run
- disposable by default
- not promoted unless workflow rules say so

Storage:
- in-process runtime state
- optional persisted debug trace in Langfuse

Examples:
- draft hypotheses
- candidate classifications
- temporary option lists

## Shared Brain Definition
The shared brain of the platform is the combination of:
- semantic memory
- episodic memory
- shared workspace

It is not a single chat transcript.
It is a structured, instance-isolated memory system that workflows and agents can query and update under policy control.

## Scope Boundaries

### Shared Within One Instance
- company knowledge
- workflow run history
- approvals
- project and client records
- delivery and finance operational state

### Not Shared Across Clients
- documents
- embeddings
- credentials
- logs
- prompts when client-specific
- operational records

## Promotion Rules
Not all information should become long-term memory.

### Promote to Working Memory
- outputs needed by downstream nodes in the same workflow

### Promote to Episodic Memory
- final workflow outcomes
- approval decisions
- important failures
- significant delivery or finance events

### Promote to Semantic Memory
- approved documents
- stable client/company facts
- reusable playbooks
- architecture decisions

### Promote to Shared Workspace
- operational facts with current business effect
- entity state changes
- approved plans, tasks, invoices, risks, and milestones

### Never Promote Automatically
- raw chain-of-thought
- low-confidence guesses
- temporary scratch reasoning
- unapproved external commitments

## Consistency Rules

### Rule 1
Shared workspace is the operational source of truth.

### Rule 2
Semantic memory is retrieval context, not authority over current operational state.

### Rule 3
Episodic memory records what happened; it does not overwrite current state directly.

### Rule 4
Any state-changing write to shared workspace must happen through a workflow step, not an unconstrained agent action.

### Rule 5
High-risk updates require CEO approval before becoming authoritative.

## Context Assembly
When a workflow runs, context should be assembled in this order:
1. workflow input payload
2. relevant shared workspace records
3. relevant semantic retrieval results
4. recent episodic events if they matter
5. current workflow working memory

This prevents overloading prompts with stale or irrelevant context.

## Memory by Time Horizon

### Immediate
- working memory
- agent scratchpad

### Short Horizon
- current daily priorities
- current approval queue
- current project/delivery state

### Long Horizon
- company knowledge base
- client history
- prior decisions and reports
- architecture and process knowledge

## Observability and Audit
Every meaningful memory mutation should be attributable.

Minimum audit fields:
- workflow id
- agent id
- timestamp
- source input
- memory layer changed
- changed entity id
- approval id if relevant

## Initial MVP Implementation Mapping
- working memory: workflow run state in PostgreSQL
- episodic memory: approvals, workflow runs, traces
- semantic memory: planned document ingestion + pgvector retrieval
- shared workspace: planned relational entity tables
- scratchpad: in-process runtime only

## Future Extensions
- memory summarization jobs
- entity-centric timeline views
- confidence-weighted memory promotion
- memory retention and archival rules
- evaluation of retrieval quality
- cross-agent coordination policies
