"""
tools/visualization.py
----------------------

Visualization utilities for FinAssist AI.
"""

import matplotlib.pyplot as plt
import pandas as pd


class FinancialVisualizer:

    # =====================================================
    # Common Figure Size
    # =====================================================

    FIGSIZE = (8, 5)

    # =====================================================
    # Expense Distribution
    # =====================================================

    @staticmethod
    def expense_pie(expense_summary: dict):

        fig, ax = plt.subplots(figsize=FinancialVisualizer.FIGSIZE)

        if not expense_summary:
            ax.text(
                0.5,
                0.5,
                "No Expense Data",
                ha="center",
                va="center",
                fontsize=14,
            )
            ax.axis("off")
            return fig

        ax.pie(
            expense_summary.values(),
            labels=expense_summary.keys(),
            autopct="%1.1f%%",
            startangle=90,
        )

        ax.set_title("Expense Distribution")

        plt.tight_layout()

        return fig

    # =====================================================
    # Expense Bar Chart
    # =====================================================

    @staticmethod
    def expense_bar(expense_summary: dict):

        fig, ax = plt.subplots(figsize=FinancialVisualizer.FIGSIZE)

        if not expense_summary:
            ax.text(
                0.5,
                0.5,
                "No Expense Data",
                ha="center",
                va="center",
                fontsize=14,
            )
            ax.axis("off")
            return fig

        categories = list(expense_summary.keys())
        amounts = list(expense_summary.values())

        ax.bar(categories, amounts)

        ax.set_title("Category-wise Expenses")

        ax.set_xlabel("Category")

        ax.set_ylabel("Amount (₹)")

        plt.xticks(rotation=30)

        plt.tight_layout()

        return fig

    # =====================================================
    # Monthly Trend
    # =====================================================

    @staticmethod
    def monthly_trend(monthly_df: pd.DataFrame):

        fig, ax = plt.subplots(figsize=FinancialVisualizer.FIGSIZE)

        if monthly_df.empty:
            ax.text(
                0.5,
                0.5,
                "No Monthly Data",
                ha="center",
                va="center",
                fontsize=14,
            )
            ax.axis("off")
            return fig

        ax.plot(
            monthly_df["Month"],
            monthly_df["Amount"],
            marker="o",
            linewidth=2,
        )

        ax.set_title("Monthly Expense Trend")

        ax.set_xlabel("Month")

        ax.set_ylabel("Expense (₹)")

        ax.grid(True)

        plt.xticks(rotation=30)

        plt.tight_layout()

        return fig

    # =====================================================
    # Income vs Expense
    # =====================================================

    @staticmethod
    def income_vs_expense(
        income,
        expense,
    ):

        fig, ax = plt.subplots(figsize=FinancialVisualizer.FIGSIZE)

        labels = ["Income", "Expense"]

        values = [income, expense]

        ax.bar(labels, values)

        ax.set_title("Income vs Expense")

        ax.set_ylabel("Amount (₹)")

        plt.tight_layout()

        return fig

    # =====================================================
    # Budget vs Actual
    # =====================================================

    @staticmethod
    def budget_vs_actual(budget_analysis):

        fig, ax = plt.subplots(figsize=FinancialVisualizer.FIGSIZE)

        if not budget_analysis:
            ax.text(
                0.5,
                0.5,
                "No Budget Data",
                ha="center",
                va="center",
                fontsize=14,
            )
            ax.axis("off")
            return fig

        categories = []

        allocated = []

        actual = []

        for category, values in budget_analysis.items():

            if category == "Savings":
                continue

            categories.append(category)

            allocated.append(values["allocated_budget"])

            actual.append(values["actual_spending"])

        x = range(len(categories))

        width = 0.35

        ax.bar(
            [i - width / 2 for i in x],
            allocated,
            width,
            label="Budget",
        )

        ax.bar(
            [i + width / 2 for i in x],
            actual,
            width,
            label="Actual",
        )

        ax.set_xticks(list(x))

        ax.set_xticklabels(
            categories,
            rotation=30,
        )

        ax.set_ylabel("Amount (₹)")

        ax.set_title("Budget vs Actual Spending")

        ax.legend()

        plt.tight_layout()

        return fig

    # =====================================================
    # Savings Progress
    # =====================================================

    @staticmethod
    def savings_progress(
        income,
        savings,
    ):

        fig, ax = plt.subplots(figsize=FinancialVisualizer.FIGSIZE)

        if income <= 0:
            percentage = 0
        else:
            percentage = (savings / income) * 100

        percentage = max(0, min(percentage, 100))

        ax.barh(
            ["Savings"],
            [100],
            alpha=0.3,
            label="Target",
        )

        ax.barh(
            ["Savings"],
            [percentage],
            label="Current",
        )

        ax.set_xlim(0, 100)

        ax.set_xlabel("Savings Rate (%)")

        ax.set_title(f"Savings Progress ({percentage:.1f}%)")

        ax.legend()

        plt.tight_layout()

        return fig