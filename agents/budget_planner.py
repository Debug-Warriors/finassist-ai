"""
agents/budget_planner.py
------------------------

Budget Planner Agent

Responsibilities
----------------
- Generate a recommended monthly budget
- Compare budget vs actual spending
- Generate budget analysis using Llama
"""

from config import llm
from memory.state import FinancialState
from tools.calculator import FinancialCalculator


def budget_planner_node(state: FinancialState) -> FinancialState:
    """
    Budget Planner Agent
    """

    # Skip this agent if Supervisor didn't select it
    if "budget_planner" not in state["execution_plan"]:
        return state

    df = state["dataframe"]

    income = FinancialCalculator.total_income(df)

    expense_summary = FinancialCalculator.expense_summary(df)

    # ====================================================
    # Create Budget
    # ====================================================

    budget = FinancialCalculator.create_budget(
        income
    )

    # ====================================================
    # Compare Budget vs Actual
    # ====================================================

    budget_analysis = FinancialCalculator.analyze_budget(
        budget,
        expense_summary
    )

    budget_summary = FinancialCalculator.budget_summary(
        budget_analysis
    )

    # ====================================================
    # LLM Budget Analysis
    # ====================================================

    prompt = f"""
You are an expert financial planner.

A customer has the following budget.

Monthly Income:
₹{income}

Budget Allocation:

{budget}

Actual Spending:

{expense_summary}

Budget Comparison:

{budget_analysis}

Generate a professional budget review.

Include:

1. Overall budget health

2. Categories exceeding budget

3. Categories under budget

4. Suggestions to improve budgeting

Limit your response to 180 words.
"""

    try:

        response = llm.invoke(prompt)

        analysis = response.content

    except Exception as e:

        analysis = (
            "Budget analysis generated successfully.\n"
            f"LLM unavailable: {str(e)}"
        )

    # ====================================================
    # Update State
    # ====================================================

    state["budget_plan"] = budget_analysis

    state["budget_summary"] = budget_summary

    state["budget_analysis"] = analysis

    return state