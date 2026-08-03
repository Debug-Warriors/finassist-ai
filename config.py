"""
config.py
---------
Central configuration for FinAssist AI.

This module:
- Loads environment variables
- Initializes the Llama model via Ollama
- Stores application constants
"""

import os
from dotenv import load_dotenv
from langchain_ollama import ChatOllama

# Load environment variables
load_dotenv()

# ==========================================================
# Application Information
# ==========================================================

APP_NAME = "FinAssist AI"

APP_VERSION = "2.0.0"

# ==========================================================
# LLM Configuration
# ==========================================================

LLM_MODEL = os.getenv("LLM_MODEL", "llama3.2")

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

TEMPERATURE = float(
    os.getenv("TEMPERATURE", "0.2")
)

# ==========================================================
# Initialize LLM
# ==========================================================

llm = ChatOllama(
    model=LLM_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=TEMPERATURE,
)

# ==========================================================
# Dataset Configuration
# ==========================================================

SUPPORTED_FILE_TYPES = [
    "csv",
    "xlsx",
]

REQUIRED_COLUMNS = [
    "Date",
    "Description",
    "Category",
    "Type",
    "Amount",
    "Payment_Method",
]

EXPENSE_CATEGORIES = [
    "Housing",
    "Food",
    "Transportation",
    "Utilities",
    "Shopping",
    "Entertainment",
    "Healthcare",
    "Education",
    "Miscellaneous",
]

# Default budget allocation (%)
DEFAULT_BUDGET_PERCENTAGES = {
    "Food": 15,
    "Transportation": 10,
    "Utilities": 10,
    "Shopping": 10,
    "Entertainment": 5,
    "Healthcare": 10,
    "Education": 10,
    "Miscellaneous": 10,
    "Savings": 20,
}

# ==========================================================
# Forecast Configuration
# ==========================================================

MIN_MONTHS_FOR_FORECAST = 3

HIGH_RISK_THRESHOLD = 1.0      # Predicted expense > 100% income
MEDIUM_RISK_THRESHOLD = 0.80   # Predicted expense > 80% income