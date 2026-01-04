import requests
import json
import time
import random
import urllib.parse
import sys

# =========================
# CONFIG
# =========================

MOVIE_URL = "https://in.bookmyshow.com/movies/chennai/jana-nayagan/ET00430817"
STATE_FILE = "state.json"

WHATSAPP_API = "https://wa.mitrape.in/api/send-text"
API_KEY = "29f6ed338b5360748bd1"

MOBILE_NUMBERS = [
    "917538841178",
    "918072246726",
    "919342953325"
]

MESSAGE_TEXT = "🎬 Jana Nayagan booking is LIVE on BookMyShow!"
DELAY_BETWEEN_MESSAGES = 10  # seconds

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

# =========================
# STATE
# =========================

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"triggered": False}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

# =========================
# WHATSAPP
# =========================

def send_whatsapp_to_all():
    msg_encoded = urllib.parse.quote(MESSAGE_TEXT)

    for i, number in enumerate(MOBILE_NUMBERS, start=1):
        url = (
            f"{WHATSAPP_API}"
            f"?api_key={API_KEY}"
            f"&number={number}"
            f"&msg={msg_encoded}"
        )

        print(f"📤 Sending {i}/{len(MOBILE_NUMBERS)} → {number}")
        try:
            requests.get(url, timeout=10)
        except Exception as e:
            print("Error:", e)

        if i < len(MOBILE_NUMBERS):
            time.sleep(DELAY_BETWEEN_MESSAGES)

# =========================
# CTA CHECK
# =========================

def booking_present():
    try:
        r = requests.get(MOVIE_URL, headers=HEADERS, timeout=15)
        html = r.text.lower()

        indicators = [
            "book tickets",
            "/buytickets/",
            "booktickets"
        ]

        return any(i in html for i in indicators)
    except:
        return False

# =========================
# MAIN
# =========================

def trigger_and_exit(state):
    send_whatsapp_to_all()
    state["triggered"] = True
    save_state(state)
    print("✅ Trigger completed")
    sys.exit(0)

def main():
    state = load_state()

    if state.get("triggered"):
        print("Already triggered")
        return

    time.sleep(random.randint(2, 6))

    print("Check #1")
    if booking_present():
        trigger_and_exit(state)

    time.sleep(30)

    print("Check #2")
    if booking_present():
        trigger_and_exit(state)

    print("Not live yet")

if __name__ == "__main__":
    main()
