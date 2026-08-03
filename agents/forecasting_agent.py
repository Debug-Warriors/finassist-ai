"""
agents/forecasting_agent.py
---------------------------

Forecasting Agent

Responsibilities
----------------
- Predict next month's expenses
- Detect spending trend
- Estimate financial risk
- Explain forecast using Llama
"""

import numpy as np
from sklearn.linear_model import LinearRegression

from config import (
    llm,
    MIN_MONTHS_FOR_FORECAST,
    HIGH_RISK_THRESHOLD,
    MEDIUM_RISK_THRESHOLD,
)

from memory.state import FinancialState
from tools.calculator import FinancialCalculator


def forecasting_agent_node(state: FinancialState) -> FinancialState:
    """
    Forecasting Agent
    """

    # Skip this agent if Supervisor didn't select it
    if "forecasting_agent" not in state["execution_plan"]:
        return state

    df = state["dataframe"]

    monthly_df = FinancialCalculator.monthly_expenses(df)

    # ======================================================
    # Check if enough historical data exists
    # ======================================================

    if len(monthly_df) < MIN_MONTHS_FOR_FORECAST:

        state["expense_forecast"] = {
            "predicted_expense": state["total_expense"],
            "trend": "Unknown",
            "risk": "Unknown"
        }

        state["forecast_analysis"] = (
            "Not enough historical data to generate a reliable forecast."
        )

        return state

    # ======================================================
    # Prepare ML Dataset
    # ======================================================

    X = np.arange(len(monthly_df)).reshape(-1, 1)

    y = monthly_df["Amount"].values

    # ======================================================
    # Train Model
    # ======================================================

    model = LinearRegression()

    model.fit(X, y)

    # ======================================================
    # Predict Next Month
    # ======================================================

    next_month = np.array([[len(monthly_df)]])

    predicted = float(model.predict(next_month)[0])

    predicted = round(predicted, 2)

    # ======================================================
    # Trend Detection
    # ======================================================

    slope = float(model.coef_[0])

    if slope > 100:

        trend = "Increasing"

    elif slope < -100:

        trend = "Decreasing"

    else:

        trend = "Stable"

    # ======================================================
    # Budget Risk
    # ======================================================

    income = FinancialCalculator.total_income(df)

    if income == 0:

        risk = "Unknown"

    else:

        ratio = predicted / income

        if ratio >= HIGH_RISK_THRESHOLD:

            risk = "High"

        elif ratio >= MEDIUM_RISK_THRESHOLD:

            risk = "Medium"

        else:

            risk = "Low"

    # ======================================================
    # LLM Explanation
    # ======================================================

    prompt = f"""
You are a financial forecasting expert.

Monthly Expense History

{monthly_df.to_string(index=False)}

Predicted Next Month Expense

₹{predicted}

Trend

{trend}

Risk Level

{risk}

Explain:

1. Forecast summary

2. Spending trend

3. Financial risk

4. Recommendations

Maximum 180 words.
"""

    try:

        response = llm.invoke(prompt)

        analysis = response.content

    except Exception as e:

        analysis = (
            "Forecast generated successfully.\n"
            f"LLM unavailable: {str(e)}"
        )

    # ======================================================
    # Update State
    # ======================================================

    state["expense_forecast"] = {

        "predicted_expense": predicted,

        "trend": trend,

        "risk": risk

    }

    state["forecast_analysis"] = analysis

    return state