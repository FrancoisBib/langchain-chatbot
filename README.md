# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a conversational AI assistant built on top of **[LangChain](https://github.com/langchain-ai/langchain)**. It demonstrates how to combine large language models (LLMs) with a retrieval layer to create a **Retrieval‑Augmented Generation (RAG)** pipeline that can answer user queries with up‑to‑date, domain‑specific knowledge.

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

- **Modular RAG pipeline** – interchangeable retrievers, vector stores, and LLM back‑ends.
- **LangChain integration** – uses `langchain` chains, prompts, and memory utilities.
- **Docker support** – run the entire stack locally with a single command.
- **Extensible architecture** – add new data sources, custom prompts, or alternative LLM providers.
- **Comprehensive tests** – unit and integration tests for core components.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | >=3.9   |
| pip         | latest  |
| Docker (optional) | >=20.10 |
| OpenAI API key (or any compatible LLM endpoint) | – |
| Pinecone/FAISS/Chroma (vector store) | – |

> **Note**: The project is LLM‑agnostic; you can swap OpenAI for Anthropic, Cohere, Azure, etc., by adjusting the `LLM` configuration.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. (Optional) Set up Docker for the vector store

If you prefer a containerised vector store (e.g., **Chroma**), run:

```bash
docker compose up -d
```

---

## Quick Start

The simplest way to see the bot in action is to run the example script that loads a small knowledge base and starts an interactive REPL.

```bash
python -m src.main --example
```

You will be prompted for a question; the bot will retrieve relevant chunks from the vector store, feed them to the LLM, and return a response.

---

## Project Structure

```
langchain-chatbot/
├─ src/                     # Source code
│  ├─ agents/               # Custom LangChain agents (optional)
│  ├─ chains/               # Prompt chains & RAG logic
│  ├─ loaders/              # Data ingestion utilities
│  ├─ retrievers/           # Vector store wrappers
│  ├─ utils/                # Helper functions (e.g., logging, env handling)
│  └─ main.py               # Entry point for the CLI / demo
├─ tests/                   # Unit and integration tests
├─ .env.example             # Template for environment variables
├─ Dockerfile               # Build image for the chatbot service
├─ docker-compose.yml       # Compose file for vector store & optional services
├─ requirements.txt         # Python dependencies
└─ README.md                # ← You are reading it!
```

---

## Configuration

All runtime configuration is read from environment variables. Copy `.env.example` to `.env` and fill in the required values.

```dotenv
# .env
OPENAI_API_KEY=sk-*****
LLM_MODEL=gpt-4o-mini   # any OpenAI model or compatible endpoint identifier
VECTOR_STORE=chroma      # options: chroma, pinecone, faiss, milvus
CHROMA_PERSIST_DIR=./data/chroma
# Optional – for Pinecone
PINECONE_API_KEY=...
PINECONE_ENV=us-east1-gcp
```

The `src.utils.config` module validates the variables at startup and raises a clear error if something is missing.

---

## Running the Bot

### 1. Index your documents

The first step is to ingest documents into the vector store. The CLI provides a helper:

```bash
python -m src.main --index path/to/your/documents
```

Supported formats include **.txt**, **.pdf**, **.md**, and **.csv**. The loader automatically extracts text, splits it into chunks (default 500 tokens), creates embeddings with the configured LLM, and stores them.

### 2. Start the interactive chat

```bash
python -m src.main --chat
```

You can also launch the bot as a FastAPI server (useful for UI integration):

```bash
uvicorn src.api:app --host 0.0.0.0 --port 8000
```

The API exposes two endpoints:
- `POST /chat` – send a user message and receive the bot's response.
- `GET /health` – simple health‑check.

---

## Testing

Run the test suite with:

```bash
pytest -v
```

The repository includes:
- **Unit tests** for loaders, retrievers, and prompt chains.
- **Integration tests** that spin up a temporary in‑memory vector store.

CI pipelines (GitHub Actions) automatically lint, type‑check (via `mypy`), and run the test suite on every push.

---

## Contributing

Contributions are welcome! Follow these steps:

1. **Fork** the repository and create a new branch for your feature or bug‑fix.
2. Ensure your code follows the existing style (PEP 8, type hints, docstrings).
3. Add or update tests to cover new functionality.
4. Run the full test suite locally (`pytest`).
5. Submit a **Pull Request** with a clear description of the change.

Please see `CONTRIBUTING.md` for detailed guidelines on coding standards, commit messages, and release process.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- **LangChain** – for the powerful abstractions that make building RAG pipelines straightforward.
- The open‑source community for vector‑store implementations (Chroma, FAISS, Pinecone, etc.).

---

---

*Happy coding!*
