import spotipy
import os
import csv
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("SECRET_KEY")

sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri="http://127.0.0.1:8888/callback",
    scope="user-library-read",
    show_dialog=True,
    cache_path=".spotify_token_cache"
)

# Try to get cached token
token_info = sp_oauth.get_cached_token()

if not token_info:
    # No cached token or expired → ask user to authorize
    auth_url = sp_oauth.get_authorize_url()
    print("Go here and authorize:", auth_url)
    response = input("Paste the full redirect URL here: ")
    code = sp_oauth.parse_response_code(response)
    token_info = sp_oauth.get_access_token(code)

# Create Spotify client
sp = spotipy.Spotify(auth=token_info['access_token'])

# --- Fetch current user info ---
user = sp.current_user()
print(f"Logged in as: {user['display_name']} ({user['id']})\n")

# --- Fetch first 5 liked songs ---
print("Your first 5 liked songs:")
saved_tracks = sp.current_user_saved_tracks(limit=5)
for idx, item in enumerate(saved_tracks['items']):
    track = item['track']
    print(f"{idx+1}. {track['name']} - {track['artists'][0]['name']}")
print("\n")

# --- Fetch all liked songs ---
print("Your number of liked songs:")
all_tracks = []
limit = 50
offset = 0

while True:
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    if not results['items']:
        break
    all_tracks.extend(results['items'])
    offset += len(results['items'])

print(f"Total liked songs fetched: {len(all_tracks)}")

track_ids = [item['track']['id'] for item in all_tracks if item['track']['id']]

features_list = []
batch_size = 50  # Max 100 per request
for i in range(0, len(track_ids), batch_size):
    batch_ids = track_ids[i:i+batch_size]
    try:
        batch_features = sp.audio_features(batch_ids)
        features_list.extend(batch_features)
    except spotipy.SpotifyException as e:
        print(f"Skipping batch {i} due to error: {e}")
        features_list.extend([None]*len(batch_ids))
