import streamlit as st
import pandas as pd
import os

file_name = "submission_data.xlsx"

# -----------------------------
# CSS Styling
# -----------------------------
st.markdown("""
<style>        
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

div.stButton > button {
    background-color: black;
    color: white;
    border-radius: 5px;
}

.title-center {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #DC143C;
}

.section-header {
    background-color: red;
    color: white;
    padding: 8px;
    border-radius: 5px;
    width: 160px;
    height: 40px;
    display: flex;
    align-items: center;
}

div[data-baseweb="select"],
div[data-baseweb="input"] {
    margin-top: -8px;
}

div[data-testid="stTextArea"] > div {
    margin-top: -25px !important;
}
textarea {
    margin-top: -10px !important;
}

.frame-box {
    border: 2px solid black;
    padding: 20px;
    border-radius: 10px;
    background-color: #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# TITLE
# -----------------------------
st.markdown('<div class="title-center">Social Eagle</div>', unsafe_allow_html=True)
st.markdown('<div class="title-center">Workbook Assignment</div>', unsafe_allow_html=True)

# -----------------------------
# WEEK
# -----------------------------
col1, col2 = st.columns([1,3], vertical_alignment="center")
with col1:
    st.markdown('<div class="section-header">Select Week</div>', unsafe_allow_html=True)
with col2:
    week = st.selectbox(" ", ["Week 1","Week 2","Week 3","Week 4","Week 5","Week 6"], key="week")

# -----------------------------
# DAY
# -----------------------------
col1, col2 = st.columns([1,3], vertical_alignment="center")
with col1:
    st.markdown('<div class="section-header">Select Day</div>', unsafe_allow_html=True)
with col2:
    day = st.selectbox(" ", ["Day 1","Day 2","Day 3","Day 4","Day 5"], key="day")

# -----------------------------
# READ + AUTO-FILL DATA
# -----------------------------
topic_val = ""
takeaway_val = ""
summary_val = ""
submitted_val = False
not_submitted_val = False
notes_val = ""

if os.path.exists(file_name):
    df_existing = pd.read_excel(file_name)

    filtered_df = df_existing[
        (df_existing["Week"] == week) &
        (df_existing["Day"] == day)
    ]

    if not filtered_df.empty:
        row = filtered_df.iloc[-1]

        topic_val = row["Topic"]
        takeaway_val = row["Take Away"]
        summary_val = row["Summary"]
        submitted_val = row["Submitted"]
        not_submitted_val = row["Not Submitted"]
        notes_val = row["Notes"]

        st.markdown("### Previous Submission")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.info("No previous submission for selected Week/Day")

# -----------------------------
# TOPIC
# -----------------------------
col1, col2 = st.columns([1,3])
with col1:
    st.markdown('<div class="section-header">Topic</div>', unsafe_allow_html=True)
with col2:
    topic = st.text_input(" ", value=topic_val, key="topic")

st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------
# TAKE AWAY
# -----------------------------
col1, col2 = st.columns([1,3])
with col1:
    st.markdown('<div class="section-header">Take away</div>', unsafe_allow_html=True)
with col2:
    takeaway = st.text_area(" ", value=takeaway_val, height=120, key="takeaway")

# -----------------------------
# SUMMARY
# -----------------------------
col1, col2 = st.columns([1,3])
with col1:
    st.markdown('<div class="section-header">Summary</div>', unsafe_allow_html=True)
with col2:
    summary = st.text_area(" ", value=summary_val, height=120, key="summary")

# -----------------------------
# SUBMISSION STATUS
# -----------------------------
col1, col2 = st.columns([1,3])
with col1:
    st.markdown('<div class="section-header">Submission Status</div>', unsafe_allow_html=True)
with col2:
    sub1, sub2 = st.columns(2)
    with sub1:
        submitted = st.checkbox("Submitted (Task Completed and shared)", value=submitted_val)
    with sub2:
        not_submitted = st.checkbox("Not Submitted (Will Catch up later)", value=not_submitted_val)

# -----------------------------
# NOTES
# -----------------------------
col1, col2 = st.columns([1,3])
with col1:
    st.markdown('<div class="section-header">Notes / Remarks</div>', unsafe_allow_html=True)
with col2:
    notes = st.text_area(" ", value=notes_val, height=120, key="notes")

# -----------------------------
# BUTTONS
# -----------------------------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    space1, b1, space2, b2, space3 = st.columns([1,2,0.5,2,1])

    with b1:
        submit = st.button("Submit", use_container_width=True)

    with b2:
        print_btn = st.button("Print", use_container_width=True)

# -----------------------------
# SAVE TO EXCEL
# -----------------------------
if submit:
    data = {
        "Week": week,
        "Day": day,
        "Topic": topic,
        "Take Away": takeaway,
        "Summary": summary,
        "Submitted": submitted,
        "Not Submitted": not_submitted,
        "Notes": notes
    }

    df_new = pd.DataFrame([data])

    if os.path.exists(file_name):
        df_existing = pd.read_excel(file_name)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new

    df_final.to_excel(file_name, index=False)
    st.success("Data saved successfully!")

# -----------------------------
# PRINT
# -----------------------------
if print_btn:
    st.info("Press Ctrl + P to print")