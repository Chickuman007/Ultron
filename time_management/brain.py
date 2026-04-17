import re
from os import getcwd
from datetime import datetime,timedelta


def parse_input(input_text):
    # 🔹 Step 1: Clean input
    input_text = input_text.replace("User:", "").strip()

    # 🔹 Step 2: Regex (robust)
    time_regex = r'(\d{1,2}:\d{2}\s?(?:a\.?m\.?|p\.?m\.?))'

    match = re.search(time_regex, input_text, re.IGNORECASE)

    if match:
        time_match = match.group()

        # 🔹 Step 3: Normalize time
        formatted_time = time_match.replace(" ", "").replace(".", "").upper()

        # 🔹 Step 4: Clean command text
        updated_input_text = re.sub(time_regex, "", input_text, flags=re.IGNORECASE)
        updated_input_text = re.sub(r'\b(at|tell me|to|remind me)\b', '', updated_input_text, flags=re.IGNORECASE).strip()

        formatted_output = f"{formatted_time} = Sir this is Your {updated_input_text} time"

        return formatted_output, formatted_time
    else:
        return "No valid time found in input", None


def save_to_file(output_text, time, filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    time_found = False
    with open(filename, 'w') as file:
        for line in lines:
            if line.startswith(time):
                file.write(output_text + '\n')
                time_found = True
            else:
                file.write(line)
        if not time_found:
            file.write(output_text + '\n')

# Example usage:

def input_manage(input_text):
    numbers=["1:","2:","3:","4:","5:","6:","7:","8:","9:"]

    output_text=input_text.replace(" p.m","P.M")
    output_text=output_text.replace(" a.m.","A.M")
    output_text=output_text.replace(" a.m","A.M") 
    output_text=output_text.replace(" p.m","P.M")   
    for n in numbers:
        pattern = r'\b' + re.escape(n)
        output_text = re.sub(pattern, f"0{n}", output_text)

    output, time = parse_input(output_text)
    if output != "No valid time found in input":
        save_to_file(output, time, r'D:\Cursor files\schedule.txt')
        print("scheduled data saved.")
    else:
        
        print(output)



#----------------------alarm------------------------------------------------------------
def parse_datetime_from_text(text):
    text = text.lower().strip()
    time_match = re.search(r'(\d{1,2}:\d{2})\s*(a\.m|p\.m|am|pm)', text)

    if not time_match:
        return None, "No valid time found"

    hour, minute = time_match.group(1).split(":")
    hour = hour.zfill(2)      # 9 → 09
    minute = minute.zfill(2)  # just safety
    ampm = time_match.group(2).replace(".", "").upper()

    time_str = f"{hour}:{minute}{ampm}"   # 05:55AM
    today = datetime.now()

    # Case 1: tomorrow
    if "tomorrow" in text:
        date_obj = today + timedelta(days=1)

    # Case 2: today
    elif "today" in text:
        date_obj = today

    # Case 3: specific date (e.g. 1 april)
    else:
        date_match = re.search(r'(\d{1,2})\s*(january|february|march|april|may|june|july|august|september|october|november|december)', text)

        if date_match:
            day = int(date_match.group(1))
            month = date_match.group(2)

            try:
                date_obj = datetime.strptime(f"{day} {month} {today.year}", "%d %B %Y")

                if date_obj < today:
                    date_obj = date_obj.replace(year=today.year + 1)

            except:
                return None, "Invalid date format"
        else:
            # Default = today
            date_obj = today


    final_datetime = date_obj.strftime("%Y-%m-%d") + " " + time_str
    return final_datetime, "Success"


def save_alarm(datetime_str, file_path):
    with open(file_path, "a") as f:
        f.write(datetime_str + "\n")


def input_manage_alarm(text):
    datetime_str, status = parse_datetime_from_text(text)

    if datetime_str:
        save_alarm(datetime_str, r'D:\Cursor files\alarm_data.txt')
        print("Alarm saved:", datetime_str)
    else:
        print(status)


'''input_manage_alarm("remind me to call someone at 5:55 a.m.")'''