import concurrent
import requests

BASE_URL = "https://lrclib.net/api"

def get_lyrics_lrclib(song_name, artist_name, uri):
    try:
        response = requests.get(
            f"{BASE_URL}/search",
            params={"track_name": song_name, "artist_name": artist_name},
            timeout=10
        )
        response.raise_for_status()
        results = response.json()
        if results:
            lyrics = results[0].get("plainLyrics") or results[0].get("syncedLyrics")
            return lyrics, uri
        return None, None
    except Exception as e:
        print(f"LRCLIB error: {e}")
        return None, None


def build_language_playlists(song_info):
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        results = executor.map(lambda args: get_lyrics_lrclib(*args), song_info)

    return results
