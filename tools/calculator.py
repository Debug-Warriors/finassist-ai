import pandas as pd


def calculate_total_income(df: pd.DataFrame) -> float:
    """
    Calculate total income.
    """

    income = df[df["Type"] == "Income"]["Amount"].sum()

    return float(income)


def calculate_total_expenses(df: pd.DataFrame) -> float:
    """
    Calculate total expenses.
    """

    expenses = df[df["Type"] == "Expense"]["Amount"].sum()

    return float(expenses)


def calculate_savings(df: pd.DataFrame) -> float:
    """
    Savings = Income - Expenses
    """

    income = calculate_total_income(df)
    expenses = calculate_total_expenses(df)

    return income - expenses


def calculate_category_expenses(df: pd.DataFrame) -> pd.Series:
    """
    Calculate expense by category.
    """

    category_totals = (
        df[df["Type"] == "Expense"]
        .groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    return category_totals


def calculate_monthly_expenses(df: pd.DataFrame) -> pd.Series:
    """
    Monthly expense summary.
    """

    monthly = (
        df[df["Type"] == "Expense"]
        .groupby(df["Date"].dt.to_period("M"))["Amount"]
        .sum()
    )

    return monthly


def calculate_expense_percentages(df: pd.DataFrame) -> pd.Series:
    """
    Expense percentage by category.
    """

    category = calculate_category_expenses(df)

    total = category.sum()

    percentages = (category / total) * 100

    return percentages.round(2)