import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from generate_report import generate_markdown_report


def test_report_includes_contributor_table_for_successful_repo():
    results = [
        {
            "repo": "owner/repo",
            "contributors": [{"login": "alice", "contributions": 5}],
            "error": None,
        }
    ]

    markdown = generate_markdown_report(results, generated_at="2026-01-01T00:00:00Z")

    assert "## owner/repo" in markdown
    assert "| 1 | alice | 5 |" in markdown


def test_report_includes_error_note_for_failed_repo():
    results = [{"repo": "owner/missing", "contributors": None, "error": "Repository not found"}]

    markdown = generate_markdown_report(results, generated_at="2026-01-01T00:00:00Z")

    assert "## owner/missing" in markdown
    assert "Repository not found" in markdown
    assert "|" not in markdown.split("## owner/missing")[1]
