import sys
sys.stdout.reconfigure(encoding="utf-8")

import requests
import sqlite3

DB_NAME = "final.db"


def setup_tables(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT,
        height INTEGER,
        weight INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS types (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemon_types (
        pokemon_id INTEGER,
        type_id INTEGER,
        PRIMARY KEY (pokemon_id, type_id),
        FOREIGN KEY(pokemon_id) REFERENCES pokemon(id),
        FOREIGN KEY(type_id) REFERENCES types(id)
    )
    """)


# ------------------ BATCH TRACKING ------------------

def setup_batches(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS batches (
        api_name TEXT PRIMARY KEY,
        last_batch INTEGER
    )
    """)


def get_next_batch(cur, api_name):
    cur.execute("""
    SELECT last_batch FROM batches WHERE api_name = ?
    """, (api_name,))
    row = cur.fetchone()

    if row is None:
        cur.execute("""
        INSERT INTO batches (api_name, last_batch)
        VALUES (?, 1)
        """, (api_name,))
        return 1
    else:
        next_batch = row[0] + 1
        cur.execute("""
        UPDATE batches
        SET last_batch = ?
        WHERE api_name = ?
        """, (next_batch, api_name))
        return next_batch


# ------------------ MAIN FUNCTION ------------------

def fetch_pokemon_batch():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    setup_tables(cur)
    setup_batches(cur)

    batch_number = get_next_batch(cur, "pokemon")

    start = (batch_number - 1) * 25 + 1
    end = start + 25

    print(f"\nFetching Pokémon batch {batch_number} (IDs {start}–{end - 1})\n")

    for poke_id in range(start, end):
        url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
        response = requests.get(url)

        if response.status_code != 200:
            continue

        data = response.json()

        cur.execute("""
        INSERT OR IGNORE INTO pokemon (id, name, height, weight)
        VALUES (?, ?, ?, ?)
        """, (poke_id, data["name"], data["height"], data["weight"]))

        for t in data["types"]:
            type_name = t["type"]["name"]

            cur.execute("""
            INSERT OR IGNORE INTO types (name)
            VALUES (?)
            """, (type_name,))

            cur.execute("""
            SELECT id FROM types WHERE name = ?
            """, (type_name,))
            type_id = cur.fetchone()[0]

            cur.execute("""
            INSERT OR IGNORE INTO pokemon_types (pokemon_id, type_id)
            VALUES (?, ?)
            """, (poke_id, type_id))

        print(f"Saved Pokémon: {data['name']}")

    conn.commit()
    conn.close()

    print(f"\nFinished Pokémon batch {batch_number}\n")


if __name__ == "__main__":
    fetch_pokemon_batch()
