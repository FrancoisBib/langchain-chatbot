# LangChain Chatbot

## Overview

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a conversational AI built on top of **[LangChain](https://python.langchain.com/)**. It demonstrates how to combine large language models (LLMs) with **Retrieval‑Augmented Generation (RAG)** pipelines to create a chatbot that can:

- Understand user intent and maintain context across turns.
- Retrieve relevant documents from a vector store to ground responses in factual data.
- Be easily customized with different LLM providers, vector stores, and document loaders.

The project is intentionally lightweight so developers can focus on the core concepts of building a RAG‑enabled chatbot while still providing a solid foundation for production‑grade extensions.

---

## Table of Contents

1. [Features](#features)
2. [Quick Start](#quick-start)
3. [Architecture Overview](#architecture-overview)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Running the Bot](#running-the-bot)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)

---

## Features

- **LLM‑agnostic** – works with OpenAI, Anthropic, Cohere, HuggingFace, etc.
- **Pluggable vector stores** – FAISS, Chroma, Pinecone, Weaviate, etc.
- **Document loaders** – supports PDF, TXT, Markdown, CSV, and web scraping.
- **Conversational memory** – built‑in `ConversationBufferMemory` for multi‑turn dialogs.
- **RAG pipeline** – retrieve‑then‑generate flow with configurable retriever and prompt templates.
- **Docker support** – containerised development and deployment.
- **Extensible** – clear separation of concerns makes it easy to swap components.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (see Configuration section)
cp .env.example .env
# edit .env with your API keys and preferences

# Index your knowledge base (run once or when data changes)
python scripts/index_documents.py

# Start the chatbot server
python app.py
```

Open your browser at `http://localhost:8000` and start chatting!

---

## Architecture Overview

```
+-------------------+        +-------------------+        +-------------------+
|   User Interface  | <----> |   FastAPI Server  | <----> |   LangChain Core   |
+-------------------+        +-------------------+        +-------------------+
                                   |   ^
                                   |   |
                                   v   |
                         +-------------------+
                         |   Retrieval Layer |
                         +-------------------+
                                   |
                         +-------------------+
                         |   Vector Store    |
                         +-------------------+
```

1. **User Interface** – a simple HTML/JS front‑end served by FastAPI (or can be swapped for a Slack/Discord bot).
2. **FastAPI Server** – receives user messages, forwards them to the LangChain chain, and returns the LLM response.
3. **LangChain Core** – orchestrates the RAG pipeline:
   - `Retriever` fetches top‑k relevant chunks from the vector store.
   - `PromptTemplate` injects retrieved context and conversation history.
   - `LLM` generates the final answer.
4. **Vector Store** – stores embeddings of your documents; default is **FAISS** for local development.

---

## Installation

### Prerequisites
- Python **3.9** or newer
- Access to an LLM provider (OpenAI API key, Anthropic key, etc.)
- (Optional) Docker & Docker‑Compose for containerised workflow

### Dependencies
The project relies on the following key packages:
- `langchain`
- `openai` (or alternative provider SDK)
- `faiss-cpu` (or `faiss-gpu` for GPU‑accelerated indexing)
- `fastapi` & `uvicorn`
- `python-dotenv`
- `pydantic`

All dependencies are listed in `requirements.txt`. Use `pip install -r requirements.txt` to install them.

---

## Configuration

Configuration is handled via a **.env** file (loaded with `python-dotenv`). Copy the example file and fill in your values:

```dotenv
# .env
# LLM provider configuration
OPENAI_API_KEY=sk-************
# Choose model (e.g., gpt-4o, gpt-3.5-turbo)
OPENAI_MODEL=gpt-4o

# Vector store configuration (FAISS is default, no env vars needed)
# For remote stores, e.g., Pinecone:
# PINECONE_API_KEY=xxxx
# PINECONE_ENVIRONMENT=us-west1-gcp

# Retrieval settings
TOP_K=4               # number of documents retrieved per query
CHUNK_SIZE=500        # max characters per chunk when splitting docs
CHUNK_OVERLAP=50

# Server settings
HOST=0.0.0.0
PORT=8000
```

### Document Indexing
Place the documents you want the bot to know about in the `data/` directory. Supported formats include:
- `.txt`
- `.md`
- `.pdf`
- `.csv`

Run the indexing script to create embeddings and store them in the vector store:

```bash
python scripts/index_documents.py --source data/ --store faiss
```

You can change the `--store` argument to `chroma`, `pinecone`, etc., provided the appropriate SDK is installed and configured.

---

## Running the Bot

### Local Development
```bash
uvicorn app:app --host $HOST --port $PORT --reload
```

The API exposes two endpoints:
- `POST /chat` – body `{ "message": "..." }` returns `{ "response": "..." }`
- `GET /health` – simple health‑check.

### Docker
A `Dockerfile` and `docker-compose.yml` are provided for containerised execution.

```bash
# Build the image
docker compose build

# Run the container (will also index docs on startup)
docker compose up -d
```

The service will be reachable at `http://localhost:8000`.

---

## Testing

Unit and integration tests live in the `tests/` directory and use **pytest**.

```bash
pip install -r requirements-dev.txt
pytest
```

Key test scenarios cover:
- Retrieval correctness (top‑k relevance)
- Prompt rendering with context
- End‑to‑end API responses

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository and create a feature branch.
2. Ensure code style with `ruff`/`black` and run tests.
3. Add or update documentation as needed.
4. Open a Pull Request describing the change and linking any related issues.

### Development Workflow
```bash
# Clone your fork
git clone https://github.com/<your‑username>/langchain-chatbot.git
cd langchain-chatbot

# Create a new branch
git checkout -b feature/awesome‑feature

# Make changes, then run lint & tests
ruff check .
black .
pytest

# Commit & push
git commit -m "feat: add awesome feature"
git push origin feature/awesome‑feature
```

Please see `CONTRIBUTING.md` for detailed guidelines.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- The LangChain community for the powerful abstractions that make RAG pipelines approachable.
- OpenAI, Anthropic, and other LLM providers for their APIs.
- Contributors of the underlying vector‑store libraries (FAISS, Chroma, Pinecone, etc.).

---

*Happy building!*