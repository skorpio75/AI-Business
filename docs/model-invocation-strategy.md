<!-- Copyright (c) Dario Pizzolante -->
# Model Invocation Strategy

## Purpose
Define the configuration model for local inference, shared client inference, and cloud fallback so the same routing semantics work locally and in OVH.

## Core Rule
Model invocation strategy is a governed runtime concern.

- families keep their routing posture in `AGENT_LLM_ROUTING_MATRIX.md`
- environments provide concrete endpoints and credentials
- local and cloud should share the same strategy names

## Strategy Modes

### `deterministic_only`
Use rules and deterministic code only.

### `local_only`
Use local or colocated `Ollama` only.

### `local_first`
Try local `Ollama`, then cloud fallback on failure.

### `guarded_local_first`
Try local `Ollama` first, but keep stronger drafting guardrails and fallback behavior.

### `cloud_first`
Use cloud model first; local is optional fallback or disabled.

### `cloud_required`
Use cloud only because task quality or context window requires it.

## Runtime Lanes

### Track A Lane
- endpoint: Track A local/internal `Ollama`
- best for internal panels, delivery lab, planning drafts, reviews, and fast iteration

### Track B Shared Lane
- endpoint: shared Track B `Ollama`
- best for cost-efficient client inference across multiple tenant runtimes

### Cloud Lane
- endpoint: LiteLLM-compatible cloud provider path
- best for larger reasoning tasks, wider context windows, or fallback resilience

## Environment Keys
Suggested keys:

- `MODEL_INVOCATION_STRATEGY`
- `OLLAMA_BASE_URL`
- `TRACK_A_OLLAMA_BASE_URL`
- `TRACK_B_SHARED_OLLAMA_BASE_URL`
- `LOCAL_MODEL`
- `EMAIL_LOCAL_MODEL`
- `EMAIL_STRONG_LOCAL_MODEL`
- `CLOUD_MODEL`
- `OPENROUTER_API_KEY`
- `MODEL_TIMEOUT_SECONDS`
- `LOCAL_CONFIDENCE_THRESHOLD`
- `FORCE_LOCAL_ONLY`

## Family-Level Overrides
Suggested config object:

```json
{
  "family_id": "project-management-delivery-coordination",
  "mode": "internal_operating",
  "strategy": "local_first",
  "preferred_lane": "track_a_local_ollama",
  "fallback_strategy": "cloud_first"
}
```

## API Response Metadata
All LLM-backed responses should expose:

- `strategy_used`
- `provider_used`
- `model_used`
- `local_llm_invoked`
- `cloud_llm_invoked`
- `fallback_mode`
- `llm_diagnostic_code`

## Local Development Rule
The strategy model must work locally first.

- local Track A should support the same strategy names as production
- local Track B seeded tenants should be able to point to either local `Ollama` or a shared local test endpoint
- do not introduce cloud-only strategy semantics

## Recommended Defaults
- Track A delivery-lab families: `local_first`
- Track A high-risk external drafting: `guarded_local_first`
- Track B compact grounded workflows: `local_first` or `guarded_local_first`
- richer consulting analysis: `cloud_first` or `local_first` with cloud fallback depending quality needs
