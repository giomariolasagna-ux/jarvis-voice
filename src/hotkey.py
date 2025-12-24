import time
import os
import threading

TRIGGER_PATH = "C:/Temp/jarvis_trigger.txt"
LOG_PATH = "C:/Temp/jarvis_python.log"

def log(msg):
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

log("=== JARVIS PYTHON START ===")

recording = False

def recording_worker():
    global recording
    log("RECORDING WORKER STARTED")
    time.sleep(2)  # placeholder
    recording = False
    log("RECORDING WORKER FINISHED")

def check_trigger():
    return os.path.exists(TRIGGER_PATH)

while True:
    if check_trigger() and not recording:
        try:
            os.remove(TRIGGER_PATH)
        except:
            pass

        log("TRIGGER DETECTED  START RECORDING")
        recording = True
        threading.Thread(target=recording_worker, daemon=True).start()

    time.sleep(0.1)
