# LangChain Chatbot

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A **LangChain** based chatbot that demonstrates **Retrieval‑Augmented Generation (RAG)** using various vector stores and LLM providers.  The project is structured to be easy to extend, test, and contribute to.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Bot](#running-the-bot)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LangChain** integration for chain orchestration.
- **RAG** pipeline: retrieve relevant documents → augment prompt → generate answer.
- Support for multiple LLM back‑ends (OpenAI, Anthropic, HuggingFace, etc.).
- Pluggable vector stores (FAISS, Chroma, Pinecone, Milvus, etc.).
- Simple CLI and optional FastAPI web UI.
- Dockerfile for reproducible container builds.
- Comprehensive test suite with `pytest`.

---

## Architecture Overview

```
+-------------------+        +-------------------+        +-------------------+
|  User Input       |  -->   |  Retrieval Chain  |  -->   |  LLM Generation   |
+-------------------+        +-------------------+        +-------------------+
        |                              ^                         |
        |                              |                         |
        v                              |                         v
+-------------------+        +-------------------+        +-------------------+
|  Prompt Builder   | <---- |  Document Store   | <---- |  Vector Store      |
+-------------------+        +-------------------+        +-------------------+
```

1. **Prompt Builder** – Formats the retrieved context and user query into a prompt compatible with the chosen LLM.
2. **Retrieval Chain** – Uses LangChain's `Retriever` to fetch top‑k documents from the vector store.
3. **LLM Generation** – Calls the LLM API to produce a response.
4. **Document Store** – Optional persistent storage (e.g., SQLite, PostgreSQL) for raw documents.

---

## Getting Started

### Prerequisites

- Python **3.9** or newer
- An LLM API key (e.g., OpenAI `OPENAI_API_KEY`)
- Optional: Docker if you prefer containerised execution

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

> **Tip**: Use `pip install -e .` if you plan to develop locally; it installs the package in editable mode.

### Running the Bot

#### CLI Mode

```bash
export OPENAI_API_KEY=sk-*****   # set your LLM key
python -m langchain_chatbot.cli --source data/documents
```

- `--source` points to a folder containing plain‑text or PDF files that will be indexed.
- The CLI will build the vector store (FAISS by default) and start an interactive REPL.

#### FastAPI Web UI (optional)

```bash
uvicorn langchain_chatbot.api:app --reload
```

Open `http://127.0.0.1:8000/docs` for the Swagger UI.

---

## Configuration

Configuration is handled via **pydantic** settings (`langchain_chatbot.settings.Settings`).  Environment variables are the preferred way to override defaults:

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | – |
| `LLM_PROVIDER` | `openai`, `anthropic`, `huggingface` | `openai` |
| `VECTOR_STORE` | `faiss`, `chroma`, `pinecone` | `faiss` |
| `TOP_K` | Number of retrieved documents | `4` |
| `EMBEDDING_MODEL` | Embedding model name (e.g., `text-embedding-ada-002`) | `text-embedding-ada-002` |

You can also create a `.env` file at the project root:

```dotenv
OPENAI_API_KEY=sk-*****
LLM_PROVIDER=openai
VECTOR_STORE=faiss
TOP_K=5
```

---

## Usage Examples

### Basic Interaction (CLI)

```text
> Hello, who is Albert Einstein?

[Retrieving relevant documents...]
[Generating answer...]
Albert Einstein (1879‑1955) was a theoretical physicist known for the theory of relativity...
```

### Programmatic Access

```python
from langchain_chatbot.core import Chatbot
from langchain_chatbot.settings import Settings

settings = Settings()
bot = Chatbot(settings)

response = bot.ask("Explain quantum entanglement in simple terms.")
print(response)
```

---

## Testing

```bash
# Run the full test suite
pytest -v
```

The repository includes unit tests for the retrieval chain, prompt builder, and LLM wrappers.  Use the `tests/fixtures` directory to add custom documents for integration tests.

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write tests for new functionality.
4. Ensure all tests pass (`pytest`).
5. Open a Pull Request with a clear description of the changes.

Please adhere to the existing code style (black, isort, flake8) and update the documentation when adding new features.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
