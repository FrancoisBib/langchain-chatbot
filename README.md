# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

Welcome to **langchain‑chatbot**, a minimal yet extensible example of building a conversational AI using **LangChain**, **OpenAI** (or any compatible LLM), and **vector‑store retrieval** for Retrieval‑Augmented Generation (RAG).

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Bot](#running-the-bot)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LangChain**‑driven pipeline: prompt templating, LLM wrappers, and memory management.
- **RAG** support using a vector store (FAISS, Chroma, Pinecone, etc.) to retrieve relevant documents at query time.
- **Modular design** – swap LLMs, embeddings, or vector stores with a single line change.
- **CLI** and **FastAPI** interfaces for quick prototyping and integration.
- **Extensible** – add custom tools, callbacks, or chain components.

---

## Architecture Overview

```
User Input → Prompt Template → LLM
                ↑            |
                |            ↓
          Retriever ← Vector Store ← Documents
```

1. **Retriever** fetches the top‑k most relevant document chunks from the vector store.
2. Retrieved snippets are injected into the prompt template.
3. The LLM generates a response that is **augmented** with the retrieved context, improving factuality and relevance.

---

## Getting Started

### Prerequisites

- Python **3.9** or newer.
- An OpenAI API key (or another LLM provider supported by LangChain).
- (Optional) A vector‑store service account if you prefer a hosted solution (e.g., Pinecone).

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

Create a `.env` file at the project root with the following variables:

```dotenv
# OpenAI (or other) LLM configuration
OPENAI_API_KEY=sk-...
# Choose an embedding model – OpenAI, Cohere, HuggingFace, etc.
EMBEDDING_MODEL=text-embedding-ada-002

# Vector store selection (FAISS is default, others require additional keys)
VECTOR_STORE=faiss   # options: faiss | chroma | pinecone
# Pinecone example (if used)
PINECONE_API_KEY=...
PINECONE_ENV=us-west1-gcp
```

The application reads these variables via `python‑dotenv`.

### Running the Bot

#### CLI mode

```bash
python -m chatbot.cli --docs path/to/documents/
```

- `--docs` points to a directory containing plain‑text (`.txt`) or markdown (`.md`) files that will be indexed.
- The first run builds the vector store; subsequent runs reuse the persisted index.

#### FastAPI server (optional)

```bash
uvicorn chatbot.api:app --reload
```

The API exposes a single endpoint:

- `POST /chat` – body `{ "message": "Your question" }`
- Returns `{ "response": "LLM answer" }`

---

## Usage Examples

```python
from chatbot.chain import get_chat_chain

# Initialise the chain (loads vector store, embeddings, LLM)
chat = get_chat_chain()

# Simple interaction
response = chat.run("Explain the difference between supervised and unsupervised learning.")
print(response)
```

**RAG in action** – the bot will retrieve relevant sections from the indexed documents (e.g., a PDF of a machine‑learning textbook) and incorporate them into the answer.

---

## Project Structure

```
langchain-chatbot/
├─ chatbot/                # Core package
│   ├─ __init__.py
│   ├─ chain.py            # LangChain chain construction
│   ├─ retriever.py        # Vector‑store wrapper
│   ├─ llm.py              # LLM provider abstraction
│   ├─ cli.py              # Command‑line interface
│   └─ api.py              # FastAPI endpoints (optional)
├─ data/                   # Sample documents (git‑ignored)
├─ tests/                  # Unit and integration tests
├─ .env.example            # Template for environment variables
├─ requirements.txt
├─ README.md               # ← this file
└─ setup.cfg               # linting / formatting configuration
```

---

## Testing

The project uses **pytest**. To run the test suite:

```bash
pytest -q
```

Tests cover:
- Vector‑store indexing and retrieval.
- Prompt templating.
- End‑to‑end chain execution with a mock LLM.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository and clone your fork.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Install the development dependencies: `pip install -r requirements-dev.txt`.
4. Write tests for new functionality.
5. Ensure code passes linting (`ruff check .`) and formatting (`ruff format .`).
6. Open a **Pull Request** with a clear description of the change.

> **Note**: Keep the focus on LangChain, RAG, and chatbot‑related improvements. Non‑relevant features will be closed.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

*Happy building with LangChain!*