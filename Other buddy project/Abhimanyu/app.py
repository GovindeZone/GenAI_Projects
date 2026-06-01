import streamlit as st
import requests
import pandas as pd


st.set_page_config(
    page_title="AI Auto Job Search Assistant",
    page_icon="TheNeuralForge_Compressed.jpg",
    layout="wide"
)

st.markdown("""
<style>

.main {
    background-color: #0e1117;
}

.stButton>button {
    background-color: #0A66C2;
    color: white;
    border-radius: 10px;
    height: 50px;
    width: 100%;
    font-size: 18px;
    font-weight: bold;
    border: none;
}

.stButton>button:hover {
    background-color: #004182;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.job-box {
    background-color: #161b22;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid #30363d;
}

</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])

with col1:
    st.image("TheNeuralForge_Compressed.jpg", width=100)

with col2:
    st.title("🤖 AI Auto Job Search Assistant")
    st.caption("LinkedIn Automation using AI + Playwright")

st.divider()

with st.sidebar:

    st.header("⚙ Search Settings")

    max_jobs = st.slider(
        "Maximum Jobs",
        min_value=5,
        max_value=50,
        value=15
    )

    st.info("""
This tool:
- Searches LinkedIn Jobs
- Scrapes detailed job info
- Saves results to Excel
- Uses Playwright Automation
""")

st.subheader("🔍 Search Jobs")

col1, col2 = st.columns(2)

with col1:
    job_role = st.text_input(
        "Job Role",
        placeholder="Python Developer"
    )

with col2:
    location = st.text_input(
        "Location",
        placeholder="Chennai"
    )

if st.button("🚀 Search LinkedIn Jobs"):

    if job_role and location:

        payload = {
            "job_role": job_role,
            "location": location,
            "max_jobs": max_jobs
        }

        try:

            with st.spinner("Searching and scraping LinkedIn jobs..."):

                response = requests.post(
                    "http://127.0.0.1:5000/apply-jobs",
                    json=payload,
                    timeout=300
                )

            data = response.json()

            if response.status_code == 200:

                st.success(data["message"])

                total_jobs = len(data["jobs"])

                c1, c2, c3 = st.columns(3)

                c1.metric("Jobs Scraped", total_jobs)
                c2.metric("Location", location)
                c3.metric("Role", job_role)

                st.divider()
                st.subheader("📄 Job Preview")

                preview_jobs = data["jobs"][:5]

                for job in preview_jobs:

                    st.markdown(f"""
                    <div class="job-box">

                    <h4>{job.get("Title", "")}</h4>

                    <p>
                    <b>Company:</b> {job.get("Company", "")}<br>
                    <b>Location:</b> {job.get("Location", "")}<br>
                    <b>Posted:</b> {job.get("Posted Date", "")}<br>
                    <b>Easy Apply:</b> {job.get("Easy Apply", "")}
                    </p>

                    </div>
                    """, unsafe_allow_html=True)

                st.subheader("⬇ Download Results")

                file_path = f"../backend/{data['file_path']}"

                with open(file_path, "rb") as file:

                    st.download_button(
                        label="📥 Download Excel File",
                        data=file,
                        file_name=data["file_path"],
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )

            else:

                st.error(data["error"])

        except Exception as e:

            st.error(f"Error: {e}")

    else:

        st.warning("Please fill all fields")