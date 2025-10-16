# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A minimal, production‑ready example of a **chatbot** built with **[LangChain](https://github.com/langchain-ai/langchain)** that leverages **Retrieval‑Augmented Generation (RAG)** to provide up‑to‑date, context‑aware answers.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline**: Combine a vector store with a language model to ground responses in your own documents.
- **Modular design**: Easy to swap out LLMs, embeddings, or vector stores.
- **Streaming UI**: Optional FastAPI + WebSocket front‑end for real‑time chat.
- **Extensible**: Hooks for custom callbacks, memory, and tool integration.
- **Docker support**: One‑command containerised deployment.

---

## Architecture Overview

```
User → FastAPI (WebSocket) → LangChain Agent
                                   │
                                   ├─ LLM (OpenAI / Ollama / Azure)
                                   └─ Retriever
                                        │
                                        └─ VectorStore (Chroma / Pinecone / FAISS)
```

1. **Retriever** fetches the most relevant chunks from the vector store.
2. **LLM** generates a response conditioned on the retrieved context.
3. **Agent** (optional) can call tools or use memory for multi‑turn conversations.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Use the provided dev container or install locally (see Installation)
make dev   # starts a Docker dev environment (optional)

# Run the chatbot locally
python -m app.main
```

Open your browser at `http://localhost:8000` and start chatting!

---

## Installation

### Prerequisites
- Python **3.10** or newer
- **Docker** (optional, for containerised workflow)
- An OpenAI API key or compatible endpoint (e.g., Ollama, Azure OpenAI)

### Using Poetry (recommended)
```bash
pip install poetry
poetry install
```

### Using pip
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Environment variables
Create a `.env` file at the project root:

```dotenv
# LLM configuration
OPENAI_API_KEY=sk-...
# OR for Ollama
OLLAMA_BASE_URL=http://localhost:11434

# Vector store configuration (example with Chroma)
CHROMA_PERSIST_DIRECTORY=./chroma_data

# Optional FastAPI settings
HOST=0.0.0.0
PORT=8000
```

---

## Configuration

The project reads configuration from **pydantic** settings located in `app/config.py`. Key options:

| Setting | Description | Default |
|---------|-------------|---------|
| `LLM_MODEL` | Identifier of the LLM (e.g., `gpt-4o`, `llama2`) | `gpt-4o` |
| `EMBEDDING_MODEL` | Embedding model used for vectorisation | `text-embedding-3-large` |
| `VECTOR_STORE` | Backend (`chroma`, `faiss`, `pinecone`) | `chroma` |
| `TOP_K` | Number of retrieved documents per query | `4` |
| `MAX_TOKENS` | Max tokens for LLM response | `512` |

You can override any setting via environment variables or by editing `app/config.py`.

---

## Running the Bot

### Development server (auto‑reload)
```bash
uvicorn app.main:app --reload --host $HOST --port $PORT
```

### Production (Gunicorn)
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

### Docker
```bash
docker build -t langchain-chatbot .
docker run -p 8000:8000 --env-file .env langchain-chatbot
```

---

## Testing

Unit and integration tests live in the `tests/` directory.
```bash
pytest -v
```

A CI workflow (GitHub Actions) runs the test suite on every push.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository.
2. Create a **feature branch** (`git checkout -b feat/your-feature`).
3. Ensure code passes linting and tests:
   ```bash
   poetry run flake8 .
   poetry run mypy .
   ```
4. Submit a **Pull Request** with a clear description of the change.
5. Include tests and update documentation when applicable.

See `CONTRIBUTING.md` for detailed guidelines.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## Acknowledgements

- **LangChain** – the backbone for building LLM‑centric applications.
- **Chroma** – lightweight vector store used in the example.
- **FastAPI** – provides the HTTP/WebSocket interface.

---

*Happy building with LangChain!*