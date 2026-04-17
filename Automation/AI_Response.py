import wikipedia
from Data import Responses
from Text_to_Speech.Custom_TTS2 import speak
from ddgs import DDGS
import requests
import json


def llm_answer(query):
    prompt=f'''You are a smart AI asssitant.
    created by Chickuman.
    you can perform music playing,system tasks,query answering and automation tasks.
    Give short,clear and factual answers.
    Limit response to 2-3 lines only.
    Question:{query}
    Answer:
    '''
    
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,"temperature":0.3,"num_predict":150},stream=True  )

    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                full_response += data["response"]

    return full_response


'''
def web_search(query):
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results=1)

            for r in results:
                answer = r["body"][:250]
                speak(answer)
                break
        #speak("Sorry sir, I couldn't find anything.")

    except Exception:
        speak("Web search failed.")
        
'''


def Ai_response(text:str):
    text = text.lower().strip()

    # 1️⃣ Exact match (highest priority)
    if text in Responses.responses:
        speak(Responses.responses[text])
        return True

    # 2️⃣ Controlled partial match (safe)
    for question in Responses.responses:
        if text.startswith(question):   # 🔥 better than "in"
            speak(Responses.responses[question])
            return True

    return False





#main QNA logic---------------------------------------------------------------------------
def llm_search(query:str):
    query=query.lower().strip()
    query=query.replace("ultron","").strip()
    query=query.replace("Ultron","").strip()
    try:
        answer = llm_answer(query)
        if answer:
            speak(answer)
    
    except Exception as e:
        speak("Sir,I could not find any result")



      







