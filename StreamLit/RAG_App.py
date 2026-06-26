import os
import tempfile
import streamlit as st
from pathlib import Path
from groq import Groq

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
    CSVLoader,
)
from langchain_community.document_loaders import UnstructuredExcelLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

# ── CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Policy Reader",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

CHUNK_SIZE = 800
CHUNK_OVERLAP = 100
TOP_K = 5
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
GROQ_MODEL = "llama-3.1-8b-instant"

SUPPORTED_TYPES = {
    "pdf": "application/pdf",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xls": "application/vnd.ms-excel",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "txt": "text/plain",
    "csv": "text/csv",
}

# ── HEADER ────────────────────────────────────────────────────────────────
st.markdown(
    "<h1 style='text-align:center;'>📘 Policy Reader / Document Reader</h1>",
    unsafe_allow_html=True
)
st.markdown("---")


# ── EMBEDDINGS (LAZY LOADED - SPEED FIX) ──────────────────────────────────
@st.cache_resource(show_spinner=False)
def get_embeddings():
    from langchain_community.embeddings import HuggingFaceEmbeddings
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


# ── LOAD FILES ─────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def cached_tmp_file(file_bytes: bytes, filename: str):
    suffix = Path(filename).suffix
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(file_bytes)
        return tmp.name


def load_documents(uploaded_files):
    docs = []
    errors = []

    for uf in uploaded_files:
        tmp_path = cached_tmp_file(uf.getvalue(), uf.name)
        ext = Path(uf.name).suffix.lower().lstrip(".")

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
                errors.append(f"Unsupported file: {uf.name}")
                continue

            loaded = loader.load()

            for d in loaded:
                d.metadata["source_file"] = uf.name

            docs.extend(loaded)

        except Exception as e:
            errors.append(f"Error loading {uf.name}: {e}")

        finally:
            try:
                os.unlink(tmp_path)
            except:
                pass

    return docs, errors


# ── VECTOR STORE ───────────────────────────────────────────────────────────
def build_vectorstore(docs):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )

    chunks = splitter.split_documents(docs)
    embeddings = get_embeddings()

    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore, len(chunks)


def retrieve_context(vectorstore, question):
    results = vectorstore.similarity_search(question, k=TOP_K)

    context = []
    sources = set()

    for r in results:
        context.append(r.page_content)
        sources.add(r.metadata.get("source_file", "unknown"))

    return "\n\n---\n\n".join(context), list(sources)


# ── GROQ LLM ───────────────────────────────────────────────────────────────
def ask_groq(question, context, mode):
    api_key = st.session_state.get("api_key") or os.environ.get("GROQ_API_KEY", "")

    if not api_key:
        return "⚠️ Please enter Groq API key in sidebar."

    client = Groq(api_key=api_key)

    if mode == "document_only":
        system_prompt = (
            "Answer ONLY from document context. "
            "If not found say: 'Not available in documents.'"
        )
    else:
        system_prompt = (
            "Use document context first, then general knowledge if needed."
        )

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"
            },
        ],
        temperature=0.2,
        max_tokens=2048,
    )

    return response.choices[0].message.content


# ── SESSION STATE ──────────────────────────────────────────────────────────
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None
if "chat" not in st.session_state:
    st.session_state.chat = []


# ── SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    api_key = st.text_input(
        "Groq API Key",
        type="password",
        value=st.session_state.get("api_key", "")
    )
    if api_key:
        st.session_state.api_key = api_key

    st.divider()

    st.header("📂 Upload Docs")

    uploaded_files = st.file_uploader(
        "Upload files",
        type=list(SUPPORTED_TYPES.keys()),
        accept_multiple_files=True
    )

    if uploaded_files:
        if st.button("Process Documents"):
            with st.spinner("Processing..."):
                docs, errors = load_documents(uploaded_files)

                if errors:
                    for e in errors:
                        st.error(e)

                if docs:
                    vs, n = build_vectorstore(docs)
                    st.session_state.vectorstore = vs
                    st.session_state.chat = []
                    st.success(f"Indexed {len(docs)} docs → {n} chunks")


    if st.session_state.vectorstore:
        if st.button("Clear"):
            st.session_state.vectorstore = None
            st.session_state.chat = []
            st.rerun()


# ── MAIN UI ────────────────────────────────────────────────────────────────
mode = st.radio(
    "Answer Mode",
    ["document_only", "enhanced"],
    horizontal=True
)

# Chat history
for c in st.session_state.chat:
    with st.chat_message("user"):
        st.write(c["q"])
    with st.chat_message("assistant"):
        st.write(c["a"])


# Input
q = st.chat_input("Ask your question...")

if q:
    if not st.session_state.vectorstore:
        st.warning("Upload documents first.")
    else:
        with st.chat_message("user"):
            st.write(q)

        context, sources = retrieve_context(
            st.session_state.vectorstore, q
        )

        answer = ask_groq(q, context, mode)

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.chat.append(
            {"q": q, "a": answer, "sources": sources}
        )