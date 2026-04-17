import time
from turtle import clear
import pywhatkit as kit
import re
from datetime import datetime
from Text_to_Speech.Custom_TTS2 import speak


now=datetime.now()
hour=now.hour
minute=now.minute
seconds=now.second


def clear_file():
    with open(fr"D:\Cursor files\input.txt","w") as file:
        file.truncate(0)

def find_person(text):
    """
    Returns (phone_or_None, contact_name_key_or_None).
    contact_name_key is the dict key used to resolve the number — needed to strip the name from the message text.
    """
    # 🔹 Step 1: Name after "to" (before bare number so name is found for "send to chickuman 98...")
    if "to" in text:
        after_to = text.split("to", 1)[1].strip()

        words = after_to.split()

        # 🔥 handle single + double name
        if len(words) >= 2:
            possible_name = " ".join(words[:2]).lower()   # first 2 words
        else:
            possible_name = words[0].lower()

        contacts = {
            "chicku man": "+919671009295",
            "jaan": "+919466838549",
            "bapu": "+918685010849",
            "moti paddu": "+918295065185",
            "ashi": "+917303513277"
        }

        print("DEBUG → trying name:", possible_name)

        # 🔹 check 2-word name first
        if possible_name in contacts:
            return contacts[possible_name], possible_name

        # 🔹 fallback to 1-word
        single_name = words[0].lower()
        if single_name in contacts:
            return contacts[single_name], single_name
        return None, None

    # 🔹 Step 2: Number only
    num_match = re.search(r'\b\d{10}\b', text)
    if num_match:
        return "+91" + num_match.group(), None

    return None, None



def identify_message(text, contact_name_key=None):
    text = re.sub(r"\b(send|message|to|tu)\b", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\+91\s*\d{10}", "", text)
    text = re.sub(r'\b\d{10}\b', '', text)
    if contact_name_key:
        text = re.sub(re.escape(contact_name_key), "", text, flags=re.IGNORECASE)
    message = re.sub(r"\s+", " ", text).strip()
    return message if message else None



def send_msg():
    speak("Whom do you wanna connect sir?")
    clear_file()
    time.sleep(3)
    
    while True:
        output_text=""
        with open(fr"D:\Cursor files\input.txt","r") as file:
            input_text=file.read().lower()

        if output_text!=input_text:
            output_text=input_text
            if output_text.startswith(("send","message")):

                # 🔥 ORIGINAL TEXT USE KAR
                phone, contact_name_key = find_person(output_text)

                msg = identify_message(output_text, contact_name_key=contact_name_key)
                print(msg)

                print("person:", phone)
                print("msg:", msg)

                if phone and msg:
                    kit.sendwhatmsg_instantly(phone, msg, wait_time=15)
                    speak("Sir, sending your message on whatsapp web")
                    break

                else:
                    speak("Sir, i could not find any such person or contact on your whatsapp")



#--------------------------------------------------system  whatsapp-------------------------------------------------
import pyautogui as gui



# use on whatsapp keyword.-------------------
def open_whatsapp():
    gui.press('win')
    time.sleep(0.2)
    gui.write("WhatsApp")
    time.sleep(0.2)

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

    

def make_calls(text):
    name=text.replace("make","").strip()
    name=name.replace("call","").strip()
    name=name.replace('to',"").strip()
    name=name.replace("on whatsapp","").strip()
    name=re.sub(r"\b(ultron|please|can you)\b","",name,flags=re.IGNORECASE).strip()
    gui.write(name)
    time.sleep(1)
    
    gui.press("down")
    time.sleep(0.5)
    gui.press("enter")

    gui.leftClick(1700,100)

    time.sleep(1)
    gui.leftClick(1400,250)
    



#open chats and groups.
def open_chats(text):
    text = text.strip().lower()
    name = re.sub(r"\b(ok|okay|will|you|please|can you|on|whatsapp|ultron|open|group|chat|named|my|'s|show)\b", "", text).strip()
    print(name)

    time.sleep(2)
    gui.write(name)

    time.sleep(1)
    gui.press('enter') 

#open chat and groups.
#reply to unread msgs.
#send files and documents.

def whatsapp(text):
    if "send message" in text or "message" in text:
        open_whatsapp()
        search_bar()
        name,message=extract_name_message(text)
        print("Name:",name)
        print("Msg:",message)
        search_contact_and_msg(name,message)
    
    elif "make call" in text or "call" in text:
        open_whatsapp()
        search_bar()
        make_calls(text)

    elif "show chat" in text or "show group" in text:
        open_whatsapp()
        search_bar()
        open_chats(text)
    else:
        pass



#--------------------------sending documents-------------------------------
def normalize(name):
    name = name.lower()

    ext_map = {
        "python": "py",
        "text": "txt",
        "javascript": "js",
        "typescript": "ts",
        "pdf":"pdf",
        "word":"docx",
        "text":"txt"
    }

    for word, ext in ext_map.items():
        name = re.sub(rf"\b{word}\b", ext, name)

    name = re.sub(r"\b dot \b", ".", name)

    return name.strip()



# ---------------- SEND DOC ---------------- #
def extract_file_and_name(text):
    text = text.strip().lower()

    # Remove extra words
    text = re.sub(
        r"\b(ok|okay|will|you|please|can you|on|whatsapp|send|file|document|named)\b",
        "",
        text
    ).strip()

    # Split by "to"
    parts = re.split(r"\bto\b", text, maxsplit=1)

    if len(parts) < 2:
        return None, None

    file_part = parts[0].strip()
    contact_part = parts[1].strip()

    # Normalize file name
    file_name = normalize(file_part)
    return file_name, contact_part
    

def send_docs(text):
    file_name,contact_name = extract_file_and_name(text)
    print(file_name)
    print(contact_name)
    open_whatsapp()
    search_bar()

    search_contact_and_msg(name=contact_name,message="None")
    gui.leftClick(690,970)

    time.sleep(1)
    gui.leftClick(690,600)

    time.sleep(1)
    gui.write(file_name)
    time.sleep(1)
    gui.press("down")
    gui.press("enter")

    time.sleep(1)
    gui.press("enter")

