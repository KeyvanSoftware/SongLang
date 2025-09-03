from langdetect import detect
from spotify_client import create_spotify_client
from genius_client import get_lyrics

# Create spotify client
sp = create_spotify_client()

# --- Fetch current user info ---
user = sp.current_user()
print(f"Logged in as: {user['display_name']} ({user['id']})\n")

# --- Fetch first 5 liked songs ---
print("Your first 5 liked songs:")
saved_tracks = sp.current_user_saved_tracks(limit=1)
for idx, item in enumerate(saved_tracks['items']):
    track = item['track']
    print(f"{idx+1}. {track['name']} - {track['artists'][0]['name']}")
    lyrics = get_lyrics(track['name'], track['artists'][0]['name'])
print("\n")
