import dataclasses

@dataclasses.dataclass
class Intention:
    name: str = ""
    intention_string: str = ""

    def validate(self, response: str) -> bool:
        raise NotImplementedError("Subclasses should implement this method.")