#Requires AutoHotkey v2
#SingleInstance Force
Persistent

JARVIS_DIR := "C:\Users\Administrator\JARVIS_VOICE"
PYTHON_EXE := JARVIS_DIR "\.venv\Scripts\python.exe"
LOG_FILE := "C:\Temp\jarvis_ahk.log"

DirCreate "C:\Temp"
FileAppend "=== JARVIS AHK START " A_Now " ===`n", LOG_FILE

cmd := '"' PYTHON_EXE '" "src\hotkey.py"'

try {
    Run cmd, JARVIS_DIR, "Hide", &pid
    FileAppend "Python started PID=" pid "`n", LOG_FILE
} catch {
    FileAppend "Python FAILED to start`n", LOG_FILE
}

; X1 trigger  file-based (robusto)
XButton1::
{
    FileAppend "X1`n", "C:\Temp\jarvis_trigger.txt"
}
