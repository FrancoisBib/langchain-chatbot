# LangChain Chatbot with Retrieval-Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A **modular, production‑ready chatbot** built on **[LangChain](https://github.com/langchain-ai/langchain)** that demonstrates Retrieval‑Augmented Generation (RAG).  The bot can answer questions over a custom knowledge base, supports multiple LLM providers, and is ready for extension or contribution.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Demo](#running-the-demo)
- [Configuration](#configuration)
- [Adding Your Own Data](#adding-your-own-data)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline**: combines a vector store retriever with a language model to produce grounded answers.
- **Pluggable LLMs**: works with OpenAI, Anthropic, Cohere, Ollama, etc.
- **Multiple vector stores**: FAISS (local), Pinecone, Weaviate, Chroma, etc.
- **Streaming responses**: optional token‑by‑token streaming for UI integration.
- **Typed settings** using `pydantic`/`dynaconf` for easy environment configuration.
- **Extensible**: clear separation of concerns (retriever, generator, prompt templates).
- **Docker support**: ready-to‑run container for reproducible environments.

---

## Architecture Overview

```
+-----------------+      +-------------------+      +-------------------+
|   User Input    | ---> |   Prompt Builder  | ---> |   LLM (Chat)      |
+-----------------+      +-------------------+      +-------------------+
                               ^   |
                               |   v
                       +-------------------+
                       |   Retriever (FAISS|   Vector Store
                       |   / Pinecone)    |
                       +-------------------+
```

1. **Retriever** – Queries the vector store for the top‑k relevant documents.
2. **Prompt Builder** – Injects retrieved documents into a **RAG prompt template**.
3. **LLM** – Generates the final answer, optionally streaming tokens back to the client.

All components are defined in `src/` and wired together in `app.py` using LangChain's `Runnable` abstractions.

---

## Getting Started

### Prerequisites

- Python **3.10** or newer
- `git` and `pip`
- An LLM API key (OpenAI, Anthropic, etc.) – see the **Configuration** section below.
- (Optional) Docker if you prefer containerised execution.

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### Running the Demo

```bash
# Load environment variables (example using a .env file)
export $(cat .env | xargs)

# Start the FastAPI server (or the script of your choice)
uvicorn app:app --reload
```

Open your browser at `http://127.0.0.1:8000/docs` to interact with the OpenAPI UI.

---

## Configuration

Configuration is handled via **environment variables** or a `.env` file. The most common settings are:

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_PROVIDER` | Which LLM backend to use (`openai`, `anthropic`, `cohere`, `ollama`, …) | `openai` |
| `OPENAI_API_KEY` | API key for OpenAI (if using OpenAI) | `sk-...` |
| `VECTOR_STORE` | Vector store implementation (`faiss`, `pinecone`, `chroma`) | `faiss` |
| `FAISS_INDEX_PATH` | Path to the persisted FAISS index (if using FAISS) | `./data/faiss.index` |
| `TOP_K` | Number of retrieved documents per query | `4` |
| `STREAMING` | Enable token streaming (`true`/`false`) | `true` |

All variables are defined in `src/config.py` using `pydantic.BaseSettings` for type safety.

---

## Adding Your Own Data

1. **Prepare documents** – any plain‑text, PDF, Markdown, or CSV file.
2. **Run the ingestion script**:

```bash
python scripts/ingest.py --source ./data/my_documents --store faiss --index_path ./data/faiss.index
```

The script:
- Loads files via LangChain's `DocumentLoaders`.
- Splits them into chunks (`RecursiveCharacterTextSplitter`).
- Embeds chunks using the configured embedding model.
- Persists the vector store for later retrieval.

3. **Restart the API** to load the new index.

---

## Testing

The project includes unit tests for the core RAG pipeline.

```bash
pytest -q
```

Coverage is measured with `pytest-cov`.  PRs should maintain at least **80 %** overall coverage.

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository and clone your fork.
2. Create a feature branch:
   ```bash
   git checkout -b feat/your-feature-name
   ```
3. Make your changes, ensuring that:
   - Code follows the existing style (black, isort, flake8).
   - New functionality is covered by tests.
   - The README is updated if you add public‑facing features.
4. Run the test suite and linting tools:
   ```bash
   pre-commit run --all-files
   ```
5. Open a Pull Request with a clear description of the change.

See `CONTRIBUTING.md` for detailed guidelines.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- **LangChain** – for the powerful abstractions that make RAG simple.
- The open‑source community for vector‑store and embedding models.
