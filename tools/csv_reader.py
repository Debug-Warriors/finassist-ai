import pandas as pd


REQUIRED_COLUMNS = [
    "Date",
    "Description",
    "Category",
    "Type",
    "Amount"
]


def load_transactions(file_path: str) -> pd.DataFrame:
    """
    Load transaction data from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded transaction data.
    """

    try:
        df = pd.read_csv(file_path)

        validate_transactions(df)

        df = clean_transactions(df)

        return df

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    except Exception as e:
        raise Exception(f"Error reading CSV: {e}")


def validate_transactions(df: pd.DataFrame):
    """
    Validate required columns.
    """

    missing_columns = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean transaction data.
    """

    df = df.copy()

    # Remove empty rows
    df.dropna(how="all", inplace=True)

    # Remove leading/trailing spaces
    df.columns = df.columns.str.strip()

    df["Description"] = df["Description"].astype(str).str.strip()
    df["Category"] = df["Category"].astype(str).str.strip()
    df["Type"] = df["Type"].astype(str).str.strip()

    # Convert Date
    df["Date"] = pd.to_datetime(df["Date"])

    # Convert Amount
    df["Amount"] = pd.to_numeric(df["Amount"])

    return df