from dotenv import load_dotenv
load_dotenv()
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.chains import RetrievalQA
import requests
import os


def generate_answer(text, query):
    # 1. Split PDF text into chunks
    splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.split_text(text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    # 2. Create vector store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(docs, embeddings)
    retriever = vectordb.as_retriever()

    # 3. Retrieve relevant chunks (using invoke, not deprecated method)
    summary_keywords = ["what is the pdf about", "summarize", "summary", "main topic", "main idea", "describe the document", "overview"]
    if any(kw in query.lower() for kw in summary_keywords):
        # For summary-type questions, use only the first 512 tokens (words) as context to avoid model limits
        max_tokens = 512
        words = text.split()
        if len(words) > max_tokens:
            context = ' '.join(words[:max_tokens])
        else:
            context = text
        prompt = f"""
You are a helpful assistant. Read the following document and provide a concise summary or main topic in 2-3 sentences.

Document:
{context}
"""
    else:
        relevant_docs = retriever.invoke(query)
        context = "\n\n".join(doc.page_content for doc in relevant_docs)
        prompt = f"""
You are a helpful assistant. Use the context below to answer the user's question. Be brief and clear.

Context:
{context}

User's question: {query}
"""

    # 5. Try regex-based extraction for student name if question is about name
    import re
    if "name" in query.lower() and "student" in query.lower():
        # Try to find a line like 'Name: ...' or similar
        name_match = re.search(r"name\s*[:\-]?\s*([A-Za-z .]+)", text, re.IGNORECASE)
        if name_match:
            return name_match.group(1).strip()
        # Try to find a line with 'of student' or similar
        student_match = re.search(r"([A-Z][A-Za-z .]+)\s+student", text)
        if student_match:
            return student_match.group(1).strip()

    # 6. Use Hugging Face Inference API for general QA
    def hf_inference_api(prompt, model="facebook/bart-large-cnn"):
        api_key = os.getenv("HF_API_KEY")
        if not api_key:
            raise ValueError("Hugging Face API key not set. Please set HF_API_KEY environment variable.")
        url = f"https://api-inference.huggingface.co/models/{model}"
        headers = {"Authorization": f"Bearer {api_key}"}
        payload = {"inputs": prompt}
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        # Try to extract generated text
        if isinstance(result, list) and len(result) > 0:
            if "generated_text" in result[0]:
                return result[0]["generated_text"]
            elif "summary_text" in result[0]:
                return result[0]["summary_text"]
            elif "output" in result[0]:
                return result[0]["output"]
            else:
                return str(result[0])
        return str(result)

    # 7. Run the prompt through the Hugging Face Inference API
    result = hf_inference_api(prompt, model="facebook/bart-large-cnn")
    return result
