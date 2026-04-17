
from Automation import Automation_brain
from Automation import Battery
from internet_checker import alert, is_Online, random_data,off_dialogues
from Text_to_Speech.Custom_TTS2 import speak
from NetHyTech_STT import listen
import time
import threading
import os 
from time_management.brain import input_manage, input_manage_alarm
from time_management.throw_alert import check_schedule,check_alarm
from Automation.weather import call_weather


def ultron():
    Automation_brain.clear_file()

    output_text = ""
    while True:
        try:
            with open(f"{os.getcwd()}\\input.txt", "r") as file:

                input_text = file.read().lower().strip()

            if input_text != output_text:
                output_text = input_text


                if output_text:
                    if "remind me" in output_text or "schedule" in output_text:

                        input_manage(output_text)   #for task scheduling or reminders.
                        Automation_brain.clear_file()
                    elif "set alarm" in output_text or "alarm for" in output_text:
                        input_manage_alarm(output_text)    #same as reminders but specifically alarms.
                        Automation_brain.clear_file()
                    
                    elif "weather" in output_text or "temperature" in output_text:
                        call_weather(output_text)

                    else:
                        try:
                            Automation_brain.Auto_main_brain(output_text)
                        except Exception as e:
                            print(e)

                if not output_text:
                    continue
                        
        except FileNotFoundError:
            pass                        

        time.sleep(0.5)   



t1 = threading.Thread(target=listen)
t2 = threading.Thread(target=ultron)
t3 = threading.Thread(target=Battery.battery_alert)
t5=threading.Thread(target=speak,args=(random_data,))
t6=threading.Thread(target=alert,args=(random_data,))
t7=threading.Thread(target=check_schedule, daemon=True)    # we didnt pass args because we used patha as a local variable.
t8=threading.Thread(target=check_alarm,daemon=True)        #same.


t1.start()
t2.start()
t3.start()
t5.start()
t6.start()
t7.start()
t8.start()

t1.join()
t2.join()
t3.join()
t5.join()
t6.join()
t7.join()
t8.join()



def main():
    if is_Online():
        ultron()
    else:
        alert(off_dialogues)

main()




    

