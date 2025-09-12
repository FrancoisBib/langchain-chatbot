# LangChain‑Chatbot

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a Retrieval‑Augmented Generation (RAG) chatbot built on top of **[LangChain](https://github.com/langchain-ai/langchain)**.  It demonstrates how to combine LLMs, vector stores, and document loaders to create a conversational AI that can answer questions using your own knowledge base.

---

## Table of Contents

1. [Features](#features)
2. [Architecture Overview](#architecture-overview)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Quick Start](#quick-start)
7. [Running the Bot](#running-the-bot)
8. [Testing](#testing)
9. [Extending & Contributing](#extending--contributing)
10. [License](#license)

---

## Features

- **RAG pipeline**: Retrieve relevant documents from a vector store and generate answers with an LLM.
- **Modular design**: Swap out document loaders, vector stores, embeddings, or LLMs with a single line change.
- **Streaming responses**: Optional streaming via LangChain callbacks.
- **Docker support**: Official Dockerfile for reproducible environments.
- **CI workflow**: GitHub Actions run unit tests and linting on every push.
- **Extensive type hints** and docstrings for easy IDE navigation.

---

## Architecture Overview

```mermaid
flowchart LR
    subgraph User
        UI[Web UI / CLI]
    end
    subgraph Bot
        LLM[LLM (e.g., OpenAI, Ollama)]
        Retriever[VectorStore Retriever]
        Docs[Document Loader]
        Embeddings[Embedding Model]
    end
    UI -->|question| Bot
    Bot -->|retrieve| Retriever
    Retriever -->|vectors| Embeddings
    Docs -->|chunks| Embeddings
    Retriever -->|relevant docs| LLM
    LLM -->|answer| UI
```

1. **Document ingestion** – `scripts/ingest.py` loads files (PDF, TXT, Markdown, etc.) and splits them into chunks.
2. **Embedding** – Chunks are embedded with the configured embedding model (OpenAI, HuggingFace, etc.) and stored in a vector store (FAISS, Chroma, Pinecone, …).
3. **Retrieval** – At query time the retriever fetches the top‑k most similar chunks.
4. **Generation** – The LLM receives the retrieved context and the user query to produce a grounded answer.

---

## Prerequisites

| Requirement | Minimum version |
|-------------|-----------------|
| Python      | 3.9             |
| pip         | 22.0            |
| Docker (optional) | 20.10 |
| OpenAI API key (or alternative LLM credentials) | – |

---

## Installation

### Using `pip`
```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install the package and development dependencies
pip install -e .[dev]
```

### Using Docker
```bash
docker build -t langchain-chatbot:latest .
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8000:8000 langchain-chatbot:latest
```

---

## Configuration

Configuration is handled via **`config.yaml`** (or environment variables).  The most common settings are:

```yaml
# config.yaml
llm:
  provider: openai          # or "ollama", "anthropic", …
  model: gpt-4o-mini        # model name recognised by the provider
  temperature: 0.0

embedding:
  provider: openai          # or "huggingface"
  model: text-embedding-ada-002

vectorstore:
  type: faiss               # other options: chroma, pinecone, weaviate
  persist_directory: ./data/vectorstore

retriever:
  top_k: 4

ingest:
  source_dir: ./data/docs   # directory containing documents to index
  chunk_size: 1000
  chunk_overlap: 200
```

You can also export variables directly, e.g. `export OPENAI_API_KEY=sk-…`.

---

## Quick Start

1. **Add documents** – Place any `.pdf`, `.txt`, `.md`, or `.docx` files inside `data/docs/`.
2. **Run the ingestion script** – This builds the vector store.
   ```bash
   python -m scripts.ingest
   ```
3. **Start the chatbot** – The default entry point launches a simple FastAPI server.
   ```bash
   uvicorn app.main:app --reload
   ```
4. **Interact** – Open `http://localhost:8000/docs` for the auto‑generated Swagger UI, or use the provided CLI:
   ```bash
   python -m scripts.chat "Quelle est la politique de confidentialité de l'entreprise ?"
   ```

---

## Running the Bot

### API (FastAPI)
The API exposes two endpoints:
- `POST /chat` – Accepts `{ "question": "..." }` and returns `{ "answer": "..." }`.
- `GET /health` – Simple health‑check.

### CLI
The `scripts/chat.py` module provides a REPL‑style interface:
```bash
python -m scripts.chat
```
Type `exit` or press `Ctrl‑D` to quit.

---

## Testing

Run the test suite with:
```bash
pytest -q
```
The CI pipeline executes the same command on every push.

---

## Extending & Contributing

### Adding a new Document Loader
1. Create a subclass of `langchain.document_loaders.base.BaseLoader`.
2. Register it in `scripts/ingest.py`.
3. Add unit tests under `tests/loaders/`.

### Supporting a new Vector Store
- Implement the `VectorStore` interface from LangChain or use an existing wrapper.
- Update `config.yaml` with the new `type` and any required credentials.

### Pull‑Request Workflow
1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Ensure all tests pass and linting (`ruff check .`).
4. Open a PR against `main` with a clear description.

Please read `CONTRIBUTING.md` for detailed guidelines.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- **LangChain** – the core framework powering the RAG pipeline.
- **FAISS** – fast similarity search for dense vectors.
- **OpenAI** – LLM and embedding models used in the reference implementation.

---

*Happy coding!*
