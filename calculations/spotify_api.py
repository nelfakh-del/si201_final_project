import sqlite3
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def setup_spotify_table(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS spotify_tracks (
        id TEXT PRIMARY KEY,
        name TEXT,
        artist TEXT,
        popularity INTEGER,
        year INTEGER
    )
    """)

def get_spotify_data():
    conn = sqlite3.connect("final.db")
    cur = conn.cursor()

    setup_spotify_table(cur)

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id="af4c5a166c7a401f97247686d8d15da7",
            client_secret="14ba3653216b4a599ff4b5a2f10adbcf"
        )
    )

    results = sp.search(q="top hits", type="track", limit=25)
    tracks = results["tracks"]["items"]

    for t in tracks:
        track_id = t["id"]
        name = t["name"]
        artist = t["artists"][0]["name"]
        popularity = t["popularity"]
        year = int(t["album"]["release_date"][:4])

        print("Saving track:", name)

        cur.execute("""
            INSERT OR IGNORE INTO spotify_tracks
            VALUES (?, ?, ?, ?, ?)
        """, (track_id, name, artist, popularity, year))

    conn.commit()
    conn.close()


# Run this file directly to save Spotify data
if __name__ == "__main__":
    get_spotify_data()