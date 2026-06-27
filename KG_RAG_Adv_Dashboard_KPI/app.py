import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from groq import Groq


# -------------------------------------------------
# CONFIG
# -------------------------------------------------

# Load environment variables
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv(
    "GROQ_MODEL",
    "llama-3.1-8b-instant"
)

# -------------------------------------------------
# PAGE SETUP
# -------------------------------------------------

st.set_page_config(
    page_title="AI FP&A Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI FP&A Dashboard")
st.caption("Budget vs Actual | Variance Analysis | Cashflow | Headcount | AI Insights")


# -------------------------------------------------
# HELPER FUNCTIONS
# -------------------------------------------------

def format_currency(value):
    return f"₹{value:,.0f}"


def format_percent(value):
    return f"{value:.2f}%"


def load_data(file):
    financials = pd.read_excel(file, sheet_name="Financials")
    headcount = pd.read_excel(file, sheet_name="Headcount")
    cashflow = pd.read_excel(file, sheet_name="Cashflow")
    kpis = pd.read_excel(file, sheet_name="KPIs")

    return financials, headcount, cashflow, kpis


def ask_groq(prompt):
    client = Groq(api_key=GROQ_API_KEY)

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are an FP&A expert. Give concise CFO-style business analysis."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------

st.sidebar.header("⚙️ Filters")

uploaded_file = st.sidebar.file_uploader(
    "Upload FP&A Excel File",
    type=["xlsx"]
)


# -------------------------------------------------
# MAIN APP
# -------------------------------------------------

