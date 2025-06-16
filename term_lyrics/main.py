import subprocess
import time
import uuid
import threading
from pyfiglet import Figlet
from term_lyrics.lyrics import fetch_lyrics
from term_lyrics.display import get_current_song, get_song_duration, get_song_position, render_text_with_alphabet, generate_alphabet_dict
import shutil
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
import shutil
import time
import os


current_render_id = None
alphabet_dict = generate_alphabet_dict(font="small")
console = Console()


def display_lyrics_from_current_position(lyrics: str, duration: float, position: float, render_id):
    global current_render_id

    if not lyrics:
        console.print("[red]❌ Lyrics not found.[/red]")
        return

    lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
    total_lines = len(lines)

    if total_lines == 0 or duration == 0:
        console.print("[red]❌ No lyrics to show.[/red]")
        return

    with Live(console=console, screen=True, refresh_per_second=4) as live:
        while True:
            if render_id != current_render_id:
                return

            current_pos = get_song_position()
            if current_pos > duration:
                return

            progress_ratio = current_pos / duration
            current_line = int(progress_ratio * total_lines)
            current_line = max(0, min(current_line, total_lines - 1))

            window_start = max(0, current_line - 2)
            window_end = min(total_lines, current_line + 3)
            lines_to_display = lines[window_start:window_end]

            rendered_lines = []

            for idx, line in enumerate(lines_to_display, start=window_start):
                art = render_text_with_alphabet(line, alphabet_dict)

                if idx == current_line:
                    text = Text(art, style="bold black")
                    panel = Panel(text, expand=True, padding=(0, 0))
                else:
                    text = Text(art, style="dim white")
                    panel = Panel(text, style="grey37", expand=True, padding=(0, 0))

                rendered_lines.append(panel)

            # rendered_lines.append(
            #     Text(f"⏱️ {round(current_pos)}s / {int(duration)}s", style="cyan", justify="center")
            # )

            group = Group(*rendered_lines)
            live.update(group)

            time.sleep(0.8)
            
def main():
    global current_render_id
    last_song = None
    lyrics_thread = None

    while True:
        artist, title = get_current_song()
        if not artist or not title:
            print("⏸️ No song is playing on Spotify...")
            time.sleep(1)
            continue

        song_id = f"{artist} - {title}"
        if song_id != last_song:
            print(f"\n🎵 {title} — {artist}")
            lyrics = fetch_lyrics(artist, title)
            duration = get_song_duration() or 180
            position = get_song_position()

            current_render_id = str(uuid.uuid4())

            if lyrics_thread and lyrics_thread.is_alive():
                print("🔁 Canción nueva: interrumpiendo letra anterior...")

            lyrics_thread = threading.Thread(
                target=display_lyrics_from_current_position,
                args=(lyrics, duration, position, current_render_id),
                daemon=True
            )
            lyrics_thread.start()

            last_song = song_id

        time.sleep(2)
