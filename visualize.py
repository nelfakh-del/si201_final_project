import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("final.db")
cur = conn.cursor()

#cur.execute("PRAGMA table_info(spotify);")
#print("SPOTIFY COLUMNS:", cur.fetchall())

#cur.execute("SELECT COUNT(*) FROM spotify;")
#print("SPOTIFY ROW COUNT:", cur.fetchone())


#average pokemon weight by type
cur.execute("""
SELECT types.name, AVG(pokemon.weight)
FROM pokemon
JOIN pokemon_types ON pokemon.id = pokemon_types.pokemon_id
JOIN types ON pokemon_types.type_id = types.id
GROUP BY types.name
ORDER BY AVG(pokemon.weight) DESC
""")
rows = cur.fetchall()

plt.figure()
types = [r[0] for r in rows]
weights = [r[1] for r in rows]

plt.bar(types, weights)
plt.title("Average Pokémon Weight by Type")
plt.xlabel("Type")
plt.ylabel("Average Weight")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#count of pokemon per type
cur.execute("""
SELECT types.name, COUNT(*)
FROM pokemon_types
JOIN types ON pokemon_types.type_id = types.id
GROUP BY types.name
ORDER BY COUNT(*) DESC
""")
rows = cur.fetchall()

plt.figure()
types = [r[0] for r in rows]
counts = [r[1] for r in rows]

plt.bar(types, counts)
plt.title("Number of Pokémon Per Type")
plt.xlabel("Type")
plt.ylabel("Count")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

#spotify - count tracks per artist
cur.execute("""
SELECT artists.name, COUNT(*)
FROM spotify
JOIN artists ON spotify.artist_id = artists.id
GROUP BY artists.name
ORDER BY COUNT(*) DESC
""")
rows = cur.fetchall()

plt.figure()
artists = [r[0] for r in rows]
counts = [r[1] for r in rows]

plt.bar(artists, counts)
plt.title("Tracks Collected Per Artist (Spotify)")
plt.xlabel("Artist")
plt.ylabel("Track Count")
plt.xticks(rotation=90)
plt.tight_layout()
plt.show()

#Movies count by genre
cur.execute("""
SELECT genres.name, COUNT(*)
FROM movies
JOIN genres ON movies.genre_id = genres.id
GROUP BY genres.name
ORDER BY COUNT(*) DESC
""")
rows = cur.fetchall()

plt.figure()
genres = [r[0] for r in rows]
counts = [r[1] for r in rows]

plt.pie(counts, labels=genres, autopct="%1.1f%%")
plt.title("Movie Genre Distribution")
plt.show()

conn.close()
