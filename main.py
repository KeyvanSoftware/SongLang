import json
import lyricsgenius
import requests
import os
from dotenv import load_dotenv
from langdetect import detect
from spotify_client import create_spotify_client

load_dotenv()

# Create spotify client
sp = create_spotify_client()

GENIUS_API_TOKEN = os.getenv("GENIUS_API_TOKEN")


def get_song_id(song_name, artist_name):
    headers = {'Authorization': f"Bearer {GENIUS_API_TOKEN}"}
    search_url = 'https://api.genius.com/search'
    params = {'q': f'{song_name} {artist_name}'}

    response = requests.get(search_url, params=params, headers=headers)
    data = response.json()

    if data['response']['hits']:
        return data['response']['hits'][0]['result']['id']
    else:
        return None
    
def get_song_data(song_id):
    headers = {'Authorization': f"Bearer {GENIUS_API_TOKEN}"}
    url = f"https://api.genius.com/songs/{song_id}"

    try:
        # Get song data from Genius API
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise exception for bad status codes
        data = response.json()
        
        song_data = data.get('response', {}).get('song', {})
        
        return song_data
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching song data: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


# --- Fetch current user info ---
user = sp.current_user()
print(f"Logged in as: {user['display_name']} ({user['id']})\n")

# --- Fetch first 5 liked songs ---
print("Your first 5 liked songs:")
saved_tracks = sp.current_user_saved_tracks(limit=1)
for idx, item in enumerate(saved_tracks['items']):
    track = item['track']
    print(f"{idx+1}. {track['name']} - {track['artists'][0]['name']}")
    song_id = get_song_id(track['name'], track['artists'][0]['name'])
    print(f"Song ID: {song_id}")
    # song_data = get_song_data(song_id)
    genius = lyricsgenius.Genius(GENIUS_API_TOKEN)
    song = genius.search_song(track['name'], track['artists'][0]['name'])
    print(song.lyrics)
    detection = detect(song.lyrics)
    print(detection)
    # print(json.dumps(song_data, indent=2))
print("\n")

# --- Fetch all liked songs ---
# print("Your number of liked songs:")
# all_tracks = []
# limit = 50
# offset = 0

# while True:
#     results = sp.current_user_saved_tracks(limit=limit, offset=offset)
#     if not results['items']:
#         break
#     all_tracks.extend(results['items'])
#     offset += len(results['items'])

# print(f"Total liked songs fetched: {len(all_tracks)}")

# track_ids = [item['track']['id'] for item in all_tracks if item['track']['id']]

# features_list = []
# batch_size = 50  # Max 100 per request
# for i in range(0, len(track_ids), batch_size):
#     batch_ids = track_ids[i:i+batch_size]
#     try:
#         batch_features = sp.audio_features(batch_ids)
#         features_list.extend(batch_features)
#     except spotipy.SpotifyException as e:
#         print(f"Skipping batch {i} due to error: {e}")
#         features_list.extend([None]*len(batch_ids))
