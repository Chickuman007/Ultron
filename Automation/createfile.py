import re
import os
from Text_to_Speech.Custom_TTS2 import speak

def get_ext(text):
    ext=""
    file_name=""
    text=re.sub(r'\b(ultron|hey|ok|create|make|please|a|an|file|can you|folder|named|with name|name)\b', '', text, flags=re.IGNORECASE).strip()
    #print(text)
    if "python" in text:
        ext = ".py"
        file_name=text.replace("python","").strip()
    elif "text" in text:
        ext = ".txt"
        file_name=text.replace("text","").strip()
    elif "html" in text:
        ext = ".html"
        file_name=text.replace("html","").strip()
    elif "css" in text:
        ext = ".css"
        file_name=text.replace("css","").strip()
    elif "javascript" in text:
        ext = ".js"
        file_name=text.replace("javascript","").strip()
    elif "json" in text:
        ext = ".json"
        file_name=text.replace("json","").strip()
    elif "image" in text:
        ext = ".png"
        file_name=text.replace("image","").strip()
    elif "video" in text:
        ext = ".mp4"
        file_name=text.replace("video","").strip()
    elif "audio" in text:
        ext = ".mp3"
        file_name=text.replace("audio","").strip()
    elif "pdf" in text:
        ext = ".pdf"
        file_name=text.replace("pdf","").strip()
    elif "word" in text:
        ext = ".docx"
        file_name=text.replace("word","").strip()
    elif "excel" in text:
        ext = ".xlsx"
        file_name=text.replace("excel","").strip()
    elif "ppt" in text:
        ext = ".pptx"
        file_name=text.replace("ppt","").strip()
    elif "csv" in text:
        ext = ".csv"
        file_name=text.replace("csv","").strip()
    elif "xml" in text:
        ext = ".xml"
        file_name=text.replace("xml","").strip()
    elif "config" in text:
        ext = ".ini"
        file_name=text.replace("config","").strip()
    elif "database" in text or "db" in text:
        ext = ".db"
        file_name=text.replace("databse","").strip()
    elif "zip" in text:
        ext=".zip"
        file_name=text.replace("zip","").strip()
    else:
        ext=""
        file_name=""
    return file_name,ext



def create_file(text):
    filename,ext=get_ext(text)
    print(filename,"\n",ext)

    if ext:
        if "named" in text or "with name" in text or "name":
            try:
                if ext==".json" or ext==".py" or ext==".css" or ext==".html" or ext==".js" or ext==".csv":
                    with open(f"{os.getcwd()}/{filename}{ext}","w"):
                        pass
                    speak("Sir,you can check the file in your current working directory.")
                
                else:
                    with open(fr"C:\Users\HP\OneDrive\Desktop\{filename}{ext}","w"):
                        pass
            except:
                speak("Sir,I couldn't find any file type")
        else:
            with open(fr"C:\Users\HP\OneDrive\Desktop\demo{ext}","w"):
                pass
    else:
        speak("Sir,please provide valid file type")
        pass



#------------------------------------------------------------------------------------------------------------------------------------------------------






