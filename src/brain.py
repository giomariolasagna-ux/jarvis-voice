import json
from pathlib import Path
from src.moonshot_client import ask

IDENTITY_PATH = Path(r"C:\Users\Administrator\JARVIS_VOICE\jarvis_identity.json")

def load_identity():
    try:
        with open(IDENTITY_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

IDENTITY = load_identity()

SELF_PATH = Path(IDENTITY["self_path"])
MUTABLE_PATH = Path(IDENTITY["mutable_path"])

def is_path_allowed(path: Path) -> bool:
    try:
        path = path.resolve()
        return MUTABLE_PATH in path.parents or path == MUTABLE_PATH
    except Exception:
        return False

def create_file_in_v2(filename: str, content: str):
    target = MUTABLE_PATH / filename

    if not is_path_allowed(target):
        return False, "Percorso non consentito."

    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as f:
            f.write(content)
        return True, str(target)
    except Exception as e:
        return False, str(e)

def jarvis_brain(user_text):
    lowered = user_text.lower().strip()

    # COMANDO CREAZIONE FILE
    if lowered.startswith("crea file"):
        messages = [
            {
                "role": "system",
                "content": (
                    "Sei Jarvis. L'utente ti chiede di creare un file. "
                    "Rispondi SOLO con JSON valido nel formato:\n"
                    "{ \"filename\": \"nomefile.txt\", \"content\": \"contenuto del file\" }"
                )
            },
            {
                "role": "user",
                "content": user_text
            }
        ]

        response = ask(messages)

        try:
            data = json.loads(response)
            ok, info = create_file_in_v2(data["filename"], data["content"])
            if ok:
                return {
                    "mode": "speak",
                    "text": f"File creato in {info}"
                }
            else:
                return {
                    "mode": "speak",
                    "text": f"Errore: {info}"
                }
        except Exception:
            return {
                "mode": "speak",
                "text": "Non sono riuscito a creare il file."
            }

    # SCRITTURA TESTO (già esistente)
    messages = [
        {
            "role": "system",
            "content": (
                "Sei Jarvis, assistente vocale locale. "
                "Se l'utente chiede di SCRIVERE testo, "
                "rispondi SOLO con il testo da scrivere."
            )
        },
        {
            "role": "user",
            "content": user_text
        }
    ]

    response = ask(messages)

    if lowered.startswith("scrivi e invia"):
        return {"mode": "write_send", "text": response.strip()}

    if lowered.startswith("scrivi"):
        return {"mode": "write", "text": response.strip()}

    return {"mode": "speak", "text": response}
