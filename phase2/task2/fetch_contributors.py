import requests


class RepoNotFoundError(Exception):
    pass


class RateLimitError(Exception):
    pass


def fetch_contributors(repo, limit=3):
    """Fetch the top `limit` contributors for a GitHub repo.

    Args:
        repo: "owner/name" string.
        limit: how many top contributors to return.

    Returns:
        List of {"login": str, "contributions": int} dicts.

    Raises:
        RepoNotFoundError: if the repo doesn't exist (404).
        RateLimitError: if GitHub rate-limits this request (403 + rate limit message).
    """
    url = f"https://api.github.com/repos/{repo}/contributors"
    response = requests.get(url, params={"per_page": limit})

    if response.status_code == 404:
        raise RepoNotFoundError(f"Repo '{repo}' not found")

    if response.status_code == 403:
        message = response.json().get("message", "")
        if "rate limit" in message.lower():
            raise RateLimitError(f"GitHub API rate limit exceeded: {message}")
        response.raise_for_status()

    response.raise_for_status()

    return [
        {"login": c["login"], "contributions": c["contributions"]}
        for c in response.json()[:limit]
    ]
