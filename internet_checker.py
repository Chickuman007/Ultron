import random
import requests
from Data import dialogue
from winotify import Notification,audio


icon_path=r"C:\Users\HP\OneDrive\Desktop\logo.webp"


random_data=random.choice(dialogue.Dialogues)
off_dialogues=random.choice(dialogue.offline_dialogues)



def is_Online(url="https://www.google.com",timeout=3):
    try:
        response=requests.get(url,timeout=timeout)
        return response.status_code>=200 and response.status_code<300
    
    except requests.ConnectionError:
        return False



def alert(text):
    toast=Notification(app_id='🔴 ULTRON ',title="⚠️ Alert!",msg=text,duration="long",icon=icon_path)

    toast.set_audio(audio.Default,loop=False)

    toast.add_actions(label="Click")
    toast.add_actions(label="Dismiss")

    toast.show()
    

alert("Online")