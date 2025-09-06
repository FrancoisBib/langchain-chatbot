# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/downloads/)

A minimal, production‑ready chatbot built on **LangChain** that demonstrates **Retrieval‑Augmented Generation (RAG)**. The bot retrieves relevant documents from a vector store, feeds them to a language model, and returns context‑aware answers.

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
- [Usage Guide](#usage-guide)
  - [Adding Documents](#adding-documents)
  - [Querying the Bot](#querying-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LangChain** integration for modular LLM pipelines.
- **RAG** workflow: document ingestion → embedding → vector store → similarity search → LLM generation.
- Supports **OpenAI**, **Anthropic**, and **local** LLM providers via LangChain's `ChatModel` abstraction.
- Simple CLI and optional FastAPI web interface.
- Dockerfile for reproducible container builds.
- Comprehensive test suite with `pytest`.

---

## Architecture Overview

```mermaid
flowchart LR
    subgraph Ingestion
        Docs[Documents] -->|Chunk & Embed| VectorStore[Vector Store]
    end
    subgraph Query
        User[User Query] --> Retriever[Similarity Retriever]
        Retriever -->|Relevant chunks| LLM[LLM (Chat Model)]
        LLM -->|Answer| Response[Chatbot Reply]
    end
    VectorStore --> Retriever
```

1. **Document Ingestion** – Text files (PDF, TXT, MD) are split into chunks and embedded using a model from `sentence‑transformers` or OpenAI embeddings.
2. **Vector Store** – Embeddings are stored in a FAISS index (or alternative back‑ends such as Chroma, Pinecone).
3. **Retriever** – At query time, the most similar chunks are fetched.
4. **LLM Generation** – The retrieved context is passed to the LLM with a prompt template, producing a grounded answer.

---

## Quick Start

### Prerequisites

- Python **3.9** or newer
- An OpenAI API key (or another supported LLM provider)
- `git` and `pip`

### Installation

```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### Running the Demo

```bash
# 1️⃣ Ingest sample documents (located in `data/`)
python scripts/ingest.py

# 2️⃣ Start the chatbot (CLI mode)
python scripts/chat.py
```

You will be prompted for a question. The bot will retrieve relevant passages and generate a response.

To launch the optional FastAPI UI:

```bash
uvicorn api.main:app --reload
```
Then open <http://127.0.0.1:8000/docs>.

---

## Project Structure

```
langchain-chatbot/
│
├─ data/                 # Sample documents for ingestion
├─ src/                  # Core library code
│   ├─ agents/           # LangChain agents (optional extensions)
│   ├─ chain/            # Retrieval‑augmented generation chain
│   ├─ prompts/          # Prompt templates (Jinja2)
│   └─ utils/            # Helper functions (logging, config)
│
├─ scripts/              # CLI utilities (ingest, chat, eval)
│   ├─ ingest.py         # Load docs → vector store
│   └─ chat.py           # Interactive REPL
│
├─ api/                  # FastAPI wrapper (optional UI)
│   └─ main.py
│
├─ tests/                # Unit & integration tests
│   └─ test_chatbot.py
│
├─ requirements.txt      # Python dependencies
├─ Dockerfile            # Container build definition
└─ README.md             # ← you are here
```

---

## Configuration

Configuration is handled through a **`.env`** file (loaded with `python‑dotenv`). Example:

```dotenv
# .env (example)
OPENAI_API_KEY=sk-****************
EMBEDDING_MODEL=text-embedding-ada-002   # OpenAI embedding model
VECTORSTORE_PATH=./vectorstore/faiss_index
LLM_MODEL=gpt-4o                         # Change to `gpt-3.5-turbo` or a local model name
TEMPERATURE=0.7
TOP_K=4                                   # Number of retrieved chunks per query
```

The `src.utils.config` module provides a typed dataclass for easy access.

---

## Usage Guide

### Adding Documents

Place any `.txt`, `.md`, or `.pdf` files inside the `data/` directory and run:

```bash
python scripts/ingest.py --source data/ --store vectorstore/faiss_index
```

The script will:
1. Load files with `UnstructuredLoader`.
2. Split them using `RecursiveCharacterTextSplitter`.
3. Embed chunks and persist the FAISS index.

### Querying the Bot

#### CLI

```bash
python scripts/chat.py
```
Enter a question and receive a context‑aware answer.

#### FastAPI

Send a POST request to `/chat` with JSON payload:

```json
{ "question": "What is Retrieval‑Augmented Generation?" }
```
The response contains the answer and the retrieved source snippets.

---

## Testing

Run the test suite with:

```bash
pytest -v
```
Coverage is enforced at **90 %**. New features should include corresponding unit tests.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository.
2. Create a **feature branch** (`git checkout -b feat/your-feature`).
3. Ensure code style with `ruff` and type‑check with `mypy`:
   ```bash
   ruff check . && mypy src/
   ```
4. Write tests for any new functionality.
5. Open a **Pull Request** with a clear description of the change.
6. CI will run linting, tests, and build the Docker image.

See `CONTRIBUTING.md` for detailed guidelines.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.
