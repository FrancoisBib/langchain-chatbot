# LangChain Chatbot

## 📖 Overview

`langchain-chatbot` is a minimal yet powerful example of building a **retrieval‑augmented generation (RAG) chatbot** using the **LangChain** framework. The project demonstrates how to:

- Connect a language model (LLM) to a vector store for context retrieval.
- Define a flexible chain that combines retrieval, prompting, and generation.
- Deploy the chatbot locally or in a containerised environment.
- Extend the solution with custom components, document loaders, and evaluation tools.

The repository is intentionally lightweight so developers can focus on the core concepts of **LangChain**, **RAG**, and **chatbot engineering**.

---

## 🛠️ Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | `>=3.9` |
| Poetry (optional) | `>=1.5` |
| OpenAI API key (or any compatible LLM provider) | – |
| `pip` or `poetry` for dependency management | – |

> **Note**: The code is LLM‑agnostic. You can swap the OpenAI provider for Anthropic, Cohere, Ollama, etc., by adjusting the `LLM` configuration in `config.py`.

---

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot
```

### 2. Install dependencies
You can use **Poetry** (recommended) or **pip**.

#### Using Poetry
```bash
poetry install
poetry shell   # activate the virtual environment
```

#### Using pip
```bash
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set environment variables
Create a `.env` file at the project root (or export variables directly) with the required keys:
```dotenv
OPENAI_API_KEY=sk-...
# Optional – vector store configuration (default: ChromaDB in ./data)
CHROMA_PERSIST_DIR=./data/chroma
```

---

## 📂 Project Structure
```
langchain-chatbot/
├─ src/                     # Core source code
│   ├─ config.py            # Global configuration & env loading
│   ├─ loaders/             # Document loaders (PDF, TXT, etc.)
│   ├─ retrievers/          # Vector store & retrieval logic
│   ├─ chains/              # LangChain chains (RAG, QA, etc.)
│   ├─ bot.py               # CLI entry‑point for interactive chat
│   └─ utils.py             # Helper functions (logging, chunking)
├─ tests/                   # Unit & integration tests
├─ data/                    # Persisted vector store & sample docs
├─ .env.example             # Example env file
├─ pyproject.toml / requirements.txt
└─ README.md                # <‑ YOU ARE HERE
```

---

## 🏃‍♂️ Quick Start (CLI)

Run the chatbot directly from the command line:
```bash
python -m src.bot
```

The first run will:
1. Load documents from `data/docs/` (you can replace them with your own).
2. Split the texts into chunks and embed them using the selected LLM.
3. Persist the embeddings in a local ChromaDB store.
4. Start an interactive REPL where you can ask questions.

### Example interaction
```
> How does LangChain handle prompt templates?
[Bot]: LangChain provides a PromptTemplate class that lets you define placeholders ...
```

---

## 🧩 Extending the Bot

### Adding New Document Sources
1. Implement a loader in `src/loaders/` that returns a list of `Document` objects.
2. Register the loader in `src/config.py` or pass it to the `EmbeddingPipeline`.

### Switching Vector Stores
The default store is **ChromaDB**, but LangChain supports FAISS, Weaviate, Pinecone, etc.
```python
from langchain.vectorstores import FAISS
vectorstore = FAISS.from_documents(docs, embeddings)
```
Replace the `Chroma` instance in `src/retrievers/__init__.py`.

### Custom Prompt Templates
Edit `src/chains/rag_chain.py` and modify the `PromptTemplate` string to suit your domain.

---

## 🧪 Testing

Run the test suite with:
```bash
pytest -q
```
The tests cover:
- Document loading and chunking
- Vector store creation & similarity search
- End‑to‑end RAG chain response generation

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write tests for new functionality.
4. Ensure all tests pass (`pytest`).
5. Open a Pull Request with a clear description of the change.

### Code Style
- Use **black** and **isort** for formatting.
- Follow the existing module layout.
- Keep docstrings concise and include type hints.

---

## 📚 Resources

- **LangChain Documentation** – https://python.langchain.com/
- **RAG Primer** – https://arxiv.org/abs/2005.11401
- **ChromaDB** – https://www.trychroma.com/

---

## 📄 License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.
