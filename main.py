import argparse
from term_lyrics.main import main

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="🎵 Show lyrics from Spotify with ASCII art.")
	parser.add_argument("--font", type=str, default="Tubes-Regular", help="Font name (from term_lyrics/fonts/) or 'none' for plain text")
	parser.add_argument("--style", type=str, default=None, help="Optional style for the lyrics.")
	parser.add_argument("--surround_lines", action="store_true", help="Number of lines to show before and after the current line (default: 3).")
	parser.add_argument("--current-line-color", type=str, default="white", help="Color for the current line (default: #00ff00).")
	parser.add_argument("--surrounding-lines-color", type=str, default="black", help="Color for surrounding lines (default: #F30131).")
	args = parser.parse_args()
	main(font_name=args.font)