import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from csv_cleaner import (  # noqa: E402
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


def test_normalize_headers():
    rows = [{" Full Name ": "Alice", "Age": "30"}]
    result = normalize_headers(rows)
    assert result == [{"full_name": "Alice", "age": "30"}]


def test_strip_whitespace_values():
    rows = [{"name": "  Alice  ", "age": "30"}]
    result = strip_whitespace_values(rows)
    assert result == [{"name": "Alice", "age": "30"}]


def test_drop_empty_rows():
    rows = [{"name": "Alice"}, {"name": "", "age": ""}]
    result = drop_empty_rows(rows)
    assert result == [{"name": "Alice"}]


def test_drop_duplicate_rows():
    rows = [{"name": "Alice"}, {"name": "Alice"}, {"name": "Bob"}]
    result = drop_duplicate_rows(rows)
    assert result == [{"name": "Alice"}, {"name": "Bob"}]


def test_fill_missing():
    rows = [{"name": "Alice", "age": ""}]
    result = fill_missing(rows, fill_value="0")
    assert result == [{"name": "Alice", "age": "0"}]


def test_coerce_column_types_success():
    rows = [{"name": "Alice", "age": "30"}]
    result = coerce_column_types(rows, {"age": int})
    assert result == [{"name": "Alice", "age": 30}]


def test_coerce_column_types_missing_column_raises_keyerror():
    rows = [{"name": "Alice"}]
    with pytest.raises(KeyError):
        coerce_column_types(rows, {"age": int})


def test_coerce_column_types_bad_value_raises_valueerror():
    rows = [{"name": "Alice", "age": "not-a-number"}]
    with pytest.raises(ValueError):
        coerce_column_types(rows, {"age": int})


def test_write_csv_empty_rows(tmp_path):
    path = tmp_path / "out.csv"
    write_csv([], str(path))
    assert path.read_text() == ""


def test_read_csv_missing_file_raises_filenotfounderror(tmp_path):
    path = tmp_path / "does_not_exist.csv"
    with pytest.raises(FileNotFoundError):
        read_csv(str(path))


def test_clean_csv_end_to_end(tmp_path):
    raw = tmp_path / "raw.csv"
    raw.write_text(
        "Name, Age\n"
        " Alice ,30\n"
        " Alice ,30\n"
        "Bob,\n"
        ",\n"
    )
    output = tmp_path / "cleaned.csv"

    result = clean_csv(
        str(raw), str(output), column_types={"age": int}, fill_value="0"
    )

    assert result == [
        {"name": "Alice", "age": 30},
        {"name": "Bob", "age": 0},
    ]
    assert output.exists()
