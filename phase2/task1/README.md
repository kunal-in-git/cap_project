# Task A — Claude Code CLI: Autonomous Python Utility Module

A CSV data cleaner built with Claude Code CLI: generated, refactored (type hints, docstrings, error handling), then tested with an 11-case pytest suite covering normal and edge cases.

## Files
- `csv_cleaner.py` — the module
- `tests/test_csv_cleaner.py` — 11 pytest tests
- `steps.txt` — the prompts used and the final test run output

## Running it
```bash
python3 -m venv venv
source venv/bin/activate
pip install pytest
pytest tests/ -v
```

## API
```python
from csv_cleaner import clean_csv

clean_csv("raw.csv", "cleaned.csv", column_types={"age": int}, fill_value="0")
```
Pipeline: normalize headers → strip whitespace → drop empty rows → fill missing values → drop duplicate rows → optionally coerce column types → write to `output_path`. Returns the cleaned rows.

## Functions
- `read_csv(path)` — read a CSV into a list of dict rows
- `normalize_headers(rows)` — lowercase, strip, spaces → underscores in header keys
- `strip_whitespace_values(rows)` — strip whitespace from string values
- `drop_empty_rows(rows)` — remove fully-empty rows
- `drop_duplicate_rows(rows)` — remove exact-duplicate rows
- `fill_missing(rows, fill_value)` — fill missing/empty values with a default
- `coerce_column_types(rows, column_types)` — convert named columns to given types; raises `KeyError` for a missing column and `ValueError` (naming the column, value, and original exception) for a bad conversion
- `write_csv(rows, path)` — write cleaned rows back out
- `clean_csv(...)` — orchestrator chaining all of the above

## Verified output
```
$ pytest tests/ -v
...
11 passed in 0.02s
```
All 11 tests passed on the first run against the current module — 6 covering individual transform functions, 5 targeting edge cases (missing column during coercion, unconvertible value during coercion, writing zero rows, reading a nonexistent file, and a full end-to-end `clean_csv` run).

## AI-Generated Parts
This module and its test suite were built with Claude Code CLI across three prompts: initial generation, a refactor pass (type hints/docstrings/error handling), and test authoring. See `steps.txt` for the exact prompts used.
