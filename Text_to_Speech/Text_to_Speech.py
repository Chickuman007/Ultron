import pyttsx3

engine=pyttsx3.init()

def  default_speak(text):
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[2].id)
    engine.say(text)
    engine.runAndWait()