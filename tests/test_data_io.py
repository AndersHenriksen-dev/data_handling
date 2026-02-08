"""Unit and integration tests for the data_io module."""

from unittest.mock import patch

import pandas as pd
import pytest

from data_handling import data_io
from data_handling.data_io import _IOFactory


@pytest.fixture
def sample_df():
    """Provide a simple DataFrame for testing."""
    return pd.DataFrame({"id": [1, 2, 3], "name": ["Alice", "Bob", "Charlie"], "score": [85.5, 90.0, 92.5]})


def test_csv_writer_creates_file(sample_df, tmp_path):
    """Test that CSV writer saves a file correctly."""
    output_file = tmp_path / "output.csv"

    data_io.save_data(sample_df, str(output_file), "csv", index=False)

    assert output_file.exists()

    loaded_df = pd.read_csv(output_file)
    pd.testing.assert_frame_equal(sample_df, loaded_df)


def test_csv_writer_creates_nested_directories(sample_df, tmp_path):
    """Test that CSV writer creates missing parent directories automatically."""
    output_file = tmp_path / "deep" / "nested" / "folder" / "data.csv"

    data_io.save_data(sample_df, str(output_file), "csv", index=False)

    assert output_file.exists()


def test_csv_reader_reads_file(sample_df, tmp_path):
    """Test that CSV reader loads data correctly."""
    input_file = tmp_path / "input.csv"
    sample_df.to_csv(input_file, index=False)

    result_df = data_io.load_data(str(input_file), "csv")

    pd.testing.assert_frame_equal(sample_df, result_df)


def test_csv_reader_raises_error_on_missing_file():
    """Test that reading a non-existent file raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        data_io.load_data("non_existent_ghost_file.csv", "csv")


def test_sql_reader_requires_query():
    """Test that SQL reader raises ValueError if 'query' kwarg is missing."""
    with pytest.raises(ValueError, match="requires a 'query' argument"):
        data_io.load_data("postgres://fake-db", "sql")


def test_sql_reader_success():
    """Test the SQL reader success path (mocked)."""
    result_df = data_io.load_data("postgres://fake-db", "sql", query="SELECT *")

    assert not result_df.empty
    assert "id" in result_df.columns


def test_sql_writer_success(sample_df):
    """Test the SQL writer success path (mocked)."""
    with patch("builtins.print") as mock_print:
        data_io.save_data(sample_df, "users_table", "sql", if_exists="append")

        args, _ = mock_print.call_args
        assert "Writing to SQL table 'users_table'" in args[0]


def test_get_reader_invalid_format():
    """Test that asking for an unknown format raises ValueError."""
    with pytest.raises(ValueError, match="No reader registered"):
        data_io.load_data("file.txt", "unknown_format")


def test_custom_extension_registration():
    """Test that a NEW format (e.g., JSON) can be registered dynamically."""

    @_IOFactory.register_reader("json")
    class JsonReader:
        def read(self, source, **kwargs):
            return pd.DataFrame({"source": [source]})

    @_IOFactory.register_writer("json")
    class JsonWriter:
        def write(self, df, target, **kwargs):
            pass

    df = data_io.load_data("fake.json", "json")
    assert df["source"][0] == "fake.json"
