"""
agents/expense_tracker.py
-------------------------

Expense Tracker Agent

Responsibilities:
- Analyze uploaded transactions
- Calculate income
- Calculate expenses
- Calculate savings
- Generate category-wise summary
- Identify highest expense category
- Generate AI-powered expense analysis
"""

from config import llm
from memory.state import FinancialState
from tools.calculator import FinancialCalculator


def expense_tracker_node(state: FinancialState) -> FinancialState:
    """
    Expense Tracker Agent
    """

    # Skip this agent if Supervisor didn't select it
    if "expense_tracker" not in state["execution_plan"]:
        return state

    df = state["dataframe"]

    # =====================================================
    # Financial Calculations
    # =====================================================

    total_income = FinancialCalculator.total_income(df)

    total_expense = FinancialCalculator.total_expense(df)

    total_savings = FinancialCalculator.total_savings(df)

    expense_summary = FinancialCalculator.expense_summary(df)

    highest_category = FinancialCalculator.highest_expense_category(df)

    # =====================================================
    # LLM Analysis
    # =====================================================

    prompt = f"""
You are a professional financial analyst.

Analyze the following financial data.

Income:
₹{total_income}

Expense:
₹{total_expense}

Savings:
₹{total_savings}

Category-wise Expenses:

{expense_summary}

Highest Expense Category:

{highest_category}

Generate a concise financial analysis.

Include:

1. Overall spending behaviour

2. Highest spending category

3. Positive observations

4. Areas needing improvement

Maximum 150 words.
"""

    try:

        response = llm.invoke(prompt)

        analysis = response.content

    except Exception as e:

        analysis = (
            f"Expense analysis generated successfully.\n"
            f"LLM unavailable: {str(e)}"
        )

    # =====================================================
    # Update Shared State
    # =====================================================

    state["total_income"] = total_income

    state["total_expense"] = total_expense

    state["total_savings"] = total_savings

    state["expense_summary"] = expense_summary

    state["highest_expense_category"] = highest_category

    state["expense_analysis"] = analysis

    return state