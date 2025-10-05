# LangChain Chatbot

## 📖 Overview

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a conversational AI assistant built on top of **[LangChain](https://github.com/langchain-ai/langchain)**. It demonstrates how to combine:

- **Large Language Models (LLMs)** for natural language generation.
- **Retrieval‑Augmented Generation (RAG)** pipelines that fetch relevant context from external knowledge sources before prompting the LLM.
- **Modular LangChain components** (chains, agents, memory, vector stores) to keep the codebase clean and easily extensible.

The repository is intended for developers who want to:

- Learn best practices for structuring a LangChain chatbot project.
- Quickly spin‑up a functional RAG‑enabled bot for prototypes or demos.
- Contribute improvements back to the community.

---

## ✨ Features

- **LLM‑agnostic** – works with OpenAI, Anthropic, Cohere, Llama‑2, etc. (any LangChain‑compatible provider).
- **RAG support** using a configurable vector store (FAISS, Chroma, Pinecone, etc.).
- **Conversation memory** (windowed or summary) to maintain context across turns.
- **Tool calling / function calling** integration for structured actions (e.g., web search, database queries).
- **Dockerised development** environment for reproducible builds.
- **Extensible architecture** – plug‑in custom retrievers, document loaders, or post‑processors with a few lines of code.

---

## 🚀 Quick Start

### Prerequisites

- Python **3.10** or newer.
- An LLM API key (e.g., `OPENAI_API_KEY`).
- (Optional) A vector‑store endpoint if you prefer a managed service.

### 1. Clone the repository

```bash
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot
```

### 2. Install dependencies

We use **Poetry** for deterministic dependency management, but a `requirements.txt` is also provided.

```bash
# Using Poetry (recommended)
poetry install
# Or with pip
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file at the project root (or export variables in your shell):

```dotenv
# LLM provider (default: openai)
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-************************
# Optional: Azure/OpenAI endpoint configuration
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=...

# Vector store configuration (FAISS is local by default)
VECTOR_STORE=faiss
# If using Pinecone, set:
# PINECONE_API_KEY=...
# PINECONE_ENVIRONMENT=...
```

### 4. Load documents (optional)

The repo ships with a small sample dataset (`data/`). To index your own documents, place them in `data/` and run:

```bash
python scripts/index_documents.py
```

This script uses LangChain loaders (PDF, TXT, Markdown, etc.) and stores embeddings in the configured vector store.

### 5. Run the chatbot

```bash
python app/main.py
```

You will be dropped into an interactive REPL where you can type queries and see the bot’s responses, enriched by retrieved context.

---

## 📂 Project Structure

```
langchain-chatbot/
├─ app/                     # FastAPI / REPL entry points
│   ├─ main.py              # CLI/REPL launcher
│   └─ api.py               # Optional FastAPI endpoints
├─ core/                    # Core LangChain abstractions
│   ├─ chatbot.py           # High‑level Chatbot class
│   ├─ rag.py               # RAG pipeline (retriever + LLM)
│   └─ memory.py           # Conversation memory utilities
├─ data/                    # Sample documents for indexing
├─ scripts/                 # Utility scripts (indexing, evaluation)
│   └─ index_documents.py
├─ tests/                   # Pytest suite
├─ .env.example             # Template for environment variables
├─ requirements.txt
├─ pyproject.toml           # Poetry config
└─ README.md                # ← You are here!
```

---

## 🛠️ Development Guide

### Running Tests

```bash
pytest -vv
```

### Linting & Formatting

```bash
# Install pre‑commit hooks
pre-commit install
# Run manually
pre-commit run --all-files
```

### Adding a New Vector Store

1. Install the provider’s Python client (e.g., `pip install pinecone-client`).
2. Implement a thin wrapper inheriting from `langchain.vectorstores.base.VectorStore`.
3. Register the wrapper in `core/rag.py` under the `VECTOR_STORE` env variable.

### Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write tests for new functionality.
4. Ensure the CI pipeline passes (`pre-commit`, `pytest`).
5. Open a Pull Request with a clear description of the change.

---

## 📚 Reference Documentation

- **LangChain Docs** – https://python.langchain.com/
- **RAG Overview** – https://python.langchain.com/docs/use_cases/rag/
- **Vector Stores** – https://python.langchain.com/docs/integrations/vectorstores/
- **Memory** – https://python.langchain.com/docs/modules/memory/

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 🙏 Acknowledgements

Thanks to the LangChain community for the excellent abstractions and to the contributors of the open‑source vector‑store backends used in this example.
