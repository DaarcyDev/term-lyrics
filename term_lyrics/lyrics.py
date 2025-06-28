from .cache import load_from_cache, save_to_cache
from .scraper import get_genius_url, fetch_genius
import concurrent.futures
import requests
from bs4 import BeautifulSoup
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.google.com/"
}
def fetch_lyrics(artist, title):
    cached = load_from_cache(artist, title)
    if cached:
        return cached

    lyrics = None

    def query_lyrics_ovh():
        url = f"https://api.lyrics.ovh/v1/{artist}/{title}"
        try:
            r = requests.get(url, timeout=5)
            return r.json().get("lyrics") if r.status_code == 200 else None
        except:
            return None



    def query_lyrist():
        url = f"https://lyrist.vercel.app/api/{artist}/{title}"
        try:
            r = requests.get(url, timeout=5)
            return r.json().get("lyrics") if r.status_code == 200 else None
        except:
            print("Error searching in lyrist")
            return None

    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(fn) for fn in (query_lyrics_ovh, query_lyrist)]
        for f in concurrent.futures.as_completed(futures):
            lyrics = f.result()
            if lyrics:
                break
    if not lyrics:

        url = get_genius_url(artist, title)
        if url:
            lyrics = fetch_genius(url)
            if lyrics:
                save_to_cache(artist, title, lyrics)
                return lyrics
            else:
                print("No lyrics found on Genius.")
                
    else:
        save_to_cache(artist, title, lyrics)
        return lyrics
    return "❌ Lyrics not found on any provider."

