# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A minimal, production‑ready example of a **chatbot** built on **[LangChain](https://github.com/hwchase17/langchain)** that leverages **Retrieval‑Augmented Generation (RAG)** to provide up‑to‑date, context‑aware answers.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LangChain** integration for prompt management, memory, and chain orchestration.
- **RAG pipeline** using a vector store (e.g., FAISS, Chroma) to retrieve relevant documents before generation.
- **Modular design** – separate modules for data ingestion, indexing, retrieval, and chat UI.
- **Docker support** for reproducible local development.
- **Extensible** – add new retrievers, LLM providers, or UI front‑ends with minimal changes.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Install dependencies (Python 3.10+ recommended)
poetry install   # or `pip install -r requirements.txt`

# Populate the knowledge base (example uses local markdown files)
python -m scripts.ingest data/

# Run the chatbot (default uses OpenAI gpt‑4o, configure your API key below)
python -m scripts.run_chatbot
```

Open your browser at `http://localhost:8000` to start chatting.

---

## Installation

### Prerequisites

- Python **3.10** or newer
- `git`
- An **OpenAI API key** (or another LLM provider – see configuration)
- Optional: Docker & Docker‑Compose if you prefer containerised execution

### Using Poetry (recommended)

```bash
pip install poetry
poetry install
```

### Using pip

```bash
pip install -r requirements.txt
```

---

## Configuration

All configurable values live in `config.yaml`. A minimal example:

```yaml
llm:
  provider: openai
  model: gpt-4o
  api_key: "${OPENAI_API_KEY}"   # set this env var or replace directly

retriever:
  type: faiss
  index_path: "./index/faiss_index"
  top_k: 5

ingest:
  source_dir: "./data"
  chunk_size: 1000
  chunk_overlap: 200
```

> **Tip:** keep secrets out of the repository – use environment variables or a `.env` file (ignored via `.gitignore`).

---

## Running the Bot

### Local development

```bash
# Load the index (if not already built) and start the FastAPI server
python -m scripts.run_chatbot
```

The server exposes two endpoints:

- `GET /` – simple health check.
- `POST /chat` – expects JSON `{ "message": "Your question" }` and returns `{ "answer": "Generated response" }`.

### Docker

```bash
docker compose up --build
```

The service will be reachable at `http://localhost:8000`.

---

## Project Structure

```
langchain-chatbot/
├─ data/                 # Raw documents (markdown, txt, pdf …)
├─ index/                # Vector store files (FAISS, Chroma, …)
├─ scripts/              # Entry‑point utilities
│   ├─ ingest.py         # Load documents → split → embed → store
│   └─ run_chatbot.py    # Starts FastAPI + LangChain chain
├─ src/                  # Core library code
│   ├─ llm.py            # LLM wrapper (OpenAI, Anthropic, etc.)
│   ├─ retriever.py      # Retrieval logic abstraction
│   └─ chatbot.py        # LangChain chain definition
├─ config.yaml           # Default configuration file
├─ requirements.txt      # pip dependencies (fallback for Poetry)
├─ pyproject.toml        # Poetry project definition
└─ README.md             # ← This file
```

---

## Testing

Unit tests live in `tests/`. Run them with:

```bash
pytest -vv
```

Integration tests that hit the LLM are marked with the `slow` marker and can be executed via:

```bash
pytest -m slow
```

---

## Contributing

We welcome contributions! Follow these steps:

1. **Fork** the repository.
2. Create a **feature branch** (`git checkout -b feat/your-feature`).
3. Ensure code style with `ruff` and type‑check with `mypy`.
4. Add or update tests to cover your changes.
5. Submit a **Pull Request** with a clear description of the change.

### Development workflow

```bash
# Install dev dependencies (included in pyproject.toml)
poetry install --with dev

# Run linting & formatting
ruff check .
black .

# Run type checking
mypy src/
```

Please adhere to the existing code style and keep the documentation up‑to‑date.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
