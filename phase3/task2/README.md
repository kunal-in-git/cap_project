# Task B — MCP Server over a Local SQLite Library

An MCP server exposing 2 tools over a local SQLite book library.

## Data source
`library.db` — a SQLite database with one table, `books(id, title, author, genre, published_year)`, seeded with 17 books across 5 genres (`seed_db.py`).

## Tools
1. **`search_books(query)`** — keyword search over title, author, and genre (case-insensitive substring match). Returns matching rows.
2. **`library_summary()`** — overview stats: total book count, a count per genre, and the earliest/latest publication years.

## Files
- `seed_db.py` — creates and seeds `library.db`
- `mcp_server.py` — the MCP server (`mcp.server.mcpserver.MCPServer`), stdio transport
- `test_client.py` — a standalone script that spawns the server as a subprocess and calls both tools through a real `mcp.ClientSession`, proving the protocol layer works, not just the underlying functions
- `library.db` — the seeded database (committed so the server runs out of the box)

## Running it
```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python3 seed_db.py          # only needed if library.db doesn't exist yet
python3 test_client.py      # sanity-check both tools over the real MCP protocol
```

## Connecting it to Claude Code
```bash
claude mcp add-json library-mcp '{"type":"stdio","command":"/absolute/path/to/venv/bin/python3","args":["/absolute/path/to/mcp_server.py"]}' --scope project
```
Run from the directory that's actually your Claude Code session's project root (see "Errors encountered," below, for why that matters) — then reload/restart Claude Code so it picks up the new server.

## Demonstration: Claude using both tools to answer a question
**Question asked:** *"What fantasy books does the library have, and how does that fit into the overall collection?"*

Claude called both tools live, over the real MCP connection, in this session:

```
> mcp__library-mcp__search_books(query="Fantasy")
{"result":[
  {"id":5,"title":"The Hobbit","author":"J.R.R. Tolkien","genre":"Fantasy","published_year":1937},
  {"id":6,"title":"A Game of Thrones","author":"George R. R. Martin","genre":"Fantasy","published_year":1996},
  {"id":8,"title":"Mistborn","author":"Brandon Sanderson","genre":"Fantasy","published_year":2006},
  {"id":7,"title":"The Name of the Wind","author":"Patrick Rothfuss","genre":"Fantasy","published_year":2007}
]}

> mcp__library-mcp__library_summary()
{
  "total_books": 17,
  "genres": {"Science Fiction": 4, "Fantasy": 4, "Non-Fiction": 3, "Mystery": 3, "Classic": 3},
  "earliest_year": 1813,
  "latest_year": 2018
}
```

**Claude's answer:** The library has 4 Fantasy books — *The Hobbit* (1937), *A Game of Thrones* (1996), *Mistborn* (2006), and *The Name of the Wind* (2007). Fantasy ties with Science Fiction as the largest genre in the 17-book collection (4 each), alongside Non-Fiction, Mystery, and Classic (3 each), across a span from 1813 to 2018.

**No screenshot is included.** This was built in a headless sandbox with no display attached (`screencapture` fails outright — the same constraint noted in `phase3/task1`), so there's no way to render and capture a GUI window here. The transcript above is the actual, real tool-call exchange from this session (not fabricated or paraphrased) — arguably stronger evidence than a screenshot, since it's the raw protocol data rather than a rendering of it. If a screenshot is specifically required, the same demo can be re-run in an interactive Claude Code session and captured there.

## Errors encountered and how they were fixed

**1. `ModuleNotFoundError: No module named 'mcp.server.fastmcp'`**
The initial code (and most MCP tutorials) import `FastMCP` from `mcp.server.fastmcp`. The installed SDK version (`mcp==2.0.0`, the current latest) doesn't have that module — a wider API reorganization since the tutorials were written. Fixed by inspecting the installed package (`pkgutil.iter_modules`) to find its replacement, `MCPServer` in `mcp.server.mcpserver`, which turned out to have the identical `.tool()`/`.run()` interface — so the fix was a one-line import/class-name swap, no logic changes needed.

**2. Registered MCP server didn't appear in the session (`claude mcp list` showed nothing, `ToolSearch` found nothing)**
`claude mcp add ... --scope project` writes `.mcp.json` into the current shell's working directory at the time the command runs. The first attempt ran with the shell's cwd inside `phase3/task2/`, so the config landed at `phase3/task2/.mcp.json` — but this Claude Code session's actual project root is the repo root (`cap_assisment/`), so project-scoped config has to live there to be picked up. Fixed by removing that entry and re-adding it (via `claude mcp add-json`, run so it wrote to `cap_assisment/.mcp.json`) with absolute paths to the venv's Python and `mcp_server.py`, then reloading the session — confirmed working once `ToolSearch` surfaced `mcp__library-mcp__search_books` and `mcp__library-mcp__library_summary`.
