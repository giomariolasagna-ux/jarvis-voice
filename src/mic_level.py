import speech_recognition as sr
import time
import os

def clear():
    os.system("cls" if os.name == "nt" else "clear")

print("--- CALIBRAZIONE VOLUME WINDOWS ---")
print("1. Apri Impostazioni Audio di Windows -> Proprietà Dispositivo (Microfono)")
print("2. Abbassa il volume (slider) finché il valore 'RUMORE' qui sotto non è < 800-1000")
print("3. Premi CTRL+C per uscire e riprovare Jarvis.")
print("------------------------------------------------")
time.sleep(3)

r = sr.Recognizer()
mics = sr.Microphone.list_microphone_names()
mic_idx = None

# Trova LifeCam
for i, name in enumerate(mics):
    if "LifeCam" in name:
        mic_idx = i
        break

try:
    with sr.Microphone(device_index=mic_idx) as source:
        while True:
            # Misura rapida dell'energia ambientale
            r.adjust_for_ambient_noise(source, duration=0.5)
            energy = int(r.energy_threshold)
            
            # Barra visuale
            bar_len = min(50, int(energy / 300))
            bar = "#" * bar_len
            
            status = "OK (SILENZIOSO)" if energy < 1000 else "TROPPO ALTO! ABBASSA IL VOLUME!"
            
            print(f"RUMORE: {energy:5d} | {bar}  << {status}")
            
except KeyboardInterrupt:
    print("\nFinito.")
except Exception as e:
    print(f"Errore: {e}")
