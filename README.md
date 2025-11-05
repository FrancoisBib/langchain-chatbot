# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

## 📖 Overview

This repository provides a **fully‑functional chatbot** built on top of **[LangChain](https://github.com/hwchase17/langchain)**.  The bot demonstrates how to combine a large language model (LLM) with a **retrieval‑augmented generation (RAG)** pipeline to answer user queries using both LLM reasoning and up‑to‑date knowledge from a custom document store.

Key highlights:
- **Modular architecture** – separate components for LLM, retriever, and memory.
- **Plug‑and‑play vector stores** – SQLite/FAISS/Chroma support out of the box.
- **Easy configuration** via a single `config.yaml` file.
- **Dockerised development** for reproducible environments.
- **Extensible** – add new document loaders, retrievers, or chain types with minimal code changes.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| **RAG pipeline** | Retrieve relevant passages from a vector store and inject them into the LLM prompt. |
| **Chat memory** | Session‑level memory (optional) to keep context across turns. |
| **Multiple LLM back‑ends** | OpenAI, Anthropic, Cohere, HuggingFace 🤗 models supported. |
| **Document loaders** | PDF, TXT, Markdown, CSV, and custom loaders via LangChain. |
| **CLI & API** | Interact via a simple command‑line interface or expose a FastAPI endpoint. |
| **Docker support** | One‑click containerisation for local dev and production. |
| **Testing suite** | Pytest‑based unit and integration tests. |

---

## 🏗️ Architecture

```
+-------------------+        +-------------------+        +-------------------+
|   User Interface  | <----> |   LangChain Bot   | <----> |  Vector Store (FAISS/Chroma) |
+-------------------+        +-------------------+        +-------------------+
           ^                         ^                         ^
           |                         |                         |
   FastAPI / CLI            Retrieval Chain           Document Store
```

1. **User Interface** – CLI (`python -m chatbot.cli`) or FastAPI (`/chat` endpoint).
2. **LangChain Bot** – orchestrates the LLM, retriever, and optional memory.
3. **Vector Store** – stores embeddings of source documents; used by the retriever to fetch relevant chunks.
4. **Document Loader** – populates the vector store from a directory of files.

---

## 📦 Getting Started

### Prerequisites

- Python **3.10** or higher
- An LLM API key (e.g., `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`)
- Optional: Docker & Docker Compose for containerised workflow

### Installation

```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `config.yaml` at the project root (a template is provided as `config.example.yaml`). Example:

```yaml
llm:
  provider: openai          # openai | anthropic | cohere | huggingface
  model_name: gpt-4o-mini
  temperature: 0.7

retriever:
  vector_store: faiss       # faiss | chroma | sqlite
  embedding_model: text-embedding-3-large
  top_k: 4

memory:
  enabled: true
  window_size: 5

paths:
  docs_dir: ./data/docs
  index_dir: ./data/index
```

### Populate the Knowledge Base

```bash
python -m chatbot.ingest
```

The command loads all files from `./data/docs`, creates embeddings, and stores them in the configured vector store.

---

## ▶️ Usage

### Run the CLI chatbot

```bash
python -m chatbot.cli
```

You will be prompted for input; the bot will retrieve relevant passages and generate a response.

### Start the FastAPI server

```bash
uvicorn chatbot.api:app --host 0.0.0.0 --port 8000
```

Send a POST request to `http://localhost:8000/chat` with JSON payload:

```json
{ "session_id": "my-session", "message": "Explain quantum entanglement" }
```

The response contains the bot's answer and the retrieved source snippets.

---

## 🧪 Development

### Running tests

```bash
pytest -v
```

### Adding a new document loader
1. Create a subclass of `langchain.document_loaders.base.BaseLoader`.
2. Register it in `chatbot/loaders/__init__.py`.
3. Update `ingest.py` to accept a `--loader` argument.

### Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write tests for new functionality.
4. Ensure linting passes (`ruff check .`).
5. Submit a Pull Request with a clear description.

---

## 📚 Retrieval‑Augmented Generation (RAG) – Quick Primer

RAG combines **retrieval** (searching a knowledge base) with **generation** (LLM response). The typical flow:
1. **Embed** each document chunk with a dense encoder.
2. **Store** embeddings in a vector database.
3. **Query** – embed the user question, retrieve top‑k similar chunks.
4. **Prompt** – inject retrieved text into the LLM prompt (e.g., using a `ContextualCompressionRetriever` or `StuffDocumentsChain`).
5. **Generate** – LLM produces a grounded answer, citing the retrieved sources when needed.

This approach mitigates hallucinations and keeps the bot up‑to‑date without fine‑tuning the model.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 🙋‍♀️ Contact & Support

- Issue tracker: <https://github.com/your‑org/langchain-chatbot/issues>
- Discussions: <https://github.com/your‑org/langchain-chatbot/discussions>

Happy coding! 🎉