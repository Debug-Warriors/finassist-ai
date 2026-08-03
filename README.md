# 💰 FinAssist AI

An Intelligent Multi-Agent Financial Assistant built using **LangGraph**, **LangChain**, **Streamlit**, and **Python**.

---

# Overview

FinAssist AI is an Agentic AI application that helps users manage their finances by analyzing transaction history, generating personalized budgets, forecasting future expenses, and providing financial recommendations.

Unlike traditional chatbots, FinAssist AI uses multiple specialized AI agents coordinated through LangGraph.

---

# Features

- Upload financial transaction history (CSV)
- Automatic expense analysis
- Personalized monthly budget generation
- Savings recommendations
- Future expense forecasting
- Financial visualizations
- Conversation memory
- Multi-Agent Architecture
- Reflection-based response validation

---

# Technology Stack

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Framework | LangChain |
| Workflow | LangGraph |
| Frontend | Streamlit |
| LLM | Gemini / OpenAI |
| Data Processing | Pandas |
| Machine Learning | Scikit-Learn |
| Visualization | Matplotlib |
| Validation | Pydantic |

---

# Project Structure

```
finassist-ai/

│
├── app.py
├── graph.py
├── supervisor.py
├── requirements.txt
├── README.md

├── agents/
│   ├── expense_tracker.py
│   ├── budget_planner.py
│   ├── financial_advisor.py
│   ├── forecasting_agent.py
│   └── reflection.py

├── memory/
│   ├── state.py
│   └── conversation_memory.py

├── prompts/

├── tools/
│   ├── calculator.py
│   ├── csv_reader.py
│   └── visualization.py

├── data/

├── tests/

└── utils/
```

---

# Multi-Agent Workflow

```
User

↓

Streamlit UI

↓

Supervisor Agent

↓

Expense Tracker

↓

Budget Planner

↓

Financial Advisor

↓

Forecasting Agent

↓

Reflection

↓

Final Response
```

---

# AI Agents

## Supervisor Agent

- Receives user query
- Coordinates workflow
- Routes tasks

---

## Expense Tracker

- Categorizes expenses
- Calculates income
- Calculates expenses
- Calculates savings

---

## Budget Planner

- Creates personalized budgets
- Calculates budget allocation
- Compares planned vs actual spending

---

## Financial Advisor

- Generates financial recommendations
- Suggests savings opportunities
- Identifies overspending

---

## Forecasting Agent

- Predicts future expenses
- Uses Linear Regression
- Identifies spending trends

---

## Reflection Node

- Validates outputs
- Checks consistency
- Generates final response

---

# Installation

Clone the repository

```bash
git clone <repository-url>
```

Move into the project

```bash
cd finassist-ai
```

Create virtual environment

```bash
python -m venv venv
```

Activate environment

Windows

```bash
venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application

```bash
streamlit run app.py
```

---

# Sample Dataset

Upload the provided sample transaction dataset.

Supported format:

- CSV

Required columns

- Date
- Description
- Category
- Type
- Amount
- Payment_Method

---

# Example Queries

- Analyze my spending.
- Create a monthly budget.
- Suggest savings recommendations.
- Forecast next month's expenses.
- Analyze my spending and create a budget.
- Which category has the highest expenses?
- How much can I save every month?

---

# Machine Learning

Forecasting uses **Linear Regression** to estimate future monthly expenses based on historical transaction data.

---

# Future Enhancements

- Bank API Integration
- Voice Assistant
- OCR Receipt Scanner
- Investment Recommendations
- Authentication
- ChromaDB Memory
- Multi-user Support
- Mobile Application

---

# Team Members

| Member | Responsibility |
|----------|----------------|
| Member 1 | Streamlit UI |
| Member 2 | Tools & Visualization |
| Member 3 | LangGraph & Agents |
| Member 4 | Testing & Documentation |

---

# Authors

Developed as part of the **FinAssist AI Multi-Agent Financial Assistant** Capstone Project.