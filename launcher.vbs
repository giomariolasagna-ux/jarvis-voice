Set WshShell = CreateObject("WScript.Shell")

' Percorsi
pythonLauncher = "C:\Users\Administrator\JARVIS_VOICE\start_daemon.ps1"
ahkScript = "C:\Users\Administrator\JARVIS_VOICE\Jarvis.ahk"

' 1. Avvia il Daemon Python nascosto (0 = Hide)
WshShell.Run "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File """ & pythonLauncher & """", 0, False

' 2. Avvia AutoHotkey
WshShell.Run """" & ahkScript & """", 1, False