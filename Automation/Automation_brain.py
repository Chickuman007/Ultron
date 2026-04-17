
from Automation.open_app import openapp,open_file_folder,delete_file_folders,execute_organiser
from Automation.open_web import  openweb,clear_all_tabs,close_tab,search_yt,add_newtab,search_google,news_assistant,get_location
import pyautogui as gui
from Automation.play_music import pause, play_music_spotify,play_music_yt
from Automation.AI_Response import Ai_response,llm_search
from Automation.Battery import current_battery
from Automation.system_control import system_tasks
from Automation.createfile import create_file
from Automation.code_engine import code,explain_code,code_fix,summarise_document
import re
from Automation.whatsapp_auto import send_msg,whatsapp,send_docs
from Text_to_Speech.Custom_TTS2 import speak

def close():
    gui.hotkey('alt','f4')

def clear_file():
    with open(r"D:\Cursor files\input.txt",'w') as file:
        file.truncate(0)


def open_brain(text):      #function for working on apps,website and files/directories.
    if "website" in text or "open website named" in text:
        text=text.replace("can you open","").strip()
        text=text.replace("ok","").strip()
        text=text.replace("please open","").strip()
        text=text.replace("open website named","").strip()
        text=text.replace("website","").strip()
        text=text.replace("hey ultron","").strip()
        openweb(text)

    elif "file" in text or "folder" in text:
        text=text.lower().replace("can you open","").strip()
        text=text.replace("open","").strip()
        text=text.replace("ok","").strip()
        text=text.replace("please open","").strip()
        text=text.replace("hey ultron","").strip()
        text=text.replace("file","").strip()
        text=text.replace("folder","").strip()
        text=text.replace("run","").strip()
        text=text.replace("please","").strip()
        text=text.replace("named","").strip()
        text=text.replace("by","py").strip()
        open_file_folder(text)
                           
    else:
        text=text.replace("hey ultron","").strip()
        text=text.replace("can you open",'').strip()
        text=text.replace("please",'').strip()
        text=text.replace("open","").strip()
        text=text.replace("start","").strip()
        text=text.replace("run","").strip()
        text=text.replace("ok open","").strip()
        openapp(text)



def Auto_main_brain(text:str):
    print(text)
    if "open" in text:
        open_brain(text)
    elif "close" in text  or "exit" in text:
        close()

    elif "delete file named" in text or "delete" in text:
        text = re.sub(r'\b(okay|hey|ultron|file|folder|can you|delete|okay|please|named|name|)\b','',text,flags=re.IGNORECASE).strip()
        delete_file_folders(text)
    elif "organise" in text or "organised" in text  or "organize" in text or "organized" in text:
        execute_organiser(text)
    elif "create" in text or "make" in text:
        create_file(text) 
    
    elif any(word in text.lower() for word in ["code","program","class","object","function","method"]):
        if "fix" in text or "debug" in text:
            code_fix()
        elif "summarize" in text or "explain" in text or "summarise" in text:
            explain_code()
        else:
            code(text)

    elif "summarise" in text or "summarize" in text :
        summarise_document(text)
    elif "news" in text or "articles" in text:
        news_assistant(query=text)

    elif "play" in text and "youtube" in text:
        play_music_yt(text)
    
    elif "on spotify" in text: 
        play_music_spotify(text)
    elif "pause" in text:
        pause()
    

    elif "clear tab" in text or "clear window" in text :
        close_tab()
    elif "clear all" in text or "windows" in text or "tabs" in text or "taps" in text:
        clear_all_tabs()
    elif "new tab" in text:
        add_newtab()


    elif "search" in text:
        if "google" in text:
            search_google(text)
        elif "youtube" in text:
            search_yt(text) 
        elif "on maps" in text or "location" in text:
            get_location(text)


    elif "web" in text or "on web" in text:
        speak("Whom do you wanna connect sir?")
        send_msg()
    elif "on whatsapp" in text:
        whatsapp(text)
    elif "send file" in text or "send" in text:
        send_docs(text)
    

    elif "ultron" in text:
        llm_search(text)
    
    elif any(word in text for word in [
        "shutdown", "restart", "sleep", "lock",
        "power off", "turn off", "terminate","stop","kill",
        "close all", "running apps","background","brightness","volume","Wi-Fi","network","bluetooth","ram","storage","space" ]):
        system_tasks(text)
        return 

    elif "battery" in text or "battery status" in text:
        current_battery()
    

    else:
        Ai_response(text)
    

        
    
    

    
        
    












