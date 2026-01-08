import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIPY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"
SPOTIPY_CLIENT_SECRET = "YOUR_SPOTIPY_CLIENT_SECRET"
SPOTIPY_REDIRECT_URI = "http://localhost:8080/callback"

scope = "playlist-read-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=scope
    )
)

def get_playlist_tracks(playlist_id):
    tracks = []
    results = sp.playlist_items(playlist_id)

    while results:
        for item in results["items"]:
            track = item["track"]
            if track:
                name = track["name"]
                artist = track["artists"][0]["name"]
                tracks.append({
                    "name": name,
                    "artist": artist
                })
        results = sp.next(results) if results["next"] else None

    return tracks

