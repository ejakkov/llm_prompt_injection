import openai
import loguru
from defence.base_defence import Defence
logger = loguru.logger

def completion_with_chatgpt(system_message: str, prompt: str, defence: Defence = Defence, model: str = "gpt-3.5-turbo") -> dict:
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    if defence.name == "Few-shot learning":
        messages = [{"role": "system", "content": system_message}] + defence.few_shot_messages + [{"role": "user", "content": prompt}]
    
    response = openai.ChatCompletion.create( model=model,
        messages=messages,
        temperature=1
    )

    return {
            "response_text": response['choices'][0]['message']['content'],
            "prompt_tokens": getattr(response.usage, 'prompt_tokens', None),
            "completion_tokens": getattr(response.usage, 'completion_tokens', None),
            "total_tokens": getattr(response.usage, 'total_tokens', None)
    }