import sys
sys.stdout.reconfigure(encoding="utf-8")

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import sqlite3
import spotipy_key_nada


# Spotify API credentials
API_KEY_spotify_1 = spotipy_key_nada.api_key_client_id
API_KEY_spotify_2 = spotipy_key_nada.api_key_client_secret


def setup_spotify(cur):
    """Create Spotify-related tables."""
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


def setup_batches(cur):
    """Tracks last used batch per API so batch numbers auto-increment."""
    cur.execute("""
    CREATE TABLE IF NOT EXISTS batches (
        api_name TEXT PRIMARY KEY,
        last_batch INTEGER
    )
    """)


def get_next_batch(cur, api_name):
    """Returns next batch number and updates batch table."""
    cur.execute(
        "SELECT last_batch FROM batches WHERE api_name = ?",
        (api_name,)
    )
    row = cur.fetchone()

    if row is None:
        cur.execute(
            "INSERT INTO batches (api_name, last_batch) VALUES (?, ?)",
            (api_name, 1)
        )
        return 1
    else:
        next_batch = row[0] + 1
        cur.execute(
            "UPDATE batches SET last_batch = ? WHERE api_name = ?",
            (next_batch, api_name)
        )
        return next_batch


def is_clean(title, artist):
    """Filters out remixes, playlists, edits, etc."""
    bad_words = ["mix", "remix", "version", "playlist", "radio", "hits", "dj", "edit"]
    t = title.lower()
    a = artist.lower()

    return not any(word in t for word in bad_words) and not any(word in a for word in bad_words)


def fetch_spotify_batch():
    conn = sqlite3.connect("final.db")
    cur = conn.cursor()

    setup_spotify(cur)
    setup_batches(cur)

    batch_number = get_next_batch(cur, "spotify")
    offset = (batch_number - 1) * 25

    collected = 0
    max_needed = 25

    sp = spotipy.Spotify(
        auth_manager=SpotifyClientCredentials(
            client_id=API_KEY_spotify_1,
            client_secret=API_KEY_spotify_2
        )
    )

    while collected < max_needed:
        results = sp.search(
            q="top hits",
            type="track",
            limit=25,
            offset=offset
        )

        if not results["tracks"]["items"]:
            break

        for item in results["tracks"]["items"]:
            if collected >= max_needed:
                break

            track_id = item["id"]
            title = item["name"]
            artist = item["artists"][0]["name"]

            if not is_clean(title, artist):
                continue

            cur.execute(
                "INSERT OR IGNORE INTO artists (name) VALUES (?)",
                (artist,)
            )
            cur.execute(
                "SELECT id FROM artists WHERE name = ?",
                (artist,)
            )
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
    fetch_spotify_batch()
