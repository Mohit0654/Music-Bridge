

# 🎵 Music Bridge

Music Bridge is a playlist conversion tool that helps users recreate their music playlists across streaming platforms — starting with **Spotify → YouTube**.

Our goal is simple:
**playlist transfer should be easy enough for anyone to use.**

---

## ❓ Problem

Music playlists are locked inside individual platforms.
When users switch platforms, they lose their playlists and must rebuild them manually.

---

## 💡 Solution

Music Bridge automates this process by:

* Reading playlist track data
* Creating a new playlist on YouTube
* Searching and adding matching songs automatically

The user only needs to:

1. Click **Export**
2. Authorize once
3. Get a ready playlist 🎶

---

## 🤖 Where AI Is Used

Music Bridge uses **Google Gemini AI** to:

* Generate a short, smart description for the created YouTube playlist
* Make playlists feel personalized instead of auto-generated

This improves the user experience without adding complexity.

---

## ⚙️ Demo Note

Due to Spotify developer access restrictions:

* Spotify data is demonstrated using demo tracks
* The full Spotify integration logic is implemented and production-ready
* YouTube playlist creation is fully real and functional

---

## 🧰 Tech Stack

* Python
* Flask
* REST APIs
* OAuth 2.0
* HTML / CSS

---

## 🧩 Google Technologies Used

* **Google Cloud Platform** – API and credential management
* **YouTube Data API v3** – playlist creation and video insertion
* **Google OAuth 2.0** – secure authentication
* **Google Gemini API** – AI-generated playlist descriptions

---

## 🔒 Security

* OAuth-based authentication
* No passwords stored
* Secrets excluded via `.gitignore`

---

## 🚀 Future Scope

* Full Spotify OAuth integration
* Support for more music platforms
* One-click cloud deployment





* Mobile-friendly UI

