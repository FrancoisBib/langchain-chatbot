# LangChain Chatbot

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a Retrieval‑Augmented Generation (RAG) chatbot built on top of **[LangChain](https://python.langchain.com/)**.  It demonstrates how to combine vector stores, document loaders, and LLMs to build a conversational agent that can answer questions using both its internal knowledge and external data sources.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Bot](#running-the-bot)
- [Usage Guide](#usage-guide)
  - [Adding Your Own Data](#adding-your-own-data)
  - [Customising the LLM](#customising-the-llm)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

---

## Features

- **RAG pipeline**: Retrieve relevant chunks from a vector store and feed them to a Large Language Model (LLM) for generation.
- **Modular design**: Swap document loaders, vector stores, and LLM providers with a single line change.
- **Streaming responses**: Optional token‑by‑token streaming for a more interactive chat experience.
- **CLI & FastAPI interfaces**: Use the bot from the command line or expose it as a REST endpoint.
- **Docker support**: Build and run the entire stack in containers for reproducibility.
- **Extensive tests**: Unit and integration tests ensure reliability when extending the codebase.

---

## Architecture Overview

```
+-------------------+      +-------------------+      +-------------------+
|   User Prompt     | ---> |   Retriever       | ---> |   LLM (LangChain) |
+-------------------+      +-------------------+      +-------------------+
          ^                         |                         |
          |                         v                         v
   +---------------+        +----------------+        +-------------------+
   |   FastAPI /   | <---- | Vector Store   | <---- | Document Loader   |
   |   CLI Client  |        (FAISS/PG)   |        (PDF, TXT…) |
   +---------------+        +----------------+        +-------------------+
```

1. **Document Loader** – Loads raw documents (PDF, TXT, CSV, etc.) and splits them into chunks.
2. **Vector Store** – Stores embeddings (FAISS, Chroma, Pinecone, etc.) and performs similarity search.
3. **Retriever** – Queries the vector store for the most relevant chunks.
4. **LLM** – Generates a response conditioned on the retrieved context and the user query.
5. **Interface** – Exposes the chatbot via a simple CLI or a FastAPI HTTP endpoint.

---

## Quick Start

### Prerequisites

- Python **3.9** or newer
- `git`
- (Optional) Docker & Docker‑Compose if you prefer containerised execution

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# Install the package and development dependencies
pip install -e .[dev]
```

The optional `dev` extra pulls in testing tools (`pytest`, `ruff`, etc.) and the FastAPI server.

### Running the Bot

#### 1️⃣ CLI mode (quickest way to test)

```bash
# Load a sample dataset (included in `data/`)
python scripts/setup_vector_store.py data/sample_docs/

# Start the interactive chat
python -m langchain_chatbot.cli
```

#### 2️⃣ FastAPI server

```bash
# Start the API (default runs on http://127.0.0.1:8000)
uvicorn langchain_chatbot.api:app --reload
```

You can then POST a JSON payload:

```json
{ "question": "Explain the difference between RAG and fine‑tuning." }
```

---

## Usage Guide

### Adding Your Own Data

1. Place documents in a directory, e.g. `data/my_corpus/`.
2. Run the vector‑store script:
   ```bash
   python scripts/setup_vector_store.py data/my_corpus/
   ```
   This will:
   - Load each file using LangChain's built‑in loaders.
   - Split the text into 1,000‑token chunks (configurable via `scripts/config.py`).
   - Compute embeddings with the selected model (default: `OpenAIEmbeddings`).
   - Persist the FAISS index to `vector_store/faiss_index`.

### Customising the LLM

The LLM is defined in `langchain_chatbot/config.py`.  To switch providers, edit the `LLM_CONFIG` dictionary:

```python
LLM_CONFIG = {
    "provider": "openai",   # or "anthropic", "cohere", "huggingface"
    "model": "gpt-4o-mini",
    "temperature": 0.0,
}
```

For local models, install the appropriate HuggingFace transformer and set `provider="huggingface"`.

### Streaming Responses (CLI only)

Enable streaming by passing the `--stream` flag:

```bash
python -m langchain_chatbot.cli --stream
```

---

## Testing

```bash
# Run the full test suite
pytest -v
```

The test suite covers:
- Document loading & chunking
- Vector‑store creation & similarity search
- End‑to‑end RAG pipeline
- API contract (FastAPI) using `httpx`

---

## Contributing

Contributions are welcome!  Follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/awesome-feature`.
3. Write code adhering to the existing style (run `ruff` and `black` before committing).
4. Add or update tests.
5. Submit a Pull Request with a clear description of the change.

Please read the [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) and the [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **LangChain** – The core framework that powers the RAG pipeline.
- **OpenAI**, **Anthropic**, **Cohere**, **FAISS**, **Chroma** – For the underlying models and vector‑store implementations.
- The open‑source community for providing excellent tutorials and examples that inspired this repository.
