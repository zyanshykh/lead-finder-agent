import os
import time
from urllib.parse import quote

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"

FALLBACK = (
    "Assalam o Alaikum! Main Zayyan hoon, Karachi se web developer. "
    "Maine dekha ke {name} ki Google Maps pe achi rating hai lekin apni website nahi hai. "
    "Main aap ke liye ek simple website banata hoon jisme menu aur WhatsApp pe order aa sake. "
    "Agar aap chahein to main ek free demo bana ke dikha doon?"
)


def normalize_phone(phone):
    """03091358888 -> 923091358888. Landline (021...) pe None."""
    digits = "".join(c for c in phone if c.isdigit())
    if digits.startswith("92"):
        digits = "0" + digits[2:]
    if digits.startswith("03") and len(digits) == 11:
        return "92" + digits[1:]
    return None


def write_message(lead):
    """Gemini se chhota personalized message; fail ho to fallback."""
    fallback = FALLBACK.format(name=lead["name"])
    if not API_KEY:
        return fallback

    prompt = (
        "Roman Urdu mein ek chhota (3-4 jumle), dostana WhatsApp message likho. "
        "Bhejne wala: Zayyan, Karachi ka web developer. "
        f"Business: {lead['name']}, rating {lead['rating']} ({lead['reviews']} reviews). "
        "Baat: unki apni website nahi hai; main menu + WhatsApp ordering wali website "
        "bana sakta hoon; free demo offer karo. Koi jhoota daava mat karo. "
        "Sirf message likho, aur kuch nahi."
    )
    body = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"x-goog-api-key": API_KEY, "Content-Type": "application/json"}

    for i in range(5):
        try:
            r = requests.post(URL, json=body, headers=headers, timeout=30)
            r.raise_for_status()
            text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
            return text.strip()
        except Exception:
            if i == 4:
                return fallback
            time.sleep(2 ** (i + 1))


def whatsapp_link(phone, text):
    number = normalize_phone(phone)
    if not number:
        return None
    return f"https://wa.me/{number}?text={quote(text)}"


if __name__ == "__main__":
    from search import search_places
    from filter import filter_leads

    leads = filter_leads(search_places("restaurants in Gulshan-e-Iqbal Karachi", 20))
    for b in leads[:3]:
        msg = write_message(b)
        print("\n==", b["name"], "|", b["phone"])
        print(msg)
        print(whatsapp_link(b["phone"], msg) or "LANDLINE: call karo")
