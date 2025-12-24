import speech_recognition as sr
import json

print("\n--- CONFIGURAZIONE MICROFONO ---")
mics = sr.Microphone.list_microphone_names()

print("Microfoni trovati:")
for i, mic_name in enumerate(mics):
    print(f"[{i}] {mic_name}")

print("\n")
index = input("Inserisci il NUMERO del microfono LifeCam (o quello che vuoi usare): ")

try:
    mic_index = int(index)
    config = {"mic_index": mic_index}
    
    with open("C:\\Users\\Administrator\\JARVIS_VOICE\\mic_config.json", "w") as f:
        json.dump(config, f)
        
    print(f" Configurazione salvata! Userò il microfono [{mic_index}]")
except:
    print(" Numero non valido. Userò il Default.")
