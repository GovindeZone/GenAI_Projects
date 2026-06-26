# 📘 Invoice KG-RAG System

## Overview

Invoice KG-RAG System is a Knowledge Graph + Retrieval Augmented Generation (KG-RAG) application built using Streamlit, Python, and Groq.

The application helps finance teams investigate invoice exceptions by connecting invoices, purchase orders, vendors, approval workflows, and policy rules to provide AI-generated explanations.

Instead of simply searching documents, the system follows business relationships and explains why an invoice was approved or rejected.

---

## Features

### Invoice Investigation

* Upload Excel-based finance data
* Analyze individual invoices
* View linked business evidence
* Generate AI-powered explanations

### Knowledge Graph Concepts

The system establishes relationships between:

* Invoice
* Purchase Order (PO)
* Vendor
* Approval Workflow
* Policy Rules

Example:

Invoice → Purchase Order

Invoice → Vendor

Invoice → Policy Rule

Invoice → Approval History

---

## Example Questions

### Invoice Analysis

* Why was INV002 rejected?
* Why was INV005 rejected?
* Explain INV004 rejection.
* Show evidence for INV001.

### Future KG-RAG Questions

* Show all rejected invoices.
* Which vendor has the most rejections?
* Which policy causes most failures?
* Show invoices with amount mismatches.
* Show blocked vendors.

---

## Technology Stack

| Component            | Technology        |
| -------------------- | ----------------- |
| Frontend             | Streamlit         |
| Programming Language | Python            |
| Data Processing      | Pandas            |
| Excel Reader         | OpenPyXL          |
| LLM                  | Groq              |
| Knowledge Graph      | NetworkX (Future) |
| Visualization        | PyVis (Future)    |
| Vector Search        | FAISS (Future)    |

---

## Project Structure

```text
Invoice_KG_RAG/
│
├── app.py
│
├── modules/
│   ├── __init__.py
│   ├── loader.py
│   ├── retriever.py
│   ├── llm.py
│   ├── entity_linker.py
│   └── graph_builder.py
│
├── requirements.txt
│
├── sample_data.xlsx
│
└── README.md
```

---

## Excel Workbook Structure

The uploaded workbook must contain the following sheets:

### Invoices

| Invoice_ID | Vendor_ID | PO_ID | Invoice_Amount | Status | Reason_Code |
| ---------- | --------- | ----- | -------------- | ------ | ----------- |

### Purchase_Orders

| PO_ID | Vendor_ID | PO_Amount |
| ----- | --------- | --------- |

### Vendors

| Vendor_ID | Vendor_Name | Vendor_Status |
| --------- | ----------- | ------------- |

### Policies

| Reason_Code | Policy_Rule |
| ----------- | ----------- |

### Approvals

| Invoice_ID | Approver | Approval_Status | Comments |
| ---------- | -------- | --------------- | -------- |

---

## Installation

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Groq API Key

Create a Groq API key from:

https://console.groq.com

Enter the API key in the Streamlit sidebar when the application starts.

---

## Run Application

```bash
streamlit run app.py
```

The application will start in your browser.

---

## Example Workflow

### Step 1

Upload finance workbook.

### Step 2

Select invoice INV002.

### Step 3

Click "Why Rejected?"

### Step 4

System retrieves:

* Invoice Amount
* PO Amount
* Vendor Information
* Approval Comments
* Policy Rule

### Step 5

Groq generates explanation.

Example:

Invoice INV002 was rejected because the invoice amount exceeded the purchase order amount by 20%.

Policy AMOUNT_MISMATCH requires rejection when invoice variance exceeds the approved threshold.

The rejection was confirmed by Manager B.

---

## Roadmap

### Version 1

* Excel Upload
* Invoice Analysis
* AI Explanation

### Version 2

* Knowledge Graph Relationships
* Graph Visualization
* Interactive Entity Exploration

### Version 3

* Hybrid KG-RAG + Vector Search
* Natural Language Finance Queries
* Vendor Risk Analytics
* Reconciliation Intelligence

### Version 4

* SAP Integration
* Oracle Fusion Integration
* Real-time Invoice Investigation

---

## Author

Gnamachivayam

Finance Transformation | Data Analytics | AI Solutions | KG-RAG Applications

---

## License

This project is intended for educational, portfolio, and demonstration purposes.
