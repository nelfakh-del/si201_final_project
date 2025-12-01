import sqlite3

conn = sqlite3.connect("final.db")
cur = conn.cursor()

# Example calculation: average Pokémon weight by type
cur.execute("""
SELECT type_name, AVG(weight)
FROM pokemon
JOIN pokemon_types ON pokemon.id = pokemon_types.pokemon_id
GROUP BY type_name
""")

avg_weights = cur.fetchall()
print("Average Pokémon weights:", avg_weights)

# Example: Spotify avg popularity per year
cur.execute("""
SELECT year, AVG(popularity)
FROM spotify_tracks
GROUP BY year
""")

avg_pop = cur.fetchall()
print("Spotify averages:", avg_pop)

# Example: movie counts by genre
cur.execute("""
SELECT genre, COUNT(*)
FROM movies
GROUP BY genre
""")

genre_counts = cur.fetchall()
print("Genre counts:", genre_counts)

conn.close()