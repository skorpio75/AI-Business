<!-- Copyright (c) Dario Pizzolante -->
# Prompts

## Purpose
Define the canonical naming, storage, and loading conventions for runtime prompt assets.

## Scope
- `AGENTS.md` defines role and operating boundaries.
- `app/models/prompt_layer.py` defines typed prompt assets, compositions, and conventions.
- `config/base/prompt_layer.yaml` mirrors the same conventions in config form.
- `app/core/prompt_loader.py` applies the loading rules at runtime.

## Asset Naming
Prompt assets use canonical IDs rather than free-form filenames.

- Family base prompt asset: `<family_id>.family.base`
- Workflow-step prompt asset: `<family_id>.workflow.<step_id>`
- Prompt composition contract: `<workflow_id>.<step_id>`

Examples:
- `email.family.base`
- `knowledge.workflow.answer-question`
- `email-operations.classify-email`

## Storage Convention
The target prompt filesystem layout is:

```text
prompts/
|- agents/
|  `- <family_id>/
|     `- system.txt
`- workflows/
   `- <workflow_id>/
      `- <step_id_snake_case>.txt
```

Rules:
- Directory names use canonical `family_id` and `workflow_id` values as-is.
- Workflow-step filenames normalize `step_id` to `snake_case`.
- Family base prompts use `system.txt`.
- Prompt files should stay ASCII-first unless an existing file already requires otherwise.
- `.txt` is the default runtime prompt asset extension in the current platform.

## Loading Convention
Runtime prompt loading follows this order:

1. If an asset has an explicit `relative_path`, use it.
2. Otherwise resolve the target convention path from the asset kind and composition metadata.
3. Load family base prompt if present.
4. Load workflow-step prompt; this is required for implemented compositions.
5. Render template fields.
6. Append injected runtime context.

## Compatibility Rule
The platform keeps supporting explicit legacy paths during migration.

That means:
- existing prompt files like `prompts/email/email_operations_prompt.txt` remain valid
- new prompt assets should prefer the canonical `agents/` and `workflows/` layout
- we do not need to rewrite every existing prompt file immediately to adopt the convention
- specialist consulting analysis prompts may also use explicit `relative_path` mappings while the advisory prompt set is expanded incrementally

## Authoring Guidance
- Put durable family behavior in a family base prompt.
- Put task-specific instructions in workflow-step prompts.
- Keep output shape, approval boundaries, tool limits, and state context injected at runtime where possible.
- For consulting specialists, use the prompt for reasoning and synthesis while keeping governance, output schemas, and approval boundaries injected at runtime.
- Avoid one giant static prompt per agent family.

## Current State
- Runtime contracts and loader conventions are implemented.
- Legacy prompt paths remain supported through explicit path overrides.
- Broad prompt authoring and migration into the target folder layout remain incremental work, not a prerequisite for current delivery.
