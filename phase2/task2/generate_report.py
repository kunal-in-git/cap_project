"""Step 2 of the pipeline: turn fetch_contributors' results into a
markdown report.

Input:  the list of dicts produced by `fetch_contributors.fetch_all`.
Output: a markdown string, and that string written to a file.
"""

import logging


def generate_markdown_report(results: list[dict], generated_at: str) -> str:
    """Build a markdown report from per-repo contributor results.

    Each repo gets a section: a table of its top contributors, or a
    note explaining why it has none (not found, rate-limited, etc).
    """
    lines = ["# Top Contributors Report", "", f"_Generated: {generated_at}_", ""]

    for entry in results:
        lines.append(f"## {entry['repo']}")
        lines.append("")
        if entry["error"]:
            lines.append(f"> ⚠️ {entry['error']}")
        elif not entry["contributors"]:
            lines.append("> No contributor data available.")
        else:
            lines.append("| Rank | Contributor | Contributions |")
            lines.append("|------|-------------|----------------|")
            for rank, c in enumerate(entry["contributors"], start=1):
                lines.append(f"| {rank} | {c['login']} | {c['contributions']} |")
        lines.append("")

    return "\n".join(lines)


def write_report(markdown: str, path: str, logger: logging.Logger) -> None:
    """Write `markdown` to `path`, logging the outcome."""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(markdown)
    except OSError as exc:
        logger.error("Step 2: failed to write report to '%s' — %s", path, exc)
        raise
    logger.info("Step 2: report written to '%s'", path)
