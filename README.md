# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-%233776AB.svg)](https://www.python.org/)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Advanced Usage (RAG)](#advanced-usage-rag)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

`langchain-chatbot` is a minimal yet extensible reference implementation of a conversational AI assistant built on **LangChain**. It demonstrates how to combine:

- **LLM back‑ends** (OpenAI, Anthropic, Ollama, …) via LangChain's `ChatModel`
- **Prompt engineering** with LangChain `ChatPromptTemplate`
- **Retrieval‑Augmented Generation (RAG)** using vector stores (FAISS, Chroma, Pinecone, etc.)
- **Tool calling** and **function calling** for dynamic actions

The repository is intentionally lightweight so developers can fork, extend, or integrate it into larger systems.

---

## Features

- ✅ **Modular design** – separate modules for LLM, prompts, memory, and retrievers.
- ✅ **RAG pipeline** – seamless integration with any LangChain vector store.
- ✅ **Config‑driven** – all runtime options live in a single `config.yaml`.
- ✅ **Docker support** – run the bot locally or in production with a single command.
- ✅ **Unit & integration tests** – CI ready out of the box.
- ✅ **Extensible** – add custom tools, agents, or retrieval strategies with minimal code changes.

---

## Architecture

```
+-------------------+        +-------------------+        +-------------------+
|  User Interface   | <----> |   FastAPI Server  | <----> |   LangChain Core   |
+-------------------+        +-------------------+        +-------------------+
                                 |   ^   |
                                 |   |   |
                                 v   |   v
                        +---------------------------+
                        | Retrieval (Vector Store) |
                        +---------------------------+
```

1. **FastAPI** exposes `/chat` and `/rag` endpoints.
2. **LangChain Core** builds the prompt, calls the LLM, and optionally retrieves context.
3. **Vector Store** (FAISS by default) holds document embeddings for RAG.
4. **Memory** (ConversationBufferMemory) preserves chat history across turns.

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment
python -m venv .venv && source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set your API keys (OpenAI example)
export OPENAI_API_KEY=sk-****

# Run the server
uvicorn app.main:app --reload
```

Open your browser at `http://127.0.0.1:8000/docs` to interact with the auto‑generated Swagger UI.

---

## Installation

### Prerequisites
- Python **3.9** or newer
- An LLM provider API key (OpenAI, Anthropic, etc.)
- (Optional) `docker` and `docker‑compose` for containerised deployment

### Pip installation
```bash
pip install -e .   # installs the package in editable mode
```

### Docker (optional)
```bash
docker compose up --build
```
The container reads the same `config.yaml` (mounted as a volume).

---

## Configuration

All configurable values are stored in **`config.yaml`**:

```yaml
llm:
  provider: openai          # or anthropic, ollama, etc.
  model: gpt-4o-mini
  temperature: 0.7

retriever:
  type: faiss               # faiss, chroma, pinecone, etc.
  index_path: ./data/faiss_index
  top_k: 5

memory:
  type: buffer
  window_size: 10

api_keys:
  openai: ${OPENAI_API_KEY}
```

You can override any key with environment variables – LangChain's `Settings` class loads them automatically.

---

## Running the Bot

### Standard chat (no retrieval)
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, who are you?"}'
```

### Chat with RAG (retrieval‑augmented)
```bash
curl -X POST http://127.0.0.1:8000/rag \
  -H "Content-Type: application/json" \
  -d '{"message": "Explain the difference between supervised and unsupervised learning."}'
```

The `/rag` endpoint first retrieves the most relevant chunks from the vector store, injects them into the prompt, and then calls the LLM.

---

## Advanced Usage (RAG)

1. **Indexing documents** – place your `.txt`, `.pdf`, or `.md` files under `data/documents/` and run:
   ```bash
   python scripts/create_index.py
   ```
   This script uses `RecursiveCharacterTextSplitter`, `OpenAIEmbeddings`, and stores the index at the path defined in `config.yaml`.

2. **Custom retriever** – implement a class inheriting from `BaseRetriever` and register it in `app/retriever_factory.py`.

3. **Hybrid search** – combine vector similarity with keyword BM25 by setting:
   ```yaml
   retriever:
     type: hybrid
     vector_weight: 0.7
     keyword_weight: 0.3
   ```

---

## Testing

```bash
pytest -v
```
The test suite covers:
- Prompt generation
- LLM wrapper (mocked)
- Retrieval pipeline
- API endpoint responses

---

## Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write tests for new functionality.
4. Ensure `black` and `isort` formatting (`make fmt`).
5. Open a Pull Request with a clear description of the change.

See `CONTRIBUTING.md` for detailed guidelines.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## Acknowledgements

- **LangChain** – the core library that powers the LLM orchestration.
- **FAISS** – for fast similarity search.
- **FastAPI** – for the lightweight API layer.
- Community contributors for ideas, bug reports, and PRs.

---

*Happy building!*