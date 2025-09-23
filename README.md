# LangChain Chatbot

## Overview

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a Retrieval‑Augmented Generation (RAG) chatbot built on top of **[LangChain](https://github.com/langchain-ai/langchain)**.  It demonstrates how to combine:

- **Document stores** (e.g., Chroma, Pinecone, FAISS) for efficient retrieval.
- **LLM back‑ends** (OpenAI, Anthropic, Ollama, etc.) for generation.
- **Chains & agents** to orchestrate the retrieval‑generation pipeline.

The goal is to provide a clear, production‑ready starting point for developers who want to build their own AI assistants, knowledge‑base bots, or customer‑support agents.

---

## Table of Contents

- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Running the Demo](#running-the-demo)
- [Project Structure](#project-structure)
- [Usage Examples](#usage-examples)
- [Extending the Bot](#extending-the-bot)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline**: Retrieve relevant chunks from a vector store and feed them to an LLM.
- **Modular design**: Swap out the vector store, LLM, or prompt template without touching core logic.
- **Typed settings**: Powered by `pydantic` for robust configuration handling.
- **Streaming responses**: Optional server‑sent events for real‑time UI updates.
- **Docker support**: Ready‑to‑run container for quick prototyping.
- **Comprehensive tests** covering retrieval, generation, and end‑to‑end flows.

---

## Getting Started

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | >=3.9   |
| pip         | latest  |
| Docker      | optional (for containerised run) |

You will also need an API key for the LLM provider you intend to use (e.g., `OPENAI_API_KEY`).

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows use `.venv\Scripts\activate`

# Install the package and development dependencies
pip install -e .[dev]
```

The `[dev]` extra pulls in testing tools (`pytest`, `pytest‑asyncio`) and linting utilities (`ruff`, `black`).

### Configuration

All configuration is driven by a **`.env`** file located at the project root.  A template is provided:

```dotenv
# .env.example – copy to .env and fill in the values
# LLM provider (openai, anthropic, ollama, ...)
LLM_PROVIDER=openai

# API keys – keep these secret!
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=...

# Vector store – default is Chroma (local).  Set to pinecone, weaviate, etc.
VECTOR_STORE=chroma
CHROMA_PERSIST_DIR=./data/chroma

# Optional: model name (e.g., gpt-4o-mini, claude-3-sonnet-20240229)
LLM_MODEL=gpt-4o-mini

# Retrieval settings
TOP_K=4
```

Copy the example file and adjust the values:

```bash
cp .env.example .env
```

### Running the Demo

```bash
# Start the FastAPI server (includes streaming endpoint)
uvicorn langchain_chatbot.api:app --reload
```

Open your browser at `http://127.0.0.1:8000/docs` to explore the OpenAPI UI or use the provided minimal React front‑end (`frontend/` directory).

---

## Project Structure

```
langchain-chatbot/
├─ src/                     # Core library code
│   ├─ chatbot/             # High‑level RAG components
│   │   ├─ chain.py         # Retrieval‑generation chain definition
│   │   ├─ prompts.py       # Prompt templates (system/user)
│   │   └─ config.py        # Pydantic settings loader
│   ├─ vectorstores/        # Wrapper classes for Chroma, Pinecone, …
│   └─ llm/                 # LLM adapters (OpenAI, Anthropic, Ollama)
│
├─ tests/                   # Unit & integration tests
│   ├─ test_chain.py
│   └─ test_api.py
│
├─ data/                    # Persistent vector store data (git‑ignored)
│
├─ frontend/                # Optional React UI (demo only)
│
├─ Dockerfile               # Build image for production
├─ docker-compose.yml       # Spin up vector store services if needed
├─ pyproject.toml           # Poetry/PEP‑517 build config
├─ .env.example             # Template for environment variables
└─ README.md                # <-- you are reading it!
```

---

## Usage Examples

### 1️⃣ Simple Python Interaction

```python
from langchain_chatbot.chatbot import Chatbot
from langchain_chatbot.config import Settings

# Load settings from .env automatically
settings = Settings()
bot = Chatbot(settings)

response = bot.ask("Comment fonctionne le modèle RAG ?")
print(response)
```

### 2️⃣ Streaming Responses (FastAPI endpoint)

```bash
curl -N -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Quelle est la capitale du Québec ?"}'
```

The endpoint returns a stream of `text/event-stream` chunks that can be consumed by a front‑end UI.

---

## Extending the Bot

- **Add a new vector store**: Implement a subclass of `BaseVectorStore` in `src/vectorstores/` and register it in `config.py`.
- **Custom prompt**: Edit `src/chatbot/prompts.py` or provide your own Jinja2 template via the `PROMPT_TEMPLATE` env variable.
- **Tool integration**: Use LangChain's `Tool` interface to add function‑calling capabilities (e.g., calculator, web‑search).
- **Deploy**: The Docker image (`docker build -t langchain-chatbot .`) can be pushed to any container registry and run behind a reverse proxy.

---

## Testing

```bash
# Run the full test suite
pytest -q
```

Coverage is enforced at **90 %**; the CI pipeline fails on regressions.

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository** and clone your fork.
2. Create a **feature branch** (`git checkout -b feat/your-feature`).
3. Write tests for any new functionality.
4. Ensure code style passes (`ruff check .` and `black --check .`).
5. Open a **Pull Request** against the `main` branch.
6. Fill the PR template – describe the problem, solution, and any breaking changes.

See `CONTRIBUTING.md` for detailed guidelines on commit messages, linting, and release process.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

*Happy building with LangChain!*