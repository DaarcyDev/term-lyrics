import subprocess
from pyfiglet import Figlet, FigletFont
import pyfiglet
import string
import os
import shutil

def get_current_song():
    try:
        artist = subprocess.check_output(["playerctl", "--player=spotify", "metadata", "xesam:artist"]).decode().strip()
        title = subprocess.check_output(["playerctl", "--player=spotify", "metadata", "xesam:title"]).decode().strip()
        return artist, title
    except subprocess.CalledProcessError:
        return None, None


def get_song_duration():
    try:
        length_us = int(subprocess.check_output(["playerctl", "--player=spotify", "metadata", "mpris:length"]).decode().strip())
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
    figlet = Figlet(font=font)  # Ya puedes usar 'miniwi'
    characters = string.ascii_letters + string.digits + "!?.,:;+-*/=()[]{}<> _"
    alphabet = {}
    for char in characters:
        rendered = figlet.renderText(char)
        alphabet[char] = rendered.rstrip('\n').split('\n')
    return alphabet

def render_text_with_alphabet(text, alphabet, max_width=None):
    if max_width is None:
        max_width = get_terminal_width() - 4  # un poco de margen

    lines = []
    current_line = []
    current_width = 0
    max_height = max(len(art) for art in alphabet.values())  # altura máxima real

    for word in text.split(" "):
        word_lines = [""] * max_height
        word_width = 0

        for char in word:
            char_art = alphabet.get(char, [" " * 4] * max_height)
            for i in range(max_height):
                word_lines[i] += char_art[i]
            word_width += len(char_art[0])

        # Si esta palabra ya no cabe en la línea actual...
        if current_width + word_width > max_width and current_line:
            lines.extend(current_line)
            lines.append("")  # espacio entre bloques
            current_line = word_lines
            current_width = word_width
        else:
            if current_line:
                for i in range(max_height):
                    current_line[i] += " " * 4 + word_lines[i]
                current_width += 4 + word_width
            else:
                current_line = word_lines
                current_width = word_width

    if current_line:
        lines.extend(current_line)

    # Centro cada línea final
    centered_lines = [line.center(max_width) for line in lines]

    return "\n".join(centered_lines)


    return "\n".join(lines)

def install_custom_fonts(project_fonts_dir=None):
    # Usa el path del módulo actual para ubicar fonts/
    if project_fonts_dir is None:
        current_dir = os.path.dirname(__file__)
        project_fonts_dir = os.path.join(current_dir, "fonts")

    pyfiglet_fonts_dir = os.path.join(os.path.dirname(pyfiglet.__file__), "fonts")
    os.makedirs(pyfiglet_fonts_dir, exist_ok=True)

    if not os.path.exists(project_fonts_dir):
        # print(f"⚠️ Directorio de fuentes no encontrado: {project_fonts_dir}")
        return

    for font_file in os.listdir(project_fonts_dir):
        if font_file.endswith(".flf"):
            source_path = os.path.join(project_fonts_dir, font_file)
            target_path = os.path.join(pyfiglet_fonts_dir, font_file)

            if not os.path.exists(target_path):
                shutil.copyfile(source_path, target_path)
                # print(f"✅ Fuente instalada: {font_file}")
            # else:
                # print(f"ℹ️ Fuente ya existente: {font_file}")
