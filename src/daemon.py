import os
import time
import sys
import logging
import traceback

# Configurazione
TRIGGER_FILE = r"C:\Temp\jarvis_trigger.txt"
LOG_FILE = r"C:\Temp\jarvis_daemon.log"
RECORD_SECONDS = 5  # Durata fissa ascolto per ogni click

# Setup Logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# SETUP MODULI
logging.info("Importazione moduli...")
MODULES_OK = False

try:
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # IMPORT CORRETTI BASATI SULLA TUA SCANSIONE
    from src.stt import record_while_pressed, transcribe_audio
    from src.brain import jarvis_brain
    from src.tts import speak
    
    MODULES_OK = True
    logging.info("Moduli importati correttamente.")

except Exception as e:
    logging.critical(f"ERRORE IMPORT: {e}")
    logging.critical(traceback.format_exc())

def process_trigger():
    if not MODULES_OK:
        logging.error("Impossibile procedere: Moduli non caricati.")
        return

    logging.info("--- CICLO ATTIVATO ---")
    
    try:
        # 1. ASCOLTO (Adattato per durata fissa)
        logging.info(f"Registrazione per {RECORD_SECONDS} secondi...")
        
        start_time = time.time()
        # Questa lambda dice a stt.py di continuare finché non passano 5 secondi
        should_record = lambda: (time.time() - start_time) < RECORD_SECONDS
        
        audio_data = record_while_pressed(should_record)
        
        logging.info("Trascrizione in corso...")
        user_text = transcribe_audio(audio_data)
        
        if not user_text or not user_text.strip():
            logging.warning("Nessun testo trascritto.")
            return

        logging.info(f"Input rilevato: {user_text}")

        # 2. CERVELLO
        logging.info("Brain elaborazione...")
        response = jarvis_brain(user_text)
        logging.info(f"Risposta: {response}")

        # 3. VOCE
        if response:
            speak(response)

    except Exception as e:
        logging.error(f"ERRORE RUNTIME: {e}")
        logging.error(traceback.format_exc())

    logging.info("--- CICLO COMPLETATO ---")

def main():
    logging.info("DAEMON PRONTO.")
    
    # Reset trigger
    if os.path.exists(TRIGGER_FILE):
        try: os.remove(TRIGGER_FILE)
        except: pass

    while True:
        try:
            if os.path.exists(TRIGGER_FILE):
                try:
                    os.remove(TRIGGER_FILE)
                    process_trigger()
                except PermissionError:
                    time.sleep(0.1)
                except Exception as e:
                    logging.error(f"Errore trigger: {e}")
            
            time.sleep(0.1)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.critical(f"Loop crash: {e}")
            time.sleep(1)

if __name__ == "__main__":
    main()
