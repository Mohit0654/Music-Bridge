import google_auth_oauthlib.flow
import googleapiclient.discovery

SCOPES = ["https://www.googleapis.com/auth/youtube"]

def get_youtube_client():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    credentials = flow.run_local_server(port=0)

    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=credentials
    )
    return youtube


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
