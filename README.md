# LangChain Chatbot

**LangChain‑Chatbot** is a modular, extensible chatbot built on top of **[LangChain](https://github.com/langchain-ai/langchain)** that demonstrates Retrieval‑Augmented Generation (RAG) techniques.  The repository provides a minimal yet production‑ready reference implementation that you can clone, run, and extend to build sophisticated conversational agents.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Example Interaction](#example-interaction)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **RAG pipeline**: Combines a vector store (FAISS) with a language model (OpenAI, Anthropic, or any `ChatModel` supported by LangChain).
- **Modular components**: Prompt templates, retrievers, and chain composition are clearly separated for easy swapping.
- **Streaming responses**: Real‑time token streaming via LangChain callbacks.
- **Docker support**: Ready‑to‑run container for reproducible environments.
- **Extensible CLI**: Simple command‑line interface to start a conversation or run batch queries.
- **Comprehensive tests**: Unit tests for each pipeline stage using `pytest` and `pytest‑asyncio`.

---

## Architecture Overview

```
+-----------------+      +-----------------+      +-----------------+
|   User Input    | ---> |   LangChain    | ---> |   LLM (Chat)    |
| (CLI / API)     |      |   Retriever    |      |   (OpenAI)      |
+-----------------+      +-----------------+      +-----------------+
          ^                     ^                     |
          |                     |                     |
          |                     |                     v
   +-----------------+   +-----------------+   +-----------------+
   |   Vector Store  |   |   Prompt       |   |   Response      |
   |   (FAISS)       |   |   Templates    |   |   Streaming     |
   +-----------------+   +-----------------+   +-----------------+
```

1. **Retriever** – Queries a FAISS vector store built from a document corpus (PDF, Markdown, etc.).
2. **Prompt Template** – Injects retrieved context into a system prompt that guides the LLM.
3. **LLM** – Generates a response using the augmented prompt.
4. **Callbacks** – Stream tokens back to the user for a smooth chat experience.

---

## Prerequisites

- **Python ≥ 3.9** (tested on 3.10 & 3.11)
- **Git**
- An OpenAI API key (or any other compatible LLM provider).  Set it as `OPENAI_API_KEY` in your environment.
- Optional: Docker & Docker‑Compose if you prefer containerised execution.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

If you want the latest LangChain features, install from the GitHub source:

```bash
pip install git+https://github.com/langchain-ai/langchain.git
```

---

## Configuration

All configurable values are read from environment variables. Create a `.env` file in the project root (the repository ships a `.env.example` you can copy).

| Variable | Description | Example |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI secret key | `sk-xxxxxxxxxxxxxxxx` |
| `LLM_MODEL` | Model name used by the LLM provider | `gpt-4o-mini` |
| `VECTORSTORE_PATH` | Path where the FAISS index is persisted | `data/faiss_index` |
| `DOCS_PATH` | Directory containing source documents for indexing | `data/docs` |
| `MAX_TOKENS` | Maximum tokens for the LLM response | `1024` |
| `TEMPERATURE` | Sampling temperature for the LLM | `0.7` |

Load the variables automatically with:

```bash
pip install python-dotenv
export $(cat .env | xargs)
```

---

## Running the Bot

### 1️⃣ Build the knowledge base (run once or when docs change)

```bash
python scripts/build_vectorstore.py \
    --docs_path data/docs \
    --index_path data/faiss_index
```

The script reads every `*.txt`, `*.md`, `*.pdf` in `data/docs`, creates embeddings via the configured LLM, and stores them in a FAISS index.

### 2️⃣ Start an interactive chat session

```bash
python -m chatbot.cli
```

You will be prompted for a message; the bot replies in real‑time.  Press `Ctrl‑C` to exit.

### 3️⃣ Run the API server (optional)

```bash
uvicorn api.main:app --reload
```

The FastAPI server exposes two endpoints:
- `POST /chat` – Send a user message and receive a streamed response.
- `GET /health` – Health check.

---

## Example Interaction

```
> Vous: Quelle est la mission de notre entreprise ?

[Streaming response]
> Bot: Notre mission est de fournir des solutions d'intelligence artificielle responsables ...
```

The answer is generated from the retrieved document snippets combined with the LLM's knowledge, illustrating the RAG principle.

---

## Testing

```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run the test suite
pytest
```

Coverage is measured with `pytest-cov`.  CI pipelines run the tests on each PR.

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write code and accompanying tests.
4. Ensure all tests pass (`pytest`).
5. Open a Pull Request with a clear description of the change.

**Coding style** – The project uses `ruff` for linting and `black` for formatting.  Run the formatter before committing:

```bash
ruff check . && black .
```

**Documentation** – Keep the README and inline docstrings up‑to‑date.  Add a section to this README if you introduce new commands or configuration options.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- **LangChain** – The core framework that powers the retrieval and generation pipelines.
- **FAISS** – Efficient similarity search for dense vectors.
- **OpenAI** – Provides the underlying language model used in the examples.
- Community contributors who have helped improve the codebase.

---

*Happy building!*