# Task C — Mini-Tasks: Copilot vs. Claude

Three small, independent prompts, each answered by both GitHub Copilot and Claude for comparison.

## Files
- `q1.txt` — Mini-task 1: validate an email address with regex
- `q2.txt` — Mini-task 2: find duplicate records in a table based on two columns
- `q3.txt` — Mini-task 3: explain a JavaScript Promise code snippet

## Q1 — Email validation
Both tools converged on the same regex shape (`^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$`). Copilot's version is a standalone function with inline example usage; Claude's version compiles the pattern once at module scope (`EMAIL_PATTERN`) and adds a type hint on the function signature.

## Q2 — Duplicate records by two columns
Copilot's answer is a generic template (`table_name`, `column1`, `column2`). Claude's answer uses concrete column names (`email`, `phone` on a `users` table) as a worked example, and additionally shows how to `JOIN` back to the source table to retrieve full duplicate rows rather than just the grouped column values + count.

## Q3 — Explaining a JS Promise snippet
A walkthrough of a `downloadFile` Promise example: promise creation with `resolve`/`reject`, the `.then()`/`.catch()`/`.finally()` consumption chain, the actual console output for both the success and failure paths, and the three Promise states (pending/fulfilled/rejected).

## AI-Generated Parts
All three answers were generated with Claude (Anthropic); Q1 and Q2 additionally include a GitHub Copilot answer for side-by-side comparison, captured verbatim in each file.
