import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, unquote, quote
import urllib.parse
import re
import random
import time
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
    # print("+--+"*10)
    # print("fetch_genius url:", url)
    # try:
    response = requests.get(url, headers=HEADERS)
    # print("'response", response)
    
    if response.status_code != 200:
        # print(f"Error fetching Genius page: {response.status_code}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    containers = soup.find_all("div", {"data-lyrics-container": "true"})
    if not containers:
        # print("No se encontró letra en Genius.")
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
    # print("quote(query):", quote(query))
    url = f"https://genius.com/api/search/multi?per_page=5&q={quote(query)}"
    # print("url:", url)
    # print(f"🔍 Buscando en Genius API: {query}")

    try:
        response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            # print(f"❌ Error al buscar en Genius API: {response.status_code}")
            return None

        data = response.json()
        sections = data.get("response", {}).get("sections", [])

        for section in sections:
            if section.get("type") == "song":
                hits = section.get("hits", [])
                if hits:
                    url = hits[0].get("result", {}).get("url")
                    # print(f"🔗 URL encontrada en Genius API: {url}")
                    return url

        # print("❌ No se encontró canción en Genius API.")
        return None

    except Exception as e:
        # print(f"⚠️ Error al hacer request a Genius API: {e}")
        return None