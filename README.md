# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

A minimal yet extensible reference implementation of a **chatbot** built on **[LangChain](https://github.com/langchain-ai/langchain)** that demonstrates **Retrieval‑Augmented Generation (RAG)**.  The bot can answer questions over a custom knowledge base, combine LLM reasoning with document retrieval, and is fully testable locally.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Testing](#testing)
- [Adding New Data Sources](#adding-new-data-sources)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline**: Combine a vector store (FAISS) with any LLM supported by LangChain.
- **Modular design**: Easy to swap the LLM, embedding model, or vector store.
- **CLI and API**: Interact via the command line or expose a FastAPI endpoint.
- **Docker support**: Build and run the whole stack in containers.
- **Extensible data ingestion**: Scripts to load PDFs, Markdown, CSV, or plain text.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | `>=3.9` |
| pip         | latest  |
| Docker (optional) | `>=20.10` |
| OpenAI API key (or any other LLM provider) | – |

You will also need an **embedding model** (e.g., `text-embedding-ada-002`).  The repository ships with a small sample dataset in `data/` for quick experimentation.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

If you prefer Docker:

```bash
docker build -t langchain-chatbot .
```

---

## Quick Start

1. **Set your environment variables** (you can copy `.env.example` to `.env`):

   ```bash
   export OPENAI_API_KEY=sk-****
   export LANGCHAIN_API_KEY=ls-****   # optional, for tracing
   ```

2. **Create the vector store** from the sample data:

   ```bash
   python scripts/ingest.py --source data/sample_docs
   ```

3. **Run the interactive CLI**:

   ```bash
   python -m langchain_chatbot.cli
   ```

   You should now be able to ask questions like:

   ```text
   > What is LangChain?
   ```

4. **Or start the API server**:

   ```bash
   uvicorn langchain_chatbot.api:app --reload
   ```

   Send a POST request to `http://127.0.0.1:8000/chat` with JSON `{ "question": "..." }`.

---

## Project Structure

```
langchain-chatbot/
├─ data/                     # Sample documents used for ingestion
├─ langchain_chatbot/        # Core package
│   ├─ __init__.py
│   ├─ config.py            # Pydantic settings (API keys, model names)
│   ├─ retrieval.py         # Vector store and retriever logic
│   ├─ generation.py        # LLM wrapper / prompt templates
│   ├─ pipeline.py          # End‑to‑end RAG pipeline
│   ├─ cli.py               # Simple REPL for local testing
│   └─ api.py               # FastAPI endpoints
├─ scripts/                  # Data ingestion utilities
│   └─ ingest.py
├─ tests/                    # Pytest suite
│   ├─ test_ingest.py
│   └─ test_pipeline.py
├─ Dockerfile
├─ requirements.txt
├─ .env.example
└─ README.md                # ← This file
```

---

## Configuration

All configurable values are stored in `langchain_chatbot/config.py` and can be overridden via environment variables.  The most common settings are:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key | – |
| `EMBEDDING_MODEL` | Embedding model name (OpenAI) | `text-embedding-ada-002` |
| `LLM_MODEL` | LLM model name (OpenAI) | `gpt-3.5-turbo` |
| `VECTOR_STORE` | Vector store backend (`faiss`, `pinecone`, …) | `faiss` |
| `CHUNK_SIZE` | Number of tokens per document chunk | `500` |
| `CHUNK_OVERLAP` | Overlap between chunks | `50` |

---

## Running the Bot

### CLI

```bash
python -m langchain_chatbot.cli
```

### API (FastAPI)

```bash
uvicorn langchain_chatbot.api:app --host 0.0.0.0 --port 8000
```

The API exposes two endpoints:

- `POST /chat` – Returns a generated answer.
- `GET /health` – Simple health check.

---

## Testing

The project uses **pytest**.  Run the suite with:

```bash
pytest -q
```

Coverage is enforced at 85 % on CI.  New tests should be added under `tests/` following the existing naming convention.

---

## Adding New Data Sources

1. Place your documents (PDF, txt, md, csv, etc.) under a new folder, e.g. `data/my_corpus/`.
2. Run the ingestion script:

   ```bash
   python scripts/ingest.py --source data/my_corpus
   ```

   The script automatically:
   - Loads files using LangChain’s `DocumentLoader`s.
   - Splits them with a `RecursiveCharacterTextSplitter`.
   - Generates embeddings.
   - Persists the vector store (FAISS index) to `vector_store/`.

3. Restart the bot to pick up the updated index.

---

## Contributing

Contributions are welcome!  Please follow these steps:

1. **Fork** the repository and create a feature branch.
2. Ensure code follows the existing style (black, isort, flake8).
3. Add or update tests for any new functionality.
4. Run the full test suite (`pytest`).
5. Open a Pull Request with a clear description of the change.

See `CONTRIBUTING.md` for detailed guidelines, commit‑message conventions, and the development workflow.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.
