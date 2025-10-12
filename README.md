# LangChain Chatbot

## Overview

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a Retrieval‑Augmented Generation (RAG) chatbot built on top of **[LangChain](https://github.com/hwchase17/langchain)**.  It demonstrates how to combine:

- **Large Language Models (LLMs)** for natural‑language generation.
- **Vector stores** (e.g., Chroma, Pinecone, FAISS) for semantic document retrieval.
- **Document loaders** and **text splitters** to ingest knowledge bases.
- **Chains** and **agents** to orchestrate the retrieval‑generation pipeline.

The repository is deliberately lightweight so developers can easily adapt it to their own data sources, LLM providers, or deployment environments.

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
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline** – retrieve relevant passages from a vector store and feed them to an LLM.
- **Modular design** – swap out document loaders, vector stores, or LLMs with a single line change.
- **Streaming responses** – optional server‑sent events (SSE) for real‑time chat UI.
- **Docker support** – containerised development and production ready.
- **Extensible CLI** – manage data ingestion, index rebuilding, and interactive chat.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | >=3.9   |
| pip         | latest  |
| Docker (optional) | >=20.10 |
| OpenAI API key (or other LLM provider) | – |

You also need a vector‑store backend. The default is **Chroma** (pure‑Python, no external service). If you prefer Pinecone, Weaviate, or FAISS, install the corresponding extras (see `pyproject.toml`).

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package with all optional extras
pip install -e .[all]
```

If you only need the core functionality, install without extras:

```bash
pip install -e .
```

---

## Quick Start

1. **Add your documents** – place any `.txt`, `.pdf`, `.md`, or supported file type under `data/`.
2. **Create the vector index**:
   ```bash
   python -m langchain_chatbot.cli ingest
   ```
   This command loads the documents, splits them into chunks, embeds them with the configured embedding model, and persists the index to `db/`.
3. **Run the interactive chatbot**:
   ```bash
   python -m langchain_chatbot.cli chat
   ```
   Type a question and watch the bot retrieve relevant passages and generate a response.

---

## Project Structure

```
langchain-chatbot/
├─ langchain_chatbot/          # Python package
│   ├─ __init__.py
│   ├─ config.py               # Pydantic settings (API keys, model names, etc.)
│   ├─ loaders/                # Document loaders (PDF, CSV, etc.)
│   ├─ vectorstores/           # Wrapper around Chroma / Pinecone / FAISS
│   ├─ chains/                 # RetrievalQA, ConversationalRetrievalChain
│   ├─ cli.py                  # Click‑based command‑line interface
│   └─ server.py               # Optional FastAPI server for UI integration
├─ data/                       # Sample documents (git‑ignored by default)
├─ tests/                      # Pytest suite
├─ Dockerfile
├─ pyproject.toml
└─ README.md                  # ← you are reading this file
```

---

## Configuration

Configuration is handled via **[pydantic‑settings](https://github.com/pydantic/pydantic-settings)**. Create a `.env` file at the project root:

```dotenv
# LLM configuration
LANGCHAIN_CHATBOT_LLM_PROVIDER=openai
LANGCHAIN_CHATBOT_OPENAI_API_KEY=sk-***
LANGCHAIN_CHATBOT_MODEL=gpt-4o-mini

# Embedding model (OpenAI, HuggingFace, etc.)
LANGCHAIN_CHATBOT_EMBEDDING_PROVIDER=openai
LANGCHAIN_CHATBOT_EMBEDDING_MODEL=text-embedding-3-large

# Vector store selection (chroma, pinecone, faiss)
LANGCHAIN_CHATBOT_VECTORSTORE=chroma

# Optional FastAPI settings
LANGCHAIN_CHATBOT_HOST=0.0.0.0
LANGCHAIN_CHATBOT_PORT=8000
```

The `config.py` module reads these variables and provides a typed `Settings` object that the rest of the code imports.

---

## Running the Bot

### 1. CLI Mode (development)

```bash
# Ingest documents (only needed when data changes)
python -m langchain_chatbot.cli ingest

# Start interactive chat
python -m langchain_chatbot.cli chat
```

### 2. API Mode (production)

```bash
# Build the Docker image
docker build -t langchain-chatbot .

# Run the container (exposes port 8000 by default)
docker run -p 8000:8000 --env-file .env langchain-chatbot
```

The FastAPI server exposes two endpoints:

- `POST /chat` – body `{ "question": "..." }` returns `{ "answer": "...", "sources": [...] }`
- `GET /health` – health‑check

You can integrate the API with any front‑end (React, Streamlit, etc.).

---

## Testing

```bash
# Run the full test suite
pytest -vv
```

The repository includes unit tests for loaders, vector‑store wrappers, and the RAG chain. CI pipelines (GitHub Actions) run these tests on every push.

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository** and clone your fork.
2. Create a **feature branch** (`git checkout -b feat/your-feature`).
3. Install the project in editable mode with the `dev` extra:
   ```bash
   pip install -e .[dev]
   ```
4. Write tests for new functionality and ensure existing tests pass.
5. Run the linter and formatter:
   ```bash
   ruff check .
   ruff format .
   ```
6. Open a **Pull Request** with a clear description of the change.

Please adhere to the **PEP 8** style guide and keep the documentation up‑to‑date.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## Acknowledgements

- **LangChain** – the backbone for chain orchestration and integrations.
- **OpenAI**, **Hugging Face**, **Chroma**, **Pinecone**, **FAISS** – for the underlying models and vector stores.
- Community contributors who help improve the example and keep it current.
