import requests
import sqlite3

def setup_pokemon_tables(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemon (
        id INTEGER PRIMARY KEY,
        name TEXT,
        height INTEGER,
        weight INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS pokemon_types (
        pokemon_id INTEGER,
        type_name TEXT,
        FOREIGN KEY(pokemon_id) REFERENCES pokemon(id)
    )
    """)


def get_pokemon_data(start_id=76, end_id=101):
    conn = sqlite3.connect("final.db")
    cur = conn.cursor()

    setup_pokemon_tables(cur)

    for poke_id in range(start_id, end_id):
        print("Saving Pokémon:", poke_id)

        url = f"https://pokeapi.co/api/v2/pokemon/{poke_id}"
        data = requests.get(url).json()

        cur.execute("""
            INSERT OR IGNORE INTO pokemon (id, name, height, weight)
            VALUES (?, ?, ?, ?)
        """, (poke_id, data["name"], data["height"], data["weight"]))

        for t in data["types"]:
            cur.execute("""
                INSERT INTO pokemon_types (pokemon_id, type_name)
                VALUES (?, ?)
            """, (poke_id, t["type"]["name"]))

    conn.commit()
    conn.close()


# Run this file directly to save Pokémon
if __name__ == "__main__":
    get_pokemon_data()
