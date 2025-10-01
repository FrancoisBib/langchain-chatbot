# LangChain Chatbot

A **LangChain** based chatbot framework that demonstrates Retrieval‑Augmented Generation (RAG) for building powerful, context‑aware conversational agents.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Demo](#running-the-demo)
- [Usage Guide](#usage-guide)
  - [Creating a Custom Bot](#creating-a-custom-bot)
  - [Adding New Knowledge Sources](#adding-new-knowledge-sources)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Retrieval‑Augmented Generation (RAG)**: Combine LLM generation with a vector store for up‑to‑date, domain‑specific knowledge.
- **Modular design**: Swap out LLM providers, vector stores, or document loaders with minimal code changes.
- **Prompt engineering utilities**: Pre‑built prompt templates for chat, QA, and summarisation.
- **Extensible**: Easy to add new document types (PDF, DOCX, CSV, etc.) and custom preprocessing pipelines.
- **Docker ready**: Containerised setup for reproducible environments.

---

## Architecture Overview

```
+-------------------+       +-------------------+       +-------------------+
|   User Interface  | <---> |   LangChain Core  | <---> |   Vector Store    |
+-------------------+       +-------------------+       +-------------------+
        ^                              ^                         ^
        |                              |                         |
        |                +---------------------------+            |
        +----------------|   LLM (OpenAI / Anthropic) |------------+
                         +---------------------------+
```

- **User Interface** – Simple FastAPI endpoint (or Streamlit UI) that forwards user messages.
- **LangChain Core** – Chains, agents, and memory handling that orchestrate retrieval and generation.
- **Vector Store** – FAISS, Chroma, or Pinecone store for embeddings generated from your knowledge base.
- **LLM** – Any LangChain‑compatible large language model (OpenAI, Anthropic, Llama‑Cpp, etc.).

---

## Getting Started

### Prerequisites

- Python **3.9+**
- Poetry or pip for dependency management
- An OpenAI API key (or another LLM provider key) – set as `OPENAI_API_KEY` in your environment.
- (Optional) Docker & Docker‑Compose if you prefer containerised execution.

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Install dependencies (using Poetry)
poetry install
# Or with pip
pip install -r requirements.txt
```

### Running the Demo

```bash
# Load sample documents and start the API server
poetry run python scripts/setup_vectorstore.py   # ingest docs into FAISS
poetry run uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` to interact with the OpenAPI UI or connect your front‑end client.

---

## Usage Guide

### Creating a Custom Bot

1. **Define your document loader** – LangChain provides loaders for many formats. Example for a local PDF folder:

```python
from langchain.document_loaders import PyPDFLoader
from pathlib import Path

def load_pdfs(folder: Path):
    docs = []
    for pdf_path in folder.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf_path))
        docs.extend(loader.load())
    return docs
```

2. **Generate embeddings and populate the vector store**:

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("vectorstore")
```

3. **Build the RAG chain**:

```python
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI

retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    retriever=retriever,
    return_source_documents=True,
)
```

4. **Expose via FastAPI** (simplified):

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: Query):
    result = qa_chain(query.question)
    return {"answer": result["result"], "sources": [doc.metadata["source"] for doc in result["source_documents"]]}
```

### Adding New Knowledge Sources

- **Web pages** – Use `langchain.document_loaders.WebBaseLoader` or `BeautifulSoup`‑based custom loaders.
- **CSV/TSV** – `langchain.document_loaders.CSVLoader` with optional column selection.
- **APIs** – Implement a loader that fetches data from an external API and returns `Document` objects.

After adding a loader, re‑run `scripts/setup_vectorstore.py` to refresh the index.

---

## Project Structure

```
langchain-chatbot/
│
├─ app/                     # FastAPI application (endpoints, dependency injection)
│   ├─ main.py              # Entry point for uvicorn
│   └─ routes.py            # API route definitions
│
├─ bots/                    # Example bot configurations
│   └─ rag_chatbot.py       # Pre‑configured RAG chain used by the demo
│
├─ scripts/                 # Utility scripts (data ingestion, index rebuild)
│   └─ setup_vectorstore.py # Loads docs, creates embeddings, stores FAISS index
│
├─ tests/                   # Unit and integration tests
│   └─ test_chatbot.py
│
├─ requirements.txt         # Pip‑compatible dependencies (for non‑Poetry users)
├─ pyproject.toml           # Poetry configuration
└─ README.md                # ← This file
```

---

## Contributing

Contributions are welcome! Follow these steps:

1. **Fork the repository** and clone your fork.
2. Create a **feature branch** (`git checkout -b feat/your-feature`).
3. Keep the code style consistent – we use **Black** and **isort**.
4. Add or update tests for new functionality.
5. Run the full test suite:
   ```bash
   poetry run pytest
   ```
6. Open a **Pull Request** with a clear description of the change.

Please see `CONTRIBUTING.md` for detailed guidelines on coding standards, commit messages, and release process.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.
