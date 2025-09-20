# LangChain Chatbot

**A modular, Retrieval‑Augmented Generation (RAG) chatbot built with LangChain**

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Bot](#running-the-bot)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Overview

`langchain-chatbot` demonstrates how to combine **LangChain** with vector stores and LLMs to build a **Retrieval‑Augmented Generation (RAG)** chatbot. The bot retrieves relevant documents from a knowledge base, injects the retrieved context into the prompt, and generates a response with a language model.

The repository is intentionally lightweight so developers can focus on the core RAG workflow, while still providing a solid foundation for extensions such as:
- Custom document loaders (PDF, CSV, web pages, etc.)
- Alternative vector stores (FAISS, Chroma, Pinecone, etc.)
- Prompt engineering and chain customization
- Deployment (FastAPI, Streamlit, Gradio, etc.)

---

## Features

- **LangChain integration** – leverages `ChatOpenAI`, `ConversationalRetrievalChain`, and modular components.
- **Vector store** – uses FAISS by default; interchangeable with any LangChain‑compatible store.
- **Document ingestion** – simple script to load text files from a folder and embed them.
- **Configurable** – all secrets and parameters are managed through a `.env` file.
- **Testing ready** – includes unit tests for the retrieval chain and document loader.
- **Docker support** – optional `Dockerfile` for containerised execution.

---

## Architecture

```mermaid
flowchart TD
    subgraph Ingestion
        Docs[Documents Folder] -->|Load| Loader[DocumentLoader]
        Loader -->|Chunk & Embed| Embedder[Embedding Model]
        Embedder -->|Store| VectorStore[FAISS / Pinecone / …]
    end

    subgraph Runtime
        User[User Input] -->|Prompt| Chat[LLM (ChatOpenAI)]
        Chat -->|Retrieve| Retriever[VectorStoreRetriever]
        Retriever -->|Context| Chat
        Chat -->|Response| Bot[Chatbot Output]
    end
```

1. **Ingestion** – Documents are loaded, split into chunks, embedded, and persisted in a vector store.
2. **Runtime** – The user query is sent to a `ConversationalRetrievalChain`. The chain retrieves the most relevant chunks, appends them to the prompt, and the LLM generates a response.

---

## Getting Started

### Prerequisites

- Python **3.9** or newer
- An OpenAI API key (or any compatible LLM provider)
- Git

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Environment variables

Create a `.env` file at the project root:

```dotenv
OPENAI_API_KEY=sk-************************
EMBEDDING_MODEL=text-embedding-ada-002   # optional, defaults to OpenAI embeddings
VECTOR_STORE=faiss                         # can be changed to pinecone, chroma, etc.
```

### Running the Bot

```bash
# Load documents (run once or when you add new files)
python scripts/ingest.py --source data/

# Start an interactive session
python scripts/chat.py
```

You will be prompted for a question; the bot will return a response enriched with retrieved context.

---

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI secret key. | – |
| `EMBEDDING_MODEL` | Embedding model used for vectorisation. | `text-embedding-ada-002` |
| `VECTOR_STORE` | Vector store implementation (`faiss`, `chroma`, `pinecone`). | `faiss` |
| `CHUNK_SIZE` | Number of characters per chunk during ingestion. | `1000` |
| `CHUNK_OVERLAP` | Overlap between chunks to preserve context. | `200` |

All variables can be overridden at runtime via environment variables.

---

## Usage Examples

### Simple CLI interaction

```bash
python scripts/chat.py "What is the capital of France?"
```

### Integration with FastAPI

The repository includes a minimal FastAPI wrapper (`app/api.py`). To run it:

```bash
uvicorn app.api:app --reload
```

You can then POST a JSON payload:

```json
{ "question": "Explain RAG in under 100 words." }
```

### Streamlit UI (optional)

```bash
streamlit run app/streamlit_app.py
```

---

## Testing

```bash
pytest -v
```

The test suite covers:
- Document loading and chunking
- Vector store indexing
- Retrieval chain correctness

---

## Contributing

Contributions are welcome! Follow these steps:

1. **Fork** the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`.
3. Install the development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```
4. Write tests for new functionality.
5. Ensure the code passes linting:
   ```bash
   flake8 .
   ```
6. Open a Pull Request with a clear description of the changes.

Please adhere to the existing code style and update the documentation accordingly.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## Acknowledgements

- **LangChain** – for the powerful abstractions that make RAG pipelines straightforward.
- **OpenAI** – for the underlying LLM and embedding models.
- Community contributors who helped improve the project.
