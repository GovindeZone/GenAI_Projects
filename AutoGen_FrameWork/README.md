# 📊 AI Multi-Agent Business Report Generator

An AI-powered business reporting application built using **Streamlit**, **Microsoft AutoGen 0.7.5**, and **Groq LLMs**.

The application allows users to upload sales/business Excel files and automatically generate executive business reports using multiple AI agents collaborating together.

---

## 🚀 Features

* Upload Excel files (`.xlsx`)
* Preview uploaded business data
* Multi-Agent AI collaboration using AutoGen
* Business insight generation
* Financial analysis and validation
* Executive summary generation
* Download report as Microsoft Word (`.docx`)
* Groq LLM integration for fast inference
* Streamlit-based interactive UI

---

## 🏗️ Architecture

```text
User Uploads Excel File
            │
            ▼
     Streamlit UI
            │
            ▼
      Data Preprocessing
            │
            ▼
   AutoGen Multi-Agent Team
            │
     ┌──────┴──────┐
     ▼             ▼
 Analyst Agent   Finance Agent
     │             │
     └──────┬──────┘
            ▼
  Business Report Generation
            │
            ▼
 Download as DOCX
```

---

## 🤖 AI Agents

### Analyst Agent

Responsible for:

* Identifying business trends
* Extracting key insights
* Detecting anomalies
* Highlighting performance drivers

### Finance Agent

Responsible for:

* Revenue validation
* Financial observations
* Risk identification
* Business performance assessment

---

## 🛠️ Technology Stack

| Technology    | Purpose               |
| ------------- | --------------------- |
| Python        | Backend               |
| Streamlit     | Web UI                |
| AutoGen 0.7.5 | Multi-Agent Framework |
| Groq API      | LLM Provider          |
| Pandas        | Data Processing       |
| OpenPyXL      | Excel Handling        |
| python-docx   | Report Export         |

---

## 📁 Project Structure

```text
AutoGen_FrameWork/
│
├── app.py
├── config.py
├── requirements.txt
├── .env
│
├── agents/
│   ├── __init__.py
│   ├── analyst.py
│   └── finance.py
│
├── utils/
│   ├── excel_reader.py
│   ├── model_client.py
│   └── report_export.py
│
├── output/
│   └── reports/
│
└── README.md
```

---

## ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/AutoGen_Business_Report.git

cd AutoGen_Business_Report
```

---

### Create Virtual Environment

```bash
python -m venv venv
```

Activate virtual environment:

**Windows**

```bash
venv\Scripts\activate
```

---

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root.

```env
GROQ_API_KEY=your_groq_api_key

MODEL_NAME=llama-3.1-8b-instant

BASE_URL=https://api.groq.com/openai/v1

TEMPERATURE=0.2

MAX_TOKENS=4096
```

---

## ▶️ Running the Application

```bash
streamlit run app.py
```

The application will open in your browser:

```text
http://localhost:8501
```

---

## 📄 Supported Input

Supported file type:

* `.xlsx`

Example datasets:

* Sales Data
* Revenue Reports
* Financial Transactions
* Business KPI Data

---

## 📥 Output

The system generates:

* Executive Summary
* Key Business Insights
* Financial Observations
* Risks and Opportunities
* Business Recommendations

Reports can be downloaded in:

* Microsoft Word (`.docx`)

---

## 📸 Screenshots

### Upload Screen

*Add screenshot here*

### Generated Report

*Add screenshot here*

---

## 🔮 Future Enhancements

* Additional AI agents
* KPI dashboard visualizations
* PDF report generation
* Charts and graphs
* Conversational chat interface
* Knowledge Graph integration
* Retrieval-Augmented Generation (RAG)
* Report history management

---

## 👨‍💻 Author

**Govindaraj Namachivayam**

AI | Automation | Business Intelligence | Generative AI

GitHub: https://github.com/GovindeZone

---

## 📜 License

This project is licensed under the MIT License.
