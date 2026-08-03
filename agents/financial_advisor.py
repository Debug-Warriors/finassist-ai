"""
agents/financial_advisor.py
---------------------------

Financial Advisor Agent

Responsibilities
----------------
- Evaluate financial health
- Calculate financial health score
- Generate personalized recommendations
- Suggest savings opportunities
"""

from config import llm
from memory.state import FinancialState
from tools.calculator import FinancialCalculator

def financial_advisor_node(state: FinancialState) -> FinancialState:
    """
    Financial Advisor Agent
    """

    # Skip this agent if Supervisor didn't select it
    if "financial_advisor" not in state["execution_plan"]:
        return state

    df = state["dataframe"]

    income = FinancialCalculator.total_income(df)

    expense = FinancialCalculator.total_expense(df)

    savings = FinancialCalculator.total_savings(df)

    expense_summary = FinancialCalculator.expense_summary(df)

    highest_category = FinancialCalculator.highest_expense_category(df)

    budget = FinancialCalculator.create_budget(income)

    budget_analysis = FinancialCalculator.analyze_budget(
        budget,
        expense_summary
    )

    budget_summary = FinancialCalculator.budget_summary(
        budget_analysis
    )

    # =========================================================
    # Financial Metrics
    # =========================================================

    health_score = FinancialCalculator.financial_health_score(
        income,
        expense
    )

    savings_rate = FinancialCalculator.savings_rate(
        income,
        savings
    )

    expense_ratio = FinancialCalculator.expense_ratio(
        income,
        expense
    )

    # =========================================================
    # Financial Health Status
    # =========================================================

    if health_score >= 90:
        health = "Excellent"

    elif health_score >= 75:
        health = "Good"

    elif health_score >= 60:
        health = "Fair"

    else:
        health = "Needs Improvement"

    # =========================================================
    # Prompt
    # =========================================================

    prompt = f"""
You are an experienced financial advisor.

Customer Financial Profile

Monthly Income:
₹{income}

Monthly Expense:
₹{expense}

Monthly Savings:
₹{savings}

Savings Rate:
{savings_rate:.2f}%

Expense Ratio:
{expense_ratio:.2f}%

Financial Health Score:
{health_score}/100

Highest Expense Category:
{highest_category}

Expense Summary:

{expense_summary}

Budget Summary:

{budget_summary}

Generate:

1. Overall financial health

2. Top strengths

3. Top weaknesses

4. Savings recommendations

5. Spending improvements

6. Long-term financial advice

Return your response as bullet points.

Maximum 250 words.
"""

    try:

        response = llm.invoke(prompt)

        advice = response.content

    except Exception as e:

        advice = (
            "Unable to generate AI recommendations.\n"
            f"Reason: {str(e)}"
        )

    # =========================================================
    # Convert Response to List
    # =========================================================

    recommendations = []

    for line in advice.split("\n"):

        line = line.strip()

        if not line:
            continue

        line = line.lstrip("-•* ")

        if line:
            recommendations.append(line)

    if not recommendations:

        recommendations = [
            "Continue monitoring your monthly expenses."
        ]

    # =========================================================
    # Update State
    # =========================================================

    state["financial_health"] = health

    state["financial_health_score"] = health_score

    state["recommendations"] = recommendations

    return state