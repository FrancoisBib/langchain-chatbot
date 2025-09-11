# LangChain Chatbot

## 📖 Overview

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a conversational AI assistant built on top of **[LangChain](https://python.langchain.com/)**.  It demonstrates how to combine:

- **LLM back‑ends** (OpenAI, Anthropic, Azure, etc.)
- **Retrieval‑Augmented Generation (RAG)** pipelines using vector stores (FAISS, Chroma, Pinecone, …)
- **Tool‑use** and **agent** patterns for dynamic function calling
- **Streamlit** UI for quick prototyping and debugging

The repository is deliberately kept lightweight so developers can fork it, adapt the prompt chain, swap out components, or integrate it into larger systems.

---

## ✨ Features

- ✅ **Modular architecture** – LLM, retriever, memory, and UI are interchangeable.
- ✅ **RAG support** – Index your own documents (PDF, TXT, Markdown) and query them in real‑time.
- ✅ **Chat memory** – Session‑level memory with optional persistent vector‑store backed history.
- ✅ **Tool integration** – Example tools (web search, calculator) showcase LangChain's tool‑use capabilities.
- ✅ **Docker ready** – One‑click container build for reproducible environments.
- ✅ **Test suite** – PyTest based unit tests for core pipelines.

---

## 🛠️ Quick Start

### Prerequisites

- Python **3.10** or newer
- An LLM API key (e.g., `OPENAI_API_KEY`)
- Optional: Docker if you prefer containerised execution

### 1. Clone the repository

```bash
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot
```

### 2. Install dependencies

```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file at the project root (or export variables in your shell):

```dotenv
# LLM provider – choose one of the supported back‑ends
OPENAI_API_KEY=sk-*************
# Optional – Azure OpenAI configuration
AZURE_OPENAI_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_OPENAI_API_KEY=********
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o

# Vector store configuration (FAISS is default, no extra vars needed)
# For Pinecone, set:
# PINECONE_API_KEY=...
# PINECONE_ENVIRONMENT=...
```

### 4. Index your knowledge base (RAG)

Place any `.txt`, `.md`, or `.pdf` files inside the `data/` directory, then run:

```bash
python scripts/index_documents.py
```

The script creates a **FAISS** index (`vector_store/faiss_index`) that the chatbot will query at runtime.

### 5. Run the chatbot UI

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser and start chatting!

---

## 📂 Project Structure

```
langchain-chatbot/
├─ app.py                 # Streamlit UI entry point
├─ chatbot.py             # Core LangChain chain (LLM + Retriever + Memory)
├─ config.py              # Centralised configuration loader (pydantic settings)
├─ data/                  # Sample documents for RAG
├─ scripts/
│   └─ index_documents.py# Utility to build the vector store
├─ vector_store/          # Persisted FAISS / other vector DB files
├─ tests/                 # PyTest suite
│   └─ test_chatbot.py
├─ requirements.txt       # Python dependencies
└─ README.md              # <‑‑ you are here
```

---

## 🧩 Extending the Bot

### Swap the LLM

Edit `config.py` or set the appropriate environment variable (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, etc.). The `chatbot.py` factory uses `langchain.llms` to instantiate the model based on `LLM_PROVIDER`.

### Use a different vector store

Replace the FAISS loader in `scripts/index_documents.py` with any LangChain `VectorStore` implementation (e.g., `Chroma`, `Pinecone`, `Weaviate`). Update `chatbot.py` to load the new store.

### Add custom tools

1. Create a new Python module under `tools/` implementing a LangChain `Tool` subclass.
2. Register it in `chatbot.py`'s `tool_list`.
3. The LLM will automatically discover the tool via the `AgentExecutor`.

---

## 🧪 Testing

Run the test suite with:

```bash
pytest -v
```

The tests cover:
- Document indexing and retrieval correctness
- End‑to‑end chat flow with mock LLM responses
- Tool execution pathways

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository and create a feature branch.
2. Write clear, concise commit messages.
3. Add or update tests for new functionality.
4. Ensure `black`, `isort`, and `flake8` pass (`make lint`).
5. Open a Pull Request with a description of the changes.

See `CONTRIBUTING.md` for detailed guidelines.

---

## 📜 License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## 📚 Further Reading

- LangChain Documentation: https://python.langchain.com/docs/
- Retrieval‑Augmented Generation Primer: https://arxiv.org/abs/2005.11401
- Streamlit Quickstart: https://docs.streamlit.io/

---

*Happy coding!*