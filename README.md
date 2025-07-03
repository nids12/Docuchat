# 📄 DocuChat

DocuChat is an AI-powered chatbot that lets you upload any PDF and ask questions in natural language. It uses Hugging Face models and Retrieval-Augmented Generation (RAG) to understand the content and provide accurate answers.

## 🚀 Features

- Upload and parse any PDF
- Ask questions in natural language
- Get smart, accurate answers based on document content
- Built with LangChain, FAISS, Hugging Face, and Streamlit
- No OpenAI needed — works with free Hugging Face models

## 🛠️ Tech Stack

- LLM: Hugging Face `flan-t5-base`
- Embeddings: `sentence-transformers/all-MiniLM-L6-v2`
- RAG: LangChain + FAISS
- Frontend: Streamlit
- PDF Parsing: PyMuPDF
- Secrets: Managed via `.env` file (excluded from Git)

## 📂 Folder Structure

docuchat/  
├── backend/  
│ ├── loader.py → handles PDF text extraction  
│ └── rag_engine.py → handles vector search & answer generation  
├── app.py → Streamlit frontend  
├── check_gemini.py → Gemini API checker (optional)  
├── testapp.py → test app  
├── requirements.txt → dependencies  
├── .env → secret keys (not pushed to GitHub)  
├── .gitignore → excluded files/folders  
└── README.md → project documentation

## 💻 How to Run Locally

1. Clone the repo:  
   `git clone https://github.com/nids12/Docuchat.git && cd Docuchat`
2. (Optional) Create virtual environment:  
   `python -m venv venv && venv\Scripts\activate` (Windows)
3. Install dependencies:  
   `pip install -r requirements.txt`
4. Create a `.env` file and add:  
   `GOOGLE_API_KEY=your_api_key_here`
5. Start the app:  
   `streamlit run app.py`

## ✅ Status

- Works locally without OpenAI
- Good for interview demos and resume projects
- Simple, clean UI using Streamlit

## 🙋 Made By

Created with ❤️ by Nidhi Sarda  
GitHub: [nids12](https://github.com/nids12)
