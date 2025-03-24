import os
import streamlit as st
import google.generativeai as genai

# Configure Gemini 
GOOGLE_API_KEY = "your_api_key"
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro')

#  Write Page Config 
st.set_page_config(page_title="ResumeBot", page_icon="📝", layout="wide")

st.title("📝 ResumeBot app")
st.write("Generate a polished resume with AI ✨")

#  Session State for Resume ---
if 'resume_text' not in st.session_state:
    st.session_state.resume_text = ""

# Write a Form Layout 
col1, col2 = st.columns(2)
with st.form("resume_form"):
    with col1:
        name = st.text_input("👤 Your Name")
        job_role = st.text_input("💼 Job Role")
        skills = st.text_area("🧰 Skills (comma-separated)")
    with col2:
        experience = st.text_area("📈 Experience")
        education = st.text_area("🎓 Education")

    submitted = st.form_submit_button("🚀 Generate Resume")

if submitted:
    if name and job_role:
        with st.spinner("Generating resume..."):
            prompt = f"""
You are ResumeBot. Generate a professional resume based on the following details:

Name: {name}
Job Role: {job_role}
Experience: {experience}
Skills: {skills}
Education: {education}


Output the resume in a clean, structured format with headings.
"""
            try:
                response = model.generate_content(prompt)
                st.session_state.resume_text = response.text
                st.success("✅ Resume Generated!")
            except Exception as e:
                st.error(f"❌ Error generating resume: {e}")
    else:
        st.warning("⚠️ Please provide at least your name and job role.")

if st.session_state.resume_text:
    st.markdown("### 📄 Resume Preview")
    st.code(st.session_state.resume_text, language="markdown")

    st.download_button(
        label="💾 Download as Text",
        data=st.session_state.resume_text,
        file_name=f"{name}_resume.txt",
        mime="text/plain"
    )


st.markdown("---")
st.caption("Made with ❤️ by Varad | Powered by Gen AI Developer❤️ ")
