# Document Q&A — RAG Application

A Retrieval-Augmented Generation (RAG) app built with LangChain, FAISS, and Claude Opus 4.8. Upload documents, ask questions, and choose between two answer modes.

---

## Features

- **Multi-format document support**: PDF, Excel (XLSX/XLS), Word (DOCX), TXT, CSV
- **Two answer modes**:
  - **Document Only** — answers strictly from your uploaded files; no outside knowledge
  - **Enhanced Context** — document content supplemented with general knowledge for richer answers
- **Vector search** using FAISS + HuggingFace sentence embeddings (`all-MiniLM-L6-v2`)
- **Chat interface** with persistent history and per-answer source file tags
- Clean, professional Streamlit UI

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements_rag.txt
```

### 2. Get an Anthropic API key

Sign up at [console.anthropic.com](https://console.anthropic.com) and create an API key.

### 3. Run the app

```bash
streamlit run RAG_App.py
```

The app opens in your browser at `http://localhost:8501`.

---

## Usage

1. **Enter your API key** in the sidebar (field at the top).
2. **Upload one or more documents** using the file uploader — you can mix formats.
3. Click **Process Documents** to index them into the vector store.
4. **Choose an answer mode** using the radio toggle:
   - `📋 Document Only` — strictly document-grounded answers
   - `🌐 Enhanced Context` — document + general knowledge
5. **Type your question** in the chat input at the bottom.
6. Answers appear with **source file tags** showing which document(s) were used.

---

## Project Structure

```
StreamLit/
├── RAG_App.py            # Main application
├── requirements_rag.txt  # Python dependencies
└── README_RAG.md         # This file
```

---

## How It Works

```
Upload files
    │
    ▼
Document Loaders (LangChain)
    │  PyPDFLoader / UnstructuredExcelLoader / Docx2txtLoader / TextLoader / CSVLoader
    ▼
Text Splitter (RecursiveCharacterTextSplitter)
    │  chunk_size=800, overlap=100
    ▼
HuggingFace Embeddings (all-MiniLM-L6-v2)
    │
    ▼
FAISS Vector Store
    │
    ▼  (on each question)
Similarity Search → top-5 chunks
    │
    ▼
Claude Opus 4.8 (Anthropic SDK)
    │  system prompt varies by mode
    ▼
Answer displayed in chat
```

---

## Dependencies

| Package | Purpose |
|---|---|
| `anthropic` | Claude API client |
| `streamlit` | UI framework |
| `langchain-community` | Document loaders, FAISS wrapper |
| `langchain-text-splitters` | Chunking |
| `faiss-cpu` | Vector similarity search |
| `sentence-transformers` | Local embeddings |
| `pypdf` | PDF parsing |
| `openpyxl` / `xlrd` | Excel parsing |
| `python-docx` | Word document parsing |
| `pandas` | CSV support |

---

## Notes

- API keys are held only in session state and never written to disk.
- Embeddings are cached with `@st.cache_resource` so re-indexing is fast after the first load.
- For large documents, indexing may take a few seconds — a spinner indicates progress.
- The vector store is rebuilt each time you click **Process Documents**; click **Clear Documents** to reset.
