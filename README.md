# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

## Overview

This repository provides a **minimal yet production‑ready** example of a chatbot built on top of **[LangChain](https://github.com/langchain-ai/langchain)**.  The bot demonstrates how to combine:

* **Large Language Models (LLMs)** for natural‑language generation.
* **Vector stores** for semantic retrieval.
* **Retrieval‑Augmented Generation (RAG)** to ground responses in external knowledge.

The code is deliberately lightweight so that developers can focus on the core concepts – extending it to more complex pipelines (multi‑turn memory, tool‑use, custom prompts, etc.) is straightforward.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Chatbot](#running-the-chatbot)
- [Project Structure](#project-structure)
- [Extending the Bot](#extending-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline**: Retrieve relevant documents from a vector store and feed them to an LLM.
- **Modular components**: Separate modules for document ingestion, embedding, retrieval, and chat UI.
- **Support for multiple LLM providers** (OpenAI, Anthropic, HuggingFace, etc.) via LangChain's `LLM` abstraction.
- **Config‑driven**: All runtime options (model name, temperature, vector store path, etc.) are defined in a single `config.yaml`.
- **Docker support**: Build and run the bot in an isolated container.
- **Unit tests** covering ingestion, retrieval, and response generation.

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | ≥ 3.9   |
| pip         | latest  |
| Docker (optional) | >= 20.10 |
| OpenAI API key (or alternative LLM credentials) | – |

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot
```

### 2. Create a virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. (Optional) Build the Docker image
```bash
docker build -t langchain‑chatbot .
```

---

## Configuration

All configurable parameters live in **`config.yaml`**.  A minimal example:

```yaml
llm:
  provider: openai          # openai | anthropic | huggingface
  model_name: gpt-4o-mini   # model identifier
  temperature: 0.2
  api_key: ${OPENAI_API_KEY}

vector_store:
  type: chroma               # chroma | faiss | pinecone
  persist_directory: ./data/vector_store

retriever:
  k: 4                       # number of top‑k documents to retrieve

ingest:
  source_path: ./data/docs   # folder containing markdown / txt files
  chunk_size: 500
  chunk_overlap: 50
```

> **Tip**: Use environment variables for secrets (`OPENAI_API_KEY`) – the file supports `${VAR_NAME}` syntax.

---

## Running the Chatbot

### 1. Ingest documents (run once or when data changes)
```bash
python -m src.ingest
```
This will:
1. Load files from `config.yaml → ingest.source_path`.
2. Split them into chunks.
3. Compute embeddings (default: `OpenAIEmbeddings`).
4. Store them in the configured vector store.

### 2. Start the interactive CLI
```bash
python -m src.chat_cli
```
You will be prompted with `>`.  Type a question and the bot will retrieve relevant passages and generate a response.

### 3. (Optional) Run the FastAPI UI
```bash
uvicorn src.api:app --reload
```
Open `http://127.0.0.1:8000/docs` for the Swagger UI or `http://127.0.0.1:8000` for a simple HTML chat page.

---

## Project Structure

```
langchain-chatbot/
├─ data/                     # Sample documents & vector store persistence
├─ src/
│   ├─ __init__.py
│   ├─ ingest.py            # Document ingestion & vector store creation
│   ├─ chat_cli.py          # Command‑line interface
│   ├─ api.py               # FastAPI wrapper (optional UI)
│   ├─ rag.py               # Core RAG pipeline (retriever + LLM chain)
│   └─ utils.py             # Helper functions (config loading, logging)
├─ tests/                    # Unit tests
├─ .env.example              # Example environment file
├─ config.yaml               # Default configuration
├─ requirements.txt
├─ Dockerfile
└─ README.md                # <-- you are reading it!
```

---

## Extending the Bot

### Add a new document source
1. Implement a loader in `src/ingest.py` (LangChain provides `DirectoryLoader`, `PyPDFLoader`, etc.).
2. Update `config.yaml → ingest.source_path` or add a new section for the source.

### Switch to a different embedding model
Modify the `Embedding` class construction in `src.rag.RAGChain` – LangChain supports `HuggingFaceEmbeddings`, `CohereEmbeddings`, etc.

### Use a different vector store
Replace the `Chroma` client with `FAISS`, `Weaviate`, or a cloud provider.  Only the initialization code in `rag.py` needs to change.

### Add memory for multi‑turn conversations
LangChain’s `ConversationBufferMemory` can be injected into the chain:
```python
from langchain.memory import ConversationBufferMemory
memory = ConversationBufferMemory()
chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    memory=memory,
)
```

---

## Testing

Run the test suite with:
```bash
pytest -v
```
Tests cover:
- Document loading and chunking.
- Vector‑store persistence.
- Retrieval correctness (top‑k).
- End‑to‑end response generation (mocked LLM).

---

## Contributing

Contributions are welcome!  Follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write code and accompanying tests.
4. Ensure the test suite passes.
5. Open a Pull Request with a clear description of the change.

Please adhere to the existing code style (black, isort, flake8) and update the documentation when adding new functionality.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- The **LangChain** community for the excellent abstractions.
- OpenAI / Anthropic / HuggingFace for providing powerful LLM APIs.
- The contributors of the underlying vector‑store libraries (Chroma, FAISS, etc.).

---

*Happy coding!*
