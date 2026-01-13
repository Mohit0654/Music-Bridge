import os
import time  # <--- Essential for preventing Error 409
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
from youtube import get_youtube_client, create_playlist, search_video, add_video_to_playlist
from spo import get_playlist_tracks # <--- Using your song list file

app = Flask(__name__)

# --- PASTE YOUR GEMINI API KEY HERE ---
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def get_ai_description(tracks):
    # Join list into a single string for the AI
    song_names = ", ".join(tracks)
    prompt = f"Write a cool, 1-sentence YouTube playlist description for these songs: {song_names}."
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "A smart playlist curated by MusicBridge AI."

@app.route("/")
def home():
    # This serves your existing index.html file
    return send_from_directory(".", "index.html")

@app.route("/export", methods=["POST"])
def export_playlist():
    data = request.json
    playlist_name = data.get("playlist_name", "My MusicBridge Playlist")

    # 1. GET TRACKS FROM SPO.PY
    # We retrieve the list of dictionaries from your spo.py file
    raw_tracks = get_playlist_tracks("dummy_id")
    
    # Convert them to search strings: "Song Name - Artist"
    tracks = [f"{t['name']} - {t['artist']}" for t in raw_tracks]

    # 2. Generate AI Description
    ai_desc = get_ai_description(tracks)

    try:
        # 3. Create YouTube Playlist
        youtube = get_youtube_client()
        yt_id = create_playlist(youtube, playlist_name, ai_desc)
        
        # Pause to let YouTube process the new playlist
        time.sleep(1) 

        # 4. Add Videos (With Safety Delays)
        for track in tracks:
            v_id = search_video(youtube, track + " official audio")
            if v_id:
                try:
                    add_video_to_playlist(youtube, yt_id, v_id)
                    # Wait 1.5s between adds to prevent crashing
                    time.sleep(1.5) 
                except Exception as e:
                    print(f"Skipped {track}: {e}")

        return jsonify({"status": "success", "ai_desc": ai_desc})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500