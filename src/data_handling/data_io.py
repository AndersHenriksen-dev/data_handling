"""Input/Output manager for DataFrame operations.

This module implements the Strategy pattern to handle reading and writing
DataFrames across different formats (SQL, CSV, etc.) using a unified API.
"""

import os
from typing import Any, ClassVar, Protocol

import pandas as pd


class _DataFrameReader(Protocol):
    """Protocol defining the interface for data readers."""

    def read(self, source: str, **kwargs: Any) -> pd.DataFrame:
        """Read data from a source into a DataFrame.

        Args:
            source: The connection string or file path.
            **kwargs: Format-specific arguments (e.g., sql query, separator).

        Returns:
            pd.DataFrame: The loaded data.

        """


class _DataFrameWriter(Protocol):
    """Protocol defining the interface for data writers."""

    def write(self, df: pd.DataFrame, target: str, **kwargs: Any) -> None:
        """Write a DataFrame to a target destination.

        Args:
            df: The DataFrame to write.
            target: The destination table name or file path.
            **kwargs: Format-specific arguments (e.g., if_exists, index).

        """


class _IOFactory:
    """Registry for Reader and Writer strategies.

    Uses a dictionary registry to map format strings (e.g., 'sql', 'csv')
    to their respective concrete classes.
    """

    _readers: ClassVar[dict[str, type[_DataFrameReader]]] = {}
    _writers: ClassVar[dict[str, type[_DataFrameWriter]]] = {}

    @classmethod
    def register_reader(cls, format_type: str):
        """Register a new reader strategy using a decorator."""

        def wrapper(wrapped_class: type[_DataFrameReader]) -> type[_DataFrameReader]:
            cls._readers[format_type] = wrapped_class
            return wrapped_class

        return wrapper

    @classmethod
    def register_writer(cls, format_type: str):
        """Register a new writer strategy using a decorator."""

        def wrapper(wrapped_class: type[_DataFrameWriter]) -> type[_DataFrameWriter]:
            cls._writers[format_type] = wrapped_class
            return wrapped_class

        return wrapper

    @classmethod
    def get_reader(cls, format_type: str) -> _DataFrameReader:
        """Retrieve a reader instance for the specific format."""
        try:
            return cls._readers[format_type]()
        except KeyError as e:
            raise ValueError(f"No reader registered for format: '{format_type}'") from e

    @classmethod
    def get_writer(cls, format_type: str) -> _DataFrameWriter:
        """Retrieve a writer instance for the specific format."""
        try:
            return cls._writers[format_type]()
        except KeyError as e:
            raise ValueError(f"No writer registered for format: '{format_type}'") from e


# --- Concrete Implementations ---


@_IOFactory.register_reader("sql")
class _SqlReader:
    """Reader strategy for SQL databases."""

    def read(self, source: str, **kwargs: Any) -> pd.DataFrame:
        """Read from a SQL database using a SQLAlchemy connection string."""
        query = kwargs.get("query")
        if not query:
            raise ValueError("SQL read requires a 'query' argument.")

        print(f"Reading from SQL DB at '{source}' with query: {query}")
        # Note: Requires 'sqlalchemy' and a database driver (e.g., psycopg2) installed.
        # return pd.read_sql(query, source, **kwargs)

        # specific mock for demonstration purposes
        return pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})


@_IOFactory.register_writer("sql")
class _SqlWriter:
    """Writer strategy for SQL databases."""

    def write(self, df: pd.DataFrame, target: str, **kwargs: Any) -> None:
        """Write to an SQL table."""
        if_exists = kwargs.get("if_exists", "fail")
        print(f"Writing to SQL table '{target}' (if_exists={if_exists})...")
        # Note: Requires 'sqlalchemy' and a database driver installed.
        # df.to_sql(target, con=kwargs.get('con'), if_exists=if_exists)


@_IOFactory.register_reader("csv")
class _CsvReader:
    """Reader strategy for CSV files."""

    def read(self, source: str, **kwargs: Any) -> pd.DataFrame:
        """Read a CSV file from the filesystem.

        Args:
            source: Path to the CSV file.
            **kwargs: Arguments passed directly to pd.read_csv (e.g., sep, encoding).

        """
        if not os.path.exists(source):
            raise FileNotFoundError(f"The file '{source}' does not exist.")

        try:
            print(f"Reading CSV from '{source}'...")
            return pd.read_csv(source, **kwargs)
        except Exception as e:
            raise OSError(f"Failed to read CSV from '{source}': {e}") from e


@_IOFactory.register_writer("csv")
class _CsvWriter:
    """Writer strategy for CSV files."""

    def write(self, df: pd.DataFrame, target: str, **kwargs: Any) -> None:
        """Write a DataFrame to a CSV file.

        Automatically creates parent directories if they don't exist.

        Args:
            df: The DataFrame to save.
            target: The file path to save to.
            **kwargs: Arguments passed directly to df.to_csv (e.g., index, sep).

        """
        directory = os.path.dirname(target)
        if directory and not os.path.exists(directory):
            print(f"Creating directory: {directory}")
            os.makedirs(directory, exist_ok=True)

        # Set default for index if not provided (usually False is preferred for exports)
        index = kwargs.pop("index", False)

        try:
            print(f"Writing CSV to '{target}'...")
            df.to_csv(target, index=index, **kwargs)
        except Exception as e:
            raise OSError(f"Failed to write CSV to '{target}': {e}") from e


def load_data(source: str, fmt: str, **kwargs: Any) -> pd.DataFrame:
    """Load data from a source in a given format.

    Args:
        source: The connection string or file path to read from.
        fmt: The format of the data (e.g., 'csv', 'sql').
        **kwargs: Format-specific arguments (e.g., sql query, separator).

    Returns:
        pd.DataFrame: The loaded data.

    """
    return _IOFactory.get_reader(fmt).read(source, **kwargs)


def save_data(df: pd.DataFrame, target: str, fmt: str, **kwargs: Any) -> None:
    """Save data to a target in a given format.

    Args:
        df: The DataFrame to save.
        target: The destination table name or file path.
        fmt: The format of the data (e.g., 'csv', 'sql').
        **kwargs: Format-specific arguments (e.g., if_exists, index).

    Returns:
        None

    """
    _IOFactory.get_writer(fmt).write(df, target, **kwargs)


if __name__ == "__main__":
    dummy_input_path = "input_data.csv"
    dummy_output_path = "output_folder/processed_data.csv"

    with open(dummy_input_path, "w", encoding="utf-8") as f:
        f.write("id,name,role\n101,Neo,The One\n102,Trinity,Hacker")

    try:
        print("--- Step 1: Reading ---")
        data = load_data(dummy_input_path, "csv")
        print(f"Data Loaded:\n{data}\n")

        print("--- Step 2: Writing ---")
        save_data(data, dummy_output_path, "csv")

        if os.path.exists(dummy_output_path):
            print(f"Success! File created at: {dummy_output_path}")

    finally:  # Clean up dummy files after demonstration
        if os.path.exists(dummy_input_path):
            os.remove(dummy_input_path)
