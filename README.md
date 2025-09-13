# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/downloads/)

A **modular, extensible** chatbot built on **[LangChain](https://github.com/hwchase17/langchain)** that demonstrates **Retrieval‑Augmented Generation (RAG)**.  The project showcases how to combine LLMs, vector stores, and custom tools to build production‑ready conversational agents.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Demo](#running-the-demo)
- [Configuration](#configuration)
- [Extending the Bot](#extending-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline**: retrieve relevant documents from a vector store and feed them to an LLM for context‑aware responses.
- **Multiple LLM back‑ends**: OpenAI, Anthropic, Cohere, Ollama, etc. (configured via environment variables).
- **Pluggable vector stores**: FAISS, Chroma, Pinecone, Weaviate – switch with a single config flag.
- **Tool integration**: custom tools (e.g., web search, calculator) can be added to the LangChain `Agent`.
- **Streaming responses**: optional server‑sent events for real‑time UI updates.
- **Docker support**: containerised development and deployment.
- **Extensive tests**: unit & integration tests with `pytest` and `pytest‑asyncio`.

---

## Architecture Overview

```
+-------------------+      +-------------------+      +-------------------+
|   User Interface  | ---> |   LangChain      | ---> |   Vector Store    |
| (FastAPI/Streamlit|      |   Agent (RAG)    |      | (FAISS/Chroma…)   |
+-------------------+      +-------------------+      +-------------------+
          ^                         |
          |                         v
          |                 +-------------------+
          +-----------------+   LLM Provider   |
                            (OpenAI, etc.)
```

1. **Input** – The UI sends a user message to the FastAPI endpoint.
2. **Retriever** – LangChain fetches the top‑k relevant chunks from the vector store.
3. **Prompt** – The retrieved context is injected into a prompt template.
4. **LLM** – The LLM generates a response, optionally using tools.
5. **Output** – The response streams back to the UI.

---

## Quick Start

### Prerequisites

- Python **3.9+**
- An OpenAI API key (or any supported LLM provider key)
- Optional: Docker & Docker‑Compose if you prefer containerised execution

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Tip**: Use `pip install -e .` if you plan to develop the package locally.

### Environment variables

Create a `.env` file in the project root:

```dotenv
# LLM provider (openai, anthropic, cohere, ollama, ...)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxxxx

# Vector store configuration (FAISS is default)
VECTOR_STORE=faiss
FAISS_INDEX_PATH=./data/faiss.index

# Retrieval settings
TOP_K=4

# FastAPI settings
HOST=0.0.0.0
PORT=8000
```

### Running the Demo

```bash
# Start the FastAPI server (auto‑reload in dev mode)
uvicorn app.main:app --reload --host $HOST --port $PORT
```

Open your browser at `http://localhost:8000/docs` to explore the OpenAPI UI or integrate the frontend of your choice (e.g., Streamlit, React).

---

## Configuration

All runtime options are driven by environment variables (see `.env.example`).  Key sections:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | Which LLM backend to use. Supported: `openai`, `anthropic`, `cohere`, `ollama` | `openai` |
| `TOP_K` | Number of documents retrieved per query. | `4` |
| `VECTOR_STORE` | Vector store implementation. | `faiss` |
| `FAISS_INDEX_PATH` | Path to the persisted FAISS index. | `./data/faiss.index` |
| `CHROMA_PERSIST_DIR` | Directory for Chroma persistence (if used). | `./data/chroma` |

Advanced settings (e.g., temperature, max tokens) can be overridden by adding `LLM_TEMPERATURE`, `LLM_MAX_TOKENS`, etc., following the naming convention used in `app/config.py`.

---

## Extending the Bot

### Adding a New Retriever

1. Implement a class inheriting from `langchain.vectorstores.base.VectorStore`.
2. Register it in `app/retrievers/__init__.py`.
3. Add a corresponding environment variable option in `app/config.py`.

### Adding a Custom Tool

```python
from langchain.tools import BaseTool

class MathTool(BaseTool):
    name = "math"
    description = "Performs basic arithmetic operations."

    def _run(self, expression: str) -> str:
        # Simple safe eval – replace with a proper parser for production
        return str(eval(expression))
```

Add the tool to the agent factory (`app/agent_factory.py`) and expose a toggle via an env var.

---

## Testing

```bash
# Run the full test suite
pytest -v
```

The repository includes:
- Unit tests for each component (`tests/unit/`)
- Integration tests that spin up an in‑memory FAISS store (`tests/integration/`)
- Fixtures for mock LLM responses using `langchain.llms.fake.FakeLLM`.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write tests for any new functionality.
4. Ensure the test suite passes (`pytest`).
5. Submit a Pull Request with a clear description of the change.

### Code Style

- Use **black** for formatting (`black .`).
- Lint with **ruff** (`ruff check .`).
- Type‑check with **mypy** (`mypy .`).

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
