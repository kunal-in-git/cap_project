"""MCP server exposing 2 tools over a local SQLite book library.

Tool 1: search_books  — keyword search over title/author/genre.
Tool 2: library_summary — overview stats (count, genres, year range).
"""

import sqlite3
from pathlib import Path

from mcp.server.mcpserver import MCPServer

DB_PATH = Path(__file__).resolve().parent / "library.db"

mcp = MCPServer("library")


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@mcp.tool()
def search_books(query: str) -> list[dict]:
    """Search the book library by keyword.

    Matches against title, author, and genre (case-insensitive,
    substring match). Returns an empty list if nothing matches.

    Args:
        query: a keyword to search for, e.g. an author's name, a
            word from a title, or a genre.
    """
    conn = _connect()
    try:
        pattern = f"%{query}%"
        rows = conn.execute(
            """
            SELECT id, title, author, genre, published_year
            FROM books
            WHERE title LIKE ? OR author LIKE ? OR genre LIKE ?
            ORDER BY published_year
            """,
            (pattern, pattern, pattern),
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()


@mcp.tool()
def library_summary() -> dict:
    """Return overview statistics about the book library.

    Includes the total number of books, a count of books per genre,
    and the earliest/latest publication years in the collection.
    """
    conn = _connect()
    try:
        total = conn.execute("SELECT COUNT(*) AS n FROM books").fetchone()["n"]
        genre_rows = conn.execute(
            "SELECT genre, COUNT(*) AS n FROM books GROUP BY genre ORDER BY n DESC"
        ).fetchall()
        year_row = conn.execute(
            "SELECT MIN(published_year) AS earliest, MAX(published_year) AS latest FROM books"
        ).fetchone()
        return {
            "total_books": total,
            "genres": {row["genre"]: row["n"] for row in genre_rows},
            "earliest_year": year_row["earliest"],
            "latest_year": year_row["latest"],
        }
    finally:
        conn.close()


if __name__ == "__main__":
    mcp.run()
