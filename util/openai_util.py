import json
import pathlib

from openai import OpenAI

from defence.base_defence import Defence

config_file_path = pathlib.Path("./config.json")
config = json.load(open(config_file_path))
client = OpenAI(api_key=config["openai_key"])


def completion_with_chatgpt(system_message: str, prompt: str, defence: Defence = Defence, model: str = "gpt-3.5-turbo") -> dict:
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt},
    ]
    if defence.name == "Few-shot learning":
        messages = [{"role": "system", "content": system_message}] + defence.few_shot_messages + [{"role": "user", "content": prompt}]

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )

    usage = response.usage
    return {
        "response_text": response.choices[0].message.content,
        "prompt_tokens": getattr(usage, "prompt_tokens", None) if usage else None,
        "completion_tokens": getattr(usage, "completion_tokens", None) if usage else None,
        "total_tokens": getattr(usage, "total_tokens", None) if usage else None,
    }
