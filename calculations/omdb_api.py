import requests
import sqlite3

def setup_movie_table(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        title TEXT PRIMARY KEY,
        year INTEGER,
        genre TEXT,
        rating REAL
    )
    """)


def safe_int(value):
    """Convert value to int unless it's 'N/A' or missing."""
    if value is None or value == "N/A":
        return None
    return int(value)

def safe_float(value):
    """Convert value to float unless it's 'N/A' or missing."""
    if value is None or value == "N/A":
        return None
    return float(value)


def get_movie_data():
    conn = sqlite3.connect("final.db")
    cur = conn.cursor()

    setup_movie_table(cur)

    api_key = "4e88f6c8"

    movie_list = [
        "Inception", "Avatar", "Frozen", "Interstellar", "The Lion King",
        "The Dark Knight", "Barbie", "Dune", "Black Panther", "Harry Potter",
        "Titanic", "Moana", "Coco", "Up", "Cars",
        "Jurassic Park", "Joker", "Mulan", "Aladdin", "Soul",
        "Shrek", "Toy Story", "Spider-Man", "Super Mario Bros", "WALL-E"
    ]

    for title in movie_list:
        print(f"Checking: {title}")

        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
        data = requests.get(url).json()

        if data.get("Response") == "False":
            print(f"Skipping {title}: Movie not found")
            continue

        movie_title = data.get("Title")
        movie_year = data.get("Year")
        movie_genre = data.get("Genre")
        movie_rating = data.get("imdbRating")

        if (
            movie_title in (None, "N/A") or
            movie_year in (None, "N/A") or
            movie_genre in (None, "N/A") or
            movie_rating in (None, "N/A")
        ):
            print(f"Skipping {movie_title}: Missing data")
            continue

        movie_year = int(movie_year)
        movie_rating = float(movie_rating)

        cur.execute("""
            INSERT OR IGNORE INTO movies (title, year, genre, rating)
            VALUES (?, ?, ?, ?)
        """, (movie_title, movie_year, movie_genre, movie_rating))

        print(f"✔ Saved: {movie_title}")
        
    conn.commit()
    conn.close()


if __name__ == "__main__":
    get_movie_data()
