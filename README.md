# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/github/license/your-org/langchain-chatbot)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue)]
[![LangChain](https://img.shields.io/badge/LangChain-0.2%2B-green)]

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Testing](#testing)
- [Contribution Guide](#contribution-guide)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

**LangChain Chatbot** is a modular, extensible chatbot built on top of **[LangChain](https://github.com/langchain-ai/langchain)** that leverages **Retrieval‑Augmented Generation (RAG)** to provide accurate, context‑aware answers. It combines a language model (LLM) with a vector store for document retrieval, enabling the bot to ground its responses in external knowledge bases such as PDFs, Markdown files, or web‑scraped content.

The repository contains:
- A clean project scaffold using Poetry for dependency management.
- Example data loaders for common document formats.
- A configurable pipeline that ties together:
  - **Document ingestion → Embedding → Vector store**
  - **Retriever → LLM → Response generation**
- A simple FastAPI (or Flask) wrapper to expose the bot as an HTTP endpoint.

---

## Features

- **RAG‑powered**: Answers are generated from both the LLM's parametric knowledge and the retrieved documents.
- **Pluggable components**: Swap out the LLM, embedding model, or vector store (e.g., OpenAI, Anthropic, Cohere, HuggingFace, Chroma, Pinecone, Weaviate).
- **Multi‑document support**: Load PDFs, DOCX, TXT, Markdown, or plain text directories.
- **Streaming responses**: Optional token‑by‑token streaming for a more interactive UI.
- **Dockerised**: Ready‑to‑run container with minimal configuration.
- **Extensible CLI**: Manage data ingestion, re‑indexing, and bot execution from the command line.
- **Test suite**: Pytest coverage for the core pipeline and API.

---

## Architecture

```mermaid
flowchart TD
    subgraph Ingestion
        Docs[Documents] --> Loader[Loader (PDF, TXT, …)] --> Split[TextSplitter]
        Split --> Embed[Embedding Model]
        Embed --> VectorStore[Vector Store (Chroma, Pinecone, …)]
    end
    subgraph Retrieval
        Query[User Query] --> Retriever[VectorStoreRetriever]
        Retriever --> Context[Relevant Docs]
    end
    subgraph Generation
        LLM[LLM (OpenAI, Anthropic, …)] --> Response[Chatbot Reply]
        Context --> LLM
    end
    Query --> LLM
    Response --> API[FastAPI Endpoint]
```

- **Ingestion**: Documents are loaded, split into manageable chunks, embedded, and stored in a vector DB.
- **Retrieval**: The user query is embedded and used to fetch the most relevant chunks.
- **Generation**: The retrieved context is passed to the LLM as a system/user prompt, producing a grounded answer.

---

## Installation

### Prerequisites
- Python **3.9+**
- **Poetry** (recommended) or pip
- An API key for the LLM provider you intend to use (e.g., `OPENAI_API_KEY`).

### Steps
```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Install dependencies via Poetry (recommended)
poetry install
# Or with pip
# pip install -r requirements.txt
```

### Environment variables
Create a `.env` file at the project root (or export variables in your shell):
```dotenv
# LLM provider (openai, anthropic, cohere, ...)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
# Embedding model (defaults to the same provider as LLM)
EMBEDDING_MODEL=text-embedding-ada-002
# Vector store configuration (example for Chroma)
CHROMA_PERSIST_DIR=./chroma_db
```

---

## Quick Start

1. **Ingest sample data**
   ```bash
   poetry run python -m chatbot.ingest ./data/sample_docs
   ```
   This command loads all supported files under `./data/sample_docs`, creates embeddings, and persists the vector store.

2. **Run the API**
   ```bash
   poetry run uvicorn chatbot.api:app --reload
   ```
   The chatbot will be reachable at `http://127.0.0.1:8000/chat`.

3. **Test with curl**
   ```bash
   curl -X POST http://127.0.0.1:8000/chat \
        -H "Content-Type: application/json" \
        -d '{"message": "What is LangChain?"}'
   ```

You should receive a JSON response containing the bot's answer.

---

## Configuration

All runtime options are defined in `config.py` and can be overridden via environment variables.

| Variable | Description | Default |
|---|---|---|
| `LLM_PROVIDER` | Provider name (`openai`, `anthropic`, `cohere`, `huggingface`). | `openai` |
| `LLM_MODEL` | Specific model identifier (e.g., `gpt-4o`). | Provider default |
| `EMBEDDING_MODEL` | Embedding model identifier. | Provider default |
| `VECTOR_STORE` | Vector store implementation (`chroma`, `pinecone`, `weaviate`). | `chroma` |
| `CHROMA_PERSIST_DIR` | Directory where Chroma persists vectors. | `./chroma_db` |
| `TOP_K` | Number of retrieved documents per query. | `4` |
| `MAX_TOKENS` | Max tokens for LLM response. | `512` |

---

## Running the Bot

You can run the bot in three common ways:

### 1. Local development (FastAPI)
```bash
poetry run uvicorn chatbot.api:app --reload
```

### 2. Docker
```bash
# Build the image
docker build -t langchain-chatbot .
# Run the container (make sure to pass your .env file)
docker run -p 8000:8000 --env-file .env langchain-chatbot
```

### 3. CLI interaction
```bash
poetry run python -m chatbot.cli "Explain the difference between RAG and fine‑tuning."
```

---

## Testing

The project includes a pytest suite. To run tests:
```bash
poetry run pytest -v
```

Coverage reports can be generated with:
```bash
poetry run pytest --cov=chatbot
```

---

## Contribution Guide

We welcome contributions! Please follow these steps:
1. **Fork** the repository and clone your fork.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Install development dependencies (already covered by `poetry install`).
4. Write tests for any new functionality.
5. Ensure code style with `ruff`/`black` (pre‑commit hooks are provided).
6. Submit a Pull Request with a clear description of the changes.

### Code Style
- Use **black** for formatting.
- Use **ruff** for linting.
- Type hints are required for all public functions.

### Documentation
- Update this README and any relevant docstrings when adding features.
- If you add new environment variables, document them in the **Configuration** table.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **LangChain** – the backbone for chainable LLM workflows.
- **OpenAI**, **Anthropic**, **Cohere**, **Hugging Face** – for providing powerful LLM and embedding APIs.
- **Chroma**, **Pinecone**, **Weaviate** – for vector store implementations.
- Community contributors who helped shape this project.

---

*Happy building with LangChain!*