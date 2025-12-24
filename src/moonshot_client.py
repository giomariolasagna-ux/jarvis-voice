import os
import requests

MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
API_URL = "https://api.moonshot.ai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {MOONSHOT_API_KEY}",
    "Content-Type": "application/json"
}

MODEL = "kimi-k2-0905-preview"

def ask(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.6,
        "max_tokens": 1024
    }

    r = requests.post(
        API_URL,
        headers=HEADERS,
        json=payload,
        timeout=90
    )
    r.raise_for_status()
    return r.json()["choices"][0]["message"]["content"]
