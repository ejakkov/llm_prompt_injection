import dataclasses
from defence.prompt_engineering.basic_defence import BasicDefence

@dataclasses.dataclass
class LLMPiDetection(BasicDefence):
    name: str = "LLM Prompt Injection Detection"
    description: str = "This is a defence mechanism that detects prompt injection attacks using fine-tuned LLM."