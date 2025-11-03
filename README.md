# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A minimal, **open‑source** reference implementation of a conversational chatbot built on **LangChain** and powered by **Retrieval‑Augmented Generation (RAG)**.  The project demonstrates how to combine LLMs, vector stores, and document loaders to build a robust, context‑aware assistant.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Bot](#running-the-bot)
- [Configuration](#configuration)
- [Extending the Bot](#extending-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LangChain** integration for chain orchestration.
- **RAG** pipeline: document ingestion → embeddings → vector store → similarity search → LLM generation.
- Support for multiple LLM providers (OpenAI, Anthropic, Ollama, etc.).
- Plug‑and‑play vector store backends (FAISS, Chroma, Pinecone, etc.).
- Simple CLI and optional FastAPI web UI.
- Fully typed Python code with `mypy` and `ruff` linting.
- Unit tests with `pytest` and CI workflow.

---

## Architecture Overview

```
+-------------------+      +-------------------+      +-------------------+
|   Document Loader | ---> |   Embedding Model | ---> |   Vector Store    |
+-------------------+      +-------------------+      +-------------------+
                                 ^                         |
                                 |                         |
                                 |               +-------------------+
                                 +---------------|   Retrieval QA   |
                                                 +-------------------+
                                                          |
                                                          v
                                                   +--------------+
                                                   |   LLM (Gen)  |
                                                   +--------------+
                                                          |
                                                          v
                                                   +--------------+
                                                   |   Chat UI    |
                                                   +--------------+
```

1. **Document Loader** – Loads raw text, PDFs, Markdown, etc.
2. **Embedding Model** – Generates dense vectors (e.g., `text‑embedding‑ada‑002`).
3. **Vector Store** – Persists embeddings for fast similarity search.
4. **Retrieval QA Chain** – Retrieves relevant chunks and feeds them to the LLM.
5. **LLM Generation** – Produces context‑aware responses.
6. **Chat UI** – CLI or FastAPI endpoint for interacting with the bot.

---

## Quick Start

### Prerequisites

- Python **3.10** or newer.
- An LLM API key (e.g., OpenAI `OPENAI_API_KEY`).
- (Optional) `git` for cloning the repository.

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

> **Tip**: The project uses `poetry` for dependency management as an alternative. See `pyproject.toml` for details.

### Running the Bot

#### 1️⃣ Ingest Documents

```bash
python scripts/ingest.py --source data/knowledge-base/ --store faiss
```

- `--source` points to a directory containing `.txt`, `.md`, `.pdf`, etc.
- `--store` selects the vector store backend (`faiss`, `chroma`, `pinecone`).

#### 2️⃣ Start the Chat Interface

```bash
# CLI mode
python scripts/chat_cli.py

# Or launch the FastAPI UI (requires `uvicorn`)
uvicorn app.main:app --reload
```

Open your browser at `http://127.0.0.1:8000/docs` to explore the OpenAPI UI.

---

## Configuration

Configuration is driven by the `config.yaml` file (or environment variables). Key sections:

```yaml
llm:
  provider: openai          # openai | anthropic | ollama
  model: gpt-4o-mini
  temperature: 0.7

vector_store:
  type: faiss               # faiss | chroma | pinecone
  path: ./vector_store/faiss

retriever:
  top_k: 4                  # Number of documents to retrieve per query

logging:
  level: INFO
```

You can override any setting at runtime via command‑line flags (see `scripts/ingest.py --help`).

---

## Extending the Bot

### Adding a New Document Loader
1. Create a subclass of `langchain.document_loaders.base.BaseLoader`.
2. Implement the `load()` method returning a list of `Document` objects.
3. Register the loader in `scripts/ingest.py` via the `--loader` flag.

### Supporting a New Vector Store
1. Install the store’s Python client (e.g., `pip install weaviate-client`).
2. Implement a wrapper that conforms to LangChain’s `VectorStore` interface.
3. Add a selection case in `config.yaml` and the ingestion script.

---

## Testing

```bash
# Run the full test suite
pytest -v
```

The repository includes:
- Unit tests for each component (`tests/unit/`).
- Integration tests that spin up a temporary FAISS store (`tests/integration/`).
- Mocked LLM calls using `langchain.callbacks.fake_callback_manager.FakeCallbackManager`.

CI is configured via GitHub Actions (`.github/workflows/ci.yml`).

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository and clone your fork.
2. Create a **feature branch** (`git checkout -b feat/your-feature`).
3. Write code adhering to the existing style (PEP 8, type hints).
4. Add or update tests to cover your changes.
5. Run the linting and test suite locally:
   ```bash
   ruff check . && ruff format . && mypy . && pytest
   ```
6. Open a **Pull Request** targeting the `main` branch.
7. Ensure the CI pipeline passes before merging.

See `CONTRIBUTING.md` for detailed guidelines.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

*Happy building with LangChain!*