"""
tools/csv_reader.py
-------------------

Loads and validates transaction datasets.

Supported:
- CSV
- Excel (.xlsx)
"""

from pathlib import Path
from typing import Union

import pandas as pd

from config import REQUIRED_COLUMNS


from pathlib import Path
from typing import Union
import pandas as pd


class CSVReader:

    @staticmethod
    def load(file: Union[str, Path, object]) -> pd.DataFrame:
        """
        Load CSV or Excel file.

        Supports:
        - File path
        - Streamlit UploadedFile
        """

        # Streamlit UploadedFile
        if hasattr(file, "name"):
            filename = file.name.lower()
        else:
            filename = str(file).lower()

        if filename.endswith(".csv"):
            df = pd.read_csv(file)

        elif filename.endswith(".xlsx"):
            df = pd.read_excel(file)

        else:
            raise ValueError(
                "Unsupported file format. Use CSV or XLSX."
            )

        return CSVReader.validate(df)

    @staticmethod
    def validate(df: pd.DataFrame) -> pd.DataFrame:
        """
        Validate dataset.
        """

        # -----------------------------------
        # Required Columns
        # -----------------------------------

        missing_columns = [
            column
            for column in REQUIRED_COLUMNS
            if column not in df.columns
        ]

        if missing_columns:

            raise ValueError(
                f"Missing columns: {missing_columns}"
            )

        # -----------------------------------
        # Convert Date
        # -----------------------------------

        df["Date"] = pd.to_datetime(
            df["Date"],
            errors="coerce"
        )

        # -----------------------------------
        # Convert Amount
        # -----------------------------------

        df["Amount"] = pd.to_numeric(
            df["Amount"],
            errors="coerce"
        )

        # -----------------------------------
        # Remove Invalid Rows
        # -----------------------------------

        df.dropna(
            subset=[
                "Date",
                "Amount"
            ],
            inplace=True
        )

        # -----------------------------------
        # Remove Duplicate Rows
        # -----------------------------------

        df.drop_duplicates(
            inplace=True
        )

        # -----------------------------------
        # Clean Text Columns
        # -----------------------------------

        text_columns = [

            "Description",

            "Category",

            "Type",

            "Payment_Method"

        ]

        for column in text_columns:

            df[column] = (

                df[column]

                .astype(str)

                .str.strip()

                .str.title()

            )

        # -----------------------------------
        # Validate Transaction Type
        # -----------------------------------

        valid_types = {

            "Income",

            "Expense"

        }

        invalid = df[
            ~df["Type"].isin(valid_types)
        ]

        if not invalid.empty:

            raise ValueError(
                "Type column must contain only Income or Expense."
            )

        # -----------------------------------
        # Sort by Date
        # -----------------------------------

        df.sort_values(
            by="Date",
            inplace=True
        )

        df.reset_index(
            drop=True,
            inplace=True
        )

        return df

    @staticmethod
    def preview(
        df: pd.DataFrame,
        rows: int = 5
    ) -> pd.DataFrame:
        """
        Return preview rows.
        """

        return df.head(rows)

    @staticmethod
    def info(df: pd.DataFrame) -> dict:
        """
        Dataset summary.
        """

        return {

            "rows": len(df),

            "columns": len(df.columns),

            "income_records": len(
                df[df["Type"] == "Income"]
            ),

            "expense_records": len(
                df[df["Type"] == "Expense"]
            ),

            "date_range": (

                str(df["Date"].min().date()),

                str(df["Date"].max().date())

            )
        }