"""Create and seed library.db with sample book data."""

import sqlite3

DB_PATH = "library.db"

BOOKS = [
    ("The Fellowship of the Ring", "J.R.R. Tolkien", "Fantasy", 1954),
    ("The Two Towers", "J.R.R. Tolkien", "Fantasy", 1954),
    ("The Return of the King", "J.R.R. Tolkien", "Fantasy", 1955),
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937),
    ("Dune", "Frank Herbert", "Science Fiction", 1965),
    ("Foundation", "Isaac Asimov", "Science Fiction", 1951),
    ("Neuromancer", "William Gibson", "Science Fiction", 1984),
    ("1984", "George Orwell", "Dystopian", 1949),
    ("Animal Farm", "George Orwell", "Satire", 1945),
    ("Brave New World", "Aldous Huxley", "Dystopian", 1932),
    ("Pride and Prejudice", "Jane Austen", "Romance", 1813),
    ("Sense and Sensibility", "Jane Austen", "Romance", 1811),
    ("Moby-Dick", "Herman Melville", "Adventure", 1851),
    ("Crime and Punishment", "Fyodor Dostoevsky", "Classic", 1866),
    ("The Brothers Karamazov", "Fyodor Dostoevsky", "Classic", 1880),
]


def main():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS books")
    cur.execute(
        """
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            published_year INTEGER NOT NULL
        )
        """
    )

    cur.executemany(
        "INSERT INTO books (title, author, category, published_year) VALUES (?, ?, ?, ?)",
        BOOKS,
    )

    conn.commit()
    conn.close()
    print(f"Seeded {len(BOOKS)} books into {DB_PATH}")


if __name__ == "__main__":
    main()
