import json
from pathlib import Path
from string import Template
from typing import Any

from app.models.prompt_layer import PROMPT_ASSET_BY_ID, PROMPT_COMPOSITION_BY_ID


class PromptLoader:
    def __init__(self, prompts_root: str = "prompts") -> None:
        self.prompts_root = Path(prompts_root)

    def load_text(self, relative_path: str) -> str:
        path = self.prompts_root / relative_path
        if not path.exists():
            raise FileNotFoundError(f"prompt_not_found:{path}")
        return path.read_text(encoding="utf-8")

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
            if base_asset and base_asset.relative_path:
                base_relative_path = base_asset.relative_path

        allowed_injected_context = {
            rule.key: injected_context[rule.key]
            for rule in composition.context_injection
            if rule.key in injected_context
        }
        return self.compose(
            step_relative_path=step_asset.relative_path,
            template_context=template_context,
            base_relative_path=base_relative_path,
            injected_context=allowed_injected_context,
        )

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
