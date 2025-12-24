Set WshShell = CreateObject("WScript.Shell")
pythonLauncher = "C:\Users\Administrator\JARVIS_VOICE\start_daemon.ps1"
ahkScript = "C:\Users\Administrator\JARVIS_VOICE\Jarvis.ahk"
WshShell.Run "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File """ & pythonLauncher & """", 0, False
WshShell.Run """" & ahkScript & """", 1, False