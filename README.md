# LangChain Chatbot with Retrieval-Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)](https://www.python.org/)
[![LangChain](https://img.shields.io/badge/LangChain-0.0.XXX-orange.svg)](https://github.com/langchain-ai/langchain)

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture Diagram](#architecture-diagram)
4. [Quick Start](#quick-start)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Running the Bot](#running-the-bot)
5. [Detailed Usage](#detailed-usage)
   - [Configuring the Retrieval Store](#configuring-the-retrieval-store)
   - [Prompt Engineering](#prompt-engineering)
   - [Customizing the LLM](#customizing-the-llm)
6. [Testing](#testing)
7. [Contributing](#contributing)
8. [Roadmap](#roadmap)
9. [License](#license)
10. [Acknowledgements](#acknowledgements)

---

## Project Overview

`langchain-chatbot` is a minimal yet extensible reference implementation of a conversational agent built on **LangChain** that demonstrates **Retrieval‑Augmented Generation (RAG)**. The bot combines a large language model (LLM) with a vector store to retrieve relevant context from a knowledge base, injects that context into the prompt, and generates answers that are both factual and conversational.

The repository is intentionally lightweight so developers can:
- Understand the core RAG workflow with LangChain.
- Plug‑in their own LLM providers, vector stores, or document loaders.
- Extend the bot with custom tools, memory, or UI front‑ends.

---

## Features

- **Modular architecture**: separate modules for document ingestion, vector store creation, and chatbot logic.
- **Support for multiple vector stores** (FAISS, Chroma, Pinecone, etc.) – just set the `VECTOR_STORE` env variable.
- **LLM agnostic**: works with OpenAI, Anthropic, Cohere, HuggingFace, etc.
- **Prompt templates** that follow best‑practice RAG patterns (system + retrieved docs + user query).
- **Streaming responses** for a real‑time chat experience.
- **Docker support** – run the whole stack with a single command.
- **Comprehensive test suite** using `pytest` and `pytest‑asyncio`.

---

## Architecture Diagram

```
+-------------------+      +-------------------+      +-------------------+
| Document Loader   | ---> | Vector Store      | <--- | Retrieval Engine |
+-------------------+      +-------------------+      +-------------------+
                                 ^                         |
                                 |                         v
                         +-------------------+      +-------------------+
                         | LLM (OpenAI…)    | ---> | Prompt Template   |
                         +-------------------+      +-------------------+
                                                     |
                                                     v
                                             +-------------------+
                                             | Chatbot (FastAPI) |
                                             +-------------------+
```

---

## Quick Start

### Prerequisites

- Python **3.9** or newer.
- An OpenAI API key (or another LLM provider key) – set it as `OPENAI_API_KEY` in your environment.
- (Optional) Docker & Docker‑Compose if you prefer containerised execution.

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Bot

1. **Ingest documents** (run once or when your knowledge base changes):
   ```bash
   python scripts/ingest.py --source data/knowledge_base/
   ```
   This script loads markdown/HTML/text files, splits them into chunks, embeds them with the configured `EMBEDDING_MODEL`, and stores the vectors in the selected vector store.

2. **Start the API server**:
   ```bash
   uvicorn app.main:app --reload
   ```
   The chatbot is now reachable at `http://localhost:8000/chat`. You can test it with `curl` or the provided Swagger UI (`/docs`).

---

## Detailed Usage

### Configuring the Retrieval Store

The project reads configuration from a `.env` file (or environment variables). Example:

```dotenv
# .env
OPENAI_API_KEY=sk-*****
EMBEDDING_MODEL=text-embedding-ada-002
VECTOR_STORE=faiss   # Options: faiss, chroma, pinecone, weaviate
FAISS_INDEX_PATH=./faiss_index
```

Switching vector stores only requires installing the corresponding Python package and updating the env variable.

### Prompt Engineering

The default prompt template follows the RAG best practice of **system → retrieved docs → user query**:

```jinja2
You are a helpful assistant. Use the following retrieved passages to answer the question. If the information is not present, say you don't know.

---
{{ retrieved_documents }}
---
Question: {{ question }}
Answer:
```

You can customise the template by editing `app/prompt.py`.

### Customizing the LLM

Replace the default OpenAI model with another provider by editing `app/llm.py`:

```python
from langchain.llms import OpenAI, Anthropic, HuggingFaceHub

def get_llm() -> BaseLLM:
    if os.getenv("LLM_PROVIDER") == "anthropic":
        return Anthropic(model="claude-v1")
    # Add more providers as needed
    return OpenAI(model="gpt-3.5-turbo")
```

---

## Testing

Run the test suite with:

```bash
pytest
```

The tests cover:
- Document ingestion and vector store creation.
- Retrieval correctness (top‑k similarity).
- End‑to‑end chat flow with mocked LLM responses.

---

## Contributing

Contributions are welcome! Follow these steps:

1. **Fork the repository** and clone your fork.
2. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Write tests** for any new functionality.
4. **Run the linting and type‑checking** tools:
   ```bash
   black . && isort . && mypy .
   ```
5. **Submit a Pull Request** with a clear description of the change.

Please adhere to the existing code style (Black, isort) and include documentation updates when adding public APIs.

---

## Roadmap

- [ ] Support for multi‑modal retrieval (image + text).
- [ ] Integration with LangChain agents for tool use.
- [ ] Deployable UI with Streamlit or React.
- [ ] Automated CI/CD pipeline with GitHub Actions.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- **LangChain** – the backbone for chaining LLMs, retrievers, and prompts.
- **OpenAI** – for the GPT models used in the reference implementation.
- Community contributors who helped shape the project.

---

*Happy building!*