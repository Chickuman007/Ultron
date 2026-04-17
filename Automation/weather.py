from bs4 import BeautifulSoup
import requests
import re
from Text_to_Speech.Custom_TTS2 import speak


def _tag_text(tag):
    """Return stripped text from a BeautifulSoup tag, or None if missing."""
    return tag.get_text(strip=True) if tag is not None else None


def _weather_from_wttr(address, headers):
    """Fallback: wttr.in JSON API (no key). Google markup often missing for scripted requests."""
    try:
        loc = address.strip().replace(" ", "+")
        url = f"https://wttr.in/{loc}?format=j1"
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        data = r.json()
        cc = data["current_condition"][0]
        area = data["nearest_area"][0]
        name = area["areaName"][0]["value"]
        country = area["country"][0]["value"]
        desc = cc["weatherDesc"][0]["value"]
        temp = cc["temp_C"]
        place = f"{name}, {country}"
        return (place, desc, f"{temp}°C")
    except (requests.RequestException, KeyError, IndexError, ValueError, TypeError):
        return None


def get_weather_by_add(address):
    search_url = f"https://www.google.com/search?q=weather+{address.replace(' ', '+')}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    response = requests.get(search_url, headers=headers, timeout=15)

    if response.status_code != 200:
        fallback = _weather_from_wttr(address, headers)
        return fallback if fallback else "Error fetching weather data"

    soup = BeautifulSoup(response.text, "html.parser")

    location_tag = _tag_text(soup.find("div", attrs={"id": "wob_loc"}))
    time_tag = _tag_text(soup.find("div", attrs={"id": "wob_dts"}))
    weather_tag = _tag_text(soup.find("span", attrs={"id": "wob_dc"}))
    temp_tag = _tag_text(soup.find("span", attrs={"id": "wob_tm"}))

    if all((location_tag, time_tag, weather_tag, temp_tag)):
        return (location_tag, weather_tag, f"{temp_tag}°C")

    fallback = _weather_from_wttr(address, headers)
    return fallback if fallback else (
        "Could not read Google's weather widget (page layout or blocking). "
        "wttr.in fallback also failed."
    )


def call_weather(address):
    address = re.sub(
        r"\b(hey ultron|what's|temperature|weather|of|about|report|from|how is|in|tell me|about the|the|current|)\b",
        "",
        address,
        flags=re.IGNORECASE,
    ).strip()
    result = get_weather_by_add(address)

    if isinstance(result, tuple) and len(result) == 3:
        place, weather, temperature = result
        line = (
            f'The current weather of {place} is {weather} with a temperature of {temperature}.'
        )
        speak(f"Sir,{line}")
        

    print(result)



#call_weather("tell me about the weather of Delhi ")
# API_KEY="5bbbb951fef660fed1ef0f651fb90687"