if uploaded_file:

    financials, headcount, cashflow, kpis = load_data(uploaded_file)

    financials["Gross_Profit"] = financials["Revenue_Actual"] - financials["COGS_Actual"]
    financials["Operating_Profit"] = financials["Gross_Profit"] - financials["OpEx_Actual"]
    financials["Revenue_Variance"] = financials["Revenue_Actual"] - financials["Revenue_Budget"]

    financials["Revenue_Variance_%"] = (
        financials["Revenue_Variance"] / financials["Revenue_Budget"]
    ) * 100

    month_filter = st.sidebar.multiselect(
        "Select Month",
        options=financials["Month"].unique(),
        default=financials["Month"].unique()
    )

    region_filter = st.sidebar.multiselect(
        "Select Region",
        options=financials["Region"].unique(),
        default=financials["Region"].unique()
    )

    product_filter = st.sidebar.multiselect(
        "Select Product",
        options=financials["Product"].unique(),
        default=financials["Product"].unique()
    )

    df = financials[
        (financials["Month"].isin(month_filter)) &
        (financials["Region"].isin(region_filter)) &
        (financials["Product"].isin(product_filter))
    ]

    # -------------------------------------------------
    # KPI CARDS
    # -------------------------------------------------

    total_revenue = df["Revenue_Actual"].sum()
    total_budget = df["Revenue_Budget"].sum()
    total_cogs = df["COGS_Actual"].sum()
    total_opex = df["OpEx_Actual"].sum()

    gross_profit = total_revenue - total_cogs
    operating_profit = gross_profit - total_opex

    gross_margin = (gross_profit / total_revenue) * 100 if total_revenue else 0
    budget_variance = total_revenue - total_budget
    budget_variance_pct = (budget_variance / total_budget) * 100 if total_budget else 0

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric("Revenue Actual", format_currency(total_revenue))
    c2.metric("Revenue Budget", format_currency(total_budget))
    c3.metric("Gross Profit", format_currency(gross_profit))
    c4.metric("Gross Margin", format_percent(gross_margin))
    c5.metric(
        "Budget Variance",
        format_currency(budget_variance),
        format_percent(budget_variance_pct)
    )

    st.divider()

    # -------------------------------------------------
    # CHARTS
    # -------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Revenue Trend")

        revenue_trend = df.groupby("Month", as_index=False)[
            ["Revenue_Actual", "Revenue_Budget"]
        ].sum()

        fig = px.line(
            revenue_trend,
            x="Month",
            y=["Revenue_Actual", "Revenue_Budget"],
            markers=True,
            title="Revenue Actual vs Budget"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Budget vs Actual by Product")

        product_data = df.groupby("Product", as_index=False)[
            ["Revenue_Actual", "Revenue_Budget"]
        ].sum()

        fig = px.bar(
            product_data,
            x="Product",
            y=["Revenue_Actual", "Revenue_Budget"],
            barmode="group",
            title="Product Performance"
        )

        st.plotly_chart(fig, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Region Performance")

        region_data = df.groupby("Region", as_index=False)["Revenue_Actual"].sum()

        fig = px.bar(
            region_data,
            x="Region",
            y="Revenue_Actual",
            title="Revenue by Region"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col4:
        st.subheader("Gross Margin by Product")

        margin_data = df.groupby("Product", as_index=False).agg(
            Revenue=("Revenue_Actual", "sum"),
            COGS=("COGS_Actual", "sum")
        )

        margin_data["Gross_Margin_%"] = (
            (margin_data["Revenue"] - margin_data["COGS"]) /
            margin_data["Revenue"]
        ) * 100

        fig = px.bar(
            margin_data,
            x="Product",
            y="Gross_Margin_%",
            title="Gross Margin % by Product"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # VARIANCE TABLE
    # -------------------------------------------------

    st.subheader("📌 Variance Analysis Table")

    variance_table = df[
        [
            "Month",
            "Region",
            "Product",
            "Revenue_Actual",
            "Revenue_Budget",
            "Revenue_Variance",
            "Revenue_Variance_%",
            "COGS_Actual",
            "OpEx_Actual",
            "Gross_Profit",
            "Operating_Profit"
        ]
    ]

    st.dataframe(variance_table, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # CASHFLOW + HEADCOUNT
    # -------------------------------------------------

    col5, col6 = st.columns(2)

    with col5:
        st.subheader("Cashflow Trend")

        fig = px.line(
            cashflow,
            x="Month",
            y=["Cash_Inflow", "Cash_Outflow", "Closing_Cash"],
            markers=True,
            title="Cashflow Movement"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col6:
        st.subheader("Headcount Actual vs Budget")

        fig = px.bar(
            headcount,
            x="Department",
            y=["Headcount_Actual", "Headcount_Budget"],
            barmode="group",
            title="Headcount by Department"
        )

        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # -------------------------------------------------
    # AI FP&A INSIGHTS
    # -------------------------------------------------

    st.subheader("🤖 AI FP&A Insights")

    summary_data = df.head(30).to_string(index=False)

    if st.button("Generate AI Insights"):

        if GROQ_API_KEY == "PASTE_YOUR_GROQ_API_KEY_HERE":
            st.error("Please paste your Groq API key inside app.py first.")
        else:
            prompt = f"""
Analyze this FP&A data and provide:

1. Executive Summary
2. Revenue vs Budget Analysis
3. Margin Analysis
4. Cost / OpEx Observations
5. Risks
6. Recommendations

Data:
{summary_data}
"""

            with st.spinner("Generating AI FP&A insights..."):
                ai_response = ask_groq(prompt)

            st.write(ai_response)

    st.divider()

    # -------------------------------------------------
    # ASK FP&A AI
    # -------------------------------------------------

    st.subheader("💬 Ask FP&A AI")

    user_question = st.text_area(
        "Ask a finance question",
        placeholder="Example: Why is revenue variance negative? Which product has the best margin?"
    )

    if st.button("Ask AI"):

        if not user_question.strip():
            st.warning("Please enter a question.")

        elif GROQ_API_KEY == "PASTE_YOUR_GROQ_API_KEY_HERE":
            st.error("Please paste your Groq API key inside app.py first.")

        else:
            prompt = f"""
Question:
{user_question}

Use this FP&A data:
{summary_data}

Answer like an FP&A analyst.
Give practical business explanation.
"""

            with st.spinner("AI is analyzing..."):
                ai_answer = ask_groq(prompt)

            st.write(ai_answer)

else:
    st.info("Upload your FP&A Excel file to begin.")