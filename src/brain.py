import json
import os
import sys
from pathlib import Path

# Tentativo di importazione robusto
try:
    from src.moonshot_client import ask
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.moonshot_client import ask

def jarvis_brain(user_text):
    print(f"Brain Input: {user_text}")
    if not user_text: return None
    
    messages = [
        {
            "role": "system",
            "content": (
                "Sei Jarvis, un assistente vocale utile e conciso. "
                "Rispondi in italiano. Non usare formattazione complessa."
            )
        },
        {"role": "user", "content": user_text}
    ]

    try:
        response = ask(messages)

        # FIX CRITICO: Estrazione stringa dal dizionario
        if isinstance(response, dict):
            if "error" in response:
                return f"Errore API: {response['error'].get('message', 'Sconosciuto')}"
            if "choices" in response and len(response["choices"]) > 0:
                return response["choices"][0]["message"]["content"].strip()
        
        return "Non ho ricevuto una risposta valida."

    except Exception as e:
        print(f"Errore critico in Brain: {e}")
        return "Errore interno del sistema."
