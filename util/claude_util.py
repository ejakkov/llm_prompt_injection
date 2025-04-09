import anthropic
import json
import pathlib
import anthropic
from defence.base_defence import Defence

config_file_path = pathlib.Path("./config.json")
config = json.load(open(config_file_path))
client = anthropic.Anthropic(api_key=config.get("anthropic_key"))


def completion_with_claude(system_message: str, prompt: str, defence: Defence = Defence, model: str = "claude-3-opus-20240229") -> dict:
    messages = [
        {"role": "user", "content": prompt}
    ]

    if defence.name == "Few-shot learning":
        messages = defence.few_shot_messages + [{"role": "user", "content": prompt}]
    
    response = client.messages.create(
        max_tokens=1024,
        model=model,
        system=system_message,
        messages=messages,
        temperature=1.0,
    )

    return {
        "response_text": response.content[0].text,
        "prompt_tokens": response.usage.input_tokens,
        "completion_tokens": response.usage.output_tokens,
        "total_tokens": response.usage.input_tokens + response.usage.output_tokens
    }