"""
memory/state.py
---------------

Shared state for the FinAssist AI LangGraph workflow.

Every node (Supervisor, Agents, Reflection) reads from and
updates this shared state.
"""

from typing import TypedDict, Dict, List, Optional
import pandas as pd


class FinancialState(TypedDict):
    """
    Shared state across the LangGraph workflow.
    """

    # =====================================================
    # USER INPUT
    # =====================================================

    query: str
    dataframe: pd.DataFrame

    # =====================================================
    # SUPERVISOR
    # =====================================================

    execution_plan: List[str]

    # =====================================================
    # EXPENSE TRACKER
    # =====================================================

    total_income: float
    total_expense: float
    total_savings: float

    expense_summary: Dict[str, float]

    highest_expense_category: Optional[str]

    expense_analysis: str

    # =====================================================
    # BUDGET PLANNER
    # =====================================================

    budget_plan: Dict[str, Dict]

    budget_summary: Dict[str, float]

    budget_analysis: str

    # =====================================================
    # FINANCIAL ADVISOR
    # =====================================================

    recommendations: List[str]

    financial_health: str

    financial_health_score: int

    # =====================================================
    # FORECASTING AGENT
    # =====================================================

    expense_forecast: Dict

    forecast_analysis: str

    # =====================================================
    # REFLECTION AGENT
    # =====================================================

    reflection: str

    final_response: str