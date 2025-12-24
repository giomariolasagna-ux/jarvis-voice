import os
import requests
import json

MOONSHOT_API_KEY = os.getenv("MOONSHOT_API_KEY")
API_URL = "https://api.moonshot.ai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {MOONSHOT_API_KEY}",
    "Content-Type": "application/json"
}

# Modello Kimi (Bilanciato)
MODEL = "kimi-k2-0905-preview"

def ask(messages):
    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.3, # Abbassata per risposte più secche e veloci
        "max_tokens": 512   # Limitato per evitare monologhi
    }
    
    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": {"message": str(e)}}
