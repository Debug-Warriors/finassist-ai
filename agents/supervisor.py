"""
agents/supervisor.py
--------------------

Supervisor Agent

Responsibilities:
- Understand user intent
- Decide which agents should execute
- Generate execution plan
"""

import json

from config import llm
from memory.state import FinancialState


AVAILABLE_AGENTS = [
    "expense_tracker",
    "budget_planner",
    "financial_advisor",
    "forecasting_agent"
]


SYSTEM_PROMPT = """
You are the Supervisor Agent of FinAssist AI.

Your job is to understand the user's request and decide
which agents should execute.

Available agents:

1. expense_tracker
   - Analyze transactions
   - Income
   - Expenses
   - Savings
   - Spending summary

2. budget_planner
   - Monthly budget
   - Budget comparison

3. financial_advisor
   - Recommendations
   - Financial health
   - Saving suggestions

4. forecasting_agent
   - Predict future expenses
   - Spending trends

Return ONLY valid JSON.

Example:

{
    "execution_plan":[
        "expense_tracker",
        "budget_planner"
    ]
}
"""


def supervisor_node(state: FinancialState) -> FinancialState:
    """
    Decide which agents should execute.
    """

    query = state["query"]

    try:

        response = llm.invoke(

            [

                ("system", SYSTEM_PROMPT),

                (

                    "human",

                    f"""
User Query:

{query}

Return ONLY JSON.
"""

                )

            ]

        )

        content = response.content.strip()

        # Remove markdown if Llama returns ```json
        content = content.replace("```json", "")
        content = content.replace("```", "").strip()

        result = json.loads(content)

        execution_plan = result.get(
            "execution_plan",
            []
        )

        execution_plan = [

            agent

            for agent in execution_plan

            if agent in AVAILABLE_AGENTS

        ]

        if not execution_plan:

            execution_plan = AVAILABLE_AGENTS.copy()

    except Exception:

        # Safe fallback
        execution_plan = AVAILABLE_AGENTS.copy()

    state["execution_plan"] = execution_plan

    return state