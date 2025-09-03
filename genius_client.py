import lyricsgenius
import os
from dotenv import load_dotenv

load_dotenv()

GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")

genius = lyricsgenius.Genius(GENIUS_API_TOKEN)

def get_lyrics(song_name, artist_name):
    song = genius.search_song(song_name, artist_name)
    if song:
        return song.lyrics
    return None
