import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import spotipy_key_nada

API_KEY_spotify_1 = spotipy_key_nada.api_key_client_id
API_KEY_spotify_2 = spotipy_key_nada.api_key_client_secret

def setup_spotify(cur):

    cur.execute("""
    CREATE TABLE IF NOT EXISTS artists (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS spotify (
        id TEXT PRIMARY KEY,
        title TEXT UNIQUE,
        artist_id INTEGER,
        FOREIGN KEY (artist_id) REFERENCES artists(id)
    )
    """)

def is_clean(title, artist):
    bad_words = ["mix", "remix", "version", "playlist", "radio", "hits", "dj", "edit"]
    t = title.lower()
    a = artist.lower()

    return not any(word in t for word in bad_words) and not any(word in a for word in bad_words)

def fetch_spotify_batch(batch_number):
    offset = (batch_number - 1) * 25
    collected = 0
    max_needed = 25

    conn = sqlite3.connect("final.db")
    cur = conn.cursor()
    setup_spotify(cur)

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=API_KEY_spotify_1,
            client_secret=API_KEY_spotify_2
        )
    )

    while collected < max_needed:
        results = sp.search(q="top hits", type="track", limit=25, offset=offset)

        if not results["tracks"]["items"]:
            break  # no more results

        for item in results["tracks"]["items"]:
            if collected >= max_needed:
                break

            track_id = item["id"]
            title = item["name"]
            artist = item["artists"][0]["name"]

            if not is_clean(title, artist):
                continue

            cur.execute("INSERT OR IGNORE INTO artists (name) VALUES (?);", (artist,))
            cur.execute("SELECT id FROM artists WHERE name = ?;", (artist,))
            artist_id = cur.fetchone()[0]

            cur.execute("""
            INSERT OR IGNORE INTO spotify (id, title, artist_id)
            VALUES (?, ?, ?)
            """, (track_id, title, artist_id))

            if cur.rowcount > 0:
                collected += 1
                print(f"Saved: {title} — {artist}")

        offset += 25


    conn.commit()
    conn.close()
    print(f"\nFinished. Saved {collected} clean tracks.\n")

if __name__ == "__main__":
    BATCH = 4     # Change this each run
    fetch_spotify_batch(BATCH)
