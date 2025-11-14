# LangChain Chatbot

A **LangChain‑powered chatbot** that demonstrates Retrieval‑Augmented Generation (RAG) for building intelligent, context‑aware conversational agents.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Example Usage](#example-usage)
- [Testing](#testing)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)

---

## Overview

This repository provides a minimal yet extensible reference implementation of a chatbot built with **[LangChain](https://github.com/langchain-ai/langchain)**.  The bot uses **RAG (Retrieval‑Augmented Generation)** to retrieve relevant documents from a vector store and feed them to a language model, enabling answers that are both up‑to‑date and grounded in external knowledge.

The codebase is deliberately kept simple so that developers can:

- Understand the core RAG workflow with LangChain.
- Swap out components (LLM, embeddings, vector store) with minimal changes.
- Extend the bot with custom tools, memory, or UI integrations.

---

## Features

- **Modular architecture** – LLM, embeddings, vector store, and retriever are configurable via environment variables.
- **RAG pipeline** – Retrieve relevant chunks from a vector database and augment the LLM prompt.
- **Chat history** – Optional conversation memory to maintain context across turns.
- **Streaming responses** – Real‑time token streaming for a smoother UI experience.
- **Docker support** – Ready-to‑run container with all dependencies isolated.
- **Extensible** – Add custom tools (e.g., web search, calculator) using LangChain's tool interface.

---

## Architecture

```mermaid
flowchart TD
    subgraph User
        UI[User Interface]
    end
    subgraph Bot
        LLM[LLM (e.g., OpenAI, Ollama)]
        Retriever[Retriever (VectorStore + Embeddings)]
        Memory[Conversation Memory]
        Prompt[Prompt Template]
    end
    UI -->|Message| Prompt
    Prompt -->|Context + Retrieval| LLM
    LLM -->|Answer| UI
    Retriever -->|Relevant docs| Prompt
    Memory -->|History| Prompt
```

- **Prompt Template** – Combines the user query, retrieved documents, and optional chat history.
- **Retriever** – Uses a vector store (FAISS, Chroma, Pinecone, etc.) with embeddings (OpenAI, HuggingFace, etc.).
- **LLM** – Any LangChain‑compatible language model.
- **Memory** – `ConversationBufferMemory` by default; can be replaced with other memory classes.

---

## Getting Started

### Prerequisites

- **Python ≥ 3.9**
- **Poetry** (or pip) for dependency management
- An API key for the LLM you intend to use (e.g., `OPENAI_API_KEY`).
- (Optional) Docker if you prefer containerised execution.

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Install dependencies using Poetry (recommended)
poetry install
# Or using pip
pip install -r requirements.txt
```

### Configuration

Create a `.env` file at the project root (or export variables) with the required settings:

```dotenv
# LLM configuration
OPENAI_API_KEY=sk-*****
# Choose one: openai, ollama, anthropic, etc.
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini

# Embedding configuration
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small

# Vector store (FAISS is default, others require extra env vars)
VECTOR_STORE=faiss

# Optional: Enable conversation memory (true/false)
USE_MEMORY=true

# Optional: Set the path to your document corpus
DOCUMENTS_PATH=./data/documents
```

> **Tip**: For a quick start, the repository includes a small sample corpus under `data/documents`.

---

## Running the Bot

### Local development

```bash
# Load environment variables
source .env

# Start the chatbot (CLI mode)
python -m chatbot.main
```

You will be prompted to type a message. The bot will retrieve relevant passages and generate a response.

### Docker

```bash
# Build the image
docker build -t langchain-chatbot .

# Run the container (make sure to pass your .env file)
docker run --env-file .env -it langchain-chatbot
```

---

## Example Usage

```python
from chatbot import Chatbot

# Initialise with default configuration (reads .env automatically)
bot = Chatbot()

# Simple one‑off query
response = bot.ask("What are the benefits of Retrieval‑Augmented Generation?")
print(response)

# Conversational flow
bot.ask("Tell me about LangChain.")
bot.ask("How does it integrate with vector stores?")
```

### Streamed response (CLI)

```bash
> python -m chatbot.main
You: Explain RAG in simple terms.
Bot: Retrieval‑Augmented Generation (RAG) combines ...
```

---

## Testing

The project uses **pytest**. Run the test suite with:

```bash
poetry run pytest
```

Tests cover:
- Retriever initialization
- Prompt template rendering
- End‑to‑end generation with a mock LLM

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository.
2. **Create a feature branch** (`git checkout -b feat/your-feature`).
3. **Write tests** for new functionality.
4. **Run the linter** (`poetry run ruff .`).
5. **Submit a Pull Request** with a clear description of the changes.

### Code Style

- Use **black** for formatting.
- Follow **PEP 8** and **ruff** recommendations.
- Keep imports grouped (standard, third‑party, local).

### Documentation

- Update the README when adding new features.
- Add docstrings to public classes/functions.

---

## Roadmap

- [ ] Support for multi‑modal retrieval (images, PDFs).
- [ ] Integration with LangChain's `Agent` framework for tool‑use.
- [ ] UI front‑end (React or Streamlit) for a web‑based chat experience.
- [ ] Automated deployment scripts (Docker Compose, Kubernetes).

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

*Happy coding!*
