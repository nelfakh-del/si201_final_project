import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3

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
            client_id="af4c5a166c7a401f97247686d8d15da7",
            client_secret="14ba3653216b4a599ff4b5a2f10adbcf"
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
