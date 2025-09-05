from spotify_client import create_spotify_client
from lrclib_client import build_language_playlists
from utils import detect_language, group_by_language, songs_by_language, get_language_name
from track_cleaning import clean_title
import time

# Create spotify client
sp = create_spotify_client()

# --- Fetch current user info ---
user = sp.current_user()
print(f"Logged in as: {user['display_name']} ({user['id']})\n")

# Start timer
start = time.time()

# --- Fetch all liked songs ---
print("Your number of liked songs:")
saved_tracks = []
limit = 50
offset = 0

while True:
    results = sp.current_user_saved_tracks(limit=limit, offset=offset)
    if not results['items']:
        break
    saved_tracks.extend(results['items'])
    offset += len(results['items'])


song_info_list = []
print("Your liked songs:")

for idx, item in enumerate(saved_tracks):
    track = item['track']
    print(f"{idx+1}. {track['name']} - {track['artists'][0]['name']}")

    artist_name = track['artists'][0]['name']
    song_name = clean_title(track['name'])
    song_info = (song_name, artist_name, track['uri'])
    song_info_list.append(song_info)
print("\n")

lyrics = build_language_playlists(song_info_list)

for lyric, uri in lyrics:
    if lyric is None:
        continue
    print("Lyrics info: ", len(lyric))
    language = detect_language(lyric)
    group_by_language(language, uri)

# End timer and print time taken
time.sleep(1)
end = time.time()
print(f"Total runtime of the program is {end - start} seconds")

# Create language specific playlist and update with relevant tracks
for language, uri_list in songs_by_language.items():
    playlist_title = get_language_name(language)
    playlist = sp.user_playlist_create(user=user['id'], name=playlist_title)
    sp.user_playlist_add_tracks(user=user['id'], playlist_id=playlist['id'], tracks=uri_list)
