import sys
sys.stdout.reconfigure(encoding="utf-8")

import sqlite3

DB_NAME = "final.db"


def run_calculations():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    print("\n--- DATABASE CALCULATIONS ---\n")

    # 1. Average Pokémon weight by type
    cur.execute("""
    SELECT types.name, ROUND(AVG(pokemon.weight), 2)
    FROM pokemon
    JOIN pokemon_types ON pokemon.id = pokemon_types.pokemon_id
    JOIN types ON pokemon_types.type_id = types.id
    GROUP BY types.name
    ORDER BY AVG(pokemon.weight) DESC
    """)
    print("Average Pokémon weight by type:")
    for row in cur.fetchall():
        print(row)

    # 2. Pokémon count per type
    cur.execute("""
    SELECT types.name, COUNT(*)
    FROM pokemon_types
    JOIN types ON pokemon_types.type_id = types.id
    GROUP BY types.name
    ORDER BY COUNT(*) DESC
    """)
    print("\nNumber of Pokémon per type:")
    for row in cur.fetchall():
        print(row)

    # 3. Average IMDb rating by movie genre
    cur.execute("""
    SELECT genres.name, ROUND(AVG(movies.rating), 2)
    FROM movies
    JOIN genres ON movies.genre_id = genres.id
    WHERE movies.rating IS NOT NULL
    GROUP BY genres.name
    ORDER BY AVG(movies.rating) DESC
    """)
    print("\nAverage IMDb rating by genre:")
    for row in cur.fetchall():
        print(row)

    # 4. Movie count by genre
    cur.execute("""
    SELECT genres.name, COUNT(*)
    FROM movies
    JOIN genres ON movies.genre_id = genres.id
    GROUP BY genres.name
    ORDER BY COUNT(*) DESC
    """)
    print("\nNumber of movies per genre:")
    for row in cur.fetchall():
        print(row)

    # 5. Top 10 artists by number of tracks collected (Spotify)
    cur.execute("""
    SELECT artists.name, COUNT(*)
    FROM spotify
    JOIN artists ON spotify.artist_id = artists.id
    GROUP BY artists.name
    ORDER BY COUNT(*) DESC
    LIMIT 10
    """)
    print("\nTop 10 artists by number of tracks collected:")
    for row in cur.fetchall():
        print(row)

    conn.close()


if __name__ == "__main__":
    run_calculations()
