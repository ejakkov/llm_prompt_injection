import dataclasses


@dataclasses.dataclass
class PromptInjection:
    name: str = ""

    def build_prompt(self, intention: str) -> str:
        raise NotImplementedError("Subclasses should implement this method.")
