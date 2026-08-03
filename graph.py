"""
graph.py
---------

LangGraph workflow for FinAssist AI.
"""

from langgraph.graph import StateGraph, START, END

from memory.state import FinancialState

from agents.supervisor import supervisor_node
from agents.expense_tracker import expense_tracker_node
from agents.budget_planner import budget_planner_node
from agents.financial_advisor import financial_advisor_node
from agents.forecasting_agent import forecasting_agent_node
from agents.reflection import reflection_node


# ==========================================================
# Build Graph
# ==========================================================

workflow = StateGraph(FinancialState)

# ----------------------------------------------------------
# Register Nodes
# ----------------------------------------------------------

workflow.add_node("supervisor", supervisor_node)

workflow.add_node(
    "expense_tracker",
    expense_tracker_node
)

workflow.add_node(
    "budget_planner",
    budget_planner_node
)

workflow.add_node(
    "financial_advisor",
    financial_advisor_node
)

workflow.add_node(
    "forecasting_agent",
    forecasting_agent_node
)

workflow.add_node(
    "reflection",
    reflection_node
)

# ----------------------------------------------------------
# Graph Flow
# ----------------------------------------------------------

workflow.add_edge(
    START,
    "supervisor"
)

workflow.add_edge(
    "supervisor",
    "expense_tracker"
)

workflow.add_edge(
    "expense_tracker",
    "budget_planner"
)

workflow.add_edge(
    "budget_planner",
    "financial_advisor"
)

workflow.add_edge(
    "financial_advisor",
    "forecasting_agent"
)

workflow.add_edge(
    "forecasting_agent",
    "reflection"
)

workflow.add_edge(
    "reflection",
    END
)

# ----------------------------------------------------------
# Compile Graph
# ----------------------------------------------------------

graph = workflow.compile()


# ==========================================================
# Run Graph
# ==========================================================

def run_finassist(query, dataframe):
    """
    Execute the FinAssist AI workflow.
    """

    initial_state = {

        # ==================================================
        # User Input
        # ==================================================

        "query": query,

        "dataframe": dataframe,

        # ==================================================
        # Supervisor
        # ==================================================

        "execution_plan": [],

        # ==================================================
        # Expense Tracker
        # ==================================================

        "total_income": 0.0,

        "total_expense": 0.0,

        "total_savings": 0.0,

        "expense_summary": {},

        "highest_expense_category": None,

        "expense_analysis": "",

        # ==================================================
        # Budget Planner
        # ==================================================

        "budget_plan": {},

        "budget_summary": {},

        "budget_analysis": "",

        # ==================================================
        # Financial Advisor
        # ==================================================

        "recommendations": [],

        "financial_health": "",

        "financial_health_score": 0,

        # ==================================================
        # Forecast
        # ==================================================

        "expense_forecast": {},

        "forecast_analysis": "",

        # ==================================================
        # Reflection
        # ==================================================

        "reflection": "",

        "final_response": ""

    }

    result = graph.invoke(initial_state)

    return result