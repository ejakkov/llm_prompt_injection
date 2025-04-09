import dataclasses
from defence.prompt_engineering.basic_defence import BasicDefence

@dataclasses.dataclass
class Paraphrasing(BasicDefence):
    name: str = "Paraphrasing"
    description: str = "This is a basic defence that uses a system prompt to restrict the chatbot's responses and paraphrases user question using another LLM query."
