# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B%20%7C%20PyPI-blue.svg)](https://pypi.org/project/langchain/)

A minimal yet production‑ready example of a **conversational AI** built on **[LangChain](https://github.com/langchain-ai/langchain)** that leverages **Retrieval‑Augmented Generation (RAG)**.  The bot can answer questions over a custom knowledge base, keep context across turns, and be easily extended with new data sources or LLM providers.

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline** – combine a vector store (FAISS) with a large language model (LLM) to answer queries using your own documents.
- **Conversation memory** – `ConversationBufferMemory` keeps chat history so the bot can reference previous turns.
- **Modular design** – replace the LLM, embedding model, or vector store with a single line change.
- **CLI & Streamlit UI** – run the bot from the terminal or launch a simple web UI.
- **Docker support** – containerised for easy deployment.

---

## Prerequisites

- Python **3.9+**
- An OpenAI API key (or any other LLM provider supported by LangChain)
- Optional: `git` if you want to clone the repository

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

If you prefer Docker:

```bash
docker build -t langchain-chatbot .
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8501:8501 langchain-chatbot
```

---

## Quick Start

### 1️⃣ Prepare your knowledge base

Place any **.txt**, **.pdf**, or **.md** files you want the bot to know about in the `data/` directory.

```bash
# Example: copy sample documents
cp examples/*.pdf data/
```

### 2️⃣ Build the vector store

```bash
python scripts/build_vector_store.py
```

This script reads the files, creates embeddings (using `OpenAIEmbeddings` by default), and stores them in a FAISS index (`faiss_index.pkl`).

### 3️⃣ Launch the chatbot

#### CLI version

```bash
python app/cli_chat.py
```

#### Streamlit UI

```bash
streamlit run app/streamlit_chat.py
```

You can now ask questions like:

```
> What is the purpose of LangChain?
```

The bot will retrieve the most relevant passages, feed them to the LLM, and return a concise answer.

---

## Project Structure

```
langchain-chatbot/
├─ app/                     # Entry points (CLI, Streamlit UI)
│   ├─ cli_chat.py          # Simple REPL chatbot
│   └─ streamlit_chat.py    # Web UI with Streamlit
├─ data/                    # Your raw documents go here
├─ scripts/                 # Utility scripts (vector store building, evaluation)
│   └─ build_vector_store.py
├─ src/                     # Core LangChain components
│   ├─ rag.py               # RAG pipeline (retriever + LLM chain)
│   └─ memory.py            # Conversation memory wrapper
├─ tests/                   # Unit / integration tests
│   └─ test_rag.py
├─ requirements.txt         # Python dependencies
├─ Dockerfile               # Container definition
└─ README.md                # <‑‑ you are here
```

---

## How It Works

1. **Document Loader** – LangChain loaders (`TextLoader`, `PDFMinerLoader`, …) read the files in `data/`.
2. **Chunking** – `RecursiveCharacterTextSplitter` splits each document into manageable chunks (default: 1000 characters, overlap 200).
3. **Embedding** – Each chunk is transformed into a dense vector using an embedding model (`OpenAIEmbeddings` by default).
4. **Vector Store** – Vectors are persisted in FAISS for fast similarity search.
5. **Retriever** – `FAISSRetriever` fetches the top‑k most relevant chunks for a user query.
6. **LLM Chain** – The retrieved context is injected into a prompt template and sent to the LLM (`ChatOpenAI`).
7. **Memory** – `ConversationBufferMemory` appends each interaction, enabling multi‑turn conversations.

---

## Configuration

All configurable options live in `src/config.py`.  Override them via environment variables or a `.env` file.

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI secret key | – |
| `EMBEDDING_MODEL` | Embedding model name (e.g., `text-embedding-ada-002`) | `text-embedding-ada-002` |
| `LLM_MODEL` | Chat model for generation (e.g., `gpt-3.5-turbo`) | `gpt-3.5-turbo` |
| `TOP_K` | Number of retrieved chunks per query | `4` |
| `CHUNK_SIZE` | Size of text chunks (characters) | `1000` |
| `CHUNK_OVERLAP` | Overlap between chunks (characters) | `200` |

Example `.env`:

```dotenv
OPENAI_API_KEY=sk-************************
EMBEDDING_MODEL=text-embedding-ada-002
LLM_MODEL=gpt-3.5-turbo
TOP_K=4
```

---

## Running Tests

```bash
pytest -v
```

The test suite covers vector‑store creation, retrieval relevance, and the end‑to‑end RAG chain.

---

## Contributing

We welcome contributions!  Follow these steps:

1. **Fork** the repository and clone your fork.
2. Create a **feature branch** (`git checkout -b feat/your-feature`).
3. Install the development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Make your changes, add tests, and ensure the test suite passes.
5. Open a **Pull Request** with a clear description of the change.

Please adhere to the existing code style (Black, isort, flake8) and update the documentation when adding new features.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
