#Requires AutoHotkey v2.0
#SingleInstance Force

; Configurazione
TRIGGER_FILE := "C:\Temp\jarvis_trigger.txt"

; XButton1 (Tasto laterale mouse) - Scrive solo il trigger
XButton1::
{
    try {
        ; Append o creazione file vuoto per segnalare l'evento
        FileAppend("1", TRIGGER_FILE)
    } catch as e {
        ; Logging minimale su file di errore AHK se necessario, altrimenti silenzioso
        FileAppend(FormatTime() . " - Errore scrittura trigger: " . e.Message . "`n", "C:\Temp\jarvis_ahk.log")
    }
}
