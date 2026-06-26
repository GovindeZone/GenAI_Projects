import pandas as pd
import networkx as nx
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

# ------------------------
# Load API Key
# ------------------------
load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# ------------------------
# Build Knowledge Graph
# ------------------------
df = pd.read_csv("employees.csv")

G = nx.Graph()

for _, row in df.iterrows():

    emp = row["Employee"]
    dept = row["Department"]
    mgr = row["Manager"]
    skill = row["Skill"]

    G.add_edge(emp, dept, relation="works_in")
    G.add_edge(emp, mgr, relation="reports_to")
    G.add_edge(emp, skill, relation="has_skill")

# ------------------------
# KG Retrieval
# ------------------------
def retrieve_from_kg(query):

    context = []

    for node in G.nodes():

        if node.lower() in query.lower():

            neighbors = G.neighbors(node)

            for n in neighbors:
                context.append(f"{node} -> {n}")

    return "\n".join(context)

# ------------------------
# Ask Question
# ------------------------
question = input("Ask: ")

kg_context = retrieve_from_kg(question)

prompt = f"""
Answer using the knowledge graph information.

Knowledge Graph Context:
{kg_context}

Question:
{question}
"""

response = llm.invoke(prompt)

print("\nAnswer:")
print(response.content)