import requests
import sqlite3
import omdb_key_sabyena

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


def get_batch(batch_number):
    start = (batch_number - 1) * 25
    end = start + 25
    return MOVIES[start:end]


def fetch_movies(batch_number):
    conn = sqlite3.connect("final.db")
    cur = conn.cursor()
    setup_movies(cur)

    api_key = API_KEY_omdb
    titles = get_batch(batch_number)

    for title in titles:
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={title}"
        data = requests.get(url).json()

        if data.get("Response") == "False":
            continue

        year = None if data["Year"] == "N/A" else int(data["Year"])
        genre_name = None if data["Genre"] == "N/A" else data["Genre"].split(",")[0].strip()
        rating = None if data["imdbRating"] == "N/A" else float(data["imdbRating"])

        if genre_name is None:
            genre_id = None
        else:
            cur.execute("INSERT OR IGNORE INTO genres (name) VALUES (?)", (genre_name,))
            cur.execute("SELECT id FROM genres WHERE name = ?", (genre_name,))
            genre_id = cur.fetchone()[0]

        cur.execute("""
        INSERT OR IGNORE INTO movies (title, year, genre_id, rating)
        VALUES (?, ?, ?, ?)
        """, (data["Title"], year, genre_id, rating))

        print(f"Saved {data['Title']}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    BATCH = 5    # Change this each run
    fetch_movies(BATCH)