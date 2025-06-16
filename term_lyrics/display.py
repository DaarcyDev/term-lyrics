import subprocess
from pyfiglet import Figlet
import string
import os
def get_current_song():
    try:
        artist = subprocess.check_output(["playerctl", "metadata", "xesam:artist"]).decode().strip()
        title = subprocess.check_output(["playerctl", "metadata", "xesam:title"]).decode().strip()
        return artist, title
    except subprocess.CalledProcessError:
        return None, None

def get_song_duration():
    try:
        length_us = int(subprocess.check_output(["playerctl", "metadata", "mpris:length"]).decode().strip())
        return length_us / 1_000_000
    except subprocess.CalledProcessError:
        return None

def get_song_position():
    try:
        position = float(subprocess.check_output(["playerctl", "position", "--player=spotify"]).decode().strip())
        return position
    except subprocess.CalledProcessError:
        return 0.0


    
def get_terminal_width():
    try:
        return max(40, os.get_terminal_size().columns - 4)
    except:
        return 80

def generate_alphabet_dict(font="standard"):
    figlet = Figlet(font=font)
    characters = string.ascii_letters + string.digits + "!?.,:;+-*/=()[]{}<> _"
    alphabet = {}
    for char in characters:
        rendered = figlet.renderText(char)
        alphabet[char] = rendered.rstrip('\n').split('\n')
    return alphabet

def render_text_with_alphabet(text, alphabet, max_width=None):
    if max_width is None:
        max_width = get_terminal_width()
    
    lines = []
    current_line = []
    current_width = 0

    # Armamos bloques por palabras para hacer wrapping por palabra
    for word in text.split(" "):
        word_lines = [""] * 4  # Asumimos altura máxima de 4 líneas (standard font)

        word_width = 0
        for char in word:
            char_art = alphabet.get(char, [" " * 4] * 4)  # fallback en blanco si no existe
            if len(char_art) > len(word_lines):
                word_lines += [""] * (len(char_art) - len(word_lines))

            for i in range(len(char_art)):
                word_lines[i] += char_art[i]
            word_width += len(char_art[0])
        
        # Si agregar esta palabra se pasa del ancho...
        if current_width + word_width > max_width:
            lines.extend(current_line)
            lines.append("")  # línea vacía entre bloques
            current_line = word_lines
            current_width = word_width
        else:
            if current_line:
                for i in range(len(current_line)):
                    current_line[i] += " " * 4 + word_lines[i]  # espacio entre palabras
                current_width += 4 + word_width
            else:
                current_line = word_lines
                current_width = word_width

    # Agrega el último bloque
    if current_line:
        lines.extend(current_line)

    return "\n".join(lines)