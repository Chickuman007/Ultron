import webbrowser
import pywhatkit as pw
import pyautogui as ui
import time
import urllib.parse


def play_music_yt(song_name:str):
    song_name=song_name.lower()
    time.sleep(2)
    song_name = song_name.replace("play", "").strip()
    song_name=song_name.replace("please",'').strip()
    song_name=song_name.replace("ok",'').strip()
    song_name=song_name.replace("my",'').strip()
    song_name = song_name.replace("on youtube", "").strip()
    song_name = song_name.replace("can you please", "").strip()
    song_name = song_name.replace("song", "").strip()
    song_name = song_name.replace("hey vision", "").strip()
    song_name=song_name.replace("music",'').strip()   
    song_name=song_name.replace("i want to listen","").strip()

    time.sleep(2)
    pw.playonyt(song_name)




def play_music_spotify(song_name: str):
    song_name = song_name.lower()
    song_name = song_name.replace("play", "").strip()
    song_name=song_name.replace("please",'').strip()
    song_name=song_name.replace("ok",'').strip()
    song_name=song_name.replace("my",'').strip()
    song_name = song_name.replace("on spotify", "").strip()
    song_name = song_name.replace("can you please", "").strip()
    song_name = song_name.replace("song", "").strip()
    song_name = song_name.replace("hey vision", "").strip()
    song_name=song_name.replace("music",'').strip() 
    song_name=song_name.replace("i want to listen","").strip()

    


    query = urllib.parse.quote(song_name)
    url = f"https://open.spotify.com/search/{query}"

    webbrowser.open(url)
    time.sleep(3)
    ui.hotkey("ctrl","shift","l")
    time.sleep(3)
    ui.write(song_name)
    time.sleep(2)
    ui.leftClick(610,630)
    ui.leftClick(610,630)

def pause():
    ui.leftClick(610,630)



