"""MCP server exposing tools over a local SQLite library database."""

import sqlite3
from pathlib import Path

from mcp.server import MCPServer

DB_PATH = Path(__file__).resolve().parent / "library.db"

mcp = MCPServer("library-server")


def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


@mcp.tool()
def search_books(query: str) -> list[dict]:
    """Search books by title or author keyword.

    Args:
        query: A keyword to match against book titles or author names.

    Returns:
        A list of matching books, each with id, title, author, category,
        and published_year.
    """
    conn = _get_connection()
    try:
        cursor = conn.execute(
            "SELECT id, title, author, category, published_year "
            "FROM books WHERE title LIKE ? OR author LIKE ?",
            (f"%{query}%", f"%{query}%"),
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()


@mcp.tool()
def library_stats() -> dict:
    """Get an overview of the library data: total records, category
    breakdown, and the range of publication years.

    Returns:
        A summary object with total_records, categories (a mapping of
        category name to count), and earliest_year/latest_year.
    """
    conn = _get_connection()
    try:
        total_records = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]

        category_rows = conn.execute(
            "SELECT category, COUNT(*) AS count FROM books GROUP BY category"
        ).fetchall()
        categories = {row["category"]: row["count"] for row in category_rows}

        year_row = conn.execute(
            "SELECT MIN(published_year), MAX(published_year) FROM books"
        ).fetchone()
        earliest_year, latest_year = year_row[0], year_row[1]

        return {
            "total_records": total_records,
            "categories": categories,
            "earliest_year": earliest_year,
            "latest_year": latest_year,
        }
    finally:
        conn.close()


if __name__ == "__main__":
    mcp.run()
