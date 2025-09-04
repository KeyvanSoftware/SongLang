from spotify_client import create_spotify_client
from genius_client import get_lyrics
from utils import detect_language
from track_cleaning import clean_title

# Create spotify client
sp = create_spotify_client()

# --- Fetch current user info ---
user = sp.current_user()
print(f"Logged in as: {user['display_name']} ({user['id']})\n")

# --- Fetch first 5 liked songs ---
print("Your first 5 liked songs:")
saved_tracks = sp.current_user_saved_tracks(limit=5)
for idx, item in enumerate(saved_tracks['items']):
    track = item['track']
    print(f"{idx+1}. {track['name']} - {track['artists'][0]['name']}")
    song_name = track['name']
    artist_name = track['artists'][0]['name']
    song_name = clean_title(song_name)
    print("Song name: ", song_name)
    lyrics = get_lyrics(song_name, artist_name)
    if lyrics is None:
        continue
    print("Lyrics info: ", len(lyrics))
    language = detect_language(lyrics)
    print("Language: ", language)
print("\n")
