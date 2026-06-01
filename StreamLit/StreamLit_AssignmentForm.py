import streamlit as st
import pandas as pd
import os

# File name
file_name = "submission_data.xlsx"

st.title("Assignment Workbook")

# Frame box
with st.container():
    st.subheader("Entry Form")

    # Week Selector
    week = st.selectbox(
        "Select Week",
        ["Week 1", "Week 2", "Week 3", "Week 4", "Week 5", "Week 6"]
    )

    # Day Selector
    day = st.selectbox(
        "Select Day",
        ["Day 1", "Day 2", "Day 3", "Day 4", "Day 5"]
    )

    # Topic (minimal input)
    topic = st.text_input("Topic")

    # Take Away
    takeaway = st.text_area("Take away")

    # Summary
    summary = st.text_area("Summary")

    # Submission Status
    st.markdown("### Submission Status")
    submitted = st.checkbox("Submitted")
    not_submitted = st.checkbox("Not Submitted")

    # Notes
    notes = st.text_area("Notes / Remarks")

    # Buttons
    col1, col2 = st.columns(2)

    with col1:
        submit = st.button("Submit")

    with col2:
        print_btn = st.button("Print")

# -----------------------------
# Save to Excel
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

    st.success("Data saved to Excel successfully!")

# -----------------------------
# Print Function
# -----------------------------
if print_btn:
    # st.write("### Print Preview")
    # st.write(f"Week: {week}")
    # st.write(f"Day: {day}")
    # st.write(f"Topic: {topic}")
    # st.write(f"Take Away: {takeaway}")
    # st.write(f"Summary: {summary}")
    # st.write(f"Submitted: {submitted}")
    # st.write(f"Not Submitted: {not_submitted}")
    # st.write(f"Notes: {notes}")

    st.info("Use browser Ctrl + P to print")