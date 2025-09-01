# LangChain Chatbot

## Overview

`langchain-chatbot` is a minimal yet extensible example of building a **retrieval‑augmented generation (RAG) chatbot** using the **LangChain** framework. The project demonstrates how to:

- Connect a language model (LLM) to a vector store for document retrieval.
- Create a conversational chain that combines retrieved context with the LLM's generative capabilities.
- Deploy the chatbot locally via a simple FastAPI server (or as a Streamlit UI).
- Run unit tests and linting to keep the codebase healthy.

The repository is intentionally lightweight so that developers can copy‑paste the pattern into their own applications, while still providing a solid foundation for more advanced use‑cases (e.g., multi‑retriever pipelines, custom prompt templates, or streaming responses).

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Project Structure](#project-structure)
- [Development & Testing](#development--testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline** built with LangChain's `RetrievalQA` chain.
- Support for **OpenAI**, **Anthropic**, **Cohere**, and any compatible **LLM** via LangChain's `ChatModel` interface.
- **FAISS** in‑memory vector store (plug‑and‑play) with optional persistence to disk.
- Simple **FastAPI** endpoint (`/chat`) for programmatic access.
- Optional **Streamlit** UI (`streamlit run app.py`) for interactive exploration.
- Dockerfile for containerised deployment.
- Comprehensive unit tests using **pytest**.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python | `>=3.9` |
| pip | latest |
| OpenAI API key (or other LLM provider key) | – |
| (Optional) Docker | latest |

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # on Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

If you prefer using **Poetry**:

```bash
poetry install
```

---

## Configuration

The bot reads configuration from environment variables. Create a `.env` file at the project root:

```dotenv
# LLM provider – choose one of: openai, anthropic, cohere, azure
LLM_PROVIDER=openai

# Provider‑specific keys
OPENAI_API_KEY=sk-*****
# ANTHROPIC_API_KEY=...
# COHERE_API_KEY=...

# Vector store persistence (optional)
FAISS_INDEX_PATH=./faiss_index

# Retrieval settings
TOP_K=4               # number of documents to retrieve per query
```

The project uses **python‑dotenv** to load the file automatically.

---

## Running the Bot

### 1️⃣ FastAPI server (programmatic usage)

```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

Send a POST request:

```bash
curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"question": "What is Retrieval‑Augmented Generation?"}'
```

### 2️⃣ Streamlit UI (interactive demo)

```bash
streamlit run app.py
```

### 3️⃣ Docker (containerised deployment)

```bash
# Build the image
docker build -t langchain-chatbot .

# Run the container
docker run -p 8000:8000 --env-file .env langchain-chatbot
```

---

## Project Structure

```
langchain-chatbot/
├─ app.py                 # Streamlit UI entry point
├─ server.py              # FastAPI server exposing /chat endpoint
├─ rag/
│   ├─ __init__.py
│   ├─ vector_store.py    # FAISS wrapper + persistence helpers
│   ├─ retriever.py       # LangChain retriever configuration
│   └─ chain.py           # RetrievalQA chain assembly
├─ tests/
│   └─ test_chain.py      # Pytest suite for the RAG pipeline
├─ requirements.txt
├─ pyproject.toml         # (optional) Poetry metadata
├─ .env.example           # Sample environment file
└─ README.md              # <-- you are here
```

---

## Development & Testing

### Linting & Formatting

```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

### Running Tests

```bash
pytest -vv
```

The test suite mocks the LLM and vector store, ensuring the chain logic works without external API calls.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write clean, documented code and add/adjust tests as needed.
4. Run the full test suite and ensure linting passes.
5. Open a Pull Request with a clear description of the changes.

See `CONTRIBUTING.md` for detailed guidelines on coding standards, commit messages, and release process.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- **LangChain** – the core framework powering the RAG pipeline.
- **FAISS** – fast similarity search library used for the vector store.
- **FastAPI** & **Streamlit** – for lightweight serving and UI.

---

*Happy building!*