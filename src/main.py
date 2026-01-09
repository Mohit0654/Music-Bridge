from youtube import get_youtube_client, create_playlist, search_video, add_video_to_playlist

# DEMO MODE: mock Spotify playlist (Spotify API temporarily disabled)
tracks = [
    "Believer - Imagine Dragons",
    "Perfect - Ed Sheeran",
    "Blinding Lights - The Weeknd",
    "Shape of You - Ed Sheeran",
    "Closer - The Chainsmokers"
]

youtube = get_youtube_client()
yt_playlist_id = create_playlist(youtube, "Spotify Imported Playlist (Demo)")

for track in tracks:
    print(f"Searching: {track}")
    video_id = search_video(youtube, track + " official audio")

    if video_id:
        add_video_to_playlist(youtube, yt_playlist_id, video_id)
        print("✔ Added")
    else:
        print("❌ Not Found")
