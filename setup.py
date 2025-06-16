from setuptools import setup, find_packages

setup(
    name="term-lyrics",
    version="0.1.0",
    description="Display real-time lyrics of your currently playing Spotify song in the terminal",
    author="Daarcy",
    packages=find_packages(),
    install_requires=["requests"],
    entry_points={
        "console_scripts": [
            "term-lyrics = term_lyrics.main:main"
        ]
    },
)

