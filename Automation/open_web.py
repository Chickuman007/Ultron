import webbrowser
from Text_to_Speech.Custom_TTS2 import speak
from Data.data import websites
import pyautogui as gui
import time
from Automation.open_app import openapp
import requests
import json
import re
from gnews import GNews
       
def openweb(webname):
    text = webname.lower()

    urls_to_open = []

    for key, url in websites.items():
        # 🔥 exact phrase match
        if key in text:
            count = text.count(key)   # kitni baar bola user ne
            urls_to_open.extend([url] * count)

        # 🔥 extra support: "chatgpt" type inputs
        elif key.replace(" ", "") in text:
            count = text.count(key.replace(" ", ""))
            urls_to_open.extend([url] * count)

    # 🔥 open all matched URLs
    for url in urls_to_open:
        webbrowser.open(url)

    if urls_to_open:
        print("Opening...")



def close_tab():
    gui.hotkey("ctrl", "w")

def clear_all_tabs():
    gui.hotkey("ctrl","shift","w")
    speak("All tabs successfuly closed")

def add_newtab():
    gui.hotkey("ctrl","t")

#------------------------------------------------------------------------------------------------------------------------------------------------------------
chrome_open=False

def open_chrome_when_needed():
    global chrome_open
    if not chrome_open:
        openapp("chrome")
        time.sleep(2)
        chrome_open=True

    elif chrome_open:
        add_newtab()
        chrome_open=True



def search_google(text):
    words_to_remove = ["search","for","about","?","google","chrome","on"]
    words = text.lower().split()

    # 🔥 clean query properly
    filtered = [w for w in words if w not in words_to_remove]
    clean_text = " ".join(filtered)
    print(clean_text)   #  always print final result


    time.sleep(2)
    open_chrome_when_needed()
    time.sleep(3)

    #gui.hotkey("ctrl","a")  for overwriting existing query search.
    gui.write(clean_text)
    time.sleep(1)
    gui.press("enter")
#----------------------------------------------------------------------------------------------------------------------------------------

yt_open=False
def open_yt_when_needed():
    global yt_open
    if not yt_open:
        openweb("youtube")
        time.sleep(1)
        yt_open=True


def search_yt(text):
    for w in text.lower().split():
        if w in ["search","for","about","?","youtube","yt","on"]:
            text=text.replace(w,"").strip()

    open_yt_when_needed()
    time.sleep(5)
    
    gui.leftClick(800, 170)
    gui.leftClick(800, 170)
    time.sleep(0.5)

    gui.hotkey("ctrl","a")

    gui.write(text)
    time.sleep(1)
    gui.press("enter")


#--------------------------------------------------------------------------------------------------------------------------------
#News search

def news_assistant(query, count=5):
    query=re.sub(r"\b(news|about|hey ultron|ultron|please|report|give me|latest|top|list|information|article|articles|trending|from|of)\b","",query,flags=re.IGNORECASE).strip()
    print(f"query:",query)
    google_news = GNews()

    google_news.max_results = count
    google_news.language = 'en'
    google_news.country = 'IN'

    news = google_news.get_news(query)

    print(f"\n📰 Top {count} News\n")

    if not news:
        print("No news found 😅")
        return

    for i, article in enumerate(news, 1):
        speak(f"{i}. {article['title']}")


# Auto Location

def location(place_name):
    place=place_name.lower()
    webbrowser.open(f"https://www.google.com/maps/place/{place}")

def get_location(text):
    text=text.lower().strip()
    text=re.sub(r"\b(please|search|about|google|maps|on|for|location|in|ultron|can you|open)\b","",text,flags=re.IGNORECASE).strip()
    print("Location Name:",text)
    speak("Sir,You can check you current search location on map")
    location(text)