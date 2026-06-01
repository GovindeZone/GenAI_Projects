import streamlit as st

st.title("My First Streamlit App")

name = st.text_input("Enter your name:")

if name:
    st.write(f"Hello, {name} 👋")

number = st.number_input("Enter a number:", value=0)

st.write("Square of number is:", number * number)cls
