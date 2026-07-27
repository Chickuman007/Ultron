import time
from turtle import clear
import pywhatkit as kit
import re
from datetime import datetime
#from Text_to_Speech.Custom_TTS2 import speak


now=datetime.now()
hour=now.hour
minute=now.minute
seconds=now.second



#--------------------------------------------------system  whatsapp-------------------------------------------------
import pyautogui as gui


# use on whatsapp keyword.-------------------
def open_whatsapp():
    gui.press('win')
    time.sleep(1)
    gui.write("WhatsApp")
    time.sleep(0.5)

    gui.press('enter')


def search_bar():
    time.sleep(1)
    gui.leftClick(200,144)
    gui.leftClick(200,144)


def extract_name_message(text):
    text = text.strip().lower()
    text = re.sub(r"\b(send|message|this|please|can you|on whatsapp|ultron)\b", "", text).strip()

    parts = re.split(r"\bto\b", text, maxsplit=1)

    if len(parts) < 2:
        return None, None

    after_to = parts[1].strip()
    words = after_to.split()

    if len(words) == 0:
        return None, None

    name = words[0]
    message = " ".join(words[1:])
    return name, message





def search_contact_and_msg(name,message):
    gui.write(name)
    time.sleep(1)
    
    gui.press("down")
    time.sleep(0.5)
    gui.press("enter")

    time.sleep(1)
    gui.write(message)
    gui.press("enter")

    if not message:
        pass

    


#open chats and groups.
def open_chats(text):
    text = text.strip().lower()
    name = re.sub(r"\b(ok|okay|will|you|please|can you|on|whatsapp|ultron|open|group|chat|named|my|'s|show)\b", "", text).strip()
    print(name)

    time.sleep(2)
    gui.write(name)

    time.sleep(1)
    gui.press('enter') 



def whatsapp(text):
    if "send message" in text or "message" in text:
        open_whatsapp()
        time.sleep(2)
        search_bar()
        time.sleep(2)
        name,message=extract_name_message(text)
        print("Name:",name)
        print("Msg:",message)
        search_contact_and_msg(name,message)
    
    elif "make call" in text or "call" in text:
        open_whatsapp()
        time.sleep(2)
        search_bar()
        time.sleep(2)
        #make_calls(text)

    elif "show chat" in text or "show group" in text:
        open_whatsapp()
        time.sleep(2)
        search_bar()
        open_chats(text)
    else:
        pass





name,message=extract_name_message("send message i love you to himanshi  ")
print("name:",name)
print('message:',message)