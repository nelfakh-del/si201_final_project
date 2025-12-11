import requests
import sqlite3

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

def fetch_pokemon_batch(batch_number):
    start = (batch_number - 1) * 25 + 1
    end = start + 25

    conn = sqlite3.connect("final.db")
    cur = conn.cursor()
    setup_tables(cur)

    for poke_id in range(start, end):
        url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
        data = requests.get(url).json()

        cur.execute("""
        INSERT OR IGNORE INTO pokemon (id, name, height, weight)
        VALUES (?, ?, ?, ?)
        """, (poke_id, data["name"], data["height"], data["weight"]))

        for t in data["types"]:
            type_name = t["type"]["name"]
            cur.execute("INSERT OR IGNORE INTO types (name) VALUES (?)", (type_name,))
            cur.execute("SELECT id FROM types WHERE name = ?", (type_name,))
            type_id = cur.fetchone()[0]
            cur.execute("""
            INSERT OR IGNORE INTO pokemon_types (pokemon_id, type_id)
            VALUES (?, ?)
            """, (poke_id, type_id))

        print(f"Saved {data['name']}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    BATCH = 4     # Change this each run
    fetch_pokemon_batch(BATCH)
