import requests
import sqlite3

MOVIES = [
    # 100+ movie list
    "Inception","Titanic","Frozen","Moana","Coco","Up","Cars","Soul","Shrek",
    "Toy Story","Jurassic Park","Avatar","Interstellar","The Dark Knight",
    "Dune","Black Panther","Harry Potter","Joker","Mulan","Aladdin",
] * 10   # repeats list to ensure large pool

def get_batch(batch_number):
    start = (batch_number - 1) * 25
    end = start + 25
    return MOVIES[start:end]

def setup_movies(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        title TEXT PRIMARY KEY,
        year INTEGER,
        genre TEXT,
        rating REAL
    )
    """)

def fetch_movies(batch_number):
    conn = sqlite3.connect("final.db")
    cur = conn.cursor()
    setup_movies(cur)

    api_key = "4e88f6c8"
    titles = get_batch(batch_number)

    for title in titles:
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
        data = requests.get(url).json()

        if data.get("Response") == "False":
            continue

        if "N/A" in (data["Year"], data["Genre"], data["imdbRating"]):
            continue

        genre = data["Genre"].split(",")[0].strip()

        cur.execute("""
        INSERT OR IGNORE INTO movies (title, year, genre, rating)
        VALUES (?, ?, ?, ?)
        """, (data["Title"], int(data["Year"]), genre, float(data["imdbRating"])))

        print(f"Saved {data['Title']}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    BATCH = 4  # change for each run
    fetch_movies(BATCH)
