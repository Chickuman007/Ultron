# this will be used to catch live text passed to the hosted website
# which will give the speech/sound.

import logging
import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

logging.getLogger('selenium').setLevel(logging.WARNING)

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--disable-blink-features=AutomationControlled')

Chrome_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=Chrome_service, options=chrome_options)

driver.get("https://chickuman007.github.io/TTS/")


def speak(text):
    try:
        # 🔥 CHANGE 2: textarea id changed to textInput (as per our HTML)
        element_to_type = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "textInput"))
        )
        element_to_type.clear()
        element_to_type.send_keys(text)
        print(text)

        sleep_duration = min(0.2 + len(text)//5, 5)

        # 🔥 CHANGE 3: button id changed to speakButton
        button_to_click = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "speakButton"))
        )
        button_to_click.click()

        time.sleep(sleep_duration)

    except Exception as e:
        print(e)


speak("Hello bhai, this is Jarvis speaking.")