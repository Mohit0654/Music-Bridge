import os
import googleapiclient.discovery
import google_auth_oauthlib.flow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# --- PASTE YOUR CLIENT ID & SECRET HERE ---
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
# ------------------------------------------

SCOPES = ["https://www.googleapis.com/auth/youtube"]

def get_youtube_client():
    creds = None
    # 1. Check if we already have a saved login "ticket" (token.json)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # 2. If no valid ticket, we must log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except:
                creds = None # Force re-login if refresh fails

        if not creds:
            # Create the config dictionary manually (replacing client_secret.json)
            client_config = {
                "installed": {
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://accounts.google.com/o/oauth2/token",
                }
            }
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(
                client_config, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # 3. Save the login ticket for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)

def create_playlist(youtube, title, description):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {"title": title, "description": description},
            "status": {"privacyStatus": "private"}
        }
    )
    response = request.execute()
    return response["id"]

def search_video(youtube, query):
    request = youtube.search().list(part="snippet", q=query, maxResults=1, type="video")
    response = request.execute()
    return response["items"][0]["id"]["videoId"] if response["items"] else None

def add_video_to_playlist(youtube, playlist_id, video_id):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {"kind": "youtube#video", "videoId": video_id}
            }
        }
    ).execute()