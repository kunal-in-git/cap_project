"""Orchestrator: chains Step 1 (fetch_contributors) -> Step 2
(generate_report) and sets up logging for the whole run.

    repos.txt --[Step 1: fetch_all]--> results --[Step 2: generate_markdown_report]--> report.md
"""

import datetime
import logging
import sys

from fetch_contributors import fetch_all, read_repo_list
from generate_report import generate_markdown_report, write_report

REPOS_FILE = "repos.txt"
REPORT_FILE = "report.md"
LOG_FILE = "pipeline.log"


def setup_logger() -> logging.Logger:
    logger = logging.getLogger("pipeline")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()

    formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger


def run() -> None:
    logger = setup_logger()
    logger.info("Pipeline started")

    repos = read_repo_list(REPOS_FILE)
    logger.info("Loaded %d repo(s) from '%s'", len(repos), REPOS_FILE)

    results = fetch_all(repos, logger)

    generated_at = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    markdown = generate_markdown_report(results, generated_at)
    write_report(markdown, REPORT_FILE, logger)

    succeeded = sum(1 for r in results if r["error"] is None)
    logger.info("Pipeline finished: %d/%d repo(s) succeeded", succeeded, len(results))


if __name__ == "__main__":
    run()
