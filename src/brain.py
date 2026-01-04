import sys
import os
import json
import traceback
from pathlib import Path

# ==================================================================================
# 1. CONFIGURAZIONE AMBIENTALE
# ==================================================================================
CORE_PATH = Path(r"C:\Users\Administrator\JARVIS_VOICE")
DEV_PATH = Path(r"C:\Users\Administrator\JARVIS_DEV")
IDENTITY_PATH = CORE_PATH / "jarvis_identity.json"

try:
    from src.moonshot_client import ask
except ImportError:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from src.moonshot_client import ask

def load_identity():
    try:
        if IDENTITY_PATH.exists():
            with open(IDENTITY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except:
        pass
    return {}

IDENTITY = load_identity()

# ==================================================================================
# 2. SISTEMA VISIONE E LETTURA
# ==================================================================================
def get_known_files_map():
    file_map = {}
    src_path = CORE_PATH / "src"
    if src_path.exists():
        for f in src_path.glob("*.py"):
            file_map[f.name.lower()] = f
    return file_map

def read_file_content(filename_part):
    fmap = get_known_files_map()
    for fname in sorted(fmap.keys(), key=len, reverse=True):
        if filename_part in fname:
            try:
                path = fmap[fname]
                return path.name, path.read_text(encoding="utf-8", errors="ignore")[:20000]
            except:
                return None, None
    return None, None

def get_anatomy_string():
    fmap = get_known_files_map()
    src_files = [f.name for n, f in fmap.items()]
    return f"\n[FILE VISIBILI SRC]: {', '.join(src_files)}\n"

def read_relevant_file(user_text):
    lowered = user_text.lower()
    fmap = get_known_files_map()
    for fname in sorted(fmap.keys(), key=len, reverse=True):
        if fname in lowered:
            target_path = fmap[fname]
            try:
                content = target_path.read_text(encoding="utf-8", errors="ignore")[:15000]
                return f"\n--- [CONTENUTO {target_path.name}] ---\n{content}\n--- [FINE] ---\n"
            except:
                pass
    return ""

# ==================================================================================
# 3. PROMPTS SPECIALIZZATI
# ==================================================================================
def get_system_prompt(mode, user_text, file_name="", file_content=""):
    
    if mode == "modify_system":
        return (
            f"Sei un SENIOR SOFTWARE ENGINEER. Devi riscrivere il file '{file_name}'.\n"
            "OBIETTIVO: Integrare la richiesta utente nel codice esistente.\n"
            "REGOLE ASSOLUTE:\n"
            "1. Restituisci SOLAMENTE IL CODICE PYTHON DEL FILE COMPLETO.\n"
            "2. NON usare blocchi markdown (`python). Solo testo puro.\n"
            "3. NON aggiungere commenti introduttivi o finali.\n"
            "4. Il codice deve essere pronto all'uso, con tutti gli import necessari.\n"
            f"--- CODICE ORIGINALE ---\n{file_content}\n--- FINE ---\n"
        )

    elif mode == "write":
        return "Sei un motore di scrittura. Genera solo il testo richiesto."
    
    elif mode == "create_file":
        return (
            "Sei un Coding Assistant. "
            "Rispondi SOLO con un blocco JSON: { \"filename\": \"nome.est\", \"code\": \"...\" }"
        )
        
    else: # speak
        anatomy = get_anatomy_string()
        return (
            "SEI JARVIS. Assistente vocale. "
            "Se ti chiedono di modificare il sistema, analizza ma non eseguire se non richiesto esplicitamente.\n"
            f"Path: {DEV_PATH}.\n{anatomy}\n{file_content}"
        )

# ==================================================================================
# 4. LOGICA CENTRALE
# ==================================================================================
def jarvis_brain(user_text):
    print(f"Brain Input: {user_text}")
    if not user_text: return None
    
    lowered = user_text.lower().strip()
    
    # --- RILEVAMENTO INTENTO ---
    mode = "speak"
    target_file = None
    file_content = None

    if "modifica" in lowered or "aggiungi funzionalit" in lowered:
        fmap = get_known_files_map()
        for fname in fmap.keys():
            if fname in lowered:
                mode = "modify_system"
                target_file, file_content = read_file_content(fname)
                break
    
    elif lowered.startswith("scrivi "):
        mode = "write"
    elif "crea file" in lowered:
        mode = "create_file"

    print(f"--- AZIONE: {mode} (File: {target_file}) ---")

    # Recupero contesto per Speak Mode
    extra_context = ""
    if mode == "speak":
        extra_context = read_relevant_file(user_text)

    messages = [
        {"role": "system", "content": get_system_prompt(mode, user_text, target_file, file_content or extra_context)},
        {"role": "user", "content": user_text}
    ]

    try:
        response = ask(messages)
        content = ""

        if isinstance(response, dict):
            if "error" in response:
                return {"mode": "speak", "content": f"Errore API: {response['error']}"}
            if "choices" in response and len(response['choices']) > 0:
                content = response["choices"][0]["message"]["content"].strip()
        
        # --- GESTIONE SPECIALE MODIFY ---
        # Impacchettiamo noi il JSON per evitare errori di sintassi dell'LLM
        if mode == "modify_system":
            # Pulizia eventuale markdown residuo
            clean_code = content.replace("`python", "").replace("`", "").strip()
            
            # Creazione pacchetto sicuro per Main.py
            safe_payload = json.dumps({
                "filename": f"src/{target_file}",
                "code": clean_code
            })
            
            return {
                "mode": "create_file",
                "content": safe_payload,
                "base_path": str(DEV_PATH)
            }

        return {
            "mode": mode,
            "content": content,
            "base_path": str(DEV_PATH)
        }

    except Exception:
        traceback.print_exc()
        return {"mode": "speak", "content": "Errore critico circuiti."}