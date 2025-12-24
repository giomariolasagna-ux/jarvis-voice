from pynput import mouse

def on_click(x, y, button, pressed):
    if pressed:
        print(button)

print("Premi i tasti del mouse (laterali inclusi). CTRL+C per uscire.")
with mouse.Listener(on_click=on_click) as listener:
    listener.join()
