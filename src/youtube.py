import os
import googleapiclient.discovery
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ["https://www.googleapis.com/auth/youtube"]

TOKEN_FILE = "token.json"      # Will store login
CLIENT_SECRET = "client_secret.json"


def get_youtube_client():
    creds = None

    # If already logged in before
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # If no token or expired → refresh or login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save login for future
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return googleapiclient.discovery.build("youtube", "v3", credentials=creds)


def create_playlist(youtube, title):
    request = youtube.playlists().insert(
        part="snippet,status",
        body={
            "snippet": {
                "title": title,
                "description": "Imported from Spotify"
            },
            "status": {
                "privacyStatus": "private"
            }
        }
    )
    response = request.execute()
    return response["id"]


def search_video(youtube, query):
    request = youtube.search().list(
        part="snippet",
        q=query,
        maxResults=1,
        type="video"
    )
    response = request.execute()

    if response["items"]:
        return response["items"][0]["id"]["videoId"]
    return None


def add_video_to_playlist(youtube, playlist_id, video_id):
    youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    ).execute()

# import os
# import google_auth_oauthlib.flow
# import googleapiclient.discovery

# SCOPES = ["https://www.googleapis.com/auth/youtube"]

# def get_youtube_client():
#     base_dir = os.path.dirname(os.path.abspath(__file__))
#     client_secret_path = os.path.join(base_dir, "client_secret.json")

#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
#         client_secret_path, SCOPES
#     )
#     credentials = flow.run_local_server(port=0)

#     youtube = googleapiclient.discovery.build(
#         "youtube", "v3", credentials=credentials
#     )
#     return youtube
