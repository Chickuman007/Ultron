
import os
import time
import threading
from time_management.notify_me import Alert
from Text_to_Speech.Custom_TTS2 import speak
from datetime import datetime


def load_schedule(file_path):
    schedule = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                stripped = line.strip()
                if not stripped or "=" not in stripped:
                    continue
                
                # Tolerate both "09:12PM = text" and "09:12PM=text"
                line_time, activity = stripped.split("=", 1)
                schedule[line_time.strip()] = activity.strip()
    except Exception as e:
        print(f"Error loading schedule: {e}")
    return schedule



def check_schedule():
    file_path=r'D:\Cursor files\schedule.txt'
    last_modified = 0
    schedule = set()
    triggered = set() 

    while True:
        current_time = time.strftime("%I:%M%p")
        #print("Current Time:", current_time)
        try:
            modified = os.path.getmtime(file_path)  

            if modified != last_modified:
                last_modified = modified
                schedule = load_schedule(file_path)
                print("Loaded Schedule:", schedule)

            if current_time in schedule and current_time not in triggered:
                triggered.add(current_time)    
                text = schedule.get(current_time)
                if text:
                    t1 = threading.Thread(target=Alert, args=(text,))
                    t2 = threading.Thread(target=speak, args=(text,))
                    t1.start()
                    t2.start()

        except Exception as e:
            print(f"Error: {e}")
        time.sleep(5)

#--------------------------------------------------------------------------------------------------------------

def load_alarm(file_path):
    with open(file_path, "r") as f:
        return set(line.strip() for line in f)


def check_alarm():
    file_path = r'D:\Cursor files\alarm_data.txt'
    last_modified = 0
    schedule = set()
    triggered = set()

    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %I:%M%p")

        try:
            modified = os.path.getmtime(file_path)

            if modified != last_modified:
                last_modified = modified
                schedule = load_alarm(file_path)

        except FileNotFoundError:
            pass

        if current_time in schedule and current_time not in triggered:
            triggered.add(current_time)

            text = "Sir, this is your alarm"

            threading.Thread(target=Alert, args=(text,)).start()
            threading.Thread(target=speak, args=(text,)).start()

        time.sleep(5)
