#Requires AutoHotkey v2.0
#SingleInstance Force
TRIGGER_FILE := "C:\Temp\jarvis_trigger.txt"
XButton1::
{
    try {
        FileAppend("1", TRIGGER_FILE)
    } catch as e {
    }
}
