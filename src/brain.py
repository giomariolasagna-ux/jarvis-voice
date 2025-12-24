import json
import os
import sys
from pathlib import Path

# Tenta l'import del client
try:
    from src.moonshot_client import ask
except ImportError:
    def ask(prompt): return "Errore critico: Client Moonshot non trovato."

IDENTITY_PATH = Path(r"C:\Users\Administrator\JARVIS_VOICE\jarvis_identity.json")

def load_identity():
    if not IDENTITY_PATH.exists():
        raise FileNotFoundError(f"Manca {IDENTITY_PATH}")
    # utf-8-sig gestisce il BOM se presente
    with open(IDENTITY_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)

print(f"Loading identity...")
IDENTITY = load_identity()

MUTABLE_PATH = Path(IDENTITY.get("mutable_path", r"C:\Users\Administrator\JARVIS_VOICE\mutable_memory"))

def jarvis_brain(user_text):
    print(f"Brain input: {user_text}")
    
    # --- FIX ERRORE 400 ---
    # L'API richiede una lista di messaggi con ruoli specifici
    messages = [
        {"role": "system", "content": "Sei Jarvis. Rispondi in modo breve e diretto in italiano."},
        {"role": "user", "content": user_text}
    ]
    
    try:
        # Inviamo la lista formattata invece della stringa grezza
        response = ask(messages)
        
        # Gestione robusta della risposta (se arriva un dizionario o una stringa)
        if isinstance(response, dict):
            if "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"]
            elif "error" in response:
                return f"Errore API: {response['error']['message']}"
        
        return str(response)

    except Exception as e:
        return f"Errore di connessione: {str(e)}"
