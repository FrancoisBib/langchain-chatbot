# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

## 📖 Overview

`langchain-chatbot` is a minimal yet production‑ready reference implementation of a **chatbot built on LangChain** that leverages **Retrieval‑Augmented Generation (RAG)**.  The bot combines a large language model (LLM) with a vector store for document retrieval, enabling it to answer questions with up‑to‑date, domain‑specific knowledge while keeping the interaction natural and conversational.

The repository demonstrates:
- Integration of LangChain components (LLM, PromptTemplate, RetrievalChain, Memory, etc.)
- Flexible configuration for different LLM providers (OpenAI, Anthropic, Ollama, …)
- Plug‑and‑play vector stores (FAISS, Chroma, Pinecone, Weaviate)
- A simple FastAPI/Flask web UI and a CLI for rapid prototyping
- Testing utilities and CI‑ready Docker setup

> **Why RAG?**
> Retrieval‑Augmented Generation lets the model ground its responses in external knowledge sources, reducing hallucinations and allowing you to keep the knowledge base up‑to‑date without retraining the model.

---

## 🚀 Getting Started

### Prerequisites
- Python **3.9** or newer
- An LLM API key (e.g., `OPENAI_API_KEY` for OpenAI models) – see the *Configuration* section below
- (Optional) Docker if you prefer containerised execution

### Installation
```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Quick Start (CLI)
```bash
# Load a sample knowledge base (FAISS index) and start an interactive session
python -m chatbot.cli --index data/faiss_index.pkl
```
Type your question and watch the bot retrieve relevant passages before generating a response.

### Quick Start (Web UI)
```bash
# Run the FastAPI server
uvicorn chatbot.api:app --reload
```
Open <http://127.0.0.1:8000/docs> for the automatic Swagger UI or navigate to <http://127.0.0.1:8000> for the bundled React front‑end (if enabled).

---

## 🛠️ Project Structure
```
langchain-chatbot/
├─ chatbot/                     # Core package
│   ├─ __init__.py
│   ├─ llm.py                   # LLM wrapper (OpenAI, Anthropic, etc.)
│   ├─ retriever.py             # Vector store abstraction & loaders
│   ├─ chain.py                 # Retrieval‑augmented generation chain
│   ├─ memory.py                # Conversation memory utilities
│   ├─ api.py                   # FastAPI endpoints
│   └─ cli.py                   # Command‑line interface
├─ data/                        # Sample documents & pre‑built indexes
├─ tests/                       # PyTest suite
├─ Dockerfile
├─ requirements.txt
├─ pyproject.toml
└─ README.md
```

---

## ⚙️ Configuration

Configuration is handled via environment variables or a `.env` file (supported by `python‑dotenv`). The most common settings are:

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_PROVIDER` | Which provider to use (`openai`, `anthropic`, `ollama`, …) | `openai` |
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-*****` |
| `VECTOR_STORE` | Vector DB backend (`faiss`, `chroma`, `pinecone`, `weaviate`) | `faiss` |
| `FAISS_INDEX_PATH` | Path to a persisted FAISS index (if using FAISS) | `data/faiss_index.pkl` |
| `TOP_K` | Number of retrieved documents per query | `4` |
| `TEMPERATURE` | LLM temperature | `0.7` |

Create a `.env` file at the project root:
```dotenv
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-************************
VECTOR_STORE=faiss
FAISS_INDEX_PATH=data/faiss_index.pkl
TOP_K=4
TEMPERATURE=0.7
```
The `settings.py` module loads these values and provides sensible defaults.

---

## 📚 Usage Guide

### 1️⃣ Preparing a Knowledge Base
The repo includes a small example dataset (PDFs, Markdown files). To index your own documents:
```python
from chatbot.retriever import DocumentLoader, VectorStoreFactory

# Load raw documents (supports .txt, .pdf, .md, .docx)
loader = DocumentLoader(source_path="./my_docs")
documents = loader.load()

# Create a vector store (FAISS shown, but you can swap the backend)
vector_store = VectorStoreFactory.create(
    backend="faiss",
    embedding_model="text-embedding-ada-002",  # OpenAI embeddings
)
vector_store.add_documents(documents)
vector_store.persist("data/my_faiss_index.pkl")
```

### 2️⃣ Running the RAG Chain
```python
from chatbot.chain import RetrievalAugmentedGenerationChain
from chatbot.llm import LLMFactory
from chatbot.retriever import VectorStoreFactory

# Initialise components
llm = LLMFactory.create(provider="openai", temperature=0.0)
vector_store = VectorStoreFactory.load("faiss", "data/my_faiss_index.pkl")
rag_chain = RetrievalAugmentedGenerationChain(llm=llm, retriever=vector_store.as_retriever(k=4))

# Ask a question
answer = rag_chain.run("What are the main security considerations for deploying LangChain?")
print(answer)
```
The chain performs:
1. **Retrieval** – fetches the top‑k most relevant passages.
2. **Prompt construction** – injects retrieved snippets into a system prompt.
3. **Generation** – calls the LLM to produce a grounded answer.

### 3️⃣ Adding Memory (Optional)
For multi‑turn conversations, wrap the chain with a memory buffer:
```python
from chatbot.memory import ConversationBufferMemory

memory = ConversationBufferMemory(k=5)  # keep last 5 exchanges
rag_chain = rag_chain.with_memory(memory)
```
The memory is automatically added to the prompt, allowing the model to reference prior turns.

---

## 🧪 Testing
```bash
# Run the full test suite
pytest -vv
```
The tests cover:
- Document loading & chunking
- Vector store indexing & similarity search
- End‑to‑end RAG pipeline with a mock LLM
- API endpoint contracts

---

## 📦 Deployment
The project can be containerised with the provided `Dockerfile`:
```bash
# Build the image
docker build -t langchain-chatbot .

# Run the container (environment variables can be passed via -e)
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -e VECTOR_STORE=faiss \
  -e FAISS_INDEX_PATH=/app/data/faiss_index.pkl \
  langchain-chatbot
```
For production, consider:
- Using a managed vector DB (Pinecone, Weaviate) for scalability.
- Enabling HTTPS behind a reverse proxy.
- Adding rate‑limiting / authentication middleware.

---

## 🤝 Contributing
We welcome contributions! Please follow these steps:
1. **Fork** the repository.
2. **Create a feature branch** (`git checkout -b feat/your-feature`).
3. Write **tests** for new functionality.
4. Ensure **code style** with `ruff`/`black` (`make lint`).
5. Submit a **Pull Request** with a clear description of the change.

See `CONTRIBUTING.md` for detailed guidelines, coding standards, and the review process.

---

## 📄 License
This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## 📚 Further Reading
- LangChain Documentation: https://python.langchain.com/
- Retrieval‑Augmented Generation Primer: https://arxiv.org/abs/2005.11401
- OpenAI Embeddings Guide: https://platform.openai.com/docs/guides/embeddings

---

*Happy hacking with LangChain!*