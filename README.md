# Term-Lyrics

Terminal app to show real-time lyrics from Spotify in your terminal, with optional ASCII art fonts and synced display based on the song's playback time. Built with `rich`, `playerctl`, and love for the terminal.

---

## Preview

![term-lyrics preview](Term-Lyrics_gif.gif) <!-- optional preview gif -->

---

## Disclaimer

I'm just a junior dev who loves music and Linux. This project was built with ChatGPT's help. Lyrics are not guaranteed to be accurate — they come from public APIs or free scrapers and may be out of sync with the actual song. Lyrics are displayed based on **song duration**, not true timestamps or word alignment.

Use at your own risk, and feel free to contribute!

---

## Features

* 🎧 **Live lyric display** from the currently playing Spotify song (via `playerctl`)
* 🔡 **ASCII Art mode**: display lyrics using Figlet `.flf` fonts (you can add your own!)
* 🎨 **Custom styles**: tweak colors for the current lyric and surrounding lines
* 🧘 **Minimalist mode**: disable styling and borders for clean, raw text
* 🔁 **Auto-refresh lyrics** when song changes
* 📁 **Local font folder**: drop your own `.flf` files into `term_lyrics/fonts/`
* 🖼️ **Optional padding** via `--surround_lines`

---

## Requirements

* Python 3.6+
* [playerctl](https://github.com/altdesktop/playerctl) installed and configured
* pip modules:

  * `rich`
  * `pyfiglet`

---

## Installation

### Using pipx (recommended)

```bash
pipx install git+https://github.com/DaarcyDev/term-lyrics.git
```

### From local clone

```bash
git clone https://github.com/DaarcyDev/term-lyrics.git
cd term-lyrics
pipx install .
```

Make sure `playerctl` is installed and working (e.g. `playerctl metadata`).

---

## Usage

```bash
term-lyrics [OPTIONS]
```

### Common examples:

```bash
# Default with Tubes-Regular ASCII art
term-lyrics

# Plain text only
term-lyrics --font none

# Change font (must exist in term_lyrics/fonts/)
term-lyrics --font miniwi

# Disable all styles (no colors)
term-lyrics --style False

# Show 5 lines before and after current
term-lyrics --surround_lines 5

# Custom colors for current line and others
term-lyrics --current-line-color '#00ff00' --surrounding-lines-color '#666666'
```

---

## Command Line Options

| Argument                    | Description                                                                   |
| --------------------------- | ----------------------------------------------------------------------------- |
| `--font`                    | Font name from `term_lyrics/fonts/` (without `.flf`) or `none` for plain text |
| `--style`                   | Optional style preset; use `False` to disable styling                          |
| `--surround_lines`          | Number of lines above and below the current lyric to show                     |
| `--current-line-color`      | Color for the active lyric line (default: white)                              |
| `--surrounding-lines-color` | Color for the surrounding lyrics (default: black)                             |

---

## Adding Fonts

To add custom Figlet fonts:

1. Download `.flf` files from [xero/figlet-fonts](https://github.com/xero/figlet-fonts) or any site
2. Copy them into the folder: `term_lyrics/fonts/`
3. Use `--font YourFontName` (without the `.flf` extension)

---

## Known Limitations

* Lyrics are **not timestamp-synced** — they're shown based on total song duration
* Lyrics may not match the song due to **free, public APIs** and scraping
* Some songs might not return any lyrics at all

---

## Contribution

Feel free to open PRs, issues or suggestions on the [GitHub repo](https://github.com/DaarcyDev/term-lyrics)

---

## License

MIT License

---

Enjoy the music. 🎶
