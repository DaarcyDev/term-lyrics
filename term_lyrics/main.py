import subprocess
import time
import uuid
import threading
import sys
import os
import argparse
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from rich.console import Group
from term_lyrics.lyrics import fetch_lyrics
from term_lyrics.display import (
    get_current_song,
    get_song_duration,
    get_song_position,
    render_text_with_alphabet,
    generate_alphabet_dict,
    install_custom_fonts
)

console = Console()
current_render_id = None

def display_lyrics_from_current_position(lyrics: str, duration: float, position: float, render_id, alphabet_dict, style, surround_lines=3, current_line_color="white", surrounding_lines_color="black"):
    global current_render_id
    
    if not lyrics:
        console.print("[red]❌ Lyrics not found.[/red]")
        return

    lines = [line.strip() for line in lyrics.split('\n') if line.strip()]
    total_lines = len(lines)

    if total_lines == 0 or duration == 0:
        console.print("[red]❌ No lyrics to show.[/red]")
        return

    if style != 'False':
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

                window_start = max(0, current_line - surround_lines)
                window_end = min(total_lines, current_line + surround_lines + 1)
                lines_to_display = lines[window_start:window_end]

                rendered_lines = []

                for idx, line in enumerate(lines_to_display, start=window_start):
                    if alphabet_dict:
                        art = render_text_with_alphabet(line, alphabet_dict)
                    else:
                        art = line  # texto plano

                    print(f"Rendering line {idx}: {art}")  # Debugging output
                    style = f"bold {current_line_color}" if idx == current_line else f"dim {surrounding_lines_color}"
                    text = Text(art, style=style)
                    panel = Panel(text, expand=True, padding=(0, 0))
                    rendered_lines.append(panel)

                # rendered_lines.append(Text(f"⏱️ {round(current_pos)}s / {int(duration)}s", style="cyan", justify="center"))
                group = Group(*rendered_lines)
                live.update(group)
                time.sleep(0.8)
    else:
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

                window_start = max(0, current_line - surround_lines)
                window_end = min(total_lines, current_line + surround_lines + 1)
                lines_to_display = lines[window_start:window_end]

                rendered_lines = []

                for idx, line in enumerate(lines_to_display, start=window_start):
                    if alphabet_dict:
                        art = render_text_with_alphabet(line, alphabet_dict)
                    else:
                        art = line  # texto plano

                    style = "bold black" if idx == current_line else "dim white"
                    text = Text(art, style=style)
                    panel = Panel(art, expand=True, padding=(0, 0))
                    rendered_lines.append(panel)

                # rendered_lines.append(Text(f"⏱️ {round(current_pos)}s / {int(duration)}s", style="cyan", justify="center"))
                group = Group(*rendered_lines)
                live.update(group)
                time.sleep(0.8)

def main():
    parser = argparse.ArgumentParser(description="🎵 Term-Lyrics: Synchronized lyrics from Spotify")
    parser.add_argument("--font", type=str, default="Tubes-Regular", help="Name of the .flf font (without extension) or 'none' for plain text")
    parser.add_argument("--style", type=str, dest="style", help="Optional style for lyrics (not yet implemented)")
    parser.add_argument("--surround_lines", type=int, default=3, help="Number of lines to show before and after the current line (default: 3)")
    parser.add_argument("--current-line-color", type=str, default="white", help="Color for the current line (default: white)")
    parser.add_argument("--surrounding-lines-color", type=str, default="black", help="Color for surrounding lines (default: black)")
    parser.set_defaults(style=True)

    args = parser.parse_args()

    font_name = args.font
    style = args.style
    surround_lines = args.surround_lines
    current_line_color = args.current_line_color
    surrounding_lines_color = args.surrounding_lines_color
    
    global current_render_id

    if font_name.lower() != "none":
        install_custom_fonts()
        font_path = os.path.join(os.path.dirname(__file__), "fonts", f"{font_name}.flf")
        if not os.path.exists(font_path):
            console.print(f"[red]❌ Font '{font_name}' not found in term_lyrics/fonts/[/red]")
            console.print("[yellow]🔤 You can download .flf fonts from: https://github.com/xero/figlet-fonts[/yellow]")
            console.print("📁 Copy the desired font to: `term_lyrics/fonts/` and use the name without extension in --font")

            sys.exit(1)
        alphabet_dict = generate_alphabet_dict(font_name)
    else:
        alphabet_dict = None

    last_song = None
    lyrics_thread = None

    while True:
        artist, title = get_current_song()
        if not artist or not title:
            console.print("⏸️ No song is playing on Spotify...")
            time.sleep(1)
            continue

        song_id = f"{artist} - {title}"
        if song_id != last_song:
            console.print(f"\n🎵 {title} — {artist}")

            if lyrics_thread and lyrics_thread.is_alive():
                console.print("🔁Interrupting previous lyric...")
                current_render_id = None
                lyrics_thread.join(timeout=1)
                time.sleep(0.1)

            lyrics = fetch_lyrics(artist, title)
            duration = get_song_duration() or 180
            position = get_song_position()

            current_render_id = str(uuid.uuid4())
            lyrics_thread = threading.Thread(
                target=display_lyrics_from_current_position,
                args=(lyrics, duration, position, current_render_id, alphabet_dict, style, surround_lines, current_line_color, surrounding_lines_color),
                daemon=True
            )
            lyrics_thread.start()

            last_song = song_id

        time.sleep(2)
