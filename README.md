# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

A **modular, production‑ready chatbot** built on **[LangChain](https://python.langchain.com/)** that demonstrates **Retrieval‑Augmented Generation (RAG)**.  The bot can answer questions over a custom knowledge base, combine LLM reasoning with vector‑store retrieval, and be extended with additional tools.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Run the Demo](#run-the-demo)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Extending the Bot](#extending-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline**: combines a Large Language Model (LLM) with a vector store (FAISS, Chroma, Pinecone, …) to retrieve relevant documents before generation.
- **LangChain integration**: uses LangChain’s `RetrievalQA`, `ConversationalRetrievalChain`, and `LLMChain` abstractions.
- **Modular design**: separate modules for data ingestion, embedding, retrieval, and chat UI.
- **Config‑driven**: all components (LLM, embeddings, vector store, prompt templates) are configurable via a single `config.yaml`.
- **Docker support**: run the entire stack in containers for reproducibility.
- **Unit & integration tests** with `pytest`.
- **Contribution guidelines** and CI configuration (GitHub Actions).

---

## Architecture Overview

```
+-------------------+      +-------------------+      +-------------------+
|   Data Sources    | ---> |   Ingestion       | ---> |   Vector Store    |
| (txt, pdf, csv…)  |      | (Chunking,       |      | (FAISS, Chroma…) |
+-------------------+      |  Embedding)      |      +-------------------+
                               |                     |
                               v                     v
                         +-------------------+   +-------------------+
                         |   Retrieval QA   |   |   Chat Interface |
                         | (LangChain)      |   | (FastAPI/Streamlit) |
                         +-------------------+   +-------------------+
```

1. **Ingestion** – Documents are loaded, split into chunks, and embedded using an LLM‑provided embedding model.
2. **Vector Store** – Embeddings are persisted in a fast similarity search index.
3. **Retrieval QA** – LangChain’s `RetrievalQA` fetches the top‑k relevant chunks and passes them to the LLM for answer generation.
4. **Chat Interface** – A lightweight FastAPI endpoint (or Streamlit UI) that maintains conversation history and streams responses.

---

## Quick Start

### Prerequisites

- Python **3.9+**
- [Poetry](https://python-poetry.org/) **or** pip/virtualenv
- An OpenAI API key (or another LLM provider supported by LangChain)
- Optional: Docker & Docker‑Compose if you prefer containerised execution

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Using Poetry (recommended)
poetry install
poetry shell

# Or with pip & venv
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file at the project root with your credentials:

```dotenv
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
# If using another provider, set the appropriate env vars (e.g., ANTHROPIC_API_KEY)
```

### Run the Demo

```bash
# Start the FastAPI server (default at http://127.0.0.1:8000)
python -m src.main
```

Open your browser and navigate to `http://127.0.0.1:8000/docs` for the interactive Swagger UI, or use the optional Streamlit UI:

```bash
streamlit run src/ui/chat_interface.py
```

You can now ask questions that are answered using the underlying knowledge base.

---

## Configuration

All runtime options are stored in `config.yaml`.  Example snippet:

```yaml
llm:
  provider: openai
  model: gpt-4o-mini
  temperature: 0.0

embeddings:
  provider: openai
  model: text-embedding-3-large

vector_store:
  type: faiss
  index_path: data/faiss_index

retrieval:
  top_k: 4
  search_type: similarity

prompt:
  system: |
    You are a helpful assistant that answers questions based on the provided context.
  user: |
    Context:\n{context}\n\nQuestion:\n{question}
```

Edit this file to switch LLM providers, change the number of retrieved documents, or point to a different vector‑store implementation.

---

## Project Structure

```
langchain-chatbot/
├─ data/                     # Raw documents & generated vector indexes
├─ src/
│  ├─ ingestion/            # Loaders, splitters, embedding logic
│  ├─ retrieval/            # RetrievalQA wrappers and prompt templates
│  ├─ api/                  # FastAPI routes (chat, health, etc.)
│  ├─ ui/                   # Optional Streamlit UI
│  ├─ core/                 # Core LangChain utilities (LLM wrappers, callbacks)
│  └─ main.py               # Application entry‑point
├─ tests/                    # Unit & integration tests
├─ config.yaml               # Default configuration
├─ requirements.txt          # Pin‑exact dependencies (for pip users)
├─ pyproject.toml           # Poetry project definition
└─ README.md                # ← you are here
```

---

## Extending the Bot

### Adding a New Data Source
1. Implement a loader in `src/ingestion/loaders.py` that returns a list of `Document` objects.
2. Register the loader in `src/ingestion/__init__.py`.
3. Run the ingestion script:
   ```bash
   python -m src.ingestion.run --source my_new_source
   ```

### Switching the Vector Store
Replace the `vector_store.type` in `config.yaml` with `chroma`, `pinecone`, or any LangChain‑compatible store.  Ensure the required SDK is added to `pyproject.toml`.

### Custom Prompt Templates
Edit `config.yaml → prompt` or create a new Jinja2 template under `src/prompt_templates/` and reference it in `src/retrieval/retrieval_qa.py`.

---

## Testing

```bash
# Run the full test suite
pytest -vv
```

The CI pipeline (GitHub Actions) runs the same command on each push, ensuring linting (`ruff`), type checking (`mypy`), and test coverage (`coverage`).

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository.
2. **Create a feature branch** (`git checkout -b feat/your-feature`).
3. **Write tests** for any new functionality.
4. **Run the test suite** locally (`pytest`).
5. **Commit** with a clear message following the conventional‑commit style.
6. **Open a Pull Request** against `main`.

See `CONTRIBUTING.md` for detailed guidelines, coding standards, and the development workflow.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
