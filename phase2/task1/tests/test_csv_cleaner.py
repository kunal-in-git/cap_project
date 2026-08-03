import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from csv_cleaner import (
    clean_csv,
    coerce_column_types,
    drop_duplicate_rows,
    drop_empty_rows,
    fill_missing,
    normalize_headers,
    read_csv,
    strip_whitespace_values,
    write_csv,
)


def test_normalize_headers_lowercases_and_underscores_spaces():
    rows = [{" Full Name ": "Alice", "Age": "30"}]

    result = normalize_headers(rows)

    assert result == [{"full_name": "Alice", "age": "30"}]


def test_strip_whitespace_values_trims_strings_only():
    rows = [{"name": "  Bob  ", "age": 5}]

    result = strip_whitespace_values(rows)

    assert result == [{"name": "Bob", "age": 5}]


def test_drop_empty_rows_removes_all_blank_rows():
    rows = [{"a": "", "b": ""}, {"a": "1", "b": ""}]

    result = drop_empty_rows(rows)

    assert result == [{"a": "1", "b": ""}]


def test_drop_duplicate_rows_keeps_first_occurrence():
    rows = [{"a": "1"}, {"a": "1"}, {"a": "2"}]

    result = drop_duplicate_rows(rows)

    assert result == [{"a": "1"}, {"a": "2"}]


def test_fill_missing_replaces_empty_and_none():
    rows = [{"a": "", "b": None, "c": "x"}]

    result = fill_missing(rows, fill_value="N/A")

    assert result == [{"a": "N/A", "b": "N/A", "c": "x"}]


def test_coerce_column_types_converts_named_columns():
    rows = [{"age": "30", "name": "Alice"}]

    result = coerce_column_types(rows, {"age": int})

    assert result == [{"age": 30, "name": "Alice"}]


# --- Edge cases -----------------------------------------------------

def test_coerce_column_types_missing_column_raises_keyerror():
    rows = [{"name": "Alice"}]

    with pytest.raises(KeyError):
        coerce_column_types(rows, {"age": int})


def test_coerce_column_types_unconvertible_value_raises_valueerror():
    rows = [{"age": "not-a-number"}]

    with pytest.raises(ValueError):
        coerce_column_types(rows, {"age": int})


def test_write_csv_with_no_rows_writes_empty_file(tmp_path):
    out = tmp_path / "empty.csv"

    write_csv([], str(out))

    assert out.read_text() == ""


def test_read_csv_missing_file_raises_filenotfounderror(tmp_path):
    missing = tmp_path / "does_not_exist.csv"

    with pytest.raises(FileNotFoundError):
        read_csv(str(missing))


def test_clean_csv_end_to_end(tmp_path):
    input_csv = tmp_path / "raw.csv"
    output_csv = tmp_path / "cleaned.csv"
    input_csv.write_text(
        "Name, Age\n"
        " Alice ,30\n"
        " Alice ,30\n"  # exact duplicate after cleaning
        "Bob,\n"
        ",\n"  # fully empty row
    )

    result = clean_csv(
        str(input_csv), str(output_csv), column_types={"age": int}, fill_value="0"
    )

    assert result == [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 0},
    ]
    assert output_csv.exists()
