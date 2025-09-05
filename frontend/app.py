import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="QuizLLM", layout="wide")

st.title("📘 QuizLLM - NCERT Quiz Generator")

tab1, tab2 = st.tabs(["📂 Upload NCERT PDF", "📝 Generate Quiz"])

with tab1:
    st.header("Upload NCERT PDF")
    uploaded_file = st.file_uploader("Upload NCERT PDF", type=["pdf"])
    if uploaded_file:
        if st.button("Ingest & Build Index"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
            res = requests.post(f"{API_URL}/ingest/upload", files=files)
            if res.status_code == 200:
                st.success(res.json())
            else:
                st.error(f"Error {res.status_code}: {res.text}")

with tab2:
    st.header("Generate Quiz")
    topic = st.text_input("Enter topic or chapter name:")
    num_q = st.slider("Number of questions", 1, 10, 5)
    if st.button("Generate Quiz"):
        payload = {"topic": topic, "num_questions": num_q}
        res = requests.post(f"{API_URL}/quiz", json=payload)
        if res.status_code == 200:
            data = res.json()
            st.subheader("Quiz")
            for i, q in enumerate(data.get("questions", []), start=1):
                st.markdown(f"**Q{i}.** {q}")
        else:
            st.error(f"Error {res.status_code}: {res.text}")
