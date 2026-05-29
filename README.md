# DocuChat 🔍
> Query your PDF documents in plain English using RAG — semantic search that actually understands what you're asking.

**Stack:** FastAPI · Qdrant · SentenceTransformers · Ollama · AWS  
**Status:** [Demo Link](#) · [Repo](#)

---

## What it does

DocuChat lets you upload PDF documents and ask questions about them in natural language. Instead of Ctrl+F for keywords, you describe what you're looking for and the system finds semantically relevant content — even if the exact words don't match.

Built on a Retrieval-Augmented Generation (RAG) pipeline: documents are chunked, embedded into vectors, stored in Qdrant, and retrieved by semantic similarity at query time before being passed to an LLM for the final answer.

---

## Why RAG (not just "send the whole PDF to an LLM")

The naive approach — dump the entire document into an LLM prompt — breaks for large documents (context limits) and is expensive per query. RAG solves this by:

1. Preprocessing documents into searchable vector chunks (done once)
2. At query time, retrieving only the *relevant* chunks (fast, cheap)
3. Sending just those chunks + the question to the LLM

The result is faster responses, lower cost, and better accuracy because the LLM sees focused relevant context rather than noise.

---

## Architecture

```
PDF Upload
    │
    ▼
Document Processor
    ├── Text extraction
    ├── Chunking (overlapping windows)
    └── Embedding (SentenceTransformers all-MiniLM)
    │
    ▼
Qdrant Vector DB
    └── Stores vectors + metadata (source doc, chunk position)

Query Flow:
User Question → Embed query → Similarity search in Qdrant
    → Top-K relevant chunks → Ollama LLM → Answer
    │
    ▼
FastAPI Backend
    ├── Upload endpoint
    ├── Query endpoint
    └── Chat history storage (AWS)
```

---

## Key Features

- **Semantic search** — finds relevant content even when exact keywords don't match
- **Multi-document support** — upload multiple PDFs, query across all of them
- **Chat history** — conversations are persisted, so context carries across questions
- **1K+ chunk search** — fast similarity search across large document collections
- **Local LLM via Ollama** — runs entirely locally, no API costs

---

## Technical Highlights

**Chunking strategy**  
Documents are split into overlapping chunks (not hard cuts at N characters). Overlap ensures that relevant information spanning a chunk boundary isn't split in a way that loses context during retrieval.

**Embedding model choice**  
Used `all-MiniLM-L6-v2` — a strong balance of speed and quality for semantic similarity. Smaller than BERT-large but performs well for retrieval tasks and runs fast enough for real-time queries.

**Qdrant for vector storage**  
Qdrant handles approximate nearest-neighbor search efficiently. Each vector is stored with metadata (source document, page number, chunk index) so retrieved results can be traced back to their origin.

**Retrieval accuracy**  
Achieved ~40% improvement in relevant document retrieval compared to simple keyword search on the same test queries — measured by whether the correct source chunk appeared in the top-3 results.

---

## Running Locally

**Prerequisites:** Python 3.9+, Ollama installed, Qdrant running

```bash
# Start Qdrant (Docker)
docker run -p 6333:6333 qdrant/qdrant

# Start Ollama with a model
ollama pull llama2

# Clone and set up
git clone https://github.com/nids12/Docuchat.git
cd Docuchat
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Set Qdrant host, Ollama endpoint, AWS credentials

# Run
uvicorn main:app --reload
```

API docs at `http://localhost:8000/docs`

---

## What I learned

RAG sounds simple in theory but the details matter a lot in practice — chunk size, overlap, embedding model choice, and how you format the retrieval context for the LLM all affect answer quality significantly. Also learned a lot about vector databases and approximate nearest-neighbor search, which is a genuinely interesting problem.

The hardest part was making the retrieval accurate enough that wrong answers (hallucinations from irrelevant context) were rare. The overlap chunking strategy helped significantly.

---

## Possible Improvements

- [ ] Re-ranking layer (cross-encoder) to improve retrieval precision
- [ ] Support for more file types (Word, txt, HTML)
- [ ] Streaming responses for faster perceived latency
- [ ] Multi-user isolation (currently shares vector space)

---

*Built by [Nidhi Sarda](https://github.com/nids12)*
