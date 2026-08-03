import csv
from typing import Any, Callable

Row = dict[str, Any]


def read_csv(path: str) -> list[Row]:
    """Read a CSV file into a list of dict rows.

    Raises:
        FileNotFoundError: if `path` does not exist.
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def normalize_headers(rows: list[Row]) -> list[Row]:
    """Lowercase, strip, and underscore-ify each row's header keys."""
    new_rows = []
    for row in rows:
        new_row = {
            key.strip().lower().replace(" ", "_"): value
            for key, value in row.items()
        }
        new_rows.append(new_row)
    return new_rows


def strip_whitespace_values(rows: list[Row]) -> list[Row]:
    """Strip leading/trailing whitespace from every string value."""
    new_rows = []
    for row in rows:
        new_row = {
            key: value.strip() if isinstance(value, str) else value
            for key, value in row.items()
        }
        new_rows.append(new_row)
    return new_rows


def drop_empty_rows(rows: list[Row]) -> list[Row]:
    """Drop rows where every value is falsy (empty string, None, etc.)."""
    return [row for row in rows if any(value for value in row.values())]


def drop_duplicate_rows(rows: list[Row]) -> list[Row]:
    """Drop rows that are exact duplicates of an earlier row."""
    seen = set()
    new_rows = []
    for row in rows:
        key = tuple(sorted(row.items()))
        if key not in seen:
            seen.add(key)
            new_rows.append(row)
    return new_rows


def fill_missing(rows: list[Row], fill_value: str = "") -> list[Row]:
    """Replace `None`/empty-string values with `fill_value`."""
    new_rows = []
    for row in rows:
        new_row = {
            key: (value if value not in (None, "") else fill_value)
            for key, value in row.items()
        }
        new_rows.append(new_row)
    return new_rows


def coerce_column_types(
    rows: list[Row], column_types: dict[str, Callable[[Any], Any]]
) -> list[Row]:
    """Convert named columns to the given target types.

    Raises:
        KeyError: if a named column is missing from a row.
        ValueError: if a value can't be converted by its target type.
    """
    new_rows = []
    for row in rows:
        new_row = dict(row)
        for column, converter in column_types.items():
            if column not in new_row:
                raise KeyError(f"Column '{column}' not found in row: {row}")
            value = new_row[column]
            try:
                new_row[column] = converter(value)
            except (ValueError, TypeError) as exc:
                raise ValueError(
                    f"Could not convert column '{column}' value {value!r} "
                    f"using {getattr(converter, '__name__', converter)}: {exc}"
                ) from exc
        new_rows.append(new_row)
    return new_rows


def write_csv(rows: list[Row], path: str) -> None:
    """Write rows to a CSV file at `path`. Writes an empty file if `rows` is empty."""
    if not rows:
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return
    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def clean_csv(
    input_path: str,
    output_path: str,
    column_types: dict[str, Callable[[Any], Any]] | None = None,
    fill_value: str = "",
) -> list[Row]:
    """Read, clean, and write a CSV file.

    Pipeline: normalize headers -> strip whitespace -> drop empty rows ->
    fill missing values -> drop duplicate rows -> optionally coerce column
    types -> write to `output_path`.

    Returns:
        The cleaned rows.
    """
    rows = read_csv(input_path)
    rows = normalize_headers(rows)
    rows = strip_whitespace_values(rows)
    rows = drop_empty_rows(rows)
    rows = fill_missing(rows, fill_value)
    rows = drop_duplicate_rows(rows)
    if column_types:
        rows = coerce_column_types(rows, column_types)
    write_csv(rows, output_path)
    return rows
