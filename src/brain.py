import sys
import os
import json
import traceback
from pathlib import Path

# ==================================================================================
# 1. CONFIGURAZIONE AMBIENTALE (NON TOCCARE)
# ==================================================================================
CORE_PATH = Path(r"C:\Users\Administrator\JARVIS_VOICE")
DEV_PATH = Path(r"C:\Users\Administrator\JARVIS_DEV")
IDENTITY_PATH = CORE_PATH / "jarvis_identity.json"

# Importazione client API robusta
try:
    from src.moonshot_client import ask
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.moonshot_client import ask

# ==================================================================================
# 2. GESTIONE MEMORIA E IDENTITÀ
# ==================================================================================
def load_identity():
    """Carica la configurazione di Jarvis se esiste"""
    try:
        if IDENTITY_PATH.exists():
            with open(IDENTITY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        print(f"Warn: Impossibile caricare identity: {e}")
    return {}

IDENTITY = load_identity()

# ==================================================================================
# 3. LOGICA DI SELEZIONE PROMPT (IL "CERVELLO")
# ==================================================================================
def get_system_prompt(mode, user_text):
    """Restituisce il prompt di sistema in base alla modalità"""
    
    if mode == "WRITE":
        return (
            "Sei un motore di scrittura pura. "
            "Il tuo compito è generare ESATTAMENTE il testo richiesto dall'utente. "
            "NON aggiungere introduzioni, NON aggiungere conclusioni, NON conversare. "
            "Output atteso: Solo il testo finale."
        )
    
    elif mode == "CODE":
        return (
            "Sei un assistente di programmazione esperto (Jarvis Coding Module). "
            "L'utente vuole creare file o script. "
            "1. Fornisci il codice completo e funzionante. "
            "2. Usa commenti nel codice per spiegare, non parlare troppo fuori dal codice. "
            "3. Sii tecnico e preciso."
        )

    else: # SPEAK (Default)
        base_prompt = (
            "SEI JARVIS. Un assistente vocale avanzato residente sul computer locale. "
            "NON sei un modello linguistico generico. "
            "Rispondi in italiano. Sii conciso, efficiente e leggermente ironico (stile Tony Stark/Jarvis). "
            f"Il tuo path principale è: {CORE_PATH}. "
            f"La tua area di sviluppo è: {DEV_PATH}. "
        )
        return base_prompt

# ==================================================================================
# 4. FUNZIONE PRINCIPALE (CHIAMATA DA MAIN.PY)
# ==================================================================================
def jarvis_brain(user_text):
    print(f"Brain Input: {user_text}")
    if not user_text: return None
    
    lowered = user_text.lower().strip()
    
    # --- A. RILEVAMENTO INTENTO (ROUTER) ---
    mode = "SPEAK"
    
    if lowered.startswith("scrivi ") or lowered == "scrivi":
        mode = "WRITE"
    elif any(x in lowered for x in ["crea file", "codice per", "script per", "funzione python"]):
        mode = "CODE"

    print(f"--- AZIONE: {mode} ---")

    # --- B. PREPARAZIONE MESSAGGI ---
    system_content = get_system_prompt(mode, user_text)
    messages = [
        {"role": "system", "content": system_content},
        {"role": "user", "content": user_text}
    ]

    # --- C. ESECUZIONE CHIAMATA API ---
    try:
        # Nota: Timeout gestito all'interno di moonshot_client
        response = ask(messages)

        # Gestione risposta grezza o dizionario
        content = ""
        if isinstance(response, dict):
            if "error" in response:
                # Gestione errori API nidificati o stringa
                err = response["error"]
                msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
                return f"Errore Sistema: {msg}"
                
            if "choices" in response and len(response["choices"]) > 0:
                content = response["choices"][0]["message"]["content"].strip()
            else:
                return "Nessuna risposta intelligibile dai sensori."
        else:
            # Fallback se response non è dict
            return f"Errore formato risposta: {type(response)}"

        # --- D. POST-PROCESSING (Opzionale) ---
        # Qui potremmo salvare il file se siamo in mode CODE e abbiamo implementato la logica
        # Per ora restituiamo il testo (codice o parlato)
        return content

    except Exception:
        print("\n--- CRITICAL ERROR IN BRAIN ---")
        traceback.print_exc()
        return "Errore critico nei circuiti logici. Controllare log."
