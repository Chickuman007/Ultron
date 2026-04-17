import json
import re
import requests
import os
from Automation.open_app import open_file_folder
import pyperclip
from Text_to_Speech.Custom_TTS2 import speak
import pyautogui 
import time
import docx
from PyPDF2 import PdfReader


#1st code generator
#2nd code explainer
#3rd code fix
#4th  document summariser

#code engine.⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐-
def llm_answer(query):
    prompt = f'''You are a smart AI assistant named Ultron.
created by Chickuman.
Give short, clear and factual answers in 2-3 lines.
If code is asked, return only code without explanation.
Question: {query}
Answer:
'''
    response = requests.post("http://localhost:11434/api/generate",
        json={"model": "llama3.2",
            "prompt": prompt,"temperature":0.3,"num_predict":150},stream=True  )

    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                full_response += data["response"]
    return full_response


def create_file(ext,response):
    path=f"{os.getcwd()}/DEMO{ext}"
    with open(path,"w") as file:
        for lines in response:
            file.write(lines)
    return path
    

def code(text):
    text=re.sub(r'\b(ultron|hey|ok|create|make|please|a|an|can you|give|write|me|a}for})\b', '', text, flags=re.IGNORECASE).strip()
    print(text)
    response=llm_answer(text)
    
    if "python" in text:
        ext=".py"
    elif "javascript" in text:
        ext=".js"
    elif "css" in text:
        ext= ".css"
    elif "html" in text:
        ext=".html"
    else:
        ext=".txt"
    path=create_file(ext,response)
    speak(f"Sir,you can check the code in {path} file")



#--------⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
#code Explain engine.
def llm_explain_answer(query):
    prompt = f'''You are a smart AI assistant named Ultron.
created by Chickuman.
Give short,clear and factual answers in 3-4 lines.
if explaination is asked, return proper simple explaination of code.
Question: {query}
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


def check_clipboard():
    return pyperclip.paste()

def is_code_present(code):
    return len(code.strip()) > 0


def explain_code():
    code=check_clipboard()

    if not is_code_present(code):
        #speak("Sir,i could find any code or program")
        return "clipboard empty"
    explaination=llm_explain_answer(code)
    print(explaination)
    speak(explaination)
    

#---⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐⭐
# Debug & Fix engine.

def llm_code_fix(query):
    prompt = f'''You are a smart AI assistant  and debugger.
Give short, clear and factual answers in 2-3 lines.
fix  code, return proper  corrected code and expected output.
Question: {query}
Answer:
'''

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,"temperature":0.3,"num_predict":200},stream=True  )

    full_response = ""
    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                full_response += data["response"]
    return full_response


def code_fix():
    code=check_clipboard()

    if not is_code_present(code):
        speak("Sir,i could find any code or program")
        return "clipboard empty"
    fixed_code=llm_code_fix(code)
    print(fixed_code)

    try:
        active_window = pyautogui.getActiveWindow()
        
        if active_window is None:
            print("❌ No active window found")
            return
        
        print(f"Active Window: {active_window.title}")

        editor_keywords = ["code", "visual studio", "pycharm", "sublime", "notepad","cursor"]
        if not any(keyword.lower() in active_window.title.lower() for keyword in editor_keywords):
            print("⚠️ Editor not detected, aborting...")
            return

        pyperclip.copy(fixed_code)
        time.sleep(0.5)

        active_window.activate()
        time.sleep(0.5)

        # Step 5: Move cursor (safe click center)
        pyautogui.click(active_window.left + 700, active_window.top + 700)
        time.sleep(0.5)

        # Step 6: Go to end of file
        pyautogui.hotkey("ctrl", "end")
        time.sleep(0.5)

        # Step 7: New line + Paste
        pyautogui.press("enter")
        pyautogui.hotkey("ctrl", "v")

        print("✅ Code pasted successfully")
        speak("Sir, your code has been fixed you can check your opened file.")
    except Exception as e:
        print("Error:", e)

    
#-----------------------------------------------------------------------------------------------------------------------------------------
#document summariser.
def llm_summariser(query):
    prompt = f"""
You are a smart AI document summariser named Ultron.

First, give a 1-line introduction of document starting with:
"This document is about: ..."

Then provide a clear and concise summary in 3-5 lines.

Rules:
- Keep it simple and factual
- Avoid repetition
-cover important points

Content:
{query}

Summary:
"""
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3.2",
            "prompt": prompt,
            "temperature": 0.3,
            "num_predict": 150
        },
        stream=True
    )

    full_response = ""

    for line in response.iter_lines():
        if line:
            data = json.loads(line.decode("utf-8"))
            if "response" in data:
                full_response += data["response"]

    return full_response


# ================= NORMALIZE (FOR USER INPUT) =================
def normalize(name):
    name = name.lower()

    name = re.sub(r"\s*dot\s*", ".", name)
    name = re.sub(r"\bpdf\b", "pdf", name)
    name = re.sub(r"\bword\b", "docx", name)
    name = re.sub(r"\bexcel\b", "xlsx", name)
    name = re.sub(r"\b(powerpoint|ppt)\b", ".pptx", name)

    return name.strip()


# ================= STRONG MATCH NORMALIZE =================
def normalize_for_match(name):
    return re.sub(r"[ _\-.()]", "", name.lower())


# ================= SEARCH =================
def search_file_or_folder(drive, target):
    target_norm = normalize_for_match(target)

    for root, dirs, files in os.walk(drive):
        for file in files:
            if file.endswith(".lnk"):
                continue

            file_norm = normalize_for_match(file)
            if target_norm in file_norm:
                return os.path.join(root, file)

    return None


# ================= OPEN FILE =================
def open_file_folder(text):
    drive_name = "C:\\Users\\HP\\OneDrive\\Desktop\\"

    path = search_file_or_folder(drive_name, text)
    print("Found Path:", path)

    if not path:
        print("File not found ❌")
        return None
    else:
        os.startfile(path)
        return path


# ================= READ FILE =================
def read_file(path):
    text = ""

    if path.endswith(".docx"):
        doc = docx.Document(path)
        for para in doc.paragraphs:
            text += para.text + "\n"

    elif path.endswith(".pdf"):
        reader = PdfReader(path)
        for page in reader.pages:
            text += page.extract_text() or ""

    elif path.endswith(".txt"):
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()

    else:
        return "Unsupported file format"

    return text


# ================= CLEAN USER QUERY =================
def extract_filename(query):

    query = re.sub(
        r'\b(okay|hey|ultron|file|folder|can you|summarise|summarize|please|named|name)\b','',query,flags=re.IGNORECASE)
    query = re.sub(r"\s+", " ", query).strip()
    return normalize(query)

def chunk_text(text, chunk_size=800):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

# ================= MAIN SUMMARISE =================
def summarise_document(user_input):
    filename = extract_filename(user_input)
    print("Cleaned Filename:", filename)

    path = open_file_folder(filename)
    print(path)

    text=read_file(path)
    print(text)
    
    chunks = chunk_text(text)
    print("Total Chunks:", len(chunks))

    partial_summaries = []

    for i, chunk in enumerate(chunks):
        print(f"Summarizing chunk {i+1}/{len(chunks)}...")
        
        summary = llm_summariser(chunk)
        partial_summaries.append(summary)

    final_summary = llm_summariser(" ".join(partial_summaries))

    speak(final_summary)
    print(final_summary)
