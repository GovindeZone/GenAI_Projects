# ============================================
# AI NEWSPAPER CHATBOT
# Reads newspaper website articles and answers questions
# ============================================

# INSTALL:
# pip install streamlit newspaper3k langchain langchain-community
# pip install langchain-groq sentence-transformers faiss-cpu
# pip install beautifulsoup4 lxml

# RUN:
# streamlit run Newspaper_Chatbot.py

# ============================================
# IMPORTS
# ============================================

import streamlit as st
from newspaper import Article

from dotenv import load_dotenv
import os

# LANGCHAIN
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
#from langchain_huggingface import HuggingFaceEmbeddings
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

st.set_page_config(page_title="AI Newspaper Chatbot")

st.title("📰 AI Newspaper Chatbot")

# =========================================================
# URL INPUT
# =========================================================

url = st.text_input(
    "Enter Newspaper Article URL",
    placeholder="https://www.bbc.com/news"
)

# =========================================================
# LOAD ARTICLE
# =========================================================

if st.button("Load Article"):

    try:

        with st.spinner("Loading article..."):

            # ============================================
            # READ ARTICLE
            # ============================================

            article = Article(url)

            article.download()
            article.parse()

            article_text = article.text

            if article_text.strip() == "":
                st.error("Unable to extract article text")
                st.stop()

            # ============================================
            # DISPLAY
            # ============================================

            st.success("Article Loaded Successfully")

            st.subheader("Article Title")
            st.write(article.title)

            st.subheader("Article Preview")
            st.write(article_text[:1000])

            # ============================================
            # TEXT SPLITTING
            # ============================================

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=100
            )

            docs = splitter.split_documents(
                [Document(page_content=article_text)]
            )

            # ============================================
            # EMBEDDINGS
            # ============================================

            #embedding = HuggingFaceEmbeddings(
            #    model_name="sentence-transformers/all-MiniLM-L6-v2"
            #)
            @st.cache_resource
            def load_embedding():
                return HuggingFaceEmbeddings(
                    model_name="sentence-transformers/all-MiniLM-L6-v2"
                )

            embedding = load_embedding()

            # ============================================
            # VECTOR STORE
            # ============================================

            vectorstore = FAISS.from_documents(
                docs,
                embedding
            )

            # SAVE VECTORSTORE
            st.session_state.vectorstore = vectorstore

            st.success("AI Ready - Ask Questions")

    except Exception as e:
        st.error(f"Error: {e}")

# =========================================================
# QUESTION SECTION
# =========================================================

if "vectorstore" in st.session_state:

    question = st.text_input("Ask Question About Article")

    if st.button("Ask"):

        try:

            with st.spinner("Generating answer..."):

                # ============================================
                # RETRIEVE DOCUMENTS
                # ============================================

                docs = st.session_state.vectorstore.similarity_search(
                    question,
                    k=3
                )

                context = "\n\n".join(
                    [doc.page_content for doc in docs]
                )

                # ============================================
                # LLM
                # ============================================

                llm = ChatGroq(
                    groq_api_key=groq_api_key,
                    model_name="llama-3.3-70b-versatile"
                )

                # ============================================
                # PROMPT
                # ============================================

                prompt = f"""
                Answer the question based on the article context below.

                Context:
                {context}

                Question:
                {question}
                """

                # ============================================
                # GENERATE RESPONSE
                # ============================================

                response = llm.invoke(prompt)

                st.subheader("Answer")

                st.write(response.content)

        except Exception as e:
            st.error(f"Error: {e}")