import streamlit as st
from resume_parser import extract_text_from_pdf
from job_parser import extract_job_text
from openrouter_api import query_openrouter
import time

st.set_page_config(page_title="AI Resume Analyzer", layout="centered")

# 💡 Custom Header with Emoji
st.markdown("""
    <h1 style='text-align: center;
               font-family: "Segoe UI", "Helvetica Neue", sans-serif;
               font-size: 42px
               margin-bottom: 0.2em;'>
        👓CVinsighT👓
    </h1>
    <p style='text-align: center;
              font-size: 18px;'>
        Let AI analyze your resume and show how well it fits the job
    </p>
""", unsafe_allow_html=True)


# 🔻 Section 1: Upload Resume
st.markdown("### 📄 Upload Your Resume (PDF)")
resume_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# 🔻 Section 2: Enter or Extract Job Description
st.markdown("### 💼 Enter Job Description")

input_method = st.radio("Input Method", ["Paste Text", "Paste Job Link"])

# Session state to persist textarea input
if "job_desc" not in st.session_state:
    st.session_state["job_desc"] = ""

job_desc = ""

if input_method == "Paste Text":
    job_desc = st.text_area("Paste the Job Description Here", 
                            value=st.session_state["job_desc"], 
                            height=200, key="job_text_area")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("🧹Clear Screen"):
            st.session_state["job_desc"] = ""
            st.experimental_rerun()

    # Keep session state updated
    st.session_state["job_desc"] = job_desc

else:
    job_url = st.text_input("Paste the Job Posting URL")
    if job_url:
        with st.spinner("Extracting job description from link..."):
            job_desc = extract_job_text(job_url)
            st.text_area("Extracted Description", value=job_desc, height=200)

# 🔘 Action Button
analyze_button = st.button("🔍 Analyze Match")

# ✅ Run Analysis
if analyze_button:
    if not resume_file or not job_desc:
        st.warning("Please upload a resume and provide a job description.")
    else:
        with st.spinner("Reading your resume and thinking hard..."):
            resume_text = extract_text_from_pdf(resume_file)
            time.sleep(1)  # Just for effect 😎
            result = query_openrouter(resume_text, job_desc)

        st.markdown("---")
        st.markdown("### 🧠 AI Feedback")
        st.success("Here's what the model thinks:")
        st.write(result)

        # Optional: expandable for raw resume/job text
        with st.expander("📄 View Parsed Resume Text"):
            st.code(resume_text[:2000], language="markdown")

        with st.expander("💼 View Job Description"):
            st.code(job_desc, language="markdown")

# 📝 Footer
st.markdown("""
<hr>
<p style='text-align: center; font-size: 14px;'>
Built using Python, Streamlit, and OpenRouter.<br>
<a href="https://github.com/tiloschankarki/Resume-Screener" target="_blank">View on GitHub</a>
</p>
""", unsafe_allow_html=True)
