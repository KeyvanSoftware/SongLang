import json
# import lyricsgenius
import requests
import os
from dotenv import load_dotenv
from langdetect import detect
from spotify_client import create_spotify_client
from genius_client import get_lyrics

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
    lyrics = get_lyrics(track['name'], track['artists'][0]['name'])
print("\n")
