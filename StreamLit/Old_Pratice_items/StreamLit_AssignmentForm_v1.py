import streamlit as st
import pandas as pd
import os

file_name = "submission_data.xlsx"

# -----------------------------
# CSS Styling (FINAL FINAL FIX)
# -----------------------------
st.markdown("""
<style>        
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* ADD BUTTON STYLE HERE  */
div.stButton > button {
    background-color: black;
    color: white;
    border-radius: 5px;
}
.title-center {
    text-align: center;
    font-size: 36px;
    font-weight: bold;
    color: #B22222;   /* brown-red */
}

/* Header box */
.section-header {
    background-color: red;
    color: white;
    padding: 8px;
    border-radius: 5px;
    width: 160px;
    height: 40px;
    display: flex;
    # align-items: flex-start;
    align-items: center;
    # padding-top: 6px;
}

/* Fix select/input spacing */
div[data-baseweb="select"],
div[data-baseweb="input"] {
    margin-top: -8px;
}

/* 🔴 CRITICAL FIX - TEXTAREA EXACT ALIGNMENT */
div[data-testid="stTextArea"] > div {
    margin-top: -25px !important;
}
textarea {
    margin-top: -10px !important;
}
/* Frame */
.frame-box {
    border: 2px solid black;
    padding: 20px;
    border-radius: 10px;
    background-color: #f9f9f9;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# FRAME START
# -----------------------------
#st.markdown('<div class="frame-box">', unsafe_allow_html=True)
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
# TOPIC
# -----------------------------
col1, col2 = st.columns([1,3], vertical_alignment="center")
with col1:
    st.markdown('<div class="section-header">Topic</div>', unsafe_allow_html=True)
with col2:
    topic = st.text_input(" ", key="topic")

# OPTION 1 (Recommended – simple space)
st.markdown("<br>", unsafe_allow_html=True)
# -----------------------------
# TAKE AWAY
# -----------------------------
col1, col2 = st.columns([1,3])
with col1:
    st.markdown('<div class="section-header">Take away</div>', unsafe_allow_html=True)
with col2:
    takeaway = st.text_area(" ", height=120, key="takeaway")

# -----------------------------
# SUMMARY
# -----------------------------
col1, col2 = st.columns([1,3])
with col1:
    st.markdown('<div class="section-header">Summary</div>', unsafe_allow_html=True)
with col2:
    summary = st.text_area(" ", height=120, key="summary")

# -----------------------------
# SUBMISSION STATUS
# -----------------------------
col1, col2 = st.columns([1,3], vertical_alignment="center")
with col1:
    st.markdown('<div class="section-header">Submission Status</div>', unsafe_allow_html=True)
with col2:
    sub1, sub2 = st.columns([1,1])
    with sub1:
        submitted = st.checkbox("Submitted (Task Completed and shared)")
    with sub2:
        not_submitted = st.checkbox("Not Submitted (Will Catch up later)")

# -----------------------------
# NOTES
# -----------------------------
col1, col2 = st.columns([1,3])
with col1:
    st.markdown('<div class="section-header">Notes / Remarks</div>', unsafe_allow_html=True)
with col2:
    notes = st.text_area(" ", height=120, key="notes")

# -----------------------------
# BUTTONS (CLOSER TOGETHER)
# -----------------------------
col1, col2, col3 = st.columns([1,2,1])

with col2:
    space1, b1, space2, b2, space3 = st.columns([1,2,0.5,2,1])

    with b1:
        submit = st.button("Submit", use_container_width=True)

    with b2:
        print_btn = st.button("Print", use_container_width=True)
 # -----------------------------
# FRAME END
# -----------------------------
st.markdown('</div>', unsafe_allow_html=True)

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
# PRINT PREVIEW
# -----------------------------
if print_btn:
    #st.write("### Print Preview")
    #st.write(data if 'data' in locals() else "No data to print")
    st.info("Press Ctrl + P to print")