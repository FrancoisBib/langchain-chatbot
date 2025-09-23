# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/downloads/)

A **minimal yet extensible** example of building a conversational chatbot powered by **LangChain** and **Retrieval‑Augmented Generation (RAG)**. The bot can answer questions over a custom knowledge base, combine LLM reasoning with vector‑store retrieval, and be easily adapted to new data sources or LLM providers.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Demo](#running-the-demo)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Extending the Bot](#extending-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LangChain** integration for LLM orchestration.
- **RAG pipeline** using a vector store (FAISS by default) to retrieve relevant documents.
- Simple **CLI** and **FastAPI** interfaces for interactive testing.
- **Modular design** – swap LLMs, embeddings, or vector stores with a single line change.
- Docker support for reproducible environments.

---

## Architecture Overview

```
User Query → Prompt Template → LLM (e.g., OpenAI gpt‑4) 
               │                               │
               └─► Retrieval Chain (FAISS) ◄─┘
                     │
                     └─► Retrieved Documents (chunks)
```

1. **Prompt Template** – Formats the user question together with retrieved context.
2. **Retriever** – Queries a vector store built from your knowledge base.
3. **LLM** – Generates a response using the combined prompt and context.
4. **Chain** – LangChain ties the components together, handling token limits and response post‑processing.

---

## Quick Start

### Prerequisites

- Python **3.9** or newer.
- An OpenAI API key (or another LLM provider – see *Configuration*).
- `git` installed.

### Installation

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

### Running the Demo

1. **Prepare a knowledge base** – place your text documents (PDF, TXT, Markdown, etc.) inside the `data/` folder.
2. **Create the vector store**:
   ```bash
   python scripts/build_index.py --source data/ --store faiss
   ```
   This script splits documents, creates embeddings (default: `OpenAIEmbeddings`), and stores them in `index/faiss/`.
3. **Start the chatbot** (CLI version):
   ```bash
   python -m chatbot.cli
   ```
   Or launch the FastAPI server for a web UI:
   ```bash
   uvicorn api.main:app --reload
   ```
   Visit `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

---

## Project Structure

```
langchain-chatbot/
├─ api/                     # FastAPI entry point
│   └─ main.py
├─ chatbot/                # Core chatbot logic
│   ├─ __init__.py
│   ├─ chain.py            # LangChain RAG chain definition
│   └─ cli.py              # Simple REPL interface
├─ data/                    # Sample knowledge‑base files (add yours here)
├─ index/                   # Generated vector store (git‑ignored)
├─ scripts/                # Utility scripts (index building, evaluation)
│   └─ build_index.py
├─ tests/                  # Unit and integration tests
│   └─ test_chain.py
├─ .env.example            # Example environment variables file
├─ requirements.txt
├─ README.md                # <‑‑ This file
└─ pyproject.toml
```

---

## Configuration

The project reads environment variables from a `.env` file (or your shell). Example (`.env.example`):

```dotenv
# OpenAI
OPENAI_API_KEY=sk-************************

# Embedding model (default: text-embedding-ada-002)
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002

# LLM model (default: gpt-4)
OPENAI_CHAT_MODEL=gpt-4

# Vector store – currently supports 'faiss' or 'chromadb'
VECTOR_STORE=faiss

# Index path (relative to project root)
INDEX_PATH=index/faiss/
```

You can replace the OpenAI components with any LangChain‑compatible provider (e.g., Cohere, HuggingFace) by editing `chatbot/chain.py` and supplying the appropriate classes.

---

## Extending the Bot

### Adding New Document Types

1. Install a parser (e.g., `pypdf`, `python-docx`).
2. Extend `scripts/build_index.py` to handle the new MIME type.
3. Update the `DocumentLoader` mapping in `chatbot/loader.py` (if you create one).

### Swapping the Vector Store

Replace the `FAISS` import with another store and adjust the `store` argument in `scripts/build_index.py`. Ensure the store implements LangChain's `VectorStore` interface.

### Custom Prompt Templates

Edit `chatbot/chain.py` – the `PROMPT_TEMPLATE` constant holds the Jinja‑style prompt. You can add system messages, few‑shot examples, or chain‑of‑thought instructions.

---

## Testing

Run the test suite with:

```bash
pytest -v
```

The tests cover:
- Document loading and chunking.
- Retrieval correctness.
- End‑to‑end chain execution with a mock LLM.

Add new tests under `tests/` to protect future contributions.

---

## Contributing

Contributions are welcome! Follow these steps:

1. **Fork** the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Keep the code style consistent – the project uses **black** and **ruff**.
   ```bash
   pip install black ruff
   black .
   ruff check .
   ```
4. Write or update documentation (README, docstrings) as needed.
5. Submit a **pull request** with a clear description of the change.

Please ensure that all tests pass and that you add tests for new functionality.

---

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
