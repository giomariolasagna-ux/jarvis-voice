import os
import requests
import json
import traceback

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
        "temperature": 0.3,
        "max_tokens": 1024
    }
    
    try:
        # DEBUG: Stampa prima della chiamata
        print(f"--- [MOONSHOT] Invio richiesta (Timeout: 120s)... ---")
        
        # Timeout aumentato drasticamente perché la chiamata NON è in streaming.
        # Dobbiamo aspettare l'intera generazione del testo.
        response = requests.post(API_URL, headers=HEADERS, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        # LOGGING DELL'ERRORE REALE (Traceback)
        print("\n--- [ERRORE CRITICO CLIENT API] ---")
        traceback.print_exc()
        print("-----------------------------------")
        
        return {"error": {"message": f"Errore Client: {str(e)}"}}