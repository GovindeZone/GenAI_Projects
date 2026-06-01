import streamlit as st
import pandas as pd
import os

FILE_NAME = "output.xlsx"

st.title("Form to Excel")

# ---------- INPUTS ----------
name = st.text_input("Enter Name")

role = st.selectbox("Select Role", ["Data Analyst", "Python Developer", "Manager"])

gender = st.radio("Select Gender", ["Male", "Female"], horizontal=True)

agree = st.checkbox("Accept Terms")

# ---------- SUBMIT ----------
if st.button("Submit"):

    # Step 1: Create new record
    new_data = {
        "Name": name,
        "Role": role,
        "Gender": gender,
        "Accepted": agree
    }

    df_new = pd.DataFrame([new_data])

    # Step 2: Check if file exists
    if os.path.exists(FILE_NAME):
        df_existing = pd.read_excel(FILE_NAME)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)
    else:
        df_final = df_new

    # Step 3: Save to Excel
    df_final.to_excel(FILE_NAME, index=False)

    st.success("Data saved to Excel!")