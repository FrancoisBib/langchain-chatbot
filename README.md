# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A minimal yet production‑ready example of a **chatbot** built on top of **[LangChain](https://github.com/hwchase17/langchain)** that leverages **Retrieval‑Augmented Generation (RAG)**.  The bot can answer questions over a custom document collection while preserving the conversational context.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start (Local Development)](#quick-start-local-development)
- [Running with Docker](#running-with-docker)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LangChain** pipelines for LLM, prompt management and memory.
- **RAG**: documents are indexed with **FAISS** (or any vector store) and retrieved at query time.
- **Chat history** persisted via LangChain's `ConversationBufferMemory`.
- **Modular**: swap LLM providers (OpenAI, Anthropic, Ollama, etc.) and vector stores with a single line change.
- **Dockerised** for reproducible environments.
- Comprehensive **type‑hints** and **unit tests**.

---

## Architecture Overview

```
User Query → LangChain PromptTemplate → LLM
                ↑                     ↓
          Retrieval (FAISS) ←─ Context (retrieved docs)
                ↑
          Vector Store (FAISS) ←─ Document Loader (txt, pdf, md…)
```

1. **Document ingestion** – `scripts/ingest.py` loads source files, splits them into chunks, embeds them with the chosen embedding model and stores the vectors in FAISS.
2. **Chat loop** – `app/chat.py` builds a `ConversationalRetrievalChain` that:
   - Retrieves the most relevant chunks for the current question.
   - Supplies those chunks to the LLM together with the conversation history.
   - Returns the answer and updates the memory.

---

## Quick Start (Local Development)

### Prerequisites

- Python **3.10** or newer
- An LLM API key (e.g., `OPENAI_API_KEY`).  The README assumes OpenAI, but any LangChain‑compatible provider works.

### 1. Clone the repository

```bash
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot
```

### 2. Install dependencies

We use **Poetry** for deterministic builds, but a `requirements.txt` is also provided.

```bash
# Using Poetry (recommended)
poetry install
# Or with pip
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file at the project root (or export variables manually):

```dotenv
# LLM provider – currently supported: openai, anthropic, ollama
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...   # required if LLM_PROVIDER=openai
# Embedding model – defaults to OpenAI text‑embedding‑ada-002
EMBEDDING_MODEL=text-embedding-ada-002
# Optional: customize FAISS index path
FAISS_INDEX_PATH=./data/faiss.index
```

### 4. Ingest your documents

Place any `.txt`, `.pdf`, `.md` or `.docx` files inside the `data/source/` directory, then run:

```bash
python scripts/ingest.py
```

This will create a FAISS index at the path defined in `FAISS_INDEX_PATH`.

### 5. Start the chatbot

```bash
python app/chat.py
```

You will be dropped into an interactive REPL.  Type your question and press **Enter**.  The bot will retrieve relevant passages and answer using the LLM.

---

## Running with Docker

A multi‑stage Dockerfile is provided for reproducibility.

```bash
# Build the image
docker build -t langchain-chatbot .

# Run the container (replace <your‑key> with a real key or mount a .env file)
docker run -e OPENAI_API_KEY=<your-key> -v $(pwd)/data:/app/data langchain-chatbot python app/chat.py
```

You can also mount a custom `.env` file:

```bash
docker run --env-file .env -v $(pwd)/data:/app/data langchain-chatbot python app/chat.py
```

---

## Configuration

All runtime options are driven by environment variables.  The most common ones are listed below:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_PROVIDER` | Which LLM backend to use (`openai`, `anthropic`, `ollama`, …). | `openai` |
| `OPENAI_API_KEY` | API key for OpenAI (required if `LLM_PROVIDER=openai`). | – |
| `EMBEDDING_MODEL` | Embedding model name. | `text-embedding-ada-002` |
| `FAISS_INDEX_PATH` | Path to the persisted FAISS index. | `./data/faiss.index` |
| `CHUNK_SIZE` | Size of text chunks (in characters) for ingestion. | `1000` |
| `CHUNK_OVERLAP` | Overlap between consecutive chunks. | `200` |

Additional providers can be added by extending `app/config.py` – see the contribution guidelines.

---

## Testing

Unit tests are located in the `tests/` folder and use **pytest**.

```bash
pytest -q
```

CI pipelines (GitHub Actions) run the test suite on every push.

---

## Contributing

Contributions are welcome!  Please follow these steps:

1. **Fork** the repository and create a feature branch.
2. Install development dependencies (`poetry install` includes `pytest`, `black`, `isort`).
3. Add or modify code **with type hints** and **docstrings**.
4. Run the test suite and ensure linting passes:
   ```bash
   black . && isort . && pytest
   ```
5. Open a **Pull Request** targeting the `main` branch.  Include a short description of the change and, if applicable, update the README.

See `CONTRIBUTING.md` for the full guidelines.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
