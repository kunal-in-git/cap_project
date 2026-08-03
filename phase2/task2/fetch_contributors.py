"""Step 1 of the pipeline: read a repo list and fetch each repo's top
contributors from the GitHub API.

Input:  a text file of "owner/repo" lines.
Output: a list of dicts, one per repo:
    {"repo": str, "contributors": list[{"login": str, "contributions": int}] | None, "error": str | None}
"""

import logging
from typing import Optional

import requests

GITHUB_API = "https://api.github.com"


class RepoNotFoundError(Exception):
    """Raised when a repo doesn't exist (GitHub returns 404)."""


class RateLimitError(Exception):
    """Raised when the GitHub API rate limit has been exhausted."""


def read_repo_list(path: str) -> list[str]:
    """Read "owner/repo" names from `path`, one per line.

    Blank lines are skipped. Raises FileNotFoundError if `path` is missing.
    """
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def fetch_top_contributors(
    repo: str, top_n: int = 3, session: Optional[requests.Session] = None
) -> list[dict]:
    """Fetch the top `top_n` contributors (by contribution count) for `repo`.

    Args:
        repo: "owner/name", e.g. "octocat/Hello-World".
        top_n: how many contributors to return.
        session: optional `requests.Session` to reuse connections/auth.

    Raises:
        RepoNotFoundError: if the repo doesn't exist (404).
        RateLimitError: if the GitHub API rate limit is exhausted (403
            with `X-RateLimit-Remaining: 0`).
        requests.HTTPError: for any other non-2xx response.
        requests.RequestException: for network-level failures.
    """
    http = session or requests
    resp = http.get(f"{GITHUB_API}/repos/{repo}/contributors", params={"per_page": top_n})

    if resp.status_code == 404:
        raise RepoNotFoundError(f"Repository '{repo}' not found")
    if resp.status_code == 403 and resp.headers.get("X-RateLimit-Remaining") == "0":
        raise RateLimitError(
            f"GitHub API rate limit exceeded while fetching '{repo}'"
        )
    resp.raise_for_status()

    contributors = resp.json()
    contributors.sort(key=lambda c: c.get("contributions", 0), reverse=True)
    return [
        {"login": c["login"], "contributions": c["contributions"]}
        for c in contributors[:top_n]
    ]


def fetch_all(repos: list[str], logger: logging.Logger) -> list[dict]:
    """Fetch top contributors for every repo in `repos`.

    Stops calling the API as soon as a rate limit is hit (to avoid
    hammering an already-exhausted quota) and marks every remaining
    repo as skipped for that reason. Any other per-repo failure
    (missing repo, network error) is recorded on that repo's entry
    without stopping the run.
    """
    session = requests.Session()
    results: list[dict] = []
    rate_limited = False

    for i, repo in enumerate(repos):
        if rate_limited:
            logger.warning("Step 1: skipping '%s' — rate limit already hit", repo)
            results.append({"repo": repo, "contributors": None, "error": "Skipped: rate limit exceeded"})
            continue

        logger.info("Step 1: fetching top contributors for '%s'", repo)
        try:
            contributors = fetch_top_contributors(repo, session=session)
        except RepoNotFoundError as exc:
            logger.error("Step 1: '%s' failed — %s", repo, exc)
            results.append({"repo": repo, "contributors": None, "error": str(exc)})
        except RateLimitError as exc:
            logger.error("Step 1: '%s' failed — %s", repo, exc)
            results.append({"repo": repo, "contributors": None, "error": str(exc)})
            rate_limited = True
        except requests.RequestException as exc:
            logger.error("Step 1: '%s' failed — network error: %s", repo, exc)
            results.append({"repo": repo, "contributors": None, "error": f"Network error: {exc}"})
        else:
            logger.info(
                "Step 1: '%s' succeeded — top contributors: %s",
                repo,
                ", ".join(c["login"] for c in contributors),
            )
            results.append({"repo": repo, "contributors": contributors, "error": None})

    return results
