import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("final.db")
cur = conn.cursor()

cur.execute("""
SELECT type_name, AVG(weight)
FROM pokemon
JOIN pokemon_types ON pokemon.id = pokemon_types.pokemon_id
GROUP BY type_name
""")
rows = cur.fetchall()

types = [r[0] for r in rows]
weights = [r[1] for r in rows]

plt.bar(types, weights)
plt.title("Average Pokémon Weight by Type")
plt.xlabel("Type")
plt.ylabel("Weight")
plt.show()

cur.execute("""
SELECT year, AVG(popularity)
FROM spotify_tracks
GROUP BY year
ORDER BY year
""")
rows = cur.fetchall()

years = [r[0] for r in rows]
popularity = [r[1] for r in rows]

plt.plot(years, popularity)
plt.title("Spotify Track Popularity Over Time")
plt.xlabel("Year")
plt.ylabel("Popularity")
plt.show()

cur.execute("""
SELECT genre, COUNT(*)
FROM movies
GROUP BY genre
""")
rows = cur.fetchall()

genres = [r[0] for r in rows]
counts = [r[1] for r in rows]

plt.pie(counts, labels=genres, autopct='%1.1f%%')
plt.title("Movie Genre Distribution")
plt.show()

conn.close()
