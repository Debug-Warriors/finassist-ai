"""
app.py
-------
Streamlit Frontend for FinAssist AI Dashboard
"""

import streamlit as st
from graph import run_finassist
from tools.csv_reader import CSVReader
from tools.calculator import FinancialCalculator
from tools.visualization import FinancialVisualizer

# ==========================================================
# Page Configuration & Styling
# ==========================================================

st.set_page_config(
    page_title="FinAssist AI",
    page_icon="💰",
    layout="wide"
)

# Custom CSS for better card formatting
st.markdown("""
<style>
    .stMetric {
        background-color: rgba(151, 166, 195, 0.1);
        padding: 15px;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================================
# Sidebar UI
# ==========================================================

with st.sidebar:
    st.title("💰 FinAssist AI")
    st.caption("Enterprise Financial Intelligence")
    st.markdown("---")
    
    st.write("### 🛠️ Technology Stack")
    st.markdown("""
    - ✅ **LangGraph** (Multi-Agent Workflow)
    - ✅ **LangChain** (LLM Orchestration)
    - ✅ **Ollama / Llama 3.2** (Local Inference)
    - ✅ **Streamlit** (Interactive Dashboard)
    """)
    
    st.markdown("---")
    st.info("💡 **How to use:** Upload your financial dataset (CSV/XLSX), inspect the baseline stats, and run AI queries to generate comprehensive financial reports.")

# ==========================================================
# Header Section
# ==========================================================

st.title("💰 FinAssist AI")
st.caption("Enterprise Multi-Agent Personal Finance Assistant powered by LangGraph + Llama 3.2")
st.divider()

# ==========================================================
# Data Ingestion
# ==========================================================

uploaded_file = st.file_uploader(
    "📂 Upload Transaction Dataset",
    type=["csv", "xlsx"],
    help="Upload a CSV or Excel file containing your transaction records."
)

if uploaded_file is None:
    st.info("👋 Welcome! Please upload a CSV or Excel transaction file to begin.")
    st.stop()

# Load Dataset safely
try:
    df = CSVReader.load(uploaded_file)
except Exception as e:
    st.error(f"Error loading dataset: {str(e)}")
    st.stop()

# ==========================================================
# Data Overview & Baseline Metrics
# ==========================================================

st.subheader("📋 Dataset Preview")
st.dataframe(df, use_container_width=True, height=200)

info = CSVReader.info(df)

# Calculated Baseline Dataset Metrics
income = FinancialCalculator.total_income(df)
expense = FinancialCalculator.total_expense(df)
savings = FinancialCalculator.total_savings(df)

st.write("### 📊 Dataset Overview")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Rows Processed", f"{info['rows']:,}")
c2.metric("Income Records", f"{info['income_records']:,}")
c3.metric("Expense Records", f"{info['expense_records']:,}")
c4.metric("Date Range", f"{info['date_range'][0]} → {info['date_range'][1]}")

st.divider()

# ==========================================================
# Query Interface & AI Pipeline
# ==========================================================

st.subheader("🤖 Ask FinAssist AI")
query = st.text_area(
    "Enter your financial question or objectives:",
    placeholder="Example: Analyze my spending patterns, evaluate my risk profile, and recommend a monthly budget plan.",
    height=100
)

generate_report = st.button("🚀 Generate AI Financial Report", use_container_width=True, type="primary")

if generate_report:
    if not query.strip():
        st.warning("Please enter a query before generating the report.")
        st.stop()

    # Run LangGraph Execution State
    with st.spinner("🔄 FinAssist AI Multi-Agent System is analyzing your financial data..."):
        try:
            state = run_finassist(
                query=query,
                dataframe=df
            )
            st.success("✨ Financial Analysis Completed Successfully!")
        except Exception as e:
            st.error(f"An error occurred during analysis: {str(e)}")
            st.stop()

    st.divider()

    # ======================================================
    # KPI Overview Section
    # ======================================================
    
    st.header("📊 Financial Key Performance Indicators")
    health_score = state.get("financial_health_score", 0)
    
    # Dynamic health score color badge indicator
    if health_score >= 80:
        health_status = f"{health_score}/100 🟢"
    elif health_score >= 50:
        health_status = f"{health_score}/100 🟡"
    else:
        health_status = f"{health_score}/100 🔴"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("💵 Total Income", f"₹{income:,.2f}")
    col2.metric("💸 Total Expense", f"₹{expense:,.2f}")
    col3.metric("💰 Total Savings", f"₹{savings:,.2f}")
    col4.metric("❤️ Financial Health", health_status)

    st.divider()

    # ======================================================
    # AI Executive Summary & Full Report
    # ======================================================

    st.header("📄 AI Executive Summary & Report")

    with st.expander("🔍 View Complete AI Financial Report", expanded=True):
        st.markdown(state.get("final_response", "No report generated."))

    st.divider()

    # ======================================================
    # Visual Analytics Dashboard
    # ======================================================

    st.header("📈 Visual Analytics Dashboard")

    expense_summary = FinancialCalculator.expense_summary(df)
    monthly_df = FinancialCalculator.monthly_expenses(df)

    # Grid Row 1
    r1_col1, r1_col2 = st.columns(2)
    with r1_col1:
        st.subheader("🥧 Expense Distribution")
        st.pyplot(
            FinancialVisualizer.expense_pie(expense_summary),
            use_container_width=True
        )

    with r1_col2:
        st.subheader("📊 Category-wise Expenses")
        st.pyplot(
            FinancialVisualizer.expense_bar(expense_summary),
            use_container_width=True
        )

    # Grid Row 2
    r2_col1, r2_col2 = st.columns(2)
    with r2_col1:
        st.subheader("📈 Monthly Expense Trend")
        st.pyplot(
            FinancialVisualizer.monthly_trend(monthly_df),
            use_container_width=True
        )

    with r2_col2:
        st.subheader("⚖️ Income vs Expense")
        st.pyplot(
            FinancialVisualizer.income_vs_expense(
                income,
                expense
            ),
            use_container_width=True
        )

    # Grid Row 3
    r3_col1, r3_col2 = st.columns(2)
    with r3_col1:
        st.subheader("📋 Budget vs Actual")
        st.pyplot(
            FinancialVisualizer.budget_vs_actual(
                state.get("budget_plan", {})
            ),
            use_container_width=True
        )

    with r3_col2:
        st.subheader("🎯 Savings Progress")
        st.pyplot(
            FinancialVisualizer.savings_progress(
                income,
                savings
            ),
            use_container_width=True
        )

    st.divider()

    # ======================================================
    # Forecast Metrics
    # ======================================================

    st.header("🔮 Expense Forecast & Risk Assessment")

    forecast = state.get("expense_forecast", {})

    if forecast:
        fc1, fc2, fc3 = st.columns(3)

        fc1.metric(
            "Predicted Next Month Expense",
            f"₹{forecast.get('predicted_expense', 0):,.2f}"
        )

        trend_val = forecast.get("trend", "-")
        if trend_val.lower() == "increasing":
            trend_display = "📈 Increasing"
        elif trend_val.lower() == "decreasing":
            trend_display = "📉 Decreasing"
        else:
            trend_display = "➡ Stable"

        fc2.metric("Projected Trend", trend_display)

        risk_val = forecast.get("risk", "Low")
        risk_emoji_map = {
            "Low": "🟢 Low",
            "Medium": "🟡 Medium",
            "High": "🔴 High"
        }
        
        fc3.metric(
            "Financial Risk Level",
            risk_emoji_map.get(risk_val, f"⚪ {risk_val}")
        )

    st.divider()

    # ======================================================
    # Actionable Recommendations
    # ======================================================

    st.header("💡 Strategic AI Recommendations")

    recommendations = state.get("recommendations", [])
    if recommendations:
        for rec in recommendations:
            st.success(f"📌 {rec}")
    else:
        st.info("No specific recommendations generated for this scenario.")