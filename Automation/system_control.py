import os
import time 
import subprocess
import pyautogui as gui
from Text_to_Speech.Custom_TTS2 import speak
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import re
import psutil



def clean_text(text):
    text=text.replace("can you","").strip()
    text=text.replace("ok so","").strip()
    text=text.replace("please","").strip()
    text=text.replace("stop","").strip()
    text=text.replace("hey ultron","").strip()
    text=text.replace("close","").strip()
    text=text.replace("systems","").strip()
    text=text.replace("app","").strip()
    text=text.replace("process","").strip()
    text=text.replace("task","").strip()
    text=text.replace("apps","").strip()
    text=text.replace("tasks","").strip()
    text=text.replace("processes","").strip()
    return text


# system controlling logic.------------------------------------------------------------------------------------
def shutdown():
    os.system("shutdown /s /t 1")

def restart():
    os.system("shutdown /r /t 1")

def sleep():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def lock():
    os.system("rundll32.exe user32.dll,LockWorkStation")

def logout():
    os.system("shutdown /l")

def close_app():
    gui.hotkey("alt","f4")



#--------------------------------------------------------------------------------------------------------------
# task manager.
def list_running_apps():
    os.system("tasklist")


def kill_process(process_name):
    try:
        subprocess.run(["taskkill", "/f", "/im", process_name], check=True)
        print(f"{process_name} closed successfully")
    except:
        print(f"Could not close {process_name}")


def kill_all_browsers():
    browsers = ["chrome.exe", "msedge.exe", "firefox.exe"]

    for b in browsers:
        kill_process(b)




#microservices logic---------------------------------------------------------------------------------------------
# 🔋 Volume
def set_volume(percent):
    percent = int(percent)
    percent = max(0, min(100, percent))

    # reset volume fast
    gui.press("volumedown", presses=50, interval=0)

    # increase fast
    steps = percent // 2
    gui.press("volumeup", presses=steps, interval=0)

    print(f"Volume set to {percent}%")


def mute():
    gui.press("volumemute")



#  Brightness (Windows)
def increase_brightness():
    os.system("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,100)")

def decrease_brightness():
    os.system("powershell (Get-WmiObject -Namespace root/WMI -Class WmiMonitorBrightnessMethods).WmiSetBrightness(1,30)")



# 🔵 Bluetooth (limited control)
def toggle_bluetooth():
    # open quick settings
    gui.hotkey("win", "a")
    time.sleep(1)

    # ⚠️ coordinates adjust karne padenge
    gui.click(1650, 560)

    time.sleep(1)
    gui.hotkey("win", "a")  # close panel

    print("Bluetooth toggled")


#wifi control.
def toggle_wifi():
    gui.hotkey("win", "a")
    time.sleep(1)

    # ⚠️ coordinates adjust karne padenge
    gui.leftClick(1500, 560)

    time.sleep(1)
    gui.hotkey("win", "a")  # close panel

    print("Wi-Fi toggled")

def toggle_airplane():
    gui.hotkey("win", "a")
    time.sleep(1)

    # ⚠️ coordinates adjust karne padenge
    gui.leftClick(1800, 560)

    time.sleep(1)
    gui.hotkey("win", "a")  # close panel

    print("airplane mode toggled")



#-------------------------ram and storage-------------------------------------------------------------------
def ram_info():
    ram=psutil.virtual_memory()
    total_ram=ram.total/(1024**3)  
    available_ram=ram.available/(1024**3)
    return f"{available_ram:.2f} ram available of Total RAM: {total_ram:.2f} GB "


def storage_info(drive):
    partition_info=psutil.disk_partitions()
    for partitions in partition_info:
        if partitions.device.startswith(drive):
            usage=psutil.disk_usage(partitions.mountpoint)
            total=usage.total/(1024**3)
            used=usage.used/(1024**3)
            free=usage.free/(1024**3)
            return (f"Drive {drive}\n"
            f"Total storage is {total:.2f} Gb\n"
            f"Used storage is {used:.2f} GB\n"
            f"Free Storage is {free:.2f} GB")
    return "Drive not availabe"


def get_info(text):
    if "ram usage" in text:
        ram=ram_info()
        speak(ram)
        print(ram)
    
    elif "storage" in text or "space" in text:
        text=re.sub(r"\b(ultron|hey|please|can you|tell me|how much|space|storage|about|is in|drive|of|what is|of)\b","",text,flags=re.IGNORECASE).strip()
        print(text.upper())

        storage=storage_info(text.upper())
        print(storage)
        speak(storage)
    else:
        pass


#  calling this function in automation brain directly.-------------------------------------------------------
def system_tasks(text):

    if "restart" in text:
        restart()
    elif "sleep" in text or "take some rest" in text :
        sleep()
    elif "shutdown" in text or  "power off" in text or "turn off" in text:
        speak("Are you sure sir, you want to turn system off")
        time.sleep(3)

        if "yes" in text:
            close_app()
            time.sleep(2)
            shutdown()
        else:
            return
            
    elif "lock" in text or 'secure' in text:
        lock()

    elif "running apps" in text or "background apps" in text:
        list_running_apps()

    elif "close all" in text or "terminate all" in text:
        kill_all_browsers()


    elif "brightness" in text:
        if "decrease" in text or "down" in text:
            decrease_brightness()
        elif "increase" in text or "up" in text:
            increase_brightness()
    
    elif "volume" in text or "set volume" in text:
        text=text.replace("%","").strip()
        text=text.replace("to","").strip()
        text=text.replace("set volume","").strip()
        text=text.replace("please","").strip()
        text=text.replace("can you ","").strip()
        text=text.replace("adjust volume","").strip()
        text=int(text)
        print(text)
        set_volume(text)

    elif "mute" in text:
        mute()
    
    elif "bluetooth" in text:
        toggle_bluetooth()

    elif any(word in text for word in ["network", "wi-fi", "internet"]):
        toggle_wifi()
    
    elif "airplane" in text:
        toggle_airplane()
    else:
        get_info(text)









