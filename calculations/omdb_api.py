import sys
sys.stdout.reconfigure(encoding="utf-8")

import requests
import sqlite3
import omdb_key_sabyena

DB_NAME = "final.db"

MOVIES = [
    "Inception","Titanic","Frozen","Moana","Coco","Up","Cars","Soul","Shrek",
    "Toy Story","Jurassic Park","Avatar","Interstellar","The Dark Knight",
    "Dune","Black Panther","Harry Potter and the Sorcerer's Stone","Joker",
    "Mulan","Aladdin","WALL-E","Finding Nemo","Inside Out","Zootopia",
    "The Lion King","The Matrix","The Godfather","The Shawshank Redemption",
    "Pulp Fiction","The Social Network","La La Land","The Avengers",
    "Avengers: Endgame","Avengers: Infinity War","Iron Man",
    "Captain America: Civil War","Spider-Man","Star Wars","The Empire Strikes Back",
    "Return of the Jedi","Django Unchained","The Great Gatsby","Back to the Future",
    "The Terminator","Terminator 2","Alien","Aliens","Ratatouille",
    "Beauty and the Beast","Encanto","Tangled","Brave","Monsters, Inc.",
    "Monsters University","The Incredibles","The Incredibles 2","Frozen II",
    "Hercules","Tarzan","The Little Mermaid","Mary Poppins","Paddington",
    "Paddington 2","The Lego Movie","The Lego Batman Movie","Cinderella",
    "Snow White and the Seven Dwarfs","Sleeping Beauty","Bambi","Pinocchio",
    "The Sound of Music","Top Gun","Top Gun: Maverick","Gladiator",
    "Saving Private Ryan","Oppenheimer","Barbie","Elemental","Raya and the Last Dragon",
    "Big Hero 6","The Princess and the Frog","A Bug's Life","Ant-Man",
    "Guardians of the Galaxy","Guardians of the Galaxy Vol. 2",
    "Shang-Chi and the Legend of the Ten Rings","Doctor Strange",
    "Doctor Strange in the Multiverse of Madness","The Hunger Games",
    "Catching Fire","Mockingjay Part 1","Mockingjay Part 2","The Fault in Our Stars",
    "The Perks of Being a Wallflower","The Breakfast Club","Mean Girls",
    "Clueless","The Blind Side","Hidden Figures","The Help","Little Women",
    "Pride & Prejudice","Emma","The Notebook","Crazy Rich Asians",
    "Hacksaw Ridge","A Quiet Place","A Quiet Place Part II","Whiplash",
    "The Prestige","The Departed"
]

API_KEY_omdb = omdb_key_sabyena.api_key_omdb


# ------------------ TABLE SETUP ------------------

def setup_movies(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS genres (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        title TEXT PRIMARY KEY,
        year INTEGER,
        genre_id INTEGER,
        rating REAL,
        FOREIGN KEY (genre_id) REFERENCES genres(id)
    )
    """)


# ------------------ BATCH TRACKING ------------------

def setup_batches(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS batches (
        api_name TEXT PRIMARY KEY,
        last_batch INTEGER
    )
    """)


def get_next_batch(cur, api_name):
    cur.execute("""
    SELECT last_batch FROM batches WHERE api_name = ?
    """, (api_name,))
    row = cur.fetchone()

    if row is None:
        cur.execute("""
        INSERT INTO batches (api_name, last_batch)
        VALUES (?, 1)
        """, (api_name,))
        return 1
    else:
        next_batch = row[0] + 1
        cur.execute("""
        UPDATE batches
        SET last_batch = ?
        WHERE api_name = ?
        """, (next_batch, api_name))
        return next_batch


# ------------------ HELPERS ------------------

def get_batch(batch_number):
    start = (batch_number - 1) * 25
    end = start + 25
    return MOVIES[start:end]


# ------------------ MAIN FUNCTION ------------------

def fetch_movies():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    setup_movies(cur)
    setup_batches(cur)

    batch_number = get_next_batch(cur, "omdb")
    titles = get_batch(batch_number)

    print(f"\nFetching OMDB batch {batch_number} ({len(titles)} movies)\n")

    for title in titles:
        url = f"http://www.omdbapi.com/?apikey={API_KEY_omdb}&t={title}"
        response = requests.get(url)

        if response.status_code != 200:
            continue

        data = response.json()

        if data.get("Response") == "False":
            continue

        year = None if data["Year"] == "N/A" else int(data["Year"])
        rating = None if data["imdbRating"] == "N/A" else float(data["imdbRating"])

        if data["Genre"] != "N/A":
            genre_name = data["Genre"].split(",")[0].strip()
            cur.execute("INSERT OR IGNORE INTO genres (name) VALUES (?)", (genre_name,))
            cur.execute("SELECT id FROM genres WHERE name = ?", (genre_name,))
            genre_id = cur.fetchone()[0]
        else:
            genre_id = None

        cur.execute("""
        INSERT OR IGNORE INTO movies (title, year, genre_id, rating)
        VALUES (?, ?, ?, ?)
        """, (data["Title"], year, genre_id, rating))

        print(f"Saved movie: {data['Title']}")

    conn.commit()
    conn.close()

    print(f"\nFinished OMDB batch {batch_number}\n")


if __name__ == "__main__":
    fetch_movies()
