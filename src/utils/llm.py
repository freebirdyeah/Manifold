import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Configure OpenRouter client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

def call_llm(system_prompt: str, user_prompt: str, model: str = None, json_mode: bool = False) -> str:
    """
    Calls the LLM via OpenRouter.
    """
    if model is None:
        model = os.getenv("MODEL")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]
    
    kwargs = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "extra_headers": {
            "HTTP-Referer": "https://github.com/Manifold", # Optional, for OpenRouter rankings
            "X-Title": "Manifold"
        }
    }
    
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
        pass

    print(f"  > Calling LLM ({model})...")
    try:
        response = client.chat.completions.create(**kwargs, timeout=60.0)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling LLM: {e}")
        raise e
