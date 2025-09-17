# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/)

A lightweight, extensible chatbot built on **[LangChain](https://github.com/hwchase17/langchain)** that demonstrates **Retrieval‑Augmented Generation (RAG)**.  The bot can answer questions over a custom knowledge base, combine LLM reasoning with vector‑store retrieval, and be easily extended for new data sources or LLM providers.

---

## 📖 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Getting Started](#-getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Running the Bot](#-running-the-bot)
- [Project Structure](#-project-structure)
- [Extending & Contributing](#-extending--contributing)
- [Testing](#-testing)
- [License](#-license)
- [Acknowledgements](#-acknowledgements)

---

## ✨ Features

- **RAG pipeline** – combines a **vector store** (FAISS, Chroma, Pinecone…) with a **LLM** (OpenAI, Anthropic, Llama‑2…) to answer queries grounded in your own documents.
- **Modular design** – interchangeable components for document loaders, embeddings, vector stores, and LLMs.
- **Prompt engineering** – built‑in system prompts and chat history handling.
- **CLI & API** – run locally via a simple CLI or expose a FastAPI endpoint.
- **Docker support** – optional `Dockerfile` for reproducible environments.
- **Extensive tests** – unit and integration tests using `pytest` and `pytest‑asyncio`.

---

## 🎥 Demo

```bash
# After installation (see below)
python -m chatbot.cli
```

You will be prompted for a question. The bot will retrieve the most relevant chunks from the knowledge base and generate a response using the selected LLM.

---

## 🚀 Getting Started

### Prerequisites

| Tool | Version |
|------|---------|
| Python | >=3.9 |
| pip | >=21.0 |
| Git | any |
| (Optional) Docker | >=20.10 |

You also need an API key for the LLM you intend to use (e.g., `OPENAI_API_KEY`).

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package in editable mode
pip install -e .[dev]
```

The optional `dev` extras install testing and linting tools.

### Configuration

Create a `.env` file at the project root (or export environment variables directly):

```dotenv
# LLM provider – currently supported: openai, anthropic, huggingface
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
# Embedding model – e.g., openai‑text‑embedding‑ada‑002
EMBEDDING_MODEL=text-embedding-ada-002
# Vector store – faiss, chroma, pinecone, etc.
VECTOR_STORE=faiss
# Path to the directory containing source documents (pdf, txt, md, etc.)
DOCS_PATH=./data
```

You can also override defaults via command‑line arguments (see the CLI help).

---

## 🏃 Running the Bot

### CLI

```bash
python -m chatbot.cli --docs ./data --store faiss
```

The CLI will:
1. Load documents from `DOCS_PATH` (or the path you provide).
2. Split them into chunks using LangChain's `RecursiveCharacterTextSplitter`.
3. Embed the chunks and store them in the selected vector store.
4. Start an interactive prompt where you can type questions.

### FastAPI server (optional)

```bash
uvicorn chatbot.api:app --reload
```

The API exposes a single endpoint:
- `POST /chat` – body `{ "question": "..." }` – returns `{ "answer": "...", "sources": [...] }`.

---

## 📁 Project Structure

```
langchain-chatbot/
├─ chatbot/                     # Core package
│   ├─ __init__.py
│   ├─ config.py                # Pydantic settings (loads .env)
│   ├─ loaders/                 # Document loaders (pdf, txt, markdown…)
│   ├─ pipelines/               # RAG pipeline implementation
│   │   ├─ __init__.py
│   │   ├─ rag.py                # High‑level RAG class
│   ├─ llms/                    # Wrapper classes for OpenAI, Anthropic, etc.
│   ├─ stores/                  # Vector‑store adapters (FAISS, Chroma…)
│   ├─ cli.py                   # Click‑based command line interface
│   └─ api.py                   # FastAPI entry point
├─ tests/                       # Unit & integration tests
│   ├─ test_rag.py
│   └─ ...
├─ data/                        # Example documents (git‑ignored in real project)
├─ .env.example                 # Template for environment variables
├─ pyproject.toml               # Poetry/PEP‑517 build config
├─ requirements.txt             # Pin‑down runtime deps (generated)
└─ README.md                    # ← this file
```

---

## 🛠️ Extending & Contributing

### Adding a new document loader
1. Create a class in `chatbot/loaders/` that inherits from `BaseLoader`.
2. Implement a `load()` method returning a list of `Document` objects.
3. Register the loader in `chatbot/pipelines/rag.py` (or expose via CLI flag).

### Supporting a new vector store
1. Implement a subclass of `BaseVectorStore` in `chatbot/stores/`.
2. Provide `add_texts`, `similarity_search`, and `save/load` methods.
3. Add a corresponding entry in the `VECTOR_STORE` enum in `config.py`.

### Development workflow
```bash
# Run the test suite
pytest -q
# Lint & format
ruff check .
black .
```

Pull requests should:
- Include tests for new functionality.
- Update the documentation (README or docstrings) as needed.
- Pass all CI checks.

---

## ✅ Testing

The repository ships with a comprehensive test suite using `pytest`.  To run:

```bash
pytest
```

For fast feedback during development, you can run only the unit tests:

```bash
pytest tests/unit
```

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- **LangChain** – the foundational framework that makes chaining LLMs and external tools effortless.
- **FAISS / Chroma** – for efficient vector similarity search.
- **OpenAI / Anthropic** – for the underlying large language models.
- Community contributors who helped refine the RAG workflow.

---

*Happy building! If you encounter issues or have ideas for improvement, feel free to open an issue or submit a pull request.*