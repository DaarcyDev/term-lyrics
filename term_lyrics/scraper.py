import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"
]

def fetch_genius(url):
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    containers = soup.find_all("div", {"data-lyrics-container": "true"})
    if not containers:
        return None
    lines = []
    for container in containers:
        for element in container.children:
            if isinstance(element, str):
                lines.append(element.strip())
            elif element.name == "br":
                lines.append("\n")
            else:
                lines.append(element.get_text(strip=True))
    return "\n".join(lines).strip()

def get_genius_url(artist, title):
    query = f"{artist} {title}"
    url = f"https://genius.com/api/search/multi?per_page=5&q={quote(query)}"

    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            return None

        data = response.json()
        sections = data.get("response", {}).get("sections", [])

        for section in sections:
            if section.get("type") == "song":
                hits = section.get("hits", [])
                if hits:
                    url = hits[0].get("result", {}).get("url")
                    return url

        return None

    except Exception as e:
        return None