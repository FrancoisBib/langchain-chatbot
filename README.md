# LangChain Chatbot

## Overview

**LangChain‑Chatbot** is a lightweight, extensible starter kit for building conversational agents powered by **LangChain** and **Retrieval‑Augmented Generation (RAG)**.  It demonstrates how to:

- Connect a large language model (LLM) to a knowledge base.
- Retrieve relevant documents with **vector stores**.
- Combine retrieved context with the LLM prompt to generate accurate, up‑to‑date answers.
- Deploy the bot locally or to a cloud environment.

The repository is intentionally minimal so you can focus on the core concepts and extend the code to suit your own use‑case (e.g., multi‑modal inputs, custom retrievers, streaming responses, etc.).

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LangChain integration** – leverages LangChain’s `LLMChain`, `RetrievalQA`, and `ConversationalRetrievalChain` utilities.
- **RAG pipeline** – uses a vector store (FAISS by default) to retrieve relevant chunks from a document collection.
- **Modular design** – separate modules for data ingestion, indexing, retrieval, and chat UI.
- **Config‑driven** – all model, vector‑store, and UI settings are defined in a single `config.yaml`.
- **Docker support** – build and run the bot in an isolated container.
- **Extensible** – plug‑in alternative LLM providers (OpenAI, Anthropic, Ollama, etc.) or custom retrievers with minimal code changes.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | >=3.9   |
| pip         | latest  |
| Docker (optional) | >=20.10 |
| OpenAI API key (or alternative LLM credentials) | – |

You also need a set of documents (PDF, TXT, Markdown, etc.) that will serve as the knowledge base for the RAG component.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

If you prefer Docker:

```bash
docker build -t langchain‑chatbot .
```

---

## Quick Start

1. **Add your documents** to the `data/` directory.
2. **Create an `.env` file** with your API keys (see `.env.example`).
3. **Index the documents** (creates the vector store):
   ```bash
   python scripts/index_documents.py
   ```
4. **Run the chatbot**:
   ```bash
   python app.py
   ```
5. Open your browser at `http://localhost:8000` and start chatting!

---

## Project Structure

```
langchain-chatbot/
│
├─ app.py                     # FastAPI entry‑point & UI server
├─ config.yaml                # Central configuration file
├─ requirements.txt           # Python dependencies
├─ Dockerfile                 # Container definition
│
├─ data/                      # Your raw documents (PDF, txt, md…)
│   └─ *.pdf
│
├─ docs/                      # Generated documentation (optional)
│
├─ scripts/
│   ├─ ingest.py              # Load raw files into LangChain Document objects
│   └─ index_documents.py     # Build / update the FAISS vector store
│
├─ src/
│   ├─ llm.py                 # Wrapper around the chosen LLM provider
│   ├─ retriever.py           # Vector store and similarity search logic
│   └─ chatbot.py             # High‑level RAG chain (RetrievalQA + memory)
│
└─ tests/
    └─ test_chatbot.py        # Basic unit / integration tests
```

---

## Configuration

All configurable parameters live in `config.yaml`.  Example:

```yaml
llm:
  provider: openai          # openai | anthropic | ollama | custom
  model_name: gpt-4o-mini
  temperature: 0.2

vector_store:
  type: faiss
  embedding_model: text-embedding-3-large
  index_path: ./vector_store/faiss.index

retrieval:
  top_k: 4
  search_type: similarity

chat:
  memory_window: 5          # number of previous turns kept in context
  system_prompt: |
    You are a helpful assistant that answers questions using the provided knowledge base.
```

Update the values to match your environment.  The `llm.provider` field determines which client class in `src/llm.py` is instantiated.

---

## Running the Bot

### Development mode

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Production (Docker)

```bash
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=$OPENAI_API_KEY \
  langchain-chatbot
```

The API follows the OpenAI chat‑completion schema, making it easy to swap the front‑end (e.g., Streamlit, Next.js) if desired.

---

## Testing

```bash
pytest -v
```

The test suite covers:
- Document ingestion & chunking
- Vector‑store creation and similarity search
- End‑to‑end RAG chain execution
- API response format

Add new tests in `tests/` when extending functionality.

---

## Contributing

Contributions are welcome!  Please follow these steps:

1. **Fork the repository** and create a feature branch.
2. **Write clear commit messages** – follow the conventional‑commits style.
3. **Add or update documentation** in the README or inline docstrings.
4. **Run the test suite** (`pytest`) and ensure all checks pass.
5. **Open a Pull Request** targeting the `main` branch.

For large changes, open an issue first to discuss the design.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- **LangChain** – for the modular LLM and RAG abstractions.
- **FAISS** – fast similarity search.
- **FastAPI** – lightweight API server.
- Community contributors who helped shape this starter kit.
