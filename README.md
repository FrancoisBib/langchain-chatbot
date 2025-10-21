# LangChain Chatbot

**A modular, Retrieval‑Augmented Generation (RAG) chatbot built on LangChain**

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

`langchain-chatbot` is a reference implementation of a **RAG‑enabled chatbot** using the **LangChain** framework. It demonstrates how to:

1. **Retrieve** relevant documents from a vector store.
2. **Augment** the generation step with retrieved context.
3. **Chain** together LLM calls, memory, and post‑processing logic.
4. Deploy the bot locally or as a lightweight API.

The repository is intentionally minimal yet production‑ready, making it an ideal starting point for developers who want to build their own knowledge‑base‑driven assistants.

---

## Features

- **LangChain integration** – Leverages `langchain` primitives (`LLMChain`, `RetrievalQA`, `ConversationalRetrievalChain`).
- **Pluggable vector stores** – Supports FAISS, Chroma, Pinecone, and any `langchain.vectorstores` implementation.
- **Multiple LLM back‑ends** – Works with OpenAI, Anthropic, Cohere, Azure OpenAI, Ollama, etc.
- **Chat memory** – Session‑level memory keeps the conversation context coherent.
- **Config‑driven** – All components (LLM, embeddings, vector store, prompt templates) are defined in a single `config.yaml`.
- **Docker support** – Build and run the bot in an isolated container.
- **Test suite** – Includes unit tests for retrieval, prompt generation, and end‑to‑end flows.

---

## Architecture

```
+-------------------+      +-------------------+      +-------------------+
|   User Interface  | ---> |   API / CLI Layer | ---> |   LangChain Core  |
+-------------------+      +-------------------+      +-------------------+
                                            |
                                            |  +-------------------+
                                            +->| Retrieval Engine  |
                                            |  +-------------------+
                                            |          |
                                            |          v
                                            |  +-------------------+
                                            +->| Vector Store (FAISS, Chroma, …)
                                            |  +-------------------+
                                            |
                                            |  +-------------------+
                                            +->| LLM Provider (OpenAI, …)
                                               +-------------------+
```

- **API / CLI Layer** – FastAPI endpoint (`/chat`) and a simple CLI for quick experimentation.
- **LangChain Core** – Orchestrates retrieval (`Retriever`), augmentation (`PromptTemplate`), and generation (`LLM`).
- **Vector Store** – Stores document embeddings; can be swapped without code changes.
- **LLM Provider** – Abstracted behind LangChain's `ChatModel` interface.

---

## Getting Started

### Prerequisites

- Python **3.9** or newer
- An LLM API key (e.g., OpenAI `OPENAI_API_KEY`)
- Optional: Docker if you prefer containerised execution

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # on Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

If you want the latest LangChain features, install from the GitHub source:

```bash
pip install git+https://github.com/langchain-ai/langchain.git@main
```

### Running the Bot

#### 1️⃣ Using the CLI (quick test)

```bash
python -m chatbot.cli
```

You will be prompted for a question; the bot will retrieve relevant passages and generate a response.

#### 2️⃣ Using the FastAPI server

```bash
uvicorn chatbot.api:app --host 0.0.0.0 --port 8000
```

The API endpoint is available at `POST http://localhost:8000/chat` with JSON payload:

```json
{ "session_id": "my-session", "message": "Explain RAG in simple terms" }
```

The response contains the generated answer and the retrieved source IDs.

#### 3️⃣ Docker (optional)

```bash
docker build -t langchain-chatbot .
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8000:8000 langchain-chatbot
```

---

## Configuration

All runtime options live in **`config.yaml`**. Example:

```yaml
llm:
  provider: openai
  model_name: gpt-4o-mini
  temperature: 0.2

embeddings:
  provider: openai
  model_name: text-embedding-3-large

vector_store:
  type: faiss
  index_path: data/faiss_index

retriever:
  search_type: similarity
  k: 4

prompt:
  system: |
    You are a helpful assistant that answers questions using the provided context.
  user: |
    Answer the following question using ONLY the supplied documents. If the answer is not present, say "I don't know."
```

You can override any field via environment variables (`LLM_MODEL_NAME`, `VECTOR_STORE_TYPE`, …) – the `config.py` loader merges them automatically.

---

## Usage Examples

### Simple Question

```bash
>>> python -m chatbot.cli
You: What is Retrieval‑Augmented Generation?
Bot: Retrieval‑Augmented Generation (RAG) combines a language model with a retrieval system ...
```

### Multi‑turn Conversation

```bash
You: Who wrote the poem "The Road Not Taken"?
Bot: The poem was written by Robert Frost.
You: Show me the stanza that mentions "roads".
Bot: "Two roads diverged in a yellow wood..."
```

The bot automatically stores the conversation in memory, so follow‑up questions are answered in context.

---

## Testing

The project includes a pytest suite. Run it with:

```bash
pytest -vv
```

Tests cover:
- Vector store loading and similarity search
- Prompt rendering
- End‑to‑end `ConversationalRetrievalChain` execution (mocked LLM)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository and create a feature branch.
2. **Write tests** for any new functionality.
3. Ensure **PEP‑8** compliance (`flake8`) and run `black` for formatting.
4. Open a **Pull Request** with a clear description of the change.
5. The CI pipeline will run linting, tests, and build the Docker image.

See `CONTRIBUTING.md` for detailed guidelines.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## Acknowledgements

- **LangChain** – The core framework powering the retrieval and chain logic.
- **OpenAI** – For the LLM and embedding models used in the reference implementation.
- **FAISS** – Vector similarity search library.

---
