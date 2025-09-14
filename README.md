# LangChain Chatbot

## Overview

**LangChain‑Chatbot** is a minimal yet extensible reference implementation for building conversational agents powered by **LangChain** and **Retrieval‑Augmented Generation (RAG)**.  The project demonstrates how to:

- Connect a large language model (LLM) to a vector store for document retrieval.
- Compose a **Retriever → LLM** pipeline using LangChain's `ConversationalRetrievalChain`.
- Deploy the chatbot locally or to a cloud environment.
- Extend the core logic with custom tools, memory, and callbacks.

The repository is intentionally lightweight so you can focus on the core concepts and adapt the code to your own use‑case.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Demo](#running-the-demo)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
  - [RAG Pipeline](#rag-pipeline)
  - [Memory & Conversation History](#memory--conversation-history)
- [Customization Guide](#customization-guide)
  - [Swapping the LLM](#swapping-the-llm)
  - [Using a Different Vector Store](#using-a-different-vector-store)
  - [Adding Tools & Functions](#adding-tools--functions)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **LangChain integration** – leverages LangChain’s `ConversationalRetrievalChain` for a clean RAG workflow.
- **Pluggable components** – swap LLMs, embeddings, and vector stores with a single line change.
- **In‑memory and persistent storage** – examples include `FAISS` (in‑memory) and `ChromaDB` (persistent).
- **Conversation memory** – keeps track of chat history using LangChain’s `ConversationBufferMemory`.
- **Docker support** – optional `Dockerfile` for containerised deployment.
- **Extensible architecture** – easy to add custom tools, callbacks, or chain components.

---

## Getting Started

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | >=3.9   |
| pip         | latest  |
| OpenAI API key (or any compatible LLM provider) |
| Optional: Docker (for containerised run) |

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

# Set your environment variables (example for OpenAI)
export OPENAI_API_KEY='sk-...'
# For Windows PowerShell:
# $env:OPENAI_API_KEY='sk-...'
```

### Running the Demo

The repository ships with a simple CLI chat interface:

```bash
python -m chatbot.main
```

You will be prompted to enter a query. The bot will retrieve relevant passages from the supplied document store and generate a response using the configured LLM.

#### Docker (optional)

```bash
# Build the image
docker build -t langchain‑chatbot .

# Run the container (remember to pass your API key)
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8000:8000 langchain‑chatbot
```

---

## Project Structure

```
langchain-chatbot/
├─ chatbot/                # Core package
│   ├─ __init__.py
│   ├─ config.py           # Settings (LLM, embeddings, vector store)
│   ├─ retriever.py        # Vector store wrapper
│   ├─ chain.py            # ConversationalRetrievalChain builder
│   └─ cli.py              # Simple command‑line UI
├─ data/                   # Example documents (Markdown, PDFs, etc.)
├─ tests/                  # Unit and integration tests
├─ Dockerfile
├─ requirements.txt
├─ README.md               # <‑ This file
└─ .github/                # CI workflows
```

---

## How It Works

### RAG Pipeline

1. **Document Ingestion** – Documents are loaded, split into chunks, and embedded using a chosen embedding model (e.g., `OpenAIEmbeddings`).
2. **Vector Store Creation** – Embeddings are stored in a vector DB (FAISS by default).  The store provides a `Retriever` that returns the most relevant chunks for a query.
3. **Conversational Retrieval Chain** – LangChain combines the retriever with an LLM. The chain formats a prompt that includes retrieved context and the chat history, then calls the LLM to produce a response.

### Memory & Conversation History

`ConversationBufferMemory` is used so the LLM can see previous exchanges.  This enables the bot to maintain context across turns without re‑retrieving the entire history.

---

## Customization Guide

### Swapping the LLM

Edit `chatbot/config.py`:
```python
from langchain.llms import OpenAI, HuggingFaceHub

# Example: switch to a HuggingFace model
LLM = HuggingFaceHub(repo_id="google/flan-t5-xl", model_kwargs={"temperature": 0.7})
```

All other components remain unchanged.

### Using a Different Vector Store

Replace the FAISS implementation with Chroma, Pinecone, or any LangChain‑compatible store:
```python
from langchain.vectorstores import Chroma

VECTOR_STORE = Chroma(embedding_function=EMBEDDINGS, persist_directory="./chroma_db")
```

Remember to adjust the `requirements.txt` if the new store introduces extra dependencies.

### Adding Tools & Functions

LangChain supports tool‑calling.  To add a custom tool (e.g., a calculator):
```python
from langchain.agents import tool

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result."""
    return str(eval(expression))

# Register the tool in the chain
CHAIN = ConversationalRetrievalChain.from_llm(
    llm=LLM,
    retriever=RETRIEVER,
    memory=MEMORY,
    callbacks=[],
    verbose=True,
    return_source_documents=True,
    # Add tools here
    tools=[calculator],
)
```

---

## Testing

```bash
pytest -v
```

The test suite covers:
- Document loading and chunking
- Vector store indexing & retrieval
- End‑to‑end generation using a mock LLM

---

## Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/awesome‑feature`).
3. Write tests for your changes.
4. Ensure the test suite passes (`pytest`).
5. Submit a Pull Request with a clear description of the change.

Please adhere to the existing code style (PEP 8) and include documentation updates when adding new functionality.

---

## License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

---

*Happy building with LangChain!*