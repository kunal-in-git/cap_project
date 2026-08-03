# Task A — Claude Code CLI: Autonomous Python Utility Module

A CSV data cleaner built end-to-end by Claude Code CLI: generated, refactored (type hints, docstrings, error handling), tested, and fixed autonomously. See [`session_log.md`](session_log.md) for the full session — prompts, outputs, the test failure that came up, and its fix.

## Files
- `csv_cleaner.py` — the module
- `tests/test_csv_cleaner.py` — 11 pytest tests, including edge cases
- `session_log.md` — the Claude Code session record

## Running it
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ -v
```

## API
```python
from csv_cleaner import clean_csv

clean_csv("raw.csv", "cleaned.csv", column_types={"age": int}, fill_value="0")
```
Pipeline: normalize headers → strip whitespace → drop empty rows → fill missing values → drop duplicate rows → optionally coerce column types → write to `output_path`. Returns the cleaned rows.
