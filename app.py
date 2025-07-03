'''import streamlit as st  # type: ignore
from backend.loader import load_pdf
from backend.rag_engine import generate_answer

st.set_page_config(page_title="DocuChat 💬", layout="centered")

st.title("📄 DocuChat")
st.subheader("Upload a PDF and ask questions about it using AI 🤖")

# Upload the PDF
uploaded_file = st.file_uploader("📤 Upload your PDF file", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF uploaded successfully!")

    # Read the PDF text using loader.py
    with st.spinner("📖 Reading the PDF..."):
        text = load_pdf(uploaded_file)

    # Input box for asking questions
    question = st.text_input("❓ Ask a question about the document:")

    if question:
        with st.spinner("🤔 Thinking..."):
            answer = generate_answer(text, question)
            st.success("💬 Answer:")
            st.write(answer)'''

from dotenv import load_dotenv
load_dotenv()


import streamlit as st  # type: ignore
from backend.loader import load_pdf
from backend.rag_engine import generate_answer
import os

st.set_page_config(page_title="DocuChat 💬", layout="centered")

st.title("📄 DocuChat")
st.subheader("Upload a PDF and ask questions about it using AI 🤖")

# Upload the PDF
uploaded_file = st.file_uploader("📤 Upload your PDF file", type=["pdf"])

if uploaded_file:
    st.success("✅ PDF uploaded successfully!")
    
    st.info("🔍 Starting to read PDF...")  # Debug line
    with st.spinner("📖 Reading the PDF..."):
        try:
            text = load_pdf(uploaded_file)
            st.success("📚 PDF read successfully!")
        except Exception as e:
            st.error(f"❌ Error while reading PDF: {e}")
            st.stop()

    # Input box for asking questions
    question = st.text_input("❓ Ask a question about the document:")

    if question:
        with st.spinner("🤔 Thinking..."):
            try:
                # Warn if API key is not set
                if not os.getenv("HF_API_KEY"):
                    st.warning("⚠️ Hugging Face API key not set. Please set the HF_API_KEY environment variable for cloud inference.")
                answer = generate_answer(text, question)
                st.success("💬 Answer:")
                st.write(answer)
            except Exception as e:
                st.error(f"❌ Error while generating answer: {e}")
