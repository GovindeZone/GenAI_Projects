import streamlit as st

st.set_page_config(page_title="Main Menu", layout="centered")

# -----------------------------
# SESSION STATE (Navigation)
# -----------------------------
if "page" not in st.session_state:
    st.session_state.page = "home"

# -----------------------------
# HOME PAGE
# -----------------------------
if st.session_state.page == "home":

    st.markdown("<h1 style='text-align:center;'>Main Menu</h1>", unsafe_allow_html=True)
    st.markdown("<br><br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Submission", use_container_width=True):
            st.session_state.page = "submission"
            st.rerun()

    with col2:
        if st.button("View History", use_container_width=True):
            st.session_state.page = "history"
            st.rerun()

# -----------------------------
# SUBMISSION PAGE
# -----------------------------
elif st.session_state.page == "submission":

    if st.button("⬅ Back"):
        st.session_state.page = "home"
        st.rerun()

    # 👉 IMPORT YOUR FILE 2 FUNCTION HERE
    import StreamLit_AssignmentForm_v1 as submission_app
    submission_app.main()

# -----------------------------
# HISTORY PAGE
# -----------------------------
if st.button("❌ Close"):
    st.info("Closing window...")
    st.markdown(
        """
        <script>
        setTimeout(function(){
            window.close();
        }, 1000);
        </script>
        """,
        unsafe_allow_html=True
    )

    # 👉 IMPORT YOUR FILE 1 FUNCTION HERE
    import StreamLit_AssignmentForm_DataMovement as history_app
    history_app.main()