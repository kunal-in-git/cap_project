import logging

from fetch_contributors import RateLimitError, RepoNotFoundError, fetch_contributors
from generate_report import generate_report

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)


def read_repo_list(path):
    """Read repo names (one per line) from a text file.

    Args:
        path: path to the input file.

    Returns:
        List of "owner/name" strings.
    """
    logger.info("Step 1: reading repo list from '%s'", path)
    with open(path, encoding="utf-8") as f:
        repos = [line.strip() for line in f if line.strip()]
    logger.info("Step 1: read %d repos", len(repos))
    return repos


def fetch_all_contributors(repos):
    """Fetch top contributors for each repo, tolerating per-repo failures.

    Args:
        repos: list of "owner/name" strings.

    Returns:
        dict mapping repo -> list of contributor dicts, or an error
        message string if that repo's fetch failed.
    """
    logger.info("Step 2: fetching contributors for %d repos", len(repos))
    results = {}
    for repo in repos:
        try:
            contributors = fetch_contributors(repo)
            results[repo] = contributors
            logger.info("Step 2: '%s' -> %d contributors", repo, len(contributors))
        except RepoNotFoundError as exc:
            results[repo] = str(exc)
            logger.warning("Step 2: '%s' failed: %s", repo, exc)
        except RateLimitError as exc:
            results[repo] = str(exc)
            logger.error("Step 2: '%s' failed: %s", repo, exc)
            logger.error("Step 2: stopping early, rate limit hit")
            break
    return results


def write_report(report, path):
    """Write the markdown report to a file.

    Args:
        report: markdown string.
        path: output file path.
    """
    logger.info("Step 3: writing report to '%s'", path)
    with open(path, "w", encoding="utf-8") as f:
        f.write(report)
    logger.info("Step 3: report written (%d bytes)", len(report))


def run_pipeline(repos_path, report_path):
    logger.info("=== Pipeline run started ===")
    repos = read_repo_list(repos_path)
    results = fetch_all_contributors(repos)
    report = generate_report(results)
    write_report(report, report_path)
    logger.info("=== Pipeline run finished ===")
    return report


if __name__ == "__main__":
    run_pipeline("repos.txt", "report.md")
