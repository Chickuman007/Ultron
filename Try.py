
from Automation import Automation_brain
from Automation import Battery
from internet_checker import alert, is_Online, random_data,off_dialogues
from Text_to_Speech.Custom_TTS2 import speak
from NetHyTech_STT import listen
import time
import threading
import os 



def ultron():
    Automation_brain.clear_file()

    output_text = ""
    while True:
        try:
            with open(fr"{os.getcwd()}\\input.txt", "r") as file:

                input_text = file.read().lower().strip()

            if input_text != output_text:
                output_text = input_text


                if output_text:
                    #speak(output_text)
                    try:
                        Automation_brain.Auto_main_brain(output_text)


                    except Exception as e:
                        print(e)
                if not output_text:
                    continue
                        

        except FileNotFoundError:
            pass                        

        time.sleep(0.5)   



# threads
t1 = threading.Thread(target=listen)
t2 = threading.Thread(target=ultron)
t3 = threading.Thread(target=Battery.battery_alert)
t5=threading.Thread(target=speak,args=(random_data,))
t6=threading.Thread(target=alert,args=(random_data,))



t1.start()
t2.start()
t3.start()
t5.start()
t6.start()

t1.join()
t2.join()

t3.join()
t5.join()
t6.join()


def main():
    if is_Online():
        ultron()
    
    else:
        alert(off_dialogues)


main()


    


