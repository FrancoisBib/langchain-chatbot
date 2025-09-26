# LangChain Chatbot

## Overview

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a conversational AI assistant built with **[LangChain](https://python.langchain.com/)**.  It demonstrates how to combine large language models (LLMs) with **Retrieval‑Augmented Generation (RAG)** pipelines, enabling the bot to answer questions using both its internal knowledge and external document sources.

The repository showcases:
- Integration of LLMs (OpenAI, Anthropic, etc.) via LangChain.
- Vector‑store based retrieval (FAISS, Chroma, Pinecone, …).
- A clean, modular architecture that is easy to extend or replace components.
- Example scripts for running the chatbot locally or deploying it as a FastAPI service.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
  - [CLI Demo](#cli-demo)
  - [FastAPI Server](#fastapi-server)
- [Project Structure](#project-structure)
- [Extending the Bot](#extending-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LLM‑agnostic**: Swap between OpenAI, Anthropic, Cohere, HuggingFace, etc.
- **RAG pipeline**: Retrieve relevant chunks from a vector store and feed them to the LLM.
- **Modular components**:
  - `DocumentLoader` – load PDFs, Markdown, plain text, or web pages.
  - `VectorStore` – plug‑in FAISS, Chroma, Pinecone, Weaviate, etc.
  - `PromptTemplate` – customise system and user prompts.
- **Streaming output** – optional token‑by‑token streaming for a responsive UI.
- **FastAPI integration** – expose a `/chat` endpoint for web or mobile front‑ends.
- **Docker support** – ready‑to‑run container for reproducible environments.

---

## Getting Started

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | `>=3.9` |
| pip         | latest  |
| Docker (optional) | latest |

You will also need an API key for the LLM provider you intend to use (e.g., `OPENAI_API_KEY`).

### Installation

```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file at the project root (or export the variables in your shell). Example:

```dotenv
# LLM provider – choose one of: openai, anthropic, cohere, huggingface
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-***
# Optional: model name (default is gpt‑3.5‑turbo)
OPENAI_MODEL=gpt-4o-mini

# Vector store configuration (FAISS is default, no env vars needed)
VECTOR_STORE=faiss

# Document source – directory containing .txt/.md/.pdf files
DOCS_PATH=./data
```

---

## Running the Bot

### CLI Demo

A quick interactive console is provided for experimentation:

```bash
python -m chatbot.cli
```

You will be prompted for a question; the bot will retrieve relevant documents, augment the prompt, and stream the answer.

### FastAPI Server

To expose the chatbot as a REST endpoint:

```bash
uvicorn chatbot.api:app --host 0.0.0.0 --port 8000
```

The API accepts a JSON payload:

```json
{ "question": "What is Retrieval‑Augmented Generation?" }
```

Response format:

```json
{
  "answer": "...",
  "sources": ["doc1.pdf", "doc2.txt"]
}
```

---

## Project Structure

```
langchain-chatbot/
├─ chatbot/                     # Core package
│   ├─ __init__.py
│   ├─ config.py               # Loads .env variables
│   ├─ loaders/                # Document loaders (PDF, Markdown, etc.)
│   ├─ vectorstores/           # FAISS, Chroma, Pinecone adapters
│   ├─ pipelines/              # RAG pipeline orchestration
│   ├─ prompts/                # PromptTemplate definitions
│   ├─ cli.py                  # Interactive command‑line interface
│   └─ api.py                  # FastAPI application
├─ data/                        # Example documents for the demo
├─ tests/                       # Unit and integration tests
├─ Dockerfile
├─ requirements.txt
├─ .env.example
└─ README.md
```

---

## Extending the Bot

### Adding a New Document Loader
1. Create a class in `chatbot/loaders/` that inherits from `BaseLoader`.
2. Implement `load()` returning a list of `Document` objects.
3. Register the loader in `chatbot/config.py` under `LOADER_CLASS`.

### Switching Vector Stores
Replace the `VECTOR_STORE` env variable with one of the supported backends (`chroma`, `pinecone`, `weaviate`). Ensure the corresponding Python client library is added to `requirements.txt`.

### Custom Prompt Templates
Edit or add files in `chatbot/prompts/`. The `PromptTemplate` is instantiated in `pipelines/rag_pipeline.py`. You can reference retrieved documents via the `{context}` placeholder.

---

## Testing

```bash
pytest -q
```

The test suite covers:
- Loader correctness for the supported file types.
- Vector‑store indexing and similarity search.
- End‑to‑end RAG pipeline with a mock LLM.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your‑feature`).
3. Ensure code style with `ruff` and type checking with `mypy`.
4. Add or update tests as needed.
5. Submit a pull request with a clear description of the changes.

Refer to `CONTRIBUTING.md` for detailed guidelines.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
