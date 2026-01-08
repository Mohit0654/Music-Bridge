from flask import Flask, request, jsonify, send_from_directory
from spo import get_playlist_tracks
from youtube import (
    get_youtube_client,
    create_playlist,
    search_video,
    add_video_to_playlist
)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return send_from_directory(".", "index.html")

@app.route("/export", methods=["POST"])

def export_playlist():
    data = request.json
    spotify_playlist_id = data.get("spotify_playlist_id")
    playlist_name = data.get("playlist_name", "Spotify Imported Playlist")

    if not spotify_playlist_id:
        return jsonify({"error": "Spotify playlist ID required"}), 400

    tracks = get_playlist_tracks(spotify_playlist_id)
    youtube = get_youtube_client()
    yt_playlist_id = create_playlist(youtube, playlist_name)

    added = []
    skipped = []

    for track in tracks:
        query = f"{track['name']} {track['artist']} official audio"
        video_id = search_video(youtube, query)

        if video_id:
            add_video_to_playlist(youtube, yt_playlist_id, video_id)
            added.append(track)
        else:
            skipped.append(track)

    return jsonify({
        "message": "Playlist exported successfully",
        "youtube_playlist_id": yt_playlist_id,
        "added_songs": len(added),
        "skipped_songs": len(skipped)
    })

if __name__ == "__main__":
    app.run(debug=True)
