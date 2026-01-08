from spotify import get_playlist_tracks
from youtube import get_youtube_client, create_playlist, search_video, add_video_to_playlist

SPOTIFY_PLAYLIST_ID = "YOUR_SPOTIFY_PLAYLIST_ID"

tracks = get_playlist_tracks(SPOTIFY_PLAYLIST_ID)

youtube = get_youtube_client()
yt_playlist_id = create_playlist(youtube, "Spotify Imported Playlist")

for track in tracks:
    print(f"Searching: {track}")
    video_id = search_video(youtube, track + " official audio")

    if video_id:
        add_video_to_playlist(youtube, yt_playlist_id, video_id)
        print("✔ Added")
    else:
        print("❌ Not Found")
