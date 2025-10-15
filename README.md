# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)

A minimal yet production‑ready example of a **chatbot** built on **[LangChain](https://github.com/langchain-ai/langchain)** that leverages **Retrieval‑Augmented Generation (RAG)**.  The repository demonstrates how to:

- Connect a language model (LLM) to a vector store for semantic retrieval.
- Build a LangChain `ConversationalRetrievalChain` that keeps context across turns.
- Deploy the bot locally via a simple CLI or expose it through an HTTP API (FastAPI).
- Write unit‑ and integration‑tests that mock the LLM and vector store.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Demo](#running-the-demo)
- [Architecture Overview](#architecture-overview)
- [Usage Guide](#usage-guide)
  - [CLI Interaction](#cli-interaction)
  - [API Interaction](#api-interaction)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **LangChain integration** – uses `ChatOpenAI`, `ConversationChain`, and `ConversationalRetrievalChain`.
- **RAG pipeline** – documents are embedded with `OpenAIEmbeddings` (or any compatible embedding model) and stored in a `FAISS` vector store.
- **Memory management** – `ConversationBufferMemory` keeps the chat history, enabling multi‑turn conversations.
- **Modular design** – separate modules for data ingestion, vector store creation, chain construction, and UI.
- **Extensible** – swap out LLMs, embeddings, or vector stores with a single line change.
- **Testable** – includes mocks for LLM responses and vector store similarity search.

---

## Quick Start

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | 3.9+    |
| pip         | latest  |
| OpenAI API key (or alternative LLM) | – |

> **Note**: The project is LLM‑agnostic.  If you prefer a local model (e.g., Llama‑2), replace `ChatOpenAI` with the appropriate LangChain wrapper.

### Installation

```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### Running the Demo

1. **Prepare a document collection** – place your `.txt`, `.pdf`, or `.md` files in the `data/` folder.
2. **Create the vector store** (run once or whenever the source documents change):

   ```bash
   python scripts/build_vector_store.py
   ```

3. **Start the interactive CLI**:

   ```bash
   python -m chatbot.cli
   ```

   You will be prompted for a question; the bot will retrieve relevant passages and generate a response.

4. **Optional – launch the FastAPI server**:

   ```bash
   uvicorn api.main:app --reload
   ```

   Then send a POST request to `http://127.0.0.1:8000/chat` with JSON payload `{ "question": "Your query" }`.

---

## Architecture Overview

```
+----------------+      +----------------------+      +-------------------+
|  Data Ingest   | ---> |  Embedding + Index   | ---> |  Retrieval Layer |
+----------------+      +----------------------+      +-------------------+
         |                         |                         |
         |                         |                         |
         v                         v                         v
+---------------------------------------------------------------+
|                     LangChain Conversational                 |
|   ConversationalRetrievalChain (LLM + VectorStore + Memory)   |
+---------------------------------------------------------------+
```

- **Data Ingest** – `scripts/ingest.py` reads files from `data/` and normalises them.
- **Embedding + Index** – `OpenAIEmbeddings` (or any `Embeddings` subclass) creates dense vectors; `FAISS` stores them for fast similarity search.
- **Retrieval Layer** – `FAISS` returns the top‑k most relevant chunks.
- **Conversational Chain** – combines the retrieved context with the chat history and passes it to the LLM.

---

## Usage Guide

### CLI Interaction

The CLI (`chatbot/cli.py`) provides a REPL‑style interface:

```bash
$ python -m chatbot.cli
> Hello!
[Bot] Hello! How can I help you today?
> Tell me about LangChain.
[Bot] LangChain is a framework ...
> quit
```

### API Interaction

The FastAPI app (`api/main.py`) exposes a single endpoint:

```http
POST /chat
Content-Type: application/json

{ "question": "Explain Retrieval‑Augmented Generation." }
```

Response format:

```json
{
  "answer": "...generated text...",
  "sources": ["doc1.txt", "doc2.pdf"]
}
```

---

## Testing

The test suite lives in the `tests/` directory and uses `pytest`.

```bash
# Run all tests
pytest
```

Key test utilities:
- `tests/conftest.py` – fixtures for a mock LLM (`FakeChatModel`) and an in‑memory FAISS store.
- `tests/test_chatbot.py` – verifies that the retrieval chain returns expected answers and that the memory correctly accumulates history.

---

## Contributing

Contributions are welcome!  Follow these steps:

1. **Fork the repository**.
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your‑feature
   ```
3. **Write code** – keep functions small, add type hints, and write tests.
4. **Run the linter and tests**:
   ```bash
   flake8 .
   pytest
   ```
5. **Submit a Pull Request** – describe the problem solved and reference any related issues.

Please adhere to the existing coding style and update the documentation (README or docstrings) when you add new functionality.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **LangChain** – the core library that makes building LLM‑centric applications straightforward.
- **OpenAI** – for the GPT models used in the demo.
- **FAISS** – for efficient similarity search.
- Community contributors who provide feedback and improvements.
