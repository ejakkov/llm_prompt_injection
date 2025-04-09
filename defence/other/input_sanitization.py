import dataclasses
from defence.prompt_engineering.basic_defence import BasicDefence

@dataclasses.dataclass
class InputSanitization(BasicDefence):
    name: str = "Input sanitization"
    description: str = "This is a basic defence that uses input sanitization to remove any harmful characters from the user input."