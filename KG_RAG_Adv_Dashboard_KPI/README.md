# 📊 AI FP&A Dashboard

An AI-powered Financial Planning & Analysis (FP&A) Dashboard built using **Streamlit, Pandas, Plotly, and Groq LLM**.

The application enables finance professionals to perform:

* Budget vs Actual analysis
* Revenue and Margin analysis
* Variance analysis
* Cashflow analysis
* Headcount analysis
* AI-generated financial insights
* Interactive financial Q&A

---

# 🚀 Features

## 📈 Dashboard Analytics

* Revenue Trend Analysis
* Budget vs Actual Comparison
* Product Performance Analysis
* Region-wise Revenue Analysis
* Gross Margin Analysis
* Variance Analysis Table
* Cashflow Trend Analysis
* Headcount Actual vs Budget

## 🤖 AI-Powered Insights

Using Groq LLM, the application can automatically generate:

* Executive summaries
* Revenue vs Budget explanations
* Margin analysis
* Cost observations
* Financial risks
* Business recommendations

## 💬 Ask FP&A AI

Users can ask questions such as:

* Why is revenue variance negative?
* Which product has the best margin?
* Which region exceeded budget?
* What are the major business risks?
* Summarize overall financial performance.

---

# 🏗️ Project Structure

```text
AI_FPNA_Dashboard/
│
├── app.py
├── requirements.txt
├── README.md
├── .env
├── .gitignore
│
└── data/
    └── fpna_dataset.xlsx
```

---

# ⚙️ Technologies Used

| Technology    | Purpose                         |
| ------------- | ------------------------------- |
| Python        | Core programming                |
| Streamlit     | Web application                 |
| Pandas        | Data processing                 |
| Plotly        | Interactive charts              |
| Groq API      | AI insights generation          |
| python-dotenv | Environment variable management |
| OpenPyXL      | Excel processing                |

---

# 📦 Installation

Clone the repository:

```bash
git clone <your_repository_url>
cd AI_FPNA_Dashboard
```

Create virtual environment:

```bash
python -m venv venv
```

Activate virtual environment:

## Windows

```bash
venv\Scripts\activate
```

## Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file in the project root.

Example:

```text
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.1-8b-instant
```

---

# 📄 Input Excel Format

The uploaded workbook should contain the following sheets:

## Sheet 1: Financials

Required columns:

```text
Month
Year
Region
Product
Revenue_Actual
Revenue_Budget
COGS_Actual
COGS_Budget
OpEx_Actual
OpEx_Budget
Units_Sold
Forecast_Revenue
```

## Sheet 2: Headcount

Required columns:

```text
Month
Department
Headcount_Actual
Headcount_Budget
Attrition_Rate
Hiring_Budget
```

## Sheet 3: Cashflow

Required columns:

```text
Month
Cash_Inflow
Cash_Outflow
Net_Cash
Opening_Cash
Closing_Cash
```

## Sheet 4: KPIs

Required columns:

```text
Month
Revenue_Growth
Margin %
Budget_Variance
Forecast_Accuracy
```

---

# ▶️ Running the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

The application will be available at:

```text
http://localhost:8501
```

---

# 📊 Dashboard Screens

The dashboard includes:

* KPI Cards
* Revenue Trend Chart
* Budget vs Actual Chart
* Region Performance Chart
* Margin Analysis Chart
* Variance Analysis Table
* Cashflow Trend
* Headcount Analysis
* AI Insights Section
* FP&A AI Chat Assistant

---

# 🔮 Future Enhancements

* Forecasting using Prophet
* PDF Report Generation
* Automated Monthly Reports
* Email Distribution
* Multi-Agent AI using AutoGen
* User Authentication
* Database Integration (PostgreSQL / Snowflake)
* Role-based Access
* Cloud Deployment

---

# 👨‍💻 Author

**Govindaraj Namachivayam**

Finance | Business Intelligence | Data Analytics | Generative AI

---

# ⭐ If you find this project useful

Please consider giving it a star on GitHub.
