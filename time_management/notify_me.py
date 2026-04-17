
from winotify import Notification, audio




icon_path=r"C:\Users\HP\OneDrive\Desktop\logo.webp"
def Alert(text):
    toast=Notification(app_id='🔴 ULTRON ',title="⚠️ Schedule Alert!",msg=text,duration="long",icon=r"C:\Users\HP\OneDrive\Desktop\logo.webp")

    toast.set_audio(audio.Default,loop=False)

    toast.add_actions(label="Click")
    toast.add_actions(label="Dismiss")

    toast.show()
