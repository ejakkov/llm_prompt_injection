import dataclasses


@dataclasses.dataclass
class Intention:
    name: str = ""
    build_prompt: str = ""
