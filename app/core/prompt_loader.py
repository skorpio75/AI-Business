from pathlib import Path
from string import Template
from typing import Any


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
        template = Template(template_text)
        return template.safe_substitute(**context)
