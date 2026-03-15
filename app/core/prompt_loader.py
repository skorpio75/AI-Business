import json
from pathlib import Path
from string import Template
from typing import Any

from app.models.prompt_layer import (
    DEFAULT_PROMPT_LAYER_REGISTRY,
    PROMPT_ASSET_BY_ID,
    PROMPT_COMPOSITION_BY_ID,
    normalize_prompt_file_segment,
)


class PromptLoader:
    def __init__(self, prompts_root: str | None = None) -> None:
        self.conventions = DEFAULT_PROMPT_LAYER_REGISTRY.conventions
        self.prompts_root = Path(prompts_root or self.conventions.storage.prompts_root)

    def load_text(self, relative_path: str) -> str:
        path = self.prompts_root / relative_path
        if not path.exists():
            raise FileNotFoundError(f"prompt_not_found:{path}")
        return path.read_text(encoding="utf-8")

    def path_exists(self, relative_path: str) -> bool:
        return (self.prompts_root / relative_path).exists()

    def render(self, relative_path: str, **context: Any) -> str:
        template_text = self.load_text(relative_path)
        return self.render_text(template_text, **context)

    def render_text(self, template_text: str, **context: Any) -> str:
        template = Template(template_text)
        return template.safe_substitute(**context)

    def compose(
        self,
        *,
        step_relative_path: str,
        template_context: dict[str, Any] | None = None,
        base_relative_path: str | None = None,
        injected_context: dict[str, Any] | None = None,
    ) -> str:
        sections: list[str] = []
        if base_relative_path:
            base_text = self.load_text(base_relative_path).strip()
            if base_text:
                sections.append(base_text)

        step_text = self.render(
            step_relative_path,
            **(template_context or {}),
        ).strip()
        if step_text:
            sections.append(step_text)

        rendered_context = self._render_injected_context(injected_context or {})
        if rendered_context:
            sections.append(rendered_context)

        return "\n\n".join(section for section in sections if section)

    def render_composition(
        self,
        composition_id: str,
        *,
        template_context: dict[str, Any] | None = None,
        injected_context: dict[str, Any] | None = None,
    ) -> str:
        composition = PROMPT_COMPOSITION_BY_ID.get(composition_id)
        if composition is None:
            raise KeyError(f"prompt_composition_not_found:{composition_id}")

        template_context = template_context or {}
        injected_context = injected_context or {}

        missing_template_fields = [
            field for field in composition.template_fields if field not in template_context
        ]
        if missing_template_fields:
            missing = ",".join(missing_template_fields)
            raise KeyError(f"prompt_template_context_missing:{missing}")

        missing_injected_context = [
            rule.key
            for rule in composition.context_injection
            if rule.required and rule.key not in injected_context
        ]
        if missing_injected_context:
            missing = ",".join(missing_injected_context)
            raise KeyError(f"prompt_injected_context_missing:{missing}")

        step_asset = PROMPT_ASSET_BY_ID.get(composition.step_prompt_asset_id)
        if step_asset is None or not step_asset.relative_path:
            raise FileNotFoundError(
                f"prompt_step_asset_unavailable:{composition.step_prompt_asset_id}"
            )

        base_relative_path: str | None = None
        if composition.base_prompt_asset_id:
            base_asset = PROMPT_ASSET_BY_ID.get(composition.base_prompt_asset_id)
            base_candidate: str | None = None
            if base_asset is not None:
                base_candidate = self._resolve_base_relative_path(
                    agent_family_id=composition.agent_family_id,
                    explicit_relative_path=base_asset.relative_path,
                )
            if base_candidate and self.path_exists(base_candidate):
                base_relative_path = base_candidate
            elif not self.conventions.loading.family_base_optional and base_candidate:
                raise FileNotFoundError(
                    f"prompt_base_asset_unavailable:{composition.base_prompt_asset_id}"
                )

        step_relative_path = self._resolve_step_relative_path(
            workflow_id=composition.workflow_id,
            step_id=composition.step_id,
            explicit_relative_path=step_asset.relative_path,
        )
        if self.conventions.loading.workflow_step_required and not self.path_exists(step_relative_path):
            raise FileNotFoundError(f"prompt_step_asset_unavailable:{step_relative_path}")

        allowed_injected_context = {
            rule.key: injected_context[rule.key]
            for rule in composition.context_injection
            if rule.key in injected_context
        }
        return self.compose(
            step_relative_path=step_relative_path,
            template_context=template_context,
            base_relative_path=base_relative_path,
            injected_context=allowed_injected_context,
        )

    def resolve_family_base_relative_path(self, agent_family_id: str) -> str:
        storage = self.conventions.storage
        directory = storage.family_base_directory.format(agent_family_id=agent_family_id)
        return f"{directory}/{storage.family_base_filename}"

    def resolve_workflow_step_relative_path(self, workflow_id: str, step_id: str) -> str:
        storage = self.conventions.storage
        directory = storage.workflow_step_directory.format(workflow_id=workflow_id)
        step_file = normalize_prompt_file_segment(step_id)
        filename = storage.workflow_step_filename.format(step_file=step_file)
        return f"{directory}/{filename}"

    def _resolve_base_relative_path(
        self,
        *,
        agent_family_id: str | None,
        explicit_relative_path: str | None,
    ) -> str | None:
        if explicit_relative_path and self.conventions.loading.explicit_relative_path_override:
            return explicit_relative_path
        if not agent_family_id:
            return None
        return self.resolve_family_base_relative_path(agent_family_id)

    def _resolve_step_relative_path(
        self,
        *,
        workflow_id: str,
        step_id: str,
        explicit_relative_path: str | None,
    ) -> str:
        if explicit_relative_path and self.conventions.loading.explicit_relative_path_override:
            return explicit_relative_path
        return self.resolve_workflow_step_relative_path(workflow_id, step_id)

    def _render_injected_context(self, injected_context: dict[str, Any]) -> str:
        sections: list[str] = []
        for key, value in injected_context.items():
            rendered = self._stringify_value(value)
            if not rendered:
                continue
            heading = key.replace("_", " ").capitalize()
            sections.append(f"{heading}:\n{rendered}")

        if not sections:
            return ""
        return "Runtime context:\n" + "\n\n".join(sections)

    def _stringify_value(self, value: Any) -> str:
        if value is None:
            return ""
        if isinstance(value, str):
            return value.strip()
        if isinstance(value, (int, float, bool)):
            return str(value)
        if isinstance(value, (list, tuple, set)):
            items = [self._stringify_value(item) for item in value]
            items = [item for item in items if item]
            return "\n".join(f"- {item}" for item in items)
        return json.dumps(value, ensure_ascii=True, indent=2, sort_keys=True)
