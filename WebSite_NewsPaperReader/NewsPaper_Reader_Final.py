import streamlit as st
import trafilatura
from dotenv import load_dotenv
import os

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_groq import ChatGroq

# =========================================================
# LOAD API KEY
# =========================================================

load_dotenv()
groq_api_key = os.getenv("GROQ_API_KEY")

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Newspaper Chatbot",
    layout="wide"
)

st.title("📰 AI Newspaper Chatbot")

# =========================================================
# EMBEDDING MODEL (LOAD ONCE)
# =========================================================

@st.cache_resource
def load_embedding():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

embedding = load_embedding()

# =========================================================
# URL INPUT
# =========================================================

url = st.text_input(
    "Enter Newspaper Article URL",
    placeholder="Paste article URL here"
)

# =========================================================
# LOAD ARTICLE
# =========================================================

if st.button("Load Article"):

    try:

        with st.spinner("Loading article..."):

            # ============================================
            # EXTRACT ARTICLE
            # ============================================

            downloaded = trafilatura.fetch_url(url)

            article_text = trafilatura.extract(downloaded)

            if not article_text:
                st.error("Unable to extract article text")
                st.stop()

            # ============================================
            # TITLE
            # ============================================

            title = url.split("/")[-1]
            title = title.replace("-", " ").title()

            # ============================================
            # DISPLAY
            # ============================================

            st.success("Article Loaded Successfully")

            st.subheader("Article Title")
            st.write(title)

            st.subheader("Article Preview")

            if len(article_text) > 1500:
                st.write(article_text[:1500] + "...")
            else:
                st.write(article_text)

            # ============================================
            # SPLIT DOCUMENT
            # ============================================

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100
            )

            docs = splitter.split_documents(
                [Document(page_content=article_text)]
            )

            # ============================================
            # VECTOR STORE
            # ============================================

            vectorstore = FAISS.from_documents(
                docs,
                embedding
            )

            st.session_state.vectorstore = vectorstore
            st.session_state.article_text = article_text

            st.success("AI Ready - Ask Questions")

    except Exception as e:
        st.error(f"Error: {str(e)}")

# =========================================================
# QUESTION SECTION
# =========================================================

if "vectorstore" in st.session_state:

    st.markdown("---")
    st.subheader("Ask Questions About This Article")

    question = st.text_input(
        "Question",
        placeholder="What is this article about?"
    )

    if st.button("Ask"):

        if question.strip() == "":
            st.warning("Enter a question")
            st.stop()

        try:

            with st.spinner("Generating answer..."):

                docs = st.session_state.vectorstore.similarity_search(
                    question,
                    k=3
                )

                context = "\n\n".join(
                    [doc.page_content for doc in docs]
                )

                llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name="llama-3.1-8b-instant"
                )

                prompt = f"""
You are a newspaper assistant.

Answer ONLY from the article content.

Article Context:
{context}

Question:
{question}

Answer:
"""

                response = llm.invoke(prompt)

                st.subheader("Answer")

                st.write(response.content)

        except Exception as e:
            st.error(f"Error: {str(e)}")