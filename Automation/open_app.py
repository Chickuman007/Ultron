import pyautogui as gui
import subprocess
import time
import os
import re
import shutil
from Text_to_Speech.Custom_TTS2 import speak




# open system apps
def openapp(text: str):
    try:
        subprocess.run(text)
    except:
        gui.press('win')
        time.sleep(0.2)

        gui.write(text)
        time.sleep(0.2)

        gui.press('enter')



def normalize(name):
    if "dot" in name:
        name=name.replace(" dot ", ".").strip()
    if "python" in name :
        name=name.replace("python", "py").strip()
    if "java" in name:
        name=name.replace("java", "java").strip()
    if "cpp" in name:
        name=name.replace("cpp", "cpp").strip()
    if "c" in name:
        name=name.replace("c", "c").strip()
    if "js" in name:
        name=name.replace("js", "js").strip()
    if "ts" in name:
        name=name.replace("ts", "ts").strip()
    if "html" in name:
        name=name.replace("html", "html").strip()
    if "css" in name:
        name=name.replace("css", "css").strip()
    if "json" in name:
        name=name.replace("json", "json").strip()
    if "md" in name:
        name=name.replace("md", "md").strip()
    if "text" in name:
        name=name.replace("text", "txt").strip()
    if "csv" in name:
        name=name.replace("csv", "csv").strip()
    return re.sub(r"[ _\-.]", "", name.lower())
    


def search_file_or_folder(drive, target):
    target_norm = normalize(target)

    for root, dirs, files in os.walk(drive):
        for folder in dirs:
            if target_norm in normalize(folder):
                return os.path.join(root, folder)

        for file in files:
            if file.endswith(".lnk"):   # skip shortcuts
                continue
            if target_norm in normalize(file):
                return os.path.join(root, file)
    return None



#open any file from root dir.
def open_file_folder(text):

    drive_name="D://"
    path = search_file_or_folder(drive_name, text)
    print(path)
    
    if not path:
            print("File not found")
            return
    else:
        os.startfile(path)
        return path
    


# delete any file from root dir.
def delete_file_folders(text):
    path = search_file_or_folder(r"D://", text)
    if path:
        if os.path.isfile(path):
            print("Deleting:",path)
            os.remove(path)
            print("deleted")
            #speak("File deleted successfuly, Sir")

        elif os.path.isdir(path):
            shutil.rmtree(path)
            #speak("Folder deleted successfuly, Sir")

    else:
        print("File/Folder not found")




def clean_command(text):
    words_to_remove = {
        "please","organize","organise","organized","organised",
        "folder","file","this","named","arrange","can","you","with name"
    }

    words = text.lower().split()
    filtered_words = [w for w in words if w not in words_to_remove]
    return " ".join(filtered_words)


FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp", ".svg", ".heic"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf",".ppt", ".pptx", ".xls", ".xlsx", ".csv",".odt", ".ods", ".odp", ".md"],
    "Videos": [ ".mp4", ".mkv", ".avi", ".mov", ".wmv",".flv", ".webm", ".mpeg", ".mpg", ".3gp"],
    "Music": [".mp3", ".wav", ".aac", ".flac",".ogg", ".m4a", ".wma"],
    "Archives": [ ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"],
    "Programs": [".exe", ".msi", ".bat", ".cmd", ".sh"],
    "Code": [".py", ".java", ".cpp", ".c", ".js", ".ts",".html", ".css", ".json", ".xml", ".yaml", ".yml"],
    "Databases": [".db", ".sqlite", ".sql", ".mdb"],
    "Fonts": [".ttf", ".otf", ".woff", ".woff2"],
    "Design": [".psd", ".ai", ".xd", ".fig", ".sketch"]
}



def get_category(ext):
    for filetype,extensions in FILE_TYPES.items():
        if ext in extensions:
            return filetype
    return "others"


def organize_files(path):
    for subfiles in os.listdir(path):
        subfile_path=os.path.join(path,subfiles)
        if os.path.isdir(subfile_path):         #this will skip the subdirectories and only select the files.
            continue

        #splitting file extensions from file to separate them
        filename,extensions=os.path.splitext(subfiles)
        if extensions:
            extension=extensions.lower()
            category=get_category(ext=extension)

        directory_name=category.upper()       #naming each diffferent file directory before creating actual.
        if not directory_name:
            directory_name="others"

        new_directory=os.path.join(path,directory_name)
        os.makedirs(new_directory,exist_ok=True)

        #move files to new directory:
        shutil.move(src=subfile_path,dst=os.path.join(new_directory,subfiles))
        print(f"Moved Files{subfiles}--> {new_directory}")



def execute_organiser(text):
    text=clean_command(text)
    print("text feeded:",text)

    # open file folder function will use search_file_folder()
    path=open_file_folder(text)   # will search and return path of the file
    if not path:
        print("File not found ⚠️")
        return

    organize_files(path)



