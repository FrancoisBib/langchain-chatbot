# LangChain Chatbot

## Overview

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a conversational AI assistant built on top of **[LangChain](https://github.com/langchain-ai/langchain)**.  It demonstrates how to combine:

- **Large Language Models (LLMs)** for natural‑language generation.
- **Retrieval‑Augmented Generation (RAG)** pipelines that fetch relevant context from external knowledge sources.
- **Tool‑use** (e.g., web search, calculator) to extend the bot’s capabilities.

The repository is intended for developers who want a clear, production‑ready starting point for building custom chatbots, as well as for contributors interested in extending the example with new data sources, agents, or UI components.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Bot](#running-the-bot)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [RAG Workflow Explained](#rag-workflow-explained)
- [Extending the Bot](#extending-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Modular RAG pipeline** – interchangeable retrievers (FAISS, Chroma, Elastic, etc.) and vector stores.
- **Support for multiple LLM providers** – OpenAI, Anthropic, Cohere, HuggingFace, etc.
- **Tool integration** – built‑in calculator, web‑search, and custom Python functions.
- **Streaming chat UI** – optional FastAPI + WebSocket front‑end.
- **Docker support** – reproducible environment for local development and CI.
- **Comprehensive tests** – unit and integration tests using `pytest`.
- **CI/CD** – GitHub Actions workflow for linting, type‑checking, and testing.

---

## Quick Start

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | `>=3.9,<4.0` |
| pip | latest (recommended via `python -m pip install --upgrade pip`) |
| Docker (optional) | `>=20.10` |
| OpenAI API key (or alternative LLM provider) | – |

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .[all]
```

The optional `all` extra installs the full stack (FAISS, OpenAI, FastAPI, etc.).  See `pyproject.toml` for the complete list.

### Running the Bot

1. **Set environment variables** – create a `.env` file in the project root:
   ```dotenv
   OPENAI_API_KEY=sk-xxxxxxx
   # Optional: other provider keys (ANTHROPIC_API_KEY, COHERE_API_KEY, ...)
   ```
2. **Start the FastAPI server** (provides a simple web UI and a REST endpoint):
   ```bash
   uvicorn langchain_chatbot.main:app --reload
   ```
3. Open your browser at `http://127.0.0.1:8000` and start chatting!

If you prefer a pure CLI experience:

```bash
python -m langchain_chatbot.cli
```

---

## Project Structure

```
langchain-chatbot/
├─ langchain_chatbot/          # Core package
│  ├─ __init__.py
│  ├─ agents/                 # Agent implementations (conversational, tool‑using)
│  ├─ retrieval/              # Vector store & retriever abstractions
│  ├─ llm/                    # Wrapper classes for supported LLMs
│  ├─ tools/                  # Built‑in tool definitions (calculator, search)
│  ├─ ui/                     # FastAPI routes & optional React front‑end
│  └─ main.py                 # Entry point for the API server
├─ tests/                     # Pytest suite
├─ scripts/                   # Helper scripts (data ingestion, index building)
├─ Dockerfile                 # Multi‑stage build for production image
├─ pyproject.toml             # Poetry/PEP‑517 configuration
├─ README.md                  # ← This file
└─ .github/                   # CI workflows
```

---

## Configuration

Configuration is handled via **Pydantic Settings** (`langchain_chatbot.settings.Settings`).  All settings can be overridden through environment variables or a `.env` file.

Key settings include:

- `LLM_PROVIDER` – `openai`, `anthropic`, `cohere`, `hf` (default: `openai`).
- `VECTOR_STORE` – `faiss`, `chroma`, `elastic` (default: `faiss`).
- `RETRIEVER_TOP_K` – number of retrieved documents per query (default: `4`).
- `MAX_TOKENS` – generation limit for the LLM.
- `USE_STREAMING` – enable token‑by‑token streaming to the UI.

---

## RAG Workflow Explained

1. **Document Ingestion** – Use `scripts/ingest.py` to load raw text, PDFs, or markdown files into a vector store.
2. **Embedding Generation** – Embeddings are computed with the same provider as the LLM (e.g., `text-embedding-ada-002`).
3. **Retrieval** – At query time, the retriever fetches the top‑k most similar chunks.
4. **Prompt Construction** – Retrieved chunks are injected into a **system prompt** that instructs the LLM to ground its answer in the provided context.
5. **Generation** – The LLM produces a response, optionally streaming tokens back to the client.
6. **Tool Invocation** – If the LLM decides a tool is needed (e.g., calculator), the `AgentExecutor` runs the tool and feeds the result back into the next generation step.

The architecture follows LangChain’s **`ConversationalRetrievalChain`** pattern, but the code is deliberately kept modular so you can swap any component.

---

## Extending the Bot

### Adding a New Data Source

1. Write an ingestion script that yields `Document` objects (`langchain.schema.Document`).
2. Register the script in `scripts/__init__.py` and add a CLI entry point if desired.
3. Update `settings.py` to include any new environment variables (e.g., `S3_BUCKET`).

### Implementing a Custom Tool

```python
from langchain.tools import BaseTool

class WeatherTool(BaseTool):
    name = "weather"
    description = "Get the current weather for a given city."

    def _run(self, city: str) -> str:
        # Call external API or mock response
        return f"The weather in {city} is sunny, 23°C."
```

Add the tool to `langchain_chatbot.tools.__init__` and include it in the `AgentExecutor` construction inside `agents/conversational.py`.

---

## Testing

Run the full test suite with:

```bash
pytest -q
```

The repository includes:

- **Unit tests** for each module (`tests/unit/`).
- **Integration tests** that spin up an in‑memory FAISS store and mock LLM responses (`tests/integration/`).
- **Linting & type‑checking** via `ruff` and `mypy` (executed in CI).

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository and clone your fork.
2. Create a **feature branch**: `git checkout -b feat/your-feature`.
3. Ensure the code passes all checks:
   ```bash
   pre-commit run --all-files
   pytest
   ```
4. Open a **Pull Request** with a clear description of the change and reference any related issue.
5. Make sure to update the documentation (README, docstrings) when adding new functionality.

See `CONTRIBUTING.md` for detailed guidelines on coding standards, commit messages, and the release process.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- The **LangChain** community for the powerful abstractions that make RAG pipelines straightforward.
- Open‑source vector store projects (FAISS, Chroma) for fast similarity search.
- All contributors who help improve the example and keep it up‑to‑date with the latest LangChain releases.
