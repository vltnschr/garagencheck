import os
import re
import requests
from pathlib import Path

URL = "https://www.oevw.at/garagen"
NTFY_TOPIC = os.environ["NTFY_TOPIC"]
PATTERN = re.compile(r"\b1110\s+Wien", re.IGNORECASE)
STATE = Path(__file__).with_name("last_state.txt")

def main():
    html = requests.get(
        URL, timeout=30,
        headers={"User-Agent": "Mozilla/5.0 (Garagen-Check, privat)"}
    ).text

    found = PATTERN.search(html) is not None
    was_found = STATE.exists() and STATE.read_text() == "1"

    if found and not was_found:
        requests.post(
            f"https://ntfy.sh/{NTFY_TOPIC}",
            data="Garage in 1110 Wien verfügbar!".encode("utf-8"),
            headers={"Title": "ÖVW Garagen", "Click": URL,
                     "Priority": "high", "Tags": "car"},
            timeout=30,
        )
    STATE.write_text("1" if found else "0")

if __name__ == "__main__":
    main()
