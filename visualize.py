import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect("final.db")
cur = conn.cursor()

cur.execute("PRAGMA table_info(spotify);")
print("SPOTIFY COLUMNS:", cur.fetchall())

cur.execute("SELECT COUNT(*) FROM spotify;")
print("SPOTIFY ROW COUNT:", cur.fetchone())


# --- Pokémon chart ---
cur.execute("""
SELECT type_name, AVG(weight)
FROM pokemon
JOIN pokemon_types ON pokemon.id = pokemon_types.pokemon_id
GROUP BY type_name
""")
rows = cur.fetchall()

plt.figure()    # <<< IMPORTANT
types = [r[0] for r in rows]
weights = [r[1] for r in rows]

plt.bar(types, weights)
plt.title("Average Pokémon Weight by Type")
plt.xlabel("Type")
plt.ylabel("Weight")
plt.show()

# --- Pokémon Count by Type ---
cur.execute("""
SELECT type_name, COUNT(*)
FROM pokemon_types
GROUP BY type_name
""")
rows = cur.fetchall()

plt.figure()
types = [r[0] for r in rows]
counts = [r[1] for r in rows]

plt.bar(types, counts)
plt.title("Number of Pokémon per Type")
plt.xlabel("Type")
plt.ylabel("Count")
plt.show()


# --- Spotify Top Artists Chart ---
cur.execute("""
SELECT artist, COUNT(*) as track_count
FROM spotify
GROUP BY artist
ORDER BY track_count DESC
LIMIT 10
""")
rows = cur.fetchall()

plt.figure()
artists = [r[0] for r in rows]
counts = [r[1] for r in rows]

plt.bar(artists, counts)
plt.title("Top 10 Artists in Spotify Dataset")
plt.xlabel("Artist")
plt.ylabel("Number of Tracks")
plt.xticks(rotation=45, ha='right')
plt.show()


# --- Movies chart ---
cur.execute("""
SELECT genre, COUNT(*)
FROM movies
GROUP BY genre
""")
rows = cur.fetchall()

plt.figure()    # <<< IMPORTANT
genres = [r[0] for r in rows]
counts = [r[1] for r in rows]

plt.pie(counts, labels=genres, autopct='%1.1f%%')
plt.title("Movie Genre Distribution")
plt.show()

conn.close()
