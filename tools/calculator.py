"""
tools/calculator.py
-------------------
Reusable financial calculation utilities.
"""

from typing import Dict

import pandas as pd

from config import DEFAULT_BUDGET_PERCENTAGES


class FinancialCalculator:
    """
    Financial calculation helper methods.
    """

    # =====================================================
    # Income
    # =====================================================

    @staticmethod
    def total_income(df: pd.DataFrame) -> float:

        return round(

            df.loc[
                df["Type"] == "Income",
                "Amount"
            ].sum(),

            2

        )

    # =====================================================
    # Expense
    # =====================================================

    @staticmethod
    def total_expense(df: pd.DataFrame) -> float:

        return round(

            df.loc[
                df["Type"] == "Expense",
                "Amount"
            ].sum(),

            2

        )

    # =====================================================
    # Savings
    # =====================================================

    @staticmethod
    def total_savings(df: pd.DataFrame) -> float:

        return round(

            FinancialCalculator.total_income(df)

            -

            FinancialCalculator.total_expense(df),

            2

        )

    # =====================================================
    # Expense Summary
    # =====================================================

    @staticmethod
    def expense_summary(df: pd.DataFrame) -> Dict[str, float]:

        expense_df = df[df["Type"] == "Expense"]

        summary = (

            expense_df

            .groupby("Category")["Amount"]

            .sum()

            .sort_values(ascending=False)

        )

        return summary.to_dict()

    # =====================================================
    # Highest Expense Category
    # =====================================================

    @staticmethod
    def highest_expense_category(df: pd.DataFrame):

        summary = FinancialCalculator.expense_summary(df)

        if not summary:

            return None

        return max(summary, key=summary.get)

    # =====================================================
    # Monthly Expenses
    # =====================================================

    @staticmethod
    def monthly_expenses(df: pd.DataFrame) -> pd.DataFrame:

        expense_df = df[df["Type"] == "Expense"].copy()

        expense_df["Month"] = (

            expense_df["Date"]

            .dt.to_period("M")

            .astype(str)

        )

        monthly = (

            expense_df

            .groupby("Month")["Amount"]

            .sum()

            .reset_index()

        )

        return monthly

    # =====================================================
    # Budget Allocation
    # =====================================================

    @staticmethod
    def create_budget(income: float):

        budget = {}

        for category, percentage in DEFAULT_BUDGET_PERCENTAGES.items():

            budget[category] = round(

                income * percentage / 100,

                2

            )

        return budget

    # =====================================================
    # Budget Analysis
    # =====================================================

    @staticmethod
    def analyze_budget(

        budget,

        expense_summary

    ):

        result = {}

        for category, allocated in budget.items():

            actual = expense_summary.get(category, 0)

            result[category] = {

                "allocated_budget": allocated,

                "actual_spending": actual,

                "remaining_budget": round(

                    allocated - actual,

                    2

                )

            }

        return result

    # =====================================================
    # Budget Summary
    # =====================================================

    @staticmethod
    def budget_summary(

        budget_analysis

    ):

        total_budget = 0

        total_spent = 0

        remaining = 0

        for values in budget_analysis.values():

            total_budget += values["allocated_budget"]

            total_spent += values["actual_spending"]

            remaining += values["remaining_budget"]

        return {

            "total_budget": round(total_budget, 2),

            "total_spent": round(total_spent, 2),

            "remaining_budget": round(remaining, 2)

        }

    # =====================================================
    # Savings Rate
    # =====================================================

    @staticmethod
    def savings_rate(

        income,

        savings

    ):

        if income == 0:

            return 0

        return round(

            (savings / income) * 100,

            2

        )

    # =====================================================
    # Expense Ratio
    # =====================================================

    @staticmethod
    def expense_ratio(

        income,

        expense

    ):

        if income == 0:

            return 0

        return round(

            (expense / income) * 100,

            2

        )

    # =====================================================
    # Financial Health Score
    # =====================================================

    @staticmethod
    def financial_health_score(

        income,

        expense

    ):

        if income == 0:

            return 0

        ratio = expense / income

        if ratio <= 0.50:

            return 100

        elif ratio <= 0.70:

            return 85

        elif ratio <= 0.85:

            return 70

        elif ratio <= 1.00:

            return 50

        return 20