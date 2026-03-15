# TODO

## Current Focus
- Active phase: `Phase 3 - Track A Internal MVP Workflows`
- Active cross-cutting stream: `AI-Business IDE handoff integration`
- Immediate goal: define prompt asset naming/storage/loading conventions, then resume the remaining Phase 3 UI panels

## Now
- [x] `H-T01` Create the missing meta-model docs from `AI-Business_IDE_Handoff.md`
- [x] `H-T02` Update governance docs to adopt the 4-pod model and normalized event/state/tool/autonomy language
- [x] `P3-T01` Scaffold React mission-control app
- [x] `P3-T02` Build workflow monitor page
- [x] `P3-T03` Build approval queue page
- [x] `P3-T04` Build agent activity page
- [x] `P3-T05` Implement email operations workflow end-to-end
- [x] `P3-T06` Implement knowledge Q&A workflow end-to-end
- [x] `P3-T07` Implement proposal generation workflow baseline
- [x] `P3-T08` Connect approval actions from UI to API

## Next
- [ ] `P2-T20` Define prompt asset naming, storage, and loading conventions

## Soon After
- [ ] `P3-T12` Add CTO/CIO panel (customer scope insights, strategy options, internal tech improvement queue)
- [ ] `P3-T13` Add finance cockpit panels (accounting exceptions, close status, CFO scenario cards)
- [ ] `P3-T14` Add Chief AI/Digital Strategy panel (opportunity portfolio, AI/data roadmap, delivery guidance cards)

## Recently Finished
- [x] `P2-T19` Add prompt-layer contracts/config for family-base assets, workflow-step assets, and runtime context injection, and wire the implemented prompt-backed services through the composable prompt loader
- [x] `P2-T18` Add normalized tool-permission profile contracts and config bindings by agent family/operating mode, and surface tool-profile metadata in the agent activity view
- [x] `P2-T17` Add typed backend ownership and persistence contracts for `opportunity_state`, `project_state`, `run_state`, and `approval_state`, and mirror the same mapping into base config
- [x] `P3-T16` Add provider bootstrap, secret handling, refresh-token lifecycle support, and bootstrap-status diagnostics for Google and Microsoft inbox/calendar connectors
- [x] `P2-T16` Add backend control-plane contracts for normalized event names, approval classes, and autonomy classes, and enrich workflow config with trigger/emitted-event/control metadata
- [x] `H-T03` Align the current markdown agent/workflow spec set with pod ownership, operating modes, state objects, emitted events, approval gates, and cross-agent handoff roles
- [x] `P2-T15` Align the runtime agent registry and base config with the pod model, family/mode/instance identity, and specialist-overlay mapping
- [x] Carry the PMO split into runtime-facing registry/config/contracts and surface pod/family/mode metadata in the agent activity view
- [x] Clarify the distinction between PMO governance/control and project-management execution coordination
- [x] `P3-T01A` Adopt `shadcn/ui` + Tailwind foundation and migrate shared mission-control UI primitives
- [x] `P3-T20` Add explicit routing badges for local model, cloud route, fallback-rule execution, and local LLM invocation status

## Watchlist
- [ ] Keep `ROADMAP.md` as the full source of truth
- [ ] Keep `TODO.md` short and execution-oriented
- [ ] Keep Track A internal instances and Track B client instances isolated even when they share an agent family
- [ ] Keep multi-agent runtime evolution workflow-first; avoid autonomous peer-agent complexity before step identity, handoff payloads, and execution logs are stable
- [ ] Treat the prompt layer as part of the target runtime architecture, but defer large-scale prompt authoring until contracts, state, and workflow boundaries are stable
- [ ] Use the high-suitability multi-agent matrix to prioritize runtime splitting instead of promoting all documented families at once
- [ ] Treat the medium-suitability set as bounded collaboration candidates, not immediate runtime-splitting priorities
- [ ] Avoid adding UI logic before API/contracts are stable enough to consume
