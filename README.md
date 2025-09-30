# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/)

A minimal, **production‑ready** reference implementation of a chatbot built on **[LangChain](https://github.com/langchain-ai/langchain)** that demonstrates **Retrieval‑Augmented Generation (RAG)**.  The bot can answer questions over a private knowledge base, combine LLM reasoning with vector‑store retrieval, and is packaged for easy extension and contribution.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start (Local)](#quick-start-local)
- [Running with Docker / Docker‑Compose](#running-with-docker--docker-compose)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LangChain** pipelines for LLM calls, prompt templates and memory.
- **RAG** using a vector store (FAISS, Chroma, Pinecone, etc.)
- Support for **multiple LLM providers** (OpenAI, Anthropic, Ollama, etc.)
- **Streaming** responses via WebSocket / SSE.
- **Dockerised** development and production images.
- Clear separation of **core logic**, **API layer**, and **infrastructure**.
- Extensible **plugin system** for custom retrievers, document loaders, and post‑processing.

---

## Architecture Overview

```
+-------------------+      +-------------------+      +-------------------+
|   FastAPI /       | ---> |   LangChain       | ---> |   Vector Store    |
|   WebSocket API   |      |   (LLM + Retriever)      (FAISS/Chroma)   |
+-------------------+      +-------------------+      +-------------------+
        ^                         ^                         ^
        |                         |                         |
        |   +-----------------+   |   +-----------------+   |
        +---|   Front‑end UI   |---+---|   Document      |---+---
            (React/Vue/etc.)      |   Loaders       |
                                    +-----------------+
```

- **API Layer** – FastAPI serves HTTP endpoints and a WebSocket for streaming token‑by‑token output.
- **LangChain Core** – PromptTemplate → LLM → Retriever → Rerank → Combine → Output.
- **Vector Store** – Stores embeddings generated from your document collection; interchangeable via LangChain adapters.
- **Front‑end** – Optional UI (not part of the core repo) can be plugged in via the WebSocket endpoint.

---

## Quick Start (Local)

### Prerequisites

- Python **3.9+**
- An LLM API key (e.g., `OPENAI_API_KEY`).
- Optional: `docker` & `docker‑compose` if you prefer containerised execution.

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot
```

### 2️⃣ Create a virtual environment and install dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

### 3️⃣ Set environment variables

Create a `.env` file at the project root (or export variables manually). Example:

```dotenv
# .env
OPENAI_API_KEY=sk-************************
LANGCHAIN_TRACING_V2=true   # optional LangChain tracing
LANGCHAIN_API_KEY=your_langchain_api_key
VECTOR_STORE=faiss           # faiss | chroma | pinecone
EMBEDDING_MODEL=text-embedding-ada-002
```

### 4️⃣ Index your knowledge base

Place the documents you want the bot to know about in the `data/` folder (supported formats: `.txt`, `.pdf`, `.md`). Then run:

```bash
python scripts/index_documents.py
```

The script will:
1. Load files via LangChain document loaders.
2. Split them into chunks.
3. Compute embeddings using the configured model.
4. Persist the vector store under `vector_store/`.

### 5️⃣ Start the API server

```bash
uvicorn app.main:app --reload
```

The chatbot is now reachable at `http://localhost:8000`.  Use the `/chat` endpoint (POST JSON) or the WebSocket at `/ws/chat` for streaming.

---

## Running with Docker / Docker‑Compose

The repo includes a **multi‑stage Dockerfile** and a `docker-compose.yml` that wires the API with a persistent volume for the vector store.

```bash
# Build the image
docker compose build

# Start the services (API + optional Redis for rate‑limiting)
docker compose up -d
```

Environment variables can be overridden in `docker-compose.override.yml` or via the CLI:

```bash
docker compose run --rm app python scripts/index_documents.py
```

---

## Configuration

All runtime configuration is read from environment variables (via `pydantic.BaseSettings`).  Key variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | API key for OpenAI models | – |
| `LLM_PROVIDER` | `openai`, `anthropic`, `ollama` … | `openai` |
| `LLM_MODEL` | Model name (e.g., `gpt-4o-mini`) | provider‑specific default |
| `VECTOR_STORE` | Vector store backend (`faiss`, `chroma`, `pinecone`) | `faiss` |
| `EMBEDDING_MODEL` | Embedding model identifier | `text-embedding-ada-002` |
| `TOP_K` | Number of retrieved documents per query | `4` |
| `RERANKER` | Optional reranker model name | – |
| `STREAMING` | Enable token‑wise streaming (`true`/`false`) | `true` |

You can also provide a **YAML** config file (`config.yaml`) and point to it with `CONFIG_PATH`.

---

## Usage Examples

### Simple HTTP request

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Comment fonctionne le système de récupération de documents ?"}'
```

Response:

```json
{
  "answer": "Le système utilise un vecteur store …",
  "sources": ["data/faq.pdf (page 3)", "data/manual.txt (line 42)"]
}
```

### Streaming via WebSocket (Python client)

```python
import websockets, json, asyncio

async def chat():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"question": "Quelles sont les limites du modèle ?"}))
        async for message in ws:
            data = json.loads(message)
            print(data["token"], end="", flush=True)

asyncio.run(chat())
```

---

## Testing

The repository ships with **pytest** tests covering:
- Document loaders and chunking.
- Vector‑store indexing and retrieval.
- End‑to‑end API calls (including streaming).

Run the test suite with:

```bash
pytest -vv
```

Coverage reports can be generated via `pytest-cov`:

```bash
pytest --cov=app
```

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository and clone your fork.
2. Create a feature branch: `git checkout -b feat/your‑feature`.
3. Install the development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Ensure code style with **ruff** and **black**:
   ```bash
   ruff check . && ruff format .
   ```
5. Add or update tests.
6. Run the full test suite and confirm coverage does not drop.
7. Submit a **Pull Request** with a clear description of the change.

### Code of Conduct

We adhere to the Contributor Covenant Code of Conduct. By participating, you agree to uphold a welcoming and inclusive environment.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **LangChain** – the backbone for LLM orchestration.
- **FAISS / Chroma** – vector store back‑ends.
- **OpenAI** – for the powerful LLM and embedding models used in the reference implementation.

Feel free to open an issue for bugs, feature requests, or general questions. Happy building! 🎉