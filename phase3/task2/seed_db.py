"""Create and seed library.db — the SQLite data source for the MCP server."""

import sqlite3

DB_PATH = "library.db"

BOOKS = [
    ("Dune", "Frank Herbert", "Science Fiction", 1965),
    ("Foundation", "Isaac Asimov", "Science Fiction", 1951),
    ("Neuromancer", "William Gibson", "Science Fiction", 1984),
    ("The Left Hand of Darkness", "Ursula K. Le Guin", "Science Fiction", 1969),
    ("The Hobbit", "J.R.R. Tolkien", "Fantasy", 1937),
    ("A Game of Thrones", "George R. R. Martin", "Fantasy", 1996),
    ("The Name of the Wind", "Patrick Rothfuss", "Fantasy", 2007),
    ("Mistborn", "Brandon Sanderson", "Fantasy", 2006),
    ("Gone Girl", "Gillian Flynn", "Mystery", 2012),
    ("The Girl with the Dragon Tattoo", "Stieg Larsson", "Mystery", 2005),
    ("And Then There Were None", "Agatha Christie", "Mystery", 1939),
    ("Sapiens", "Yuval Noah Harari", "Non-Fiction", 2011),
    ("Educated", "Tara Westover", "Non-Fiction", 2018),
    ("The Immortal Life of Henrietta Lacks", "Rebecca Skloot", "Non-Fiction", 2010),
    ("Pride and Prejudice", "Jane Austen", "Classic", 1813),
    ("Nineteen Eighty-Four", "George Orwell", "Classic", 1949),
    ("The Great Gatsby", "F. Scott Fitzgerald", "Classic", 1925),
]


def seed() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DROP TABLE IF EXISTS books")
    conn.execute(
        """
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            genre TEXT NOT NULL,
            published_year INTEGER NOT NULL
        )
        """
    )
    conn.executemany(
        "INSERT INTO books (title, author, genre, published_year) VALUES (?, ?, ?, ?)",
        BOOKS,
    )
    conn.commit()
    conn.close()
    print(f"Seeded {len(BOOKS)} books into {DB_PATH}")


if __name__ == "__main__":
    seed()
