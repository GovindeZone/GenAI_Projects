import os
import tempfile
import streamlit as st
from pathlib import Path
import anthropic

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
)
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Document Q&A",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1a1a2e;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #555;
        margin-bottom: 1.5rem;
    }
    .mode-card {
        background: #f8f9fa;
        border-left: 4px solid #4f8ef7;
        padding: 0.8rem 1rem;
        border-radius: 6px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    .answer-box {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1.2rem 1.5rem;
        line-height: 1.7;
    }
    .source-tag {
        display: inline-block;
        background: #e8f0fe;
        color: #1967d2;
        border-radius: 4px;
        padding: 2px 8px;
        font-size: 0.78rem;
        margin: 2px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Constants ─────────────────────────────────────────────────────────────────
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 5
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
CLAUDE_MODEL = "claude-opus-4-8"

SUPPORTED_TYPES = {
    "pdf": "application/pdf",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xls": "application/vnd.ms-excel",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain",
    "csv": "text/csv",
}


# ── Helpers ───────────────────────────────────────────────────────────────────

@st.cache_resource(show_spinner=False)
def get_embeddings():
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def load_documents(uploaded_files):
    """Load all uploaded files and return LangChain Document objects."""
    docs = []
    errors = []
    for uf in uploaded_files:
        ext = Path(uf.name).suffix.lower().lstrip(".")
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{ext}") as tmp:
            tmp.write(uf.getbuffer())
            tmp_path = tmp.name
        try:
            if ext == "pdf":
                loader = PyPDFLoader(tmp_path)
            elif ext in ("xlsx", "xls"):
                loader = UnstructuredExcelLoader(tmp_path)
            elif ext == "docx":
                loader = Docx2txtLoader(tmp_path)
            elif ext == "txt":
                loader = TextLoader(tmp_path, encoding="utf-8")
            elif ext == "csv":
                loader = CSVLoader(tmp_path, encoding="utf-8")
            else:
                errors.append(f"Unsupported file type: {uf.name}")
                continue
            loaded = loader.load()
            # Tag each chunk with its source filename
            for doc in loaded:
                doc.metadata["source_file"] = uf.name
            docs.extend(loaded)
        except Exception as e:
            errors.append(f"Error loading {uf.name}: {e}")
        finally:
            os.unlink(tmp_path)
    return docs, errors


def build_vectorstore(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP
    )
    chunks = splitter.split_documents(docs)
    embeddings = get_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore, len(chunks)


def retrieve_context(vectorstore, question):
    results = vectorstore.similarity_search(question, k=TOP_K)
    context_parts = []
    sources = set()
    for r in results:
        context_parts.append(r.page_content)
        sources.add(r.metadata.get("source_file", "unknown"))
    return "\n\n---\n\n".join(context_parts), list(sources)


def ask_claude(question: str, context: str, mode: str) -> str:
    api_key = st.session_state.get("api_key") or os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        return "⚠️ Please enter your Anthropic API key in the sidebar."

    client = anthropic.Anthropic(api_key=api_key)

    if mode == "document_only":
        system_prompt = (
            "You are a precise document assistant. Answer the user's question "
            "using ONLY the information provided in the DOCUMENT CONTEXT below. "
            "If the answer is not found in the context, say: "
            "'This information is not available in the provided documents.' "
            "Do not use any outside knowledge."
        )
    else:  # enhanced
        system_prompt = (
            "You are a knowledgeable assistant. First answer the user's question "
            "using the DOCUMENT CONTEXT provided. Then, if helpful, supplement "
            "with relevant general knowledge to give a more complete and insightful answer. "
            "Clearly distinguish between what comes from the documents and what is general knowledge."
        )

    user_message = f"""DOCUMENT CONTEXT:
{context}

USER QUESTION:
{question}"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=2048,
        thinking={"type": "adaptive"},
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}],
    )

    # Extract text blocks only (skip thinking blocks)
    answer_parts = [
        block.text for block in response.content if block.type == "text"
    ]
    return "\n".join(answer_parts)


# ── Session state init ────────────────────────────────────────────────────────
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "file_names" not in st.session_state:
    st.session_state.file_names = []
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        value=st.session_state.get("api_key", ""),
        placeholder="sk-ant-...",
        help="Your Anthropic API key. Never stored permanently.",
    )
    if api_key:
        st.session_state.api_key = api_key

    st.divider()
    st.markdown("## 📂 Upload Documents")
    uploaded_files = st.file_uploader(
        "Drag & drop or browse",
        type=list(SUPPORTED_TYPES.keys()),
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    if uploaded_files:
        if st.button("📥 Process Documents", use_container_width=True, type="primary"):
            with st.spinner("Loading and indexing documents…"):
                docs, errors = load_documents(uploaded_files)
                if errors:
                    for e in errors:
                        st.error(e)
                if docs:
                    vs, n_chunks = build_vectorstore(docs)
                    st.session_state.vectorstore = vs
                    st.session_state.file_names = [f.name for f in uploaded_files]
                    st.session_state.chat_history = []
                    st.success(f"✅ Indexed {len(docs)} pages → {n_chunks} chunks")
                else:
                    st.error("No documents could be loaded.")

    if st.session_state.file_names:
        st.divider()
        st.markdown("**Loaded files:**")
        for fn in st.session_state.file_names:
            st.markdown(f"- 📎 `{fn}`")

    if st.session_state.vectorstore and st.button(
        "🗑️ Clear Documents", use_container_width=True
    ):
        st.session_state.vectorstore = None
        st.session_state.file_names = []
        st.session_state.chat_history = []
        st.rerun()

    st.divider()
    st.markdown(
        "<small>Supported: PDF · XLSX · XLS · DOCX · TXT · CSV</small>",
        unsafe_allow_html=True,
    )


# ── Main area ─────────────────────────────────────────────────────────────────
st.markdown('<p class="main-header">📄 Document Q&A</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="sub-header">Ask questions about your uploaded documents — choose how deep the answer goes.</p>',
    unsafe_allow_html=True,
)

# Answer mode selector
col1, col2 = st.columns(2)
with col1:
    st.markdown(
        '<div class="mode-card"><b>📋 Document Only</b><br>'
        "Answers strictly from your uploaded files. No outside knowledge added.</div>",
        unsafe_allow_html=True,
    )
with col2:
    st.markdown(
        '<div class="mode-card" style="border-color:#34a853"><b>🌐 Enhanced Context</b><br>'
        "Document content + relevant general knowledge for a richer answer.</div>",
        unsafe_allow_html=True,
    )

answer_mode = st.radio(
    "Answer mode",
    options=["document_only", "enhanced"],
    format_func=lambda x: "📋 Document Only" if x == "document_only" else "🌐 Enhanced Context",
    horizontal=True,
    label_visibility="collapsed",
)

st.divider()

# Chat history display
for entry in st.session_state.chat_history:
    with st.chat_message("user"):
        st.write(entry["question"])
    with st.chat_message("assistant"):
        st.markdown(
            f'<div class="answer-box">{entry["answer"]}</div>', unsafe_allow_html=True
        )
        if entry.get("sources"):
            st.markdown(
                "**Sources:** "
                + " ".join(
                    f'<span class="source-tag">{s}</span>' for s in entry["sources"]
                ),
                unsafe_allow_html=True,
            )

# Question input
question = st.chat_input(
    "Ask a question about your documents…"
    if st.session_state.vectorstore
    else "Upload and process documents first, then ask a question…"
)

if question:
    if not st.session_state.vectorstore:
        st.warning("Please upload and process at least one document first.")
    elif not (st.session_state.get("api_key") or os.environ.get("ANTHROPIC_API_KEY")):
        st.warning("Please enter your Anthropic API key in the sidebar.")
    else:
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching documents and generating answer…"):
                context, sources = retrieve_context(
                    st.session_state.vectorstore, question
                )
                answer = ask_claude(question, context, answer_mode)

            st.markdown(
                f'<div class="answer-box">{answer}</div>', unsafe_allow_html=True
            )
            if sources:
                st.markdown(
                    "**Sources:** "
                    + " ".join(
                        f'<span class="source-tag">{s}</span>' for s in sources
                    ),
                    unsafe_allow_html=True,
                )

        st.session_state.chat_history.append(
            {"question": question, "answer": answer, "sources": sources}
        )
