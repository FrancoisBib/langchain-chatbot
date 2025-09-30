# LangChain‑Chatbot

**A modular, Retrieval‑Augmented Generation (RAG) chatbot built on LangChain**

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Quick Start](#quick-start)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

`langchain-chatbot` demonstrates how to combine **LangChain**, a large language model (LLM), and a vector store to build a **RAG‑enabled conversational agent**. The bot retrieves relevant documents from a knowledge base, augments the LLM prompt with those passages, and returns a context‑aware answer.

The repository is intentionally lightweight so you can focus on the **core RAG pipeline** while still having a fully functional FastAPI‑based chat interface.

---

## Features

- **LangChain integration** – leverages `ChatOpenAI`, `ConversationalRetrievalChain` and custom memory.
- **Pluggable vector stores** – default uses `FAISS`; adapters for `Chroma`, `Pinecone`, `Weaviate`, etc.
- **Document ingestion** – supports plain text, PDFs and Markdown via LangChain loaders.
- **Streaming responses** – FastAPI endpoint streams tokens for a smooth UI experience.
- **Docker ready** – `docker-compose.yml` bundles the API, a vector store, and an optional UI.
- **Extensible** – clear separation of concerns (loader, retriever, chain, API) for easy contribution.

---

## Architecture

```
+-----------------+      +-------------------+      +-------------------+
|   Document      | ---> |   Chunk + Embed   | ---> |   Vector Store    |
|   Loader(s)     |      |   (FAISS)         |      |   (FAISS)         |
+-----------------+      +-------------------+      +-------------------+
        ^                         ^                         ^
        |                         |                         |
        |                         |                         |
        |                         |                         |
        |                         |                         |
+-----------------+      +-------------------+      +-------------------+
|   FastAPI       | <--- |   RetrievalChain  | <--- |   LLM (ChatOpenAI) |
|   Endpoint      |      |   (RAG)           |      |   (gpt‑4o)        |
+-----------------+      +-------------------+      +-------------------+
```

1. **Ingestion** – Documents are loaded, split into chunks, and embedded with the chosen embedding model.
2. **Vector Store** – Embeddings are persisted in a local FAISS index (or any compatible store).
3. **Retrieval** – At query time a similarity search returns the top‑k relevant passages.
4. **RAG Chain** – The retrieved passages are injected into the LLM prompt via LangChain’s `ConversationalRetrievalChain`.
5. **API** – The FastAPI endpoint streams the generated answer back to the client.

---

## Prerequisites

- Python **3.10+**
- An OpenAI API key (or compatible LLM endpoint)
- (Optional) Docker & Docker‑Compose for containerised development

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### With Docker (recommended for quick start)

```bash
docker compose up --build
```

The API will be exposed at `http://localhost:8000` and the optional UI at `http://localhost:3000`.

---

## Configuration

Create a `.env` file at the project root:

```dotenv
# .env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
# Choose the embedding model – default is text-embedding-ada-002
EMBEDDING_MODEL=text-embedding-ada-002
# LLM model (e.g., gpt-4o, gpt-3.5-turbo)
LLM_MODEL=gpt-4o
# Number of retrieved documents per query
TOP_K=4
```

The `settings.py` module loads these variables via `python‑dotenv`.

---

## Quick Start

1. **Load documents** (run once to build the index):
   ```bash
   python scripts/ingest.py data/knowledge-base/
   ```
   This will create a `faiss_index` directory containing the vector store.

2. **Start the API**:
   ```bash
   uvicorn app.main:app --reload
   ```
   The endpoint `POST /chat` expects a JSON payload:
   ```json
   {"question": "Your question here", "chat_history": []}
   ```

3. **Interact via cURL** (or any HTTP client):
   ```bash
   curl -X POST http://localhost:8000/chat \
        -H "Content-Type: application/json" \
        -d '{"question": "Explain RAG in simple terms", "chat_history": []}'
   ```

---

## Usage Examples

### Basic Python client

```python
import httpx

api_url = "http://localhost:8000/chat"
payload = {"question": "What is LangChain?", "chat_history": []}

response = httpx.post(api_url, json=payload, timeout=60)
print(response.json()["answer"])  # streamed answer as a single string
```

### Streamed response (async)

```python
import httpx, asyncio

async def ask(question: str):
    async with httpx.AsyncClient() as client:
        async for line in client.stream("POST", "http://localhost:8000/chat", json={"question": question, "chat_history": []}):
            print(line.text, end="")

asyncio.run(ask("How does retrieval‑augmented generation work?"))
```

---

## Testing

```bash
# Run unit tests
pytest -v
```

The test suite covers:
- Document ingestion and chunking
- Vector‑store creation and similarity search
- End‑to‑end RAG chain execution (mocked LLM)

---

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write tests for new functionality.
4. Ensure `black`, `isort` and `flake8` pass (`make lint`).
5. Open a Pull Request with a clear description of the change.

Please adhere to the **PEP 8** style guide and keep the documentation up‑to‑date.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- **LangChain** – for the powerful abstractions that make RAG pipelines straightforward.
- **OpenAI** – for the LLM and embedding models used in the examples.
- **FAISS** – for fast similarity search.

---
