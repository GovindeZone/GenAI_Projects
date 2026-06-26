import streamlit as st
import re

from modules.loader import load_excel
from modules.retriever import get_invoice_details
from modules.llm import explain_invoice
from modules.kg_builder import build_kg   # ✅ FIX: missing import

from pyvis.network import Network
import streamlit.components.v1 as components


# -------------------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------------------

st.set_page_config(
    page_title="Invoice KG-RAG System",
    page_icon="📘",
    layout="wide"
)

st.title("📘 Invoice KG-RAG System")
st.caption("Knowledge Graph + RAG for Invoice Intelligence")


# -------------------------------------------------------------------
# HELPERS
# -------------------------------------------------------------------

def extract_invoice_id(text):
    if not text:
        return None

    pattern = r"INV\d+"
    match = re.search(pattern, text.upper())

    if match:
        return match.group()

    return None


def draw_graph(nodes, edges):
    net = Network(
        height="600px",
        width="100%",
        bgcolor="#ffffff",
        font_color="black"
    )

    # Add nodes
    for n in nodes:
        net.add_node(n)

    # Add edges
    for e in edges:
        net.add_edge(e["source"], e["target"])

    # Save and render
    net.save_graph("kg.html")

    with open("kg.html", "r", encoding="utf-8") as f:
        source_code = f.read()

    components.html(source_code, height=650, scrolling=True)


# -------------------------------------------------------------------
# SIDEBAR
# -------------------------------------------------------------------

with st.sidebar:
    st.header("⚙️ Configuration")

    api_key = st.text_input("Groq API Key", type="password")

    st.divider()

    uploaded_file = st.file_uploader(
        "Upload Excel Workbook",
        type=["xlsx"]
    )


# -------------------------------------------------------------------
# MAIN APP
# -------------------------------------------------------------------

if uploaded_file:

    try:
        invoices, po, vendors, policies, approvals = load_excel(uploaded_file)

        invoice_list = invoices["Invoice_ID"].tolist()

        tab1, tab2 = st.tabs([
            "📄 Invoice Analysis",
            "💬 Ask Any Question"
        ])

        # ============================================================
        # TAB 1 - INVOICE ANALYSIS
        # ============================================================

        with tab1:

            st.subheader("Invoice Investigation")

            invoice_id = st.selectbox("Select Invoice", invoice_list)

            # -------------------------
            # REJECTION EXPLANATION
            # -------------------------
            if st.button("Why Rejected?", key="invoice_btn"):

                evidence = get_invoice_details(
                    invoice_id,
                    invoices,
                    po,
                    vendors,
                    policies,
                    approvals
                )

                if evidence is None:
                    st.error(f"Invoice {invoice_id} not found.")

                else:
                    col1, col2 = st.columns([1, 2])

                    with col1:
                        st.subheader("Evidence")
                        st.json(evidence)

                    with col2:
                        if api_key:
                            answer = explain_invoice(evidence, api_key)

                            st.subheader("AI Explanation")
                            st.write(answer)
                        else:
                            st.warning("Please enter Groq API Key.")

            # -------------------------
            # KG BUTTON (FIXED)
            # -------------------------
            st.divider()

            if st.button("Generate KG"):

                try:
                    with st.spinner("Building Knowledge Graph..."):

                        nodes, edges = build_kg(
                            invoices,
                            po,
                            vendors,
                            policies,
                            approvals
                        )

                    if not nodes or not edges:
                        st.warning("No graph data generated.")
                    else:
                        st.success("Knowledge Graph generated successfully!")
                        draw_graph(nodes, edges)

                except Exception as e:
                    st.error(f"KG generation failed: {e}")


        # ============================================================
        # TAB 2 - ASK ANY QUESTION
        # ============================================================

        with tab2:

            st.subheader("Ask Anything")

            user_question = st.text_area(
                "Question",
                placeholder="""
Examples:
Why was INV002 rejected?
Show details for INV004
Explain rejection reason for INV005
                """,
                height=150
            )

            if st.button("Ask", key="question_btn"):

                if not user_question.strip():
                    st.warning("Please enter a question.")

                else:
                    invoice_id = extract_invoice_id(user_question)

                    if not invoice_id:
                        st.error("Please mention an invoice ID like INV001.")

                    else:

                        evidence = get_invoice_details(
                            invoice_id,
                            invoices,
                            po,
                            vendors,
                            policies,
                            approvals
                        )

                        if evidence is None:
                            st.error(f"Invoice {invoice_id} not found.")

                        else:
                            st.subheader(f"Invoice Found: {invoice_id}")

                            with st.expander("View Evidence", expanded=True):
                                st.json(evidence)

                            if api_key:
                                answer = explain_invoice(evidence, api_key)

                                st.subheader("AI Answer")
                                st.write(answer)

                            else:
                                st.warning("Please enter Groq API Key.")

    except Exception as e:
        st.error(f"Error loading workbook: {str(e)}")

else:
    st.info("Upload the Invoice KG-RAG Excel workbook to begin.")