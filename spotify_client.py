import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_KEY = os.getenv("SPOTIFY_SECRET_KEY")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

def create_spotify_client():
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_SECRET_KEY,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope="user-library-read playlist-modify-private playlist-modify-public",
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

    return spotipy.Spotify(auth=token_info['access_token'])
