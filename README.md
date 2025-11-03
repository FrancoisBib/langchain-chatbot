# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/downloads/)

A minimal yet extensible reference implementation of a **chatbot powered by LangChain** that demonstrates **Retrieval‑Augmented Generation (RAG)**.  The project showcases how to:

* Connect a large language model (LLM) via LangChain.
* Index and retrieve documents using vector stores.
* Combine retrieved context with the LLM to produce grounded, up‑to‑date answers.
* Deploy the bot locally or as a simple FastAPI service.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Bot](#running-the-bot)
6. [Project Structure](#project-structure)
7. [Testing](#testing)
8. [Contributing](#contributing)
9. [License](#license)

---

## Features

- **LangChain integration** – Leverages LangChain's `LLMChain`, `RetrievalQA`, and `PromptTemplate` utilities.
- **Vector store support** – Out‑of‑the‑box with **FAISS**; can be swapped for Pinecone, Weaviate, etc.
- **Document loaders** – Includes loaders for Markdown, PDF, and plain text.
- **Modular design** – Easy to replace the LLM, vector store, or retrieval strategy.
- **FastAPI endpoint** – Optional HTTP API for remote usage.
- **Docker ready** – `Dockerfile` and `docker-compose.yml` provided for containerised deployment.

---

## Prerequisites

- Python **3.9** or newer.
- An OpenAI API key (or any other LLM provider supported by LangChain).
- Optional: `git` and `docker` if you wish to build the container image.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

If you prefer Docker:

```bash
docker compose up --build
```

---

## Configuration

Create a `.env` file at the project root with the following variables:

```dotenv
# LLM provider – currently supports OpenAI and HuggingFace
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx

# Vector store – default is FAISS (local). Change to pinecone, weaviate, etc.
VECTOR_STORE=faiss

# Path to the document directory that will be indexed
DOCS_PATH=./data
```

You can also override the default prompt template by editing `prompts/custom_prompt.txt`.

---

## Running the Bot

### 1️⃣ Index your knowledge base

```bash
python scripts/index_documents.py --source ./data
```

The script walks through the `DOCS_PATH` directory, loads supported file types, creates embeddings using the configured LLM, and persists the FAISS index to `./index`.

### 2️⃣ Start the interactive CLI

```bash
python -m langchain_chatbot.cli
```

You will be prompted for a question; the bot will retrieve relevant passages and generate a response.

### 3️⃣ (Optional) Run the FastAPI server

```bash
uvicorn langchain_chatbot.api:app --host 0.0.0.0 --port 8000
```

Send a POST request to `http://localhost:8000/chat` with JSON payload:

```json
{ "question": "Explain RAG in simple terms." }
```

---

## Project Structure

```
langchain-chatbot/
├─ data/                     # Sample documents (markdown, pdf, txt)
├─ index/                    # Persisted vector store
├─ langchain_chatbot/        # Core package
│   ├─ __init__.py
│   ├─ api.py                # FastAPI endpoints
│   ├─ cli.py                # Command‑line interface
│   ├─ rag.py                # Retrieval‑augmented generation logic
│   └─ utils.py              # Helper functions (loaders, embeddings)
├─ prompts/                  # Prompt templates
│   └─ custom_prompt.txt
├─ scripts/                  # Utility scripts (indexing, evaluation)
│   └─ index_documents.py
├─ tests/                    # Unit and integration tests
├─ .env.example              # Example environment file
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
└─ README.md                 # ← This file
```

---

## Testing

```bash
pytest -v
```

The test suite covers:
- Document loading and chunking.
- Vector store creation and similarity search.
- End‑to‑end RAG pipeline with a mock LLM.

---

## Contributing

Contributions are welcome! Follow these steps:

1. **Fork** the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Ensure code style with `ruff` (or `flake8`).
4. Write tests for new functionality.
5. Submit a **Pull Request** with a clear description of the changes.

Please read the [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md) and [CONTRIBUTING](CONTRIBUTING.md) guidelines before submitting.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
