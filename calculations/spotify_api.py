import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import spotipy_key_nada

API_KEY_spotify_1 = spotipy_key_nada.api_key_client_id
API_KEY_spotify_2 = spotipy_key_nada.api_key_client_secret

def setup_spotify(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS spotify (
        id TEXT PRIMARY KEY,
        title TEXT,
        artist TEXT
    )
    """)

def fetch_spotify_batch(batch_number):
    offset = (batch_number - 1) * 25

    conn = sqlite3.connect("final.db")
    cur = conn.cursor()
    setup_spotify(cur)

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=API_KEY_spotify_1,
            client_secret=API_KEY_spotify_2
        )
    )

    results = sp.search(q="top hits", type="track", limit=25, offset=offset)

    for item in results["tracks"]["items"]:
        track_id = item["id"]
        title = item["name"]
        artist = item["artists"][0]["name"]

        cur.execute("""
        INSERT OR IGNORE INTO spotify (id, title, artist)
        VALUES (?, ?, ?)
        """, (track_id, title, artist))

        print(f"Saved track: {title}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    BATCH = 4  # Change this each run
    fetch_spotify_batch(BATCH)
