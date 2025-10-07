# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/downloads/)

A minimal yet extensible **Chatbot** built on top of **[LangChain](https://github.com/langchain-ai/langchain)** that demonstrates **Retrieval‑Augmented Generation (RAG)**.  The bot can:
- ingest arbitrary documents (PDF, txt, markdown, CSV, …),
- index them with a vector store (FAISS, Chroma, Pinecone, …),
- retrieve relevant passages at query time,
- generate context‑aware responses using any LLM supported by LangChain.

---

## Table of Contents

1. [Features](#features)
2. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Configuration](#configuration)
   - [Running the Bot](#running-the-bot)
3. [Project Structure](#project-structure)
4. [Usage Examples](#usage-examples)
5. [Extending / Customising](#extending--customising)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)
9. [Acknowledgements](#acknowledgements)

---

## Features

- **RAG pipeline**: Document ingestion → Embedding → Vector store → Retrieval → LLM generation.
- **Modular design**: Swap out LLMs, embeddings, or vector stores with a single line change.
- **CLI & API**: Interact via command‑line or integrate the `Chatbot` class in your own FastAPI/Flask app.
- **Docker support**: Build and run the whole stack in containers for reproducibility.
- **Unit tests** with `pytest` covering ingestion, retrieval and generation.

---

## Getting Started

### Prerequisites

| Tool | Minimum Version |
|------|-----------------|
| Python | 3.9 |
| pip | 22.0 |
| Docker (optional) | 20.10 |

You also need an OpenAI API key (or any other LLM provider key) and, if you use a remote vector store, the corresponding credentials.

### Installation

```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

If you prefer Docker:

```bash
docker compose up --build
```

### Configuration

Create a `.env` file in the project root and set the required variables:

```dotenv
# LLM provider – currently supported: openai, anthropic, huggingface
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-***

# Embedding model – e.g., text-embedding-ada-002 (OpenAI) or sentence‑transformers
EMBEDDING_MODEL=text-embedding-ada-002

# Vector store – faiss (local), chroma, pinecone, weaviate, etc.
VECTOR_STORE=faiss
FAISS_INDEX_PATH=./data/faiss_index

# Optional: path to the folder containing documents to ingest
DOCS_PATH=./data/docs
```

The bot will automatically fall back to sensible defaults (FAISS locally stored in `./data/faiss_index`).

### Running the Bot

#### 1. Ingest documents (once or when you add new data)

```bash
python -m chatbot.ingest --source ./data/docs
```

This command:
- walks the `DOCS_PATH` directory,
- extracts plain text from supported file types,
- creates embeddings using the configured model,
- stores them in the chosen vector store.

#### 2. Start an interactive chat session

```bash
python -m chatbot.cli
```

You will be prompted for a question; the bot retrieves the most relevant passages and generates a response.

#### 3. Use as a library

```python
from chatbot.core import Chatbot

bot = Chatbot()
answer = bot.ask("Explain the difference between supervised and unsupervised learning.")
print(answer)
```

---

## Project Structure

```
langchain-chatbot/
│
├─ chatbot/                 # Core package
│   ├─ __init__.py
│   ├─ core.py              # High‑level Chatbot class
│   ├─ ingest.py            # Document ingestion utilities
│   ├─ retrieval.py         # Vector‑store wrappers
│   ├─ generation.py        # LLM wrapper
│   └─ cli.py               # Command‑line interface
│
├─ data/                    # Sample documents & FAISS index (git‑ignored)
│
├─ tests/                   # pytest suite
│   ├─ test_ingest.py
│   ├─ test_retrieval.py
│   └─ test_generation.py
│
├─ .env.example             # Template for environment variables
├─ requirements.txt
├─ Dockerfile
├─ docker-compose.yml
└─ README.md                # <-- This file
```

---

## Usage Examples

### Simple Q&A

```bash
$ python -m chatbot.cli
> What are the key benefits of RAG?

Retrieval‑Augmented Generation allows the model to:
- Access up‑to‑date factual information.
- Reduce hallucinations by grounding responses in real documents.
- Scale to large knowledge bases without fine‑tuning the LLM.
```

### Programmatic Access (FastAPI example)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from chatbot.core import Chatbot

app = FastAPI()
bot = Chatbot()

class Query(BaseModel):
    question: str

@app.post("/chat")
async def chat(query: Query):
    try:
        answer = bot.ask(query.question)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

## Extending / Customising

The architecture follows the **Strategy pattern** – each component (LLM, Embedding, VectorStore) implements a small interface.  To replace a component:

```python
from chatbot.core import Chatbot
from langchain.llms import HuggingFaceHub
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

custom_bot = Chatbot(
    llm=HuggingFaceHub(repo_id="google/flan-t5-xl"),
    embedder=HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"),
    vectorstore=Chroma(collection_name="my_docs")
)
```

You can also implement your own `DocumentLoader` (e.g., for Notion, Confluence) and register it in `chatbot.ingest`.

---

## Testing

Run the test suite with:

```bash
pytest -vv
```

The tests cover:
- Document parsing for supported formats.
- Embedding generation and vector‑store insertion.
- Retrieval relevance (basic sanity checks).
- End‑to‑end generation using a mock LLM.

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository and clone your fork.
2. Create a **feature branch** (`git checkout -b feat/your-feature`).
3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Make your changes, add tests, and ensure the full test suite passes.
5. Run the linter and formatter:
   ```bash
   black . && flake8
   ```
6. Commit with a clear message and push to your fork.
7. Open a **Pull Request** targeting `main`.

Please read our [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- The **LangChain** community for providing the building blocks.
- **FAISS**, **Chroma**, **Pinecone** for vector‑store implementations.
- OpenAI / Anthropic / HuggingFace for the LLM APIs used in examples.

---

*Happy building with LangChain!*