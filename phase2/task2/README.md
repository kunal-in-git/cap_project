# Task B — Agentic GitHub Contributors Pipeline

A working agentic pipeline: read a list of GitHub repo names from a text file → call the GitHub API to get each repo's top contributors → write a summary markdown report. Built with Claude Code CLI, with real error handling and logging, not just described.

## Files
- `repos.txt` — input: one `owner/repo` per line
- `fetch_contributors.py` — calls the GitHub API for one repo; raises `RepoNotFoundError` / `RateLimitError` on failure
- `generate_report.py` — builds the markdown report from per-repo results
- `pipeline.py` — orchestrator: reads the repo list, fetches all contributors (tolerating per-repo failures), writes the report; logs every step to `pipeline.log`
- `report.md` — the generated output
- `pipeline.log` — the execution log from the run that produced `report.md`
- `requirements.txt` — just `requests`

## Running it
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python pipeline.py
```
Reads `repos.txt`, writes `report.md`, and appends to `pipeline.log`.

## The 3 distinct steps
1. `read_repo_list(path) -> list[str]` — reads repo names from the input file
2. `fetch_all_contributors(repos) -> dict` — calls `fetch_contributors()` per repo, catching `RepoNotFoundError`/`RateLimitError` so one bad repo doesn't kill the run
3. `write_report(report, path)` — writes the markdown built by `generate_report(results) -> str`

`run_pipeline()` orchestrates all three in order.

## Error handling
- **Repo doesn't exist** (404) → `RepoNotFoundError`, logged as a warning, shown in the report as `_Error: ..._`, pipeline continues to the next repo.
- **GitHub API rate limit** (403 + rate-limit message) → `RateLimitError`, logged as an error, pipeline stops early (no point hammering a rate-limited API further) — everything fetched so far still makes it into the report.

`repos.txt` intentionally includes a fake repo (`this-repo/does-not-exist`) so the 404 path is actually exercised, not just present in code.

## Verified output
`report.md`, generated from a real run against the GitHub API:
```
# Contributor Report

## pallets/flask
1. davidism — 1846 contributions
2. mitsuhiko — 1189 contributions
3. untitaker — 274 contributions

## psf/requests
1. kennethreitz — 1006 contributions
2. Lukasa — 610 contributions
3. sigmavirus24 — 396 contributions

## this-repo/does-not-exist
_Error: Repo 'this-repo/does-not-exist' not found_
```
`pipeline.log` shows the matching per-step trace (repos read, per-repo fetch outcome, the 404 warning, report bytes written).

## AI-Generated Parts
Built with Claude Code CLI in one pass covering all three requirements (≥3 distinct steps, error handling, logging) together, then run for real against the live GitHub API to confirm the error-handling path actually fires.
