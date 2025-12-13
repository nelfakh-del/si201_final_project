import sqlite3

conn = sqlite3.connect("final.db")
cur = conn.cursor()

# Example calculation: average Pokémon weight by type
cur.execute("""
SELECT types.name, AVG(pokemon.weight)
FROM pokemon
JOIN pokemon_types ON pokemon.id = pokemon_types.pokemon_id
JOIN types ON pokemon_types.type_id = types.id
GROUP BY types.name
""")

avg_weights = cur.fetchall()
print("Average Pokémon weights by Type:", avg_weights)

# Example: Spotify number of tracks per artist
cur.execute("""
SELECT artists.name, COUNT(*)
FROM spotify
JOIN artists ON spotify.artist_id = artists.id
GROUP BY artists.name
ORDER BY COUNT(*) DESC
""")

artist_track_counts = cur.fetchall()
print("\nTrackes per Artist", artist_track_counts)

# Example: movie counts by genre
cur.execute("""
SELECT genres.name, COUNT(*)
FROM movies
JOIN genres ON movies.genre_id = genres.id
GROUP BY genres.name
ORDER BY COUNT(*) DESC
""")

genre_counts = cur.fetchall()
print("\nMovie Counts by Genre", genre_counts)

conn.close()