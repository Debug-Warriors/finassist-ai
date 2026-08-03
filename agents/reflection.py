"""
agents/reflection.py
--------------------

Reflection Agent

Responsibilities
----------------
- Review outputs from all agents
- Validate recommendations
- Generate the final financial report
"""

from config import llm
from memory.state import FinancialState


def reflection_node(state: FinancialState) -> FinancialState:
    """
    Reflection Agent
    """

    prompt = f"""
You are the final reviewer of FinAssist AI.

Your responsibility is to combine all agent outputs into one
professional financial report.

======================================================
USER QUERY
======================================================

{state["query"]}

======================================================
EXPENSE ANALYSIS
======================================================

Income:
₹{state["total_income"]}

Expense:
₹{state["total_expense"]}

Savings:
₹{state["total_savings"]}

Highest Expense Category:
{state["highest_expense_category"]}

Expense Summary:

{state["expense_summary"]}

Expense Analysis:

{state["expense_analysis"]}

======================================================
BUDGET ANALYSIS
======================================================

{state["budget_analysis"]}

Budget Summary:

{state["budget_summary"]}

======================================================
FINANCIAL ADVISOR
======================================================

Financial Health:

{state["financial_health"]}

Financial Health Score:

{state["financial_health_score"]}/100

Recommendations:

{state["recommendations"]}

======================================================
FORECAST
======================================================

Forecast:

{state["expense_forecast"]}

Forecast Analysis:

{state["forecast_analysis"]}

======================================================

Generate a professional report.

The report must contain:

# Executive Summary

# Spending Analysis

# Budget Review

# Financial Health

# Forecast

# Recommendations

# Final Conclusion

Use Markdown formatting.

Maximum 450 words.
"""

    try:

        response = llm.invoke(prompt)

        final_report = response.content

    except Exception as e:

        final_report = f"""
# Executive Summary

Income : ₹{state['total_income']}

Expense : ₹{state['total_expense']}

Savings : ₹{state['total_savings']}

Financial Health : {state['financial_health']}

Forecast :

{state['expense_forecast']}

Recommendations

{chr(10).join(state['recommendations'])}

Reflection could not be generated.

Reason:

{str(e)}
"""

    # ======================================================
    # Save Results
    # ======================================================

    state["reflection"] = (
        "Reflection completed successfully."
    )

    state["final_response"] = final_report

    return state