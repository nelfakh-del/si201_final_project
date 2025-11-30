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
