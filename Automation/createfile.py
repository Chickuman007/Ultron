import re
import os
from Text_to_Speech.Custom_TTS2 import speak
import requests
import json
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from pathlib import Path


# ---------------- FILE TYPES ---------------- #

FILE_TYPES = {
    "python": ".py",
    "text": ".txt",
    "html": ".html",
    "css": ".css",
    "javascript": ".js",
    "js": ".js",
    "json": ".json",
    "image": ".png",
    "video": ".mp4",
    "audio": ".mp3",
    "pdf": ".pdf",
    "word": ".docx",
    "excel": ".xlsx",
    "ppt": ".pptx",
    "csv": ".csv",
    "xml": ".xml",
    "config": ".ini",
    "zip": ".zip"
}


# ---------------- GET FILE INFO ---------------- #

def get_file_info(text):

    original_text = text.lower()

    # Find extension
    ext = ""

    for key, value in FILE_TYPES.items():
        if key in original_text:
            ext = value
            text = re.sub(rf"\b{key}\b", "", text, flags=re.IGNORECASE)
            break

    # Remove unnecessary words
    text = re.sub(r'\b(create|make|please|a|an|file|named|with|name|called|can you|hey|ok)\b','',text,flags=re.IGNORECASE).strip()

    # Clean extra spaces
    print("text:",text)
    file_name = " ".join(text.split())

    return file_name, ext


# ---------------- CREATE FILE ---------------- #

def create_file(text):
    filename, ext = get_file_info(text)

    print("Filename:", filename)
    print("Extension:", ext)

    # Invalid type
    if not ext:
        print("Please provide a valid file type.")
        return

    # If filename exists -> current working directory
    if filename:

        full_path = os.path.join(os.getcwd(), f"{filename}{ext}")

    # If filename NOT exists -> Desktop with demo name
    else:

        full_path = fr"C:\Users\HP\OneDrive\Desktop\demo{ext}"


    # Create file
    with open(full_path, "w") as f:
        pass

    print(f"File created successfully:\n{full_path}")



#------------------------------------------------------------------------------------------------------------------------------------------------------




def generate_content(query):
    prompt=f'''You are Ultron a smart AI content writer.
    you can write blogs,summary,notes,question answers and emails.
    Give short,clear and factual answers.
    for csv: use different columns to describe data.
    for documets: use proper headings and title.
    for resume: use proper cv srtucture ,format and spacing 
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




FILE_INTENTS = {
    "email": {
        "keywords": ["mail", "email", "gmail", "compose"],
        "ext": ".txt",
        "name": "Email"
    },

    "qna": {
        "keywords": ["question", "questions", "qna", "interview", "quiz","resume","cover letter"],
        "ext": ".pdf",
        "name": "Q&A"
    },

    "document": {
        "keywords": ["summary", "blog", "content", "article", "notes", "essay","acknowledgement","report","something","about"],
        "ext": ".docx",
        "name": "Document"
    },

    "data": {
        "keywords": ["csv", "table", "data", "dataset", "spreadsheet"],
        "ext": ".csv",
        "name": "Data"
    }
}


def get_ext(query):
    query = query.lower()

    for intent, config in FILE_INTENTS.items():
        if any(keyword in query for keyword in config["keywords"]):
            return config["ext"], config["name"]
    return ".txt", "New File"



def save_file(query):
    query=re.sub(r"\b(please|can you|ultron|hey)\b","",query,flags=re.IGNORECASE).lower().strip()
    content = ""
    ext, file_name = "", ""

    try:
        content = generate_content(query)
        ext, file_name = get_ext(query)
    except Exception as e:
        print(e)
        return

    if not content:
        speak("Sorry Sir,I couldn't generate any content")
        print("Sorry Sir,I couldn't generate any content")
        return

    path = fr"C:\Users\HP\OneDrive\Desktop\{file_name}"

    if ext == ".docx":
        from docx import Document
        doc = Document()
        doc.add_paragraph(content)
        doc.save(f"{path}{ext}")


    elif ext == ".pdf":
        doc = SimpleDocTemplate(path)
        styles = getSampleStyleSheet()
        story = [Paragraph(content, styles["Normal"])]
        doc.build(story)


    elif ext == ".csv":
        import csv
        with open(f"{path}{ext}", "w", newline="") as file:
            writer = csv.writer(file)
            for line in content.split("\n"):
                writer.writerow([line])

    else:
        with open(f"{path}{ext}", "w", encoding="utf-8") as file:
            file.write(content)

    print("Sir,File saved successfuly, you can check your desktop file")
    speak("Sir,File saved successfuly, you can check your desktop file")

