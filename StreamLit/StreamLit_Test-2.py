import streamlit as st

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="My App", layout="centered")

# ---------- CUSTOM STYLE ----------
st.markdown("""
    <style>
    /* Full page background */
    .stApp {
        background-color: #d4edda;   /* light green */
    }

    /* Main container box */
    .custom-box {
        border: 2px solid green;
        padding: 20px;
        border-radius: 10px;
        background-color: #e9f7ef;
    }

    /* Button styling */
    .stButton>button {
        background-color: green;
        color: white;
        border-radius: 8px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- UI ----------
st.title("Streamlit Styled App")

# Custom bordered container
st.markdown('<div class="custom-box">', unsafe_allow_html=True)

# Inputs
name = st.text_input("Enter Name")

#gender = st.radio("Select Gender", ["Male", "Female"])

gender = st.radio(
    "Select Gender",
    ["Male", "Female"],
    horizontal=True   # ✅ makes it horizontal
)

# OPTION KEY (Dropdown)
role = st.selectbox("Select Role", ["Data Analyst", "Python Developer", "Manager"])

# Checkbox
agree = st.checkbox("Accept Terms")

# Button
if st.button("Submit"):
    st.success(f"Name: {name}")
    st.success(f"Role: {role}")
    st.success(f"Accepted: {agree}")

st.markdown('</div>', unsafe_allow_html=True)