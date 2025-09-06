# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

![LangChain](https://img.shields.io/badge/Powered%20by-LangChain-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B%20%7C%203.10%7C%203.11-blue)
![License](https://img.shields.io/badge/License-MIT-green)

A minimal yet extensible reference implementation of a **chatbot** built with **[LangChain](https://github.com/hwchase17/langchain)** that leverages **Retrieval‑Augmented Generation (RAG)** to answer questions using a custom knowledge base.

---

## Table of Contents

1. [Features](#features)
2. [Architecture Overview](#architecture-overview)
3. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Demo](#running-the-demo)
4. [Project Structure](#project-structure)
5. [Configuration](#configuration)
6. [Usage Guide](#usage-guide)
   - [Indexing Documents](#indexing-documents)
   - [Chatting with the Bot](#chatting-with-the-bot)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)
10. [References](#references)

---

## Features

- **RAG pipeline** – combines a vector store retriever with a LLM for grounded responses.
- **Modular design** – easy to swap the LLM, embeddings model, or vector store.
- **Document ingestion** – supports plain‑text, PDFs and Markdown out‑of‑the‑box.
- **Prompt templating** – customizable system and human prompts.
- **Simple CLI demo** – start a conversational session in seconds.
- **Extensible** – ready for integration with FastAPI, Streamlit, or any custom UI.

---

## Architecture Overview

```
User Input ──► PromptTemplate ──► LLM (e.g., OpenAI, Anthropic)
                     ▲                │
                     │                ▼
                Retriever ◄── VectorStore ◄── Indexed Docs
```

1. **Document Loader** – reads source files and splits them into chunks.
2. **Embeddings** – converts each chunk into a dense vector (e.g., OpenAI `text-embedding-ada-002`).
3. **Vector Store** – persists embeddings (default: `FAISS`).
4. **Retriever** – fetches the most relevant chunks for a user query.
5. **LLM** – generates the final answer using a prompt that includes the retrieved context.

---

## Getting Started

### Prerequisites

- Python **3.9** or newer (tested on 3.9‑3.11).
- An OpenAI API key (or another provider supported by LangChain).
- Git (to clone the repository).

### Installation

```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Tip** – If you prefer `poetry` or `pipenv`, the `pyproject.toml` is already provided.

### Running the Demo

```bash
# Set your OpenAI key (or other provider) as an environment variable
export OPENAI_API_KEY='sk-...'
# On Windows PowerShell:
# $env:OPENAI_API_KEY='sk-...'

# Index example documents (run once or when docs change)
python scripts/index_documents.py --source data/

# Start the interactive chat CLI
python scripts/chat_cli.py
```

You should now be able to ask natural‑language questions and receive answers grounded in the indexed knowledge base.

---

## Project Structure

```
langchain-chatbot/
├─ data/                # Sample documents (txt, pdf, md) used for indexing
├─ scripts/            # Utility scripts (indexing, CLI, tests)
│   ├─ index_documents.py   # Loads docs → splits → embeds → stores
│   └─ chat_cli.py           # Simple REPL chat interface
├─ src/                # Core library code (can be imported as a package)
│   ├─ __init__.py
│   ├─ config.py       # Centralised configuration (LLM, embeddings, store)
│   ├─ loaders.py      # Document loaders & chunking helpers
│   ├─ retriever.py    # Vector store wrapper
│   └─ chatbot.py      # RAG chain definition
├─ tests/              # Pytest suite
│   └─ test_chatbot.py
├─ .gitignore
├─ requirements.txt
├─ pyproject.toml
└─ README.md
```

---

## Configuration

All configurable items live in `src/config.py`. The defaults work with OpenAI, but you can replace them with any LangChain‑compatible component.

```python
# src/config.py
from langchain.llms import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# LLM – you can swap to Anthropic, Cohere, etc.
LLM = OpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

# Embeddings model
EMBEDDINGS = OpenAIEmbeddings()

# Vector store – persists to `./vector_store/faiss_index`
VECTOR_STORE_PATH = "vector_store/faiss_index"
```

To use a different provider, edit the corresponding class imports and parameters.

---

## Usage Guide

### Indexing Documents

```bash
python scripts/index_documents.py --source data/ --store_path vector_store/faiss_index
```

- `--source` – directory containing the documents to ingest.
- `--store_path` – optional custom location for the FAISS index.

The script will:
1. Load supported file types (`.txt`, `.md`, `.pdf`).
2. Split them with a `RecursiveCharacterTextSplitter` (default chunk size 1000, overlap 200).
3. Generate embeddings and store them in FAISS.

### Chatting with the Bot

Run the CLI as shown earlier, or import the chain in your own code:

```python
from src.chatbot import get_chat_chain
from src.config import LLM, EMBEDDINGS, VECTOR_STORE_PATH

chain = get_chat_chain(
    llm=LLM,
    embeddings=EMBEDDINGS,
    vector_store_path=VECTOR_STORE_PATH,
)

while True:
    query = input("🗨️ > ")
    if query.lower() in {"exit", "quit"}:
        break
    response = chain.run(query)
    print("🤖", response)
```

You can also expose the chain via an API (FastAPI example in `examples/fastapi_app.py`).

---

## Testing

The repository includes a minimal test suite using **pytest**.

```bash
pip install pytest
pytest -q
```

Tests cover:
- Document loading & chunking.
- Vector store creation and retrieval.
- End‑to‑end RAG chain execution with a mock LLM.

---

## Contributing

Contributions are welcome! Follow these steps:

1. **Fork** the repository.
2. Create a **feature branch** (`git checkout -b feat/your-feature`).
3. Keep the code style consistent – we use **black** and **isort**.
4. Add or update tests for new functionality.
5. Ensure the CI pipeline passes (`pytest` and `flake8`).
6. Open a **Pull Request** with a clear description of the change.

Please see `CONTRIBUTING.md` for detailed guidelines (code of conduct, commit message format, etc.).

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## References

- LangChain Documentation: https://langchain.com/docs/
- Retrieval‑Augmented Generation (RAG) paper: https://arxiv.org/abs/2005.11401
- OpenAI Embeddings: https://platform.openai.com/docs/guides/embeddings
- FAISS vector store: https://github.com/facebookresearch/faiss

---

*Happy building with LangChain!*