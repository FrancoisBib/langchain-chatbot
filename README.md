# LangChain Chatbot

**LangChain‑Chatbot** is a lightweight, extensible reference implementation of a Retrieval‑Augmented Generation (RAG) chatbot built on top of **[LangChain](https://github.com/langchain-ai/langchain)**.  It demonstrates how to combine LLMs, vector stores, and custom tooling to build conversational agents that can answer questions with up‑to‑date, domain‑specific knowledge.

---

## Table of Contents

1. [Features](#features)
2. [Quick Start](#quick-start)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Demo](#running-the-demo)
3. [Project Structure](#project-structure)
4. [How It Works](#how-it-works)
   - [Retrieval‑Augmented Generation (RAG)](#retrieval-augmented-generation-rag)
   - [Key LangChain Components](#key-langchain-components)
5. [Customization Guide](#customization-guide)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [License](#license)
9. [Acknowledgements](#acknowledgements)

---

## Features

- **Modular architecture** – swap out LLM providers, vector stores, or document loaders with a single line change.
- **RAG pipeline** – ingest documents, embed them, store embeddings in a vector DB, and retrieve relevant chunks at query time.
- **Streaming responses** – optional token‑wise streaming for a more chat‑like experience.
- **Prompt templating** – safe, reusable prompt templates powered by LangChain's `PromptTemplate`.
- **Extensible tooling** – easy integration of custom tools (e.g., web search, calculator) via LangChain `Tool` interface.
- **Docker support** – containerised development and deployment.

---

## Quick Start

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | >=3.9   |
| pip         | latest  |
| Docker (optional) | >=20.10 |
| OpenAI API key (or alternative LLM provider) |

You also need access to a vector store. The default configuration uses **FAISS** (in‑memory) for simplicity, but you can switch to **Pinecone**, **Weaviate**, **Chroma**, etc.

### Installation

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
```

### Running the Demo

1. **Set your environment variables** – create a `.env` file at the project root:

```dotenv
# .env
OPENAI_API_KEY=sk-...   # or set any other LLM provider variables
```

2. **Ingest sample documents** (only needed the first time):

```bash
python scripts/ingest.py --source data/
```

3. **Start the chatbot**:

```bash
python app.py
```

Open your browser at `http://localhost:8000` (or the port you configured) and start chatting!

---

## Project Structure

```
langchain-chatbot/
├─ app.py                 # FastAPI server exposing the chat endpoint
├─ chain.py               # Core LangChain RAG chain definition
├─ prompts/               # Prompt templates (system, user, etc.)
│   └─ chat_prompt.txt
├─ scripts/               # Utility scripts (ingest, evaluate, etc.)
│   └─ ingest.py
├─ tests/                 # Unit and integration tests
│   └─ test_chain.py
├─ requirements.txt       # Python dependencies
├─ Dockerfile             # Container build definition
└─ README.md              # <‑‑ you are here
```

---

## How It Works

### Retrieval‑Augmented Generation (RAG)

1. **Document Loading** – `scripts/ingest.py` walks a directory, loads supported file types (PDF, TXT, Markdown, CSV) using LangChain `DocumentLoaders`.
2. **Embedding** – Each document chunk is transformed into a dense vector using an OpenAI embedding model (or any `Embedding` compatible with LangChain).
3. **Vector Store** – Vectors are persisted in a vector DB (FAISS by default).  At query time the store returns the *k* most similar chunks.
4. **LLM Generation** – Retrieved chunks are injected into a prompt template and passed to the LLM, producing a context‑aware answer.

The entire flow is encapsulated in `chain.RagChain` which can be instantiated with custom components.

### Key LangChain Components

| Component | Role |
|-----------|------|
| `DocumentLoader` | Reads raw files and splits them into `Document` objects. |
| `TextSplitter` | Breaks large documents into manageable chunks (e.g., 1,000 tokens). |
| `Embedding` | Converts text chunks to vectors. |
| `VectorStore` | Stores embeddings and performs similarity search. |
| `PromptTemplate` | Defines the system‑level instruction and how retrieved context is presented to the LLM. |
| `LLM` | Generates the final answer (OpenAI `ChatOpenAI`, Azure, Anthropic, etc.). |
| `Tool` (optional) | Extends the agent with external capabilities (e.g., web search). |

---

## Customization Guide

### Swapping the LLM

```python
from langchain.llms import OpenAI
# Replace with AzureOpenAI, Anthropic, etc.
llm = OpenAI(model_name="gpt-4o-mini", temperature=0.2)
```

### Using a Different Vector Store

```python
from langchain.vectorstores import Pinecone
vectorstore = Pinecone.from_documents(
    docs, embedding, index_name="my-index"
)
```

### Adding a New Document Source

Create a loader subclass or use an existing one, then update `scripts/ingest.py`:

```python
from langchain.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://example.com/article")
```

### Extending the Prompt

Edit `prompts/chat_prompt.txt`.  The file uses Jinja‑style placeholders:

```
{{context}}
Question: {{question}}
Answer:
```

You can add system‑level instructions (e.g., tone, length limits) without touching the Python code.

---

## Testing

Run the test suite with:

```bash
pytest -v
```

The repository includes:
- Unit tests for the RAG chain (`tests/test_chain.py`).
- Integration tests that spin up a temporary FAISS store.

Add new tests under `tests/` to cover custom loaders, alternative vector stores, or tool integrations.

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository** and clone your fork.
2. **Create a feature branch** (`git checkout -b feat/your-feature`).
3. **Write code** and add/modify tests.
4. **Run the full test suite** (`pytest`).
5. **Submit a Pull Request** with a clear description of the change.

### Code Style

- Use **black** for formatting (`black .`).
- Type hints are required for public functions.
- Keep the public API stable; deprecate only with a major version bump.

### Documentation

If you add new functionality, update the relevant sections of this README and, when appropriate, add docstrings and examples in the code.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- The **LangChain** community for the excellent abstractions that make RAG pipelines straightforward.
- **FAISS**, **Pinecone**, **Weaviate**, and other vector‑store projects for open‑source similarity search.
- Contributors of the original LangChain examples that inspired this repository.

---

*Happy building!*