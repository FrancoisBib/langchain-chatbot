# LangChain Chatbot

## Overview

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a Retrieval‑Augmented Generation (RAG) chatbot built on top of **[LangChain](https://github.com/langchain-ai/langchain)**.  It demonstrates how to combine:

- **Large Language Models (LLMs)** for natural‑language generation.
- **Vector stores** (e.g., Chroma, Pinecone, FAISS) for semantic document retrieval.
- **Document loaders** and **text splitters** to ingest arbitrary knowledge bases.
- **Chains & agents** to orchestrate the retrieval‑generation workflow.

The project is deliberately lightweight so developers can quickly fork, adapt, and extend it for their own use‑cases (customer support, knowledge‑base assistants, internal tools, …).

---

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Example Usage](#example-usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline** – retrieve relevant chunks from a vector store and feed them to the LLM.
- **Modular components** – swap out the LLM, embeddings model, vector store, or document loader with a single line change.
- **Streaming responses** – optional real‑time token streaming for a chat‑like experience.
- **Typed settings** – `pydantic`‑based configuration for reproducible runs.
- **Docker support** – containerised execution for CI/CD or cloud deployment.

---

## Prerequisites

| Requirement | Minimum version |
|-------------|-----------------|
| Python      | 3.9             |
| pip         | 22.0            |
| Docker (optional) | 20.10 |

You will also need an API key for the LLM you intend to use (e.g., OpenAI, Anthropic, Cohere).  Set the key in an environment variable as described in the **Configuration** section.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install the package and development dependencies
pip install -e .[dev]
```

The optional `dev` extra installs testing tools (`pytest`, `ruff`) and documentation helpers.

---

## Configuration

Configuration is driven by a **`.env`** file at the project root.  The most common variables are:

```dotenv
# LLM provider (openai, anthropic, cohere, ...)
LANGCHAIN_LLM=openai

# Model name – refer to the provider's documentation for valid values
LANGCHAIN_MODEL=gpt-4o-mini

# Your provider API key (e.g., OPENAI_API_KEY)
OPENAI_API_KEY=sk-****

# Embeddings model – defaults to the same provider as the LLM
EMBEDDINGS_MODEL=text-embedding-3-large

# Vector store – one of: chroma, faiss, pinecone, weaviate
VECTOR_STORE=chroma

# Path to the directory that contains the source documents
DOCS_PATH=./data
```

Load the environment variables with:

```python
from dotenv import load_dotenv
load_dotenv()
```

You can also pass configuration programmatically via the `ChatbotConfig` pydantic model located in `src/config.py`.

---

## Running the Bot

### 1️⃣ Index your knowledge base

```bash
python -m langchain_chatbot.indexer
```

The indexer reads all supported files in `DOCS_PATH` (PDF, TXT, Markdown, CSV, …), splits them into manageable chunks, computes embeddings, and persists them to the selected vector store.

### 2️⃣ Start the interactive CLI

```bash
python -m langchain_chatbot.cli
```

You will be prompted for a question; the bot will retrieve relevant context and generate a response.

### 3️⃣ Run the optional FastAPI server

```bash
uvicorn langchain_chatbot.api:app --host 0.0.0.0 --port 8000
```

The server exposes a single POST endpoint `/chat` that accepts JSON payloads of the form:

```json
{ "question": "How does RAG work?" }
```

---

## Example Usage

```python
from langchain_chatbot.bot import Chatbot

bot = Chatbot()
answer = bot.ask("What is the refund policy for premium users?")
print(answer)
```

**Streaming example** (requires an LLM that supports token streaming):

```python
for token in bot.ask_stream("Explain the difference between embeddings and vectors."):
    print(token, end="", flush=True)
```

---

## Project Structure

```
langchain-chatbot/
├─ src/                     # Core package
│  ├─ bot.py               # High‑level Chatbot wrapper
│  ├─ config.py            # Pydantic settings
│  ├─ indexer.py           # Document ingestion & vector store creation
│  ├─ retrieval.py         # Retrieval chain utilities
│  ├─ generation.py        # LLM wrapper with optional streaming
│  └─ api.py               # FastAPI entry point
├─ data/                    # Sample documents (git‑ignored in production)
├─ tests/                   # Unit & integration tests
├─ .env.example             # Template for environment variables
├─ pyproject.toml           # Poetry/PEP‑517 build configuration
└─ README.md                # <‑ You are reading it!
```

---

## Contributing

Contributions are welcome!  Follow these steps:

1. **Fork the repository** and clone your fork.
2. **Create a feature branch** (`git checkout -b feat/your‑feature`).
3. **Write tests** for any new functionality.  The test suite can be executed with:
   ```bash
   pytest
   ```
4. **Run the linter** (`ruff check .`) and formatter (`ruff format .`).
5. **Submit a pull request** targeting the `main` branch.  Include a concise description of the change and reference any related issue.

Please see `CONTRIBUTING.md` for detailed guidelines on coding style, commit messages, and release workflow.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.
