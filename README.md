# LangChain Chatbot with Retrieval-Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A minimal yet production‑ready example of a **chatbot** built on top of **[LangChain](https://github.com/langchain-ai/langchain)** that demonstrates **Retrieval‑Augmented Generation (RAG)**.  The bot can answer questions over a custom knowledge base (PDFs, Markdown, CSV, etc.) while preserving the conversational context.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Usage Guide](#usage-guide)
  - [Adding Your Own Documents](#adding-your-own-documents)
  - [Chatting with the Bot](#chatting-with-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline** – combines a vector store (FAISS) with a LLM (OpenAI, Anthropic, Ollama, etc.)
- **Document loaders** for PDFs, text, CSV, Markdown and more (via LangChain loaders)
- **Conversational memory** – `ConversationBufferMemory` keeps the dialogue context
- **Modular design** – easy to swap LLMs, vectorstores, or retrievers
- **Docker support** – containerised for reproducible environments
- **Extensive type hints & tests** – ready for production use

---

## Architecture Overview

```
+----------------+      +-----------------+      +-------------------+
|  User Input    | ---> |  LangChain      | ---> |  Vector Store     |
| (CLI / UI)     |      |  Chain          |      |  (FAISS)          |
+----------------+      +-----------------+      +-------------------+
        |                     |                         |
        |                     v                         v
        |               +-----------+           +---------------+
        |               | Retriever |           | LLM (Chat)   |
        |               +-----------+           +---------------+
        |                     \_______________________________/
        |                                    |
        v                                    v
+----------------+                   +-----------------+
|  Response      | <----------------- |  LangChain      |
|  (CLI / UI)    |   formatted text   |  OutputParser   |
+----------------+                   +-----------------+
```

1. **Document ingestion** – PDFs/Markdown are split into chunks and embedded with a chosen embedding model (e.g., `OpenAIEmbeddings`).
2. **Vector store** – embeddings are stored in FAISS for fast similarity search.
3. **Retriever** – returns the top‑k most relevant chunks for a user query.
4. **LLM** – generates a response using the retrieved context and the conversation history.
5. **Memory** – `ConversationBufferMemory` feeds past turns back into the chain, enabling multi‑turn dialogue.

---

## Quick Start

### Prerequisites

- **Python ≥ 3.9**
- An **OpenAI API key** (or any other supported LLM provider). Export it as an environment variable:
  ```bash
  export OPENAI_API_KEY='sk-...'
  ```
- **Git** and **Docker** (optional, for containerised execution)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

If you prefer Docker:

```bash
docker build -t langchain-chatbot .
```

### Running the App

#### Using the CLI (default)

```bash
python -m chatbot.main
```
You will be prompted for a question. The bot will answer using the knowledge base located in `data/`.

#### Using the Streamlit UI (optional)

```bash
streamlit run app/streamlit_chat.py
```
Open the displayed URL (usually `http://localhost:8501`).

---

## Usage Guide

### Adding Your Own Documents

1. Place any supported files (PDF, `.txt`, `.md`, `.csv`) inside the `data/` directory.
2. Run the ingestion script to (re)build the vector store:
   ```bash
   python -m chatbot.ingest
   ```
   The script uses LangChain's `RecursiveCharacterTextSplitter` and stores embeddings in `faiss_index.pkl`.

### Chatting with the Bot

The bot can be accessed via:
- **CLI** – `python -m chatbot.main`
- **REST API** – `python -m chatbot.api` (FastAPI, optional)
- **Streamlit UI** – `streamlit run app/streamlit_chat.py`

All interfaces share the same underlying `ChatBot` class, ensuring consistent behaviour.

---

## Testing

Unit tests are located in the `tests/` folder and use `pytest`. Run them with:

```bash
pytest -vv
```
Coverage is above 90 % for the core pipeline (ingestion, retrieval, generation).

---

## Contributing

Contributions are welcome! Follow these steps:

1. **Fork** the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature/awesome-feature
   ```
3. Make your changes and ensure all tests pass.
4. Open a **Pull Request** with a clear description of the change.
5. Follow the existing code style (Black, isort, mypy). You can run the linting suite with:
   ```bash
   make lint
   ```

Please read the `CODE_OF_CONDUCT.md` for community guidelines.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
