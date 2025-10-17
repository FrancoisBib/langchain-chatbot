# LangChain Chatbot

## Overview

**LangChain‑Chatbot** is a modular, extensible chatbot built on top of **[LangChain](https://python.langchain.com/)** that demonstrates **Retrieval‑Augmented Generation (RAG)**.  It showcases how to combine LLMs, vector stores, and custom tooling to create conversational agents that can retrieve relevant context from external data sources and generate accurate, grounded responses.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline** using LangChain’s `Retriever` and `LLMChain`
- Support for multiple vector‑store backends (FAISS, Chroma, Pinecone, etc.)
- Easy plug‑and‑play for custom data loaders (CSV, PDF, Markdown, web‑scraped content)
- Conversational memory with configurable window size
- Simple CLI and optional FastAPI web UI
- Dockerfile for reproducible container deployment
- Comprehensive unit tests with `pytest`

---

## Architecture Overview

```
User ↔️ Interface (CLI / FastAPI) ↔️ LangChain Agent ↔️ Retriever ↔️ Vector Store
                                   ↕
                                 LLM (OpenAI / Anthropic / Ollama …)
```

1. **Interface** – Accepts user messages via the command line or HTTP endpoint.
2. **Agent** – Orchestrates the RAG flow: fetches relevant chunks, injects them into the prompt, and calls the LLM.
3. **Retriever** – Uses a vector store to perform similarity search on embedded documents.
4. **LLM** – Generates the final answer, optionally with streaming support.

---

## Installation

### Prerequisites

- Python **3.9+**
- `pip` (or `uv`/`poetry` if you prefer) 
- An OpenAI API key (or any other LLM provider supported by LangChain)

### Steps

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Tip**: If you use `uv` or `poetry`, replace the `pip install` line accordingly.

---

## Quick Start

1. **Add your data** – Place documents you want the bot to know about in the `data/` directory. Supported formats: `.txt`, `.md`, `.pdf`, `.csv`.
2. **Create the vector store** (run once or whenever you add new data):

```bash
python scripts/build_index.py --source data/ --store faiss
```

3. **Start the chatbot** (CLI example):

```bash
python -m langchain_chatbot.cli
```

   You will be prompted for a question; the bot will retrieve relevant passages and answer.

4. **Optional – Run the FastAPI UI**:

```bash
uvicorn langchain_chatbot.api:app --reload
```

   Open `http://127.0.0.1:8000/docs` to explore the OpenAPI interface.

---

## Configuration

Configuration is handled via a **`.env`** file at the project root. Example:

```dotenv
# .env
OPENAI_API_KEY=sk-****************
EMBEDDING_MODEL=text-embedding-ada-002
LLM_MODEL=gpt-4o-mini
VECTOR_STORE=faiss   # or chroma, pinecone, etc.
RETRIEVER_TOP_K=5
MEMORY_WINDOW=3
```

The `config.py` module loads these variables using `python-dotenv` and provides a typed `Settings` object for the rest of the codebase.

---

## Running the Bot

### CLI

```bash
python -m langchain_chatbot.cli
```

### Docker

```bash
# Build the image
docker build -t langchain-chatbot .

# Run the container (remember to pass your .env or set env vars)
docker run -it --rm \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  -p 8000:8000 \
  langchain-chatbot
```

---

## Project Structure

```
langchain-chatbot/
│
├─ data/                 # Sample documents for the RAG index
├─ docs/                 # Additional documentation (architecture diagrams, etc.)
├─ scripts/              # Utility scripts (index building, data cleaning)
│   └─ build_index.py    # Creates/updates the vector store
├─ langchain_chatbot/    # Core Python package
│   ├─ __init__.py
│   ├─ agent.py          # LangChain agent implementation
│   ├─ retriever.py      # Wrapper around vector stores
│   ├─ memory.py         # Conversational memory utilities
│   ├─ config.py         # Settings loader
│   ├─ cli.py            # Command‑line interface
│   └─ api.py            # FastAPI endpoints (optional UI)
├─ tests/                # Unit and integration tests
│   ├─ test_agent.py
│   └─ test_retriever.py
├─ .env.example          # Template for environment variables
├─ requirements.txt
├─ Dockerfile
└─ README.md             # ← You are reading it!
```

---

## Testing

```bash
pytest -v
```

The test suite covers the agent logic, retriever integration, and configuration loading. CI pipelines (GitHub Actions) run these tests on every push.

---

## Contributing

Contributions are welcome! Follow these steps:

1. **Fork** the repository and clone your fork.
2. Create a **feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. Make your changes, ensuring that:
   - Code follows the existing style (PEP 8, type hints).
   - New functionality is covered by tests.
   - Documentation is updated where appropriate.
4. Run the test suite locally.
5. Open a **Pull Request** against the `main` branch with a clear description of the change.

Please read the `CODE_OF_CONDUCT.md` and `CONTRIBUTING.md` files for detailed guidelines.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- The **LangChain** community for the powerful abstractions that make RAG pipelines straightforward.
- Contributors of the underlying vector‑store libraries (FAISS, Chroma, Pinecone, etc.).

---

*Happy building with LangChain!*