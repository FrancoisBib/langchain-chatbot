# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/downloads/)
[![LangChain](https://img.shields.io/badge/LangChain-0.1.0-orange.svg)](https://github.com/langchain-ai/langchain)

A minimal, production‑ready reference implementation of a **chatbot** built on **[LangChain](https://github.com/langchain-ai/langchain)** that leverages **Retrieval‑Augmented Generation (RAG)** to answer questions over arbitrary document collections.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Demo](#running-the-demo)
- [Configuration](#configuration)
- [Development & Contribution](#development--contribution)
- [Testing](#testing)
- [License](#license)

---

## Features

- **RAG pipeline**: Combine a vector store (FAISS, Chroma, Pinecone, …) with a language model to retrieve relevant chunks and generate context‑aware answers.
- **Modular design**: Swap out LLMs, embeddings, or vector stores with a single line change.
- **Streaming UI**: Optional Streamlit interface for real‑time chat.
- **Extensible prompts**: Prompt templates are stored in `prompts/` and can be customized without code changes.
- **Docker support**: Build and run the whole stack in containers for reproducibility.
- **Comprehensive tests**: Unit and integration tests using `pytest` and `langchain‑test` utilities.

---

## Architecture Overview

```mermaid
graph LR
    subgraph User
        UI[Streamlit UI / CLI]
    end
    subgraph Core
        LLM[LLM (OpenAI / Ollama / HuggingFace)]
        EMB[Embedding Model]
        VS[Vector Store]
        RAG[Retrieval‑Augmented Generation Chain]
    end
    UI -->|question| RAG
    RAG -->|retrieve| VS
    VS -->|embeddings| EMB
    RAG -->|generate| LLM
    LLM -->|answer| UI
```

- **LLM** – any LangChain‑compatible language model (OpenAI `gpt‑4o`, Anthropic, Ollama, etc.).
- **Embedding Model** – `sentence‑transformers/all‑mpnet‑base‑v2` by default, but configurable.
- **Vector Store** – FAISS for local development; can be replaced by Chroma, Pinecone, Weaviate, etc.
- **RAG Chain** – `RetrievalQA` chain with a custom prompt that injects retrieved documents.

---

## Quick Start

### Prerequisites

- Python **3.9+**
- `pip` (or `uv` / `poetry` if preferred)
- An OpenAI API key **or** a locally hosted LLM (Ollama, Llama.cpp, etc.)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Tip**: For GPU‑accelerated embeddings you can install `torch` with the appropriate CUDA version before installing the rest of the requirements.

### Running the Demo

1. **Prepare a document collection** – place any `.txt`, `.pdf`, `.md` files inside `data/`.
2. **Create the vector store**:

```bash
python scripts/build_index.py --source data/ --store faiss
```

3. **Start the chat UI** (Streamlit) or the CLI:

```bash
# Streamlit UI (default on http://localhost:8501)
streamlit run app.py

# OR CLI mode
python -m chatbot.cli
```

You can now ask questions and the bot will retrieve the most relevant passages and generate an answer.

---

## Configuration

All configurable parameters live in `config.yaml`. Example:

```yaml
llm:
  provider: openai            # openai | ollama | huggingface
  model_name: gpt-4o
  temperature: 0.0

embeddings:
  provider: sentence_transformers
  model_name: all-mpnet-base-v2

vector_store:
  type: faiss                # faiss | chroma | pinecone
  index_path: ./vector_store/faiss_index

retrieval:
  top_k: 4
  search_type: similarity

prompt:
  template_path: prompts/rag_prompt.txt
```

You can override any field via environment variables prefixed with `CHATBOT_` (e.g., `CHATBOT_LLM_MODEL_NAME`). The `config.py` module loads the file using `pydantic` for type safety.

---

## Development & Contribution

1. **Fork the repository** and create a feature branch.
2. **Install development dependencies**:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

3. **Run the test suite** to ensure everything passes:

```bash
pytest -q
```

4. **Add documentation** – any new module should have a docstring and, if relevant, an entry in the `README` under *Features* or *Configuration*.
5. **Submit a Pull Request** – make sure CI passes and that you have updated the changelog (`CHANGELOG.md`).

### Code Style

- Follow **PEP 8** and **Black** formatting.
- Type hints are required for all public functions.
- Use `logging` instead of `print` for runtime messages.

---

## Testing

The repository includes unit tests for each component (LLM wrapper, vector store adapter, RAG chain) located in `tests/`. Integration tests spin up a temporary FAISS index and use a mock LLM to verify end‑to‑end behaviour.

Run all tests with coverage:

```bash
pytest --cov=chatbot
```

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **LangChain** – for the powerful abstractions that make building RAG pipelines straightforward.
- **Sentence‑Transformers** – for high‑quality open‑source embeddings.
- The open‑source community for providing free vector‑store back‑ends (FAISS, Chroma) and LLMs.
