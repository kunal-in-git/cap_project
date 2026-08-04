# Task B — MCP Server over a Local SQLite Library

An MCP server exposing 2 tools over a local SQLite database, connected to and demonstrated with Claude.

## Files
- `mcp_server.py` — the MCP server (`search_books`, `library_stats`)
- `seed_db.py` — creates and seeds `library.db` with 15 sample books
- `library.db` — the SQLite database
- `requirements.txt` — the `mcp` SDK
- `bugfix.txt` — a real bug hit while running this against Claude, and its fix

## Data source
A local SQLite `books` table: `id`, `title`, `author`, `category`, `published_year` — 15 books across 6 categories (Fantasy, Science Fiction, Dystopian, Romance, Adventure, Classic), spanning 1811–1984.

## Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python seed_db.py
```

## Tool 1 — `search_books(query)`
Runs `SELECT ... WHERE title LIKE ? OR author LIKE ?` with the keyword wrapped for partial matching, and returns matching rows as a list of dicts.

## Tool 2 — `library_stats()`
Returns one summary object built from three queries: total record count, a category → count breakdown, and the earliest/latest `published_year`.

## Testing standalone (MCP Inspector)
```bash
npx @modelcontextprotocol/inspector venv/bin/python3 mcp_server.py
```
Opens a browser UI to call each tool directly and inspect the raw MCP protocol messages.

## Connecting to Claude
```bash
claude mcp add library-server -- venv/bin/python3 mcp_server.py
claude mcp list      # confirm it shows connected
```
Then, in a Claude Code session, ask a question that needs both tools, e.g.: *"How many books are in the library and what categories are represented? Also, do we have anything by Tolkien?"* — Claude calls `library_stats` for the first part and `search_books` for the second.

## Errors encountered and fixes
See `bugfix.txt` for the full trace. Summary: the server initially opened `library.db` with a relative path (`DB_PATH = "library.db"`). SQLite resolves relative paths against the **process's** working directory, not the script's location — since Claude launched the MCP server with its cwd at the project root, this silently created and queried an empty `library.db` there instead of the real seeded one in `phase3/task2/`, producing a `no such table: books` error. Fixed by resolving the path relative to the script itself: `DB_PATH = Path(__file__).resolve().parent / "library.db"`, and deleting the stray empty database that had been auto-created at the root.

## AI-Generated Parts
Built with Claude Code CLI: the seed script, both MCP tools, and the fix for the working-directory bug above (diagnosed and applied by Claude after the server was connected and actually exercised).
