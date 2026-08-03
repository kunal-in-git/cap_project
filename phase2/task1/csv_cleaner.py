"""A small utility module for cleaning CSV data.

Provides composable row-transform functions (normalize headers, strip
whitespace, drop empty/duplicate rows, fill missing values, coerce
column types) plus a `clean_csv` orchestrator that chains them and
writes the result back out to disk.
"""

import csv
from typing import Any, Callable, Optional

Row = dict[str, Any]


def read_csv(path: str) -> list[Row]:
    """Read a CSV file into a list of dict rows, keyed by header.

    Raises:
        FileNotFoundError: if `path` does not exist.
    """
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def normalize_headers(rows: list[Row]) -> list[Row]:
    """Lowercase, strip, and underscore-ify each row's keys."""
    return [
        {key.strip().lower().replace(" ", "_"): value for key, value in row.items()}
        for row in rows
    ]


def strip_whitespace_values(rows: list[Row]) -> list[Row]:
    """Strip leading/trailing whitespace from every string value."""
    return [
        {k: (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
        for row in rows
    ]


def drop_empty_rows(rows: list[Row]) -> list[Row]:
    """Drop rows where every value is an empty string."""
    return [row for row in rows if any(v != "" for v in row.values())]


def drop_duplicate_rows(rows: list[Row]) -> list[Row]:
    """Drop exact-duplicate rows, keeping the first occurrence."""
    seen: set[tuple[tuple[str, Any], ...]] = set()
    result = []
    for row in rows:
        key = tuple(sorted(row.items()))
        if key not in seen:
            seen.add(key)
            result.append(row)
    return result


def fill_missing(rows: list[Row], fill_value: str = "") -> list[Row]:
    """Replace `None` or empty-string values with `fill_value`."""
    return [
        {k: (fill_value if v is None or v == "" else v) for k, v in row.items()}
        for row in rows
    ]


def coerce_column_types(
    rows: list[Row], column_types: dict[str, Callable[[Any], Any]]
) -> list[Row]:
    """Convert each named column's values using the given callables.

    Args:
        rows: rows to convert (not mutated; a new list is returned).
        column_types: mapping of column name to a converter, e.g.
            `{"age": int, "price": float}`.

    Raises:
        KeyError: if a column named in `column_types` is missing from a row.
        ValueError: if a value cannot be converted by its column's converter.
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
    """Write rows to `path` as CSV, using the first row's keys as headers.

    Writes an empty file if `rows` is empty.
    """
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
    column_types: Optional[dict[str, Callable[[Any], Any]]] = None,
    fill_value: str = "",
) -> list[Row]:
    """Read, clean, and rewrite a CSV file.

    Pipeline: normalize headers -> strip whitespace -> drop empty rows ->
    fill missing values -> drop duplicate rows -> optionally coerce
    column types -> write to `output_path`.

    Args:
        input_path: path to the source CSV.
        output_path: path the cleaned CSV is written to.
        column_types: optional mapping of column name to converter,
            applied after cleaning (see `coerce_column_types`).
        fill_value: value used to replace missing/empty cells.

    Returns:
        The cleaned rows, as written to `output_path`.

    Raises:
        FileNotFoundError: if `input_path` does not exist.
        KeyError, ValueError: propagated from `coerce_column_types`
            if `column_types` names a missing column or an
            unconvertible value.
    """
    rows = read_csv(input_path)
    rows = normalize_headers(rows)
    rows = strip_whitespace_values(rows)
    rows = drop_empty_rows(rows)
    rows = fill_missing(rows, fill_value=fill_value)
    rows = drop_duplicate_rows(rows)
    if column_types:
        rows = coerce_column_types(rows, column_types)
    write_csv(rows, output_path)
    return rows
