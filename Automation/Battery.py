from email import message
import psutil 
import time 
from internet_checker import icon_path
from Text_to_Speech.Custom_TTS2 import speak
import plyer
from winotify import Notification,audio

icon_path=r"C:\Users\HP\OneDrive\Desktop\logo.webp"


def alert(text):
    toast=Notification(app_id='🔴 ULTRON',title="⚠️ Battery Alert!",msg=text,duration="long",icon=icon_path)

    toast.set_audio(audio.Default,loop=False)

    toast.add_actions(label="Click")
    toast.add_actions(label="Dismiss")

    toast.show()
    

def battery_alert():
    while True:
        time.sleep(10)
        battery=psutil.sensors_battery()
        percentage = int(battery.percent)

        if percentage==100:
            alert("Sir, System is fully charged, please unplug the charger.")
            #speak("Battery fully charged, Please unplug the charger !🔋")
        elif percentage<=20:
            alert("Battery level low, Please plug in the charger !🪫")
            speak("Battery level low, Please plug in the charger !🪫")


def current_battery():
    battery=psutil.sensors_battery()
    percentage = int(battery.percent)
    battery=f"sir, system currently has {percentage} percent battery"
    speak(battery)









        