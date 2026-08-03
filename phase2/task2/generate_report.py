def generate_report(results):
    """Build a markdown report from per-repo contributor data.

    Args:
        results: dict mapping repo name -> either a list of contributor
            dicts ({"login", "contributions"}) or an error string.

    Returns:
        Markdown-formatted report as a string.
    """
    lines = ["# Contributor Report", ""]
    for repo, contributors in results.items():
        lines.append(f"## {repo}")
        if isinstance(contributors, str):
            lines.append(f"_Error: {contributors}_")
        elif not contributors:
            lines.append("_No contributors found._")
        else:
            for i, contributor in enumerate(contributors, start=1):
                lines.append(
                    f"{i}. {contributor['login']} — {contributor['contributions']} contributions"
                )
        lines.append("")
    return "\n".join(lines)
