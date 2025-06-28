import argparse
from term_lyrics.main import main

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="🎵 Show lyrics from Spotify with ASCII art.")
	parser.add_argument("--font", type=str, default="Tubes-Regular", help="Font name (from term_lyrics/fonts/) or 'none' for plain text")
	parser.add_argument("--style", type=str, default=None, help="Optional style for the lyrics.")
	parser.add_argument("--surround_lines", action="store_true", help="Number of lines to show before and after the current line (default: 3).")
	args = parser.parse_args()
	print(f"Using font: {args.font}")
	main(font_name=args.font)