# Task B — Agentic GitHub Contributors Pipeline

An agentic pipeline: read repo names from a text file → fetch each repo's top 3 contributors from the GitHub API → write a markdown summary report.

## Pipeline steps
Two distinct steps with a clear data contract between them:

1. **`fetch_contributors.py`** — `read_repo_list(path) -> list[str]`, then `fetch_all(repos, logger) -> list[dict]`. Each result dict is `{"repo": str, "contributors": list[{"login", "contributions"}] | None, "error": str | None}`.
2. **`generate_report.py`** — `generate_markdown_report(results, generated_at) -> str`, then `write_report(markdown, path, logger)`.

`pipeline.py` sets up logging and chains the two:
```
repos.txt --[Step 1: fetch_all]--> results --[Step 2: generate_markdown_report]--> report.md
```

## Error handling
- **Repo doesn't exist:** the GitHub API returns 404 → `RepoNotFoundError` is caught per-repo; that repo's entry gets `error: "Repository '...' not found"` and the pipeline keeps going.
- **Rate-limited:** a 403 with `X-RateLimit-Remaining: 0` → `RateLimitError`. The pipeline stops making further API calls (to avoid hammering an exhausted quota) and marks every remaining repo as `"Skipped: rate limit exceeded"`.
- Both paths are covered by mocked tests in `tests/test_fetch_contributors.py` (`test_fetch_all_stops_calling_api_after_rate_limit`, `test_fetch_all_records_not_found_without_stopping`) — mocked so the tests don't burn real API quota to prove the rate-limit branch works.

## Logging
Every step logs its action and result via Python's `logging` module to both stdout and `pipeline.log` (timestamp, level, message) — e.g. `Step 1: fetching top contributors for 'owner/repo'` followed by either a success line listing the contributors or an error line.

## Running it
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 pipeline.py
```
Reads `repos.txt`, writes `report.md` and `pipeline.log`.

Run the tests with:
```bash
pip install pytest
pytest tests/ -v
```

## Verified run
`repos.txt` includes two real repos and one that doesn't exist, to exercise both the success and 404 paths in one run:
```
octocat/Hello-World
octocat/Spoon-Knife
octocat/this-repo-does-not-exist-xyz123
```
Actual output — `pipeline.log`:
```
Pipeline started
Loaded 3 repo(s) from 'repos.txt'
Step 1: fetching top contributors for 'octocat/Hello-World'
Step 1: 'octocat/Hello-World' succeeded — top contributors: Spaceghost, octocat, Cameron423698
Step 1: fetching top contributors for 'octocat/Spoon-Knife'
Step 1: 'octocat/Spoon-Knife' succeeded — top contributors: octocat
Step 1: fetching top contributors for 'octocat/this-repo-does-not-exist-xyz123'
Step 1: 'octocat/this-repo-does-not-exist-xyz123' failed — Repository '...' not found
Step 2: report written to 'report.md'
Pipeline finished: 2/3 repo(s) succeeded
```
The resulting `report.md` is committed in this folder as evidence of a real, successful run.

## AI tool usage per step
Every step below was built with Claude Code CLI (Claude, Anthropic), in the same session:

1. **Initial pipeline code** — prompt: *"Write a two-step Python pipeline: step 1 reads a list of 'owner/repo' names from a text file and fetches each repo's top 3 contributors from the GitHub API; step 2 turns those results into a markdown report. Give each step a clear input/output contract and handle a repo that doesn't exist and a GitHub API rate-limit response without crashing the whole run."* Claude generated `fetch_contributors.py`, `generate_report.py`, and the `pipeline.py` orchestrator directly from this prompt.
2. **Step separation** — the input/output contract between the two steps (the `{"repo", "contributors", "error"}` dict shape) was part of the same initial generation, designed so Step 2 never needs to know how Step 1 got its data.
3. **Error handling** — the `RepoNotFoundError`/`RateLimitError` distinction and the "stop calling the API after a rate limit, but keep going after a 404" behavior were specified in the initial prompt and implemented by Claude; verified with mocked tests rather than by actually exhausting the GitHub rate limit.
4. **Logging** — added by Claude as part of the initial generation (`setup_logger()` in `pipeline.py`, called at both the fetch and report-write steps).
5. **Report formatting** — the markdown table structure was written by Claude and validated against a real pipeline run (see `report.md`).
6. **This README** — written by Claude, summarizing the above.
