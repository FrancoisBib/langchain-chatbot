# LangChain Chatbot

A **LangChain‑based chatbot** that demonstrates Retrieval‑Augmented Generation (RAG) for building intelligent, context‑aware conversational agents.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Project Structure](#project-structure)
- [Development & Contribution](#development--contribution)
- [Testing](#testing)
- [FAQ](#faq)
- [License](#license)

---

## Features

- **LangChain core** – leverages LangChain primitives (`LLMChain`, `RetrievalQA`, `ConversationalRetrievalChain`).
- **RAG pipeline** – integrates vector stores (e.g., `FAISS`, `Chroma`) to retrieve relevant documents and augment LLM responses.
- **Modular design** – easy to swap LLM providers (OpenAI, Anthropic, Ollama, etc.) and vector‑store back‑ends.
- **Streaming responses** – optional token‑by‑token streaming for a more natural chat experience.
- **Docker support** – ready‑to‑run container for reproducible environments.
- **Extensible** – clear entry points for custom prompt templates, memory strategies, and post‑processing.

---

## Quick Start

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables (see Configuration section)
cp .env.example .env
# Edit .env to add your API keys and preferred settings

# Run the chatbot
python -m app.main
```

You should now have a local web UI (or CLI, depending on the `INTERFACE` setting) where you can interact with the bot.

---

## Installation

### Prerequisites
- **Python ≥ 3.9**
- **Git**
- An LLM provider API key (OpenAI, Anthropic, etc.)
- (Optional) **Docker** if you prefer containerised execution

### Dependencies
The project uses the following key libraries:
- `langchain`
- `openai` (or alternative LLM client)
- `faiss-cpu` / `chromadb` for vector stores
- `fastapi` + `uvicorn` for the HTTP API
- `pydantic` for settings management
- `python-dotenv` for environment variable handling

All dependencies are listed in `requirements.txt`. Use `pip install -r requirements.txt` to install them.

---

## Configuration

Configuration is handled via a `.env` file (loaded with `python-dotenv`). Copy the example file and fill in the required values:

```dotenv
# .env
# -------------------------------------------------
# LLM provider configuration
OPENAI_API_KEY=sk-************************
LLM_MODEL=gpt-4o-mini

# Vector store configuration
VECTOR_STORE=faiss   # or 'chroma'
EMBEDDING_MODEL=text-embedding-ada-002

# Retrieval settings
TOP_K=4               # number of documents to retrieve per query

# Application settings
INTERFACE=web         # 'web' (FastAPI UI) or 'cli'
HOST=0.0.0.0
PORT=8000

# Misc
LOG_LEVEL=INFO
# -------------------------------------------------
```

### Environment variables reference
| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | Your OpenAI API key (required for the default LLM). | – |
| `LLM_MODEL` | Model name used by the LLM client. | `gpt-4o-mini` |
| `VECTOR_STORE` | Backend for the vector store (`faiss` or `chroma`). | `faiss` |
| `EMBEDDING_MODEL` | Embedding model for document indexing. | `text-embedding-ada-002` |
| `TOP_K` | Number of retrieved documents per query. | `4` |
| `INTERFACE` | Choose between a web UI (`web`) or command‑line interface (`cli`). | `web` |
| `HOST` / `PORT` | FastAPI server host and port. | `0.0.0.0` / `8000` |
| `LOG_LEVEL` | Logging verbosity (`DEBUG`, `INFO`, `WARNING`, `ERROR`). | `INFO` |

---

## Running the Bot

### Web UI (FastAPI)
```bash
uvicorn app.main:app --host $HOST --port $PORT
```
Open `http://localhost:8000/docs` for the OpenAPI UI or `http://localhost:8000` for the simple chat page (if provided).

### Command‑Line Interface
```bash
python -m app.cli
```
Enter your queries directly in the terminal. The CLI streams responses token‑by‑token when `STREAMING=True` in the settings.

---

## Project Structure

```
langchain-chatbot/
├─ app/                     # Application package
│  ├─ __init__.py
│  ├─ main.py               # FastAPI entry point
│  ├─ cli.py                # Simple CLI entry point
│  ├─ core/                 # LangChain core components
│  │   ├─ llm.py            # LLM wrapper / factory
│  │   ├─ embeddings.py    # Embedding model wrapper
│  │   ├─ vector_store.py   # Vector store abstraction
│  │   └─ retrieval.py      # Retrieval chain (RAG)
│  ├─ prompts/              # Prompt templates (Jinja2 / LangChain PromptTemplate)
│  │   └─ chat_prompt.txt
│  └─ utils/                # Helper utilities (logging, config loader)
│      └─ settings.py
├─ data/                    # Sample documents for indexing (optional)
├─ tests/                   # Unit and integration tests
│  └─ test_chatbot.py
├─ .env.example             # Example environment file
├─ requirements.txt
├─ README.md                # <-- you are reading this file
└─ Dockerfile               # Container build definition
```

---

## Development & Contribution

1. **Fork the repository** and create a feature branch.
2. Follow the **coding style** enforced by `ruff` and `black` (run `make lint`).
3. Add or update tests in the `tests/` directory. Aim for >80 % coverage (`make coverage`).
4. Document any new public functions or classes in the docstrings – they are automatically rendered by `pdoc`.
5. Submit a Pull Request with a clear description of the changes.

### Useful Makefile commands
| Command | Description |
|---------|-------------|
| `make install` | Install dependencies in editable mode |
| `make lint` | Run `ruff` and `black` checks |
| `make test` | Execute the test suite |
| `make coverage` | Generate coverage report |
| `make docker-build` | Build the Docker image |
| `make docker-run` | Run the container locally |

---

## Testing

The project uses **pytest**. To run the full suite:
```bash
pytest -vv
```
For fast feedback on a single test file:
```bash
pytest tests/test_chatbot.py -k "retrieval"
```
Mocking of external API calls (OpenAI) is provided via `responses` fixtures located in `tests/conftest.py`.

---

## FAQ

**Q: Can I use a different LLM provider?**
A: Yes. Implement a new provider class in `app/core/llm.py` that adheres to the `BaseLLM` interface and update the factory in `settings.py`.

**Q: How do I switch to a persistent vector store?**
A: Replace the `FAISS` wrapper with `Chroma` (or another supported store) and set `VECTOR_STORE=chroma`. Ensure the store directory is persisted (e.g., mount a volume in Docker).

**Q: Is streaming mandatory?**
A: No. Set `STREAMING=False` in the configuration to receive the full answer after retrieval.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.
