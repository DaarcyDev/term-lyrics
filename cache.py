import os
import hashlib

CACHE_DIR = os.path.expanduser("~/.cache/term-lyrics")

def get_cache_path(artist, title):
    os.makedirs(CACHE_DIR, exist_ok=True)
    key = f"{artist}_{title}".lower().replace(" ", "_")
    key = hashlib.md5(key.encode()).hexdigest()
    return os.path.join(CACHE_DIR, f"{key}.txt")

def load_from_cache(artist, title):
    path = get_cache_path(artist, title)
    if os.path.isfile(path):
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    return None

def save_to_cache(artist, title, lyrics):
    print("save_to_cafe")
    path = get_cache_path(artist, title)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(lyrics)

