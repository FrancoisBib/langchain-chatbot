# LangChain Chatbot

## 📖 Overview

`langchain-chatbot` is a **modular, extensible chatbot** built on top of **[LangChain](https://github.com/langchain-ai/langchain)** that demonstrates **Retrieval‑Augmented Generation (RAG)**. The project showcases how to combine large language models (LLMs) with external knowledge sources (vector stores, databases, APIs) to build conversational agents that can:

- Answer questions using up‑to‑date information.
- Perform tool‑use (e.g., web search, calculator) within a conversation.
- Be easily customized or extended with new data sources and LLM providers.

The repository contains:

- A minimal but functional example app (`app.py`).
- A reusable `Chatbot` class that encapsulates the RAG pipeline.
- Configuration files for environment variables and vector store setup.
- Tests and CI configuration for continuous integration.

---

## 🚀 Quick Start

### Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | `>=3.9` |
| pip         | latest  |
| OpenAI API key (or any compatible LLM provider) |

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### Environment configuration

Create a `.env` file at the project root and add the required keys:

```dotenv
# .env
OPENAI_API_KEY=sk-...          # or any other LLM provider key
VECTOR_STORE_URL=sqlite:///data.db   # example using SQLite; adjust for Pinecone, Weaviate, etc.
```

### Run the demo chatbot

```bash
python app.py
```

You will be dropped into an interactive REPL where you can type questions and receive RAG‑augmented answers.

---

## 🛠️ Architecture & Core Concepts

### 1. Retrieval‑Augmented Generation (RAG)

RAG combines **retrieval** (searching a knowledge base) with **generation** (LLM response). The typical flow is:

1. **User query** → embed the query.
2. **Retriever** fetches the most relevant documents from a vector store.
3. **Prompt template** combines the retrieved docs with the original query.
4. **LLM** generates the final answer.

### 2. Main Components

| Component | Responsibility |
|-----------|-----------------|
| `Chatbot` (src/chatbot.py) | Orchestrates the RAG pipeline, manages session history, and provides a simple `ask(question: str) -> str` API. |
| `Retriever` | Wraps a LangChain `VectorStoreRetriever` (e.g., FAISS, Pinecone, Chroma). |
| `PromptTemplate` | Defines how retrieved documents are injected into the LLM prompt. |
| `LLM` | Any LangChain‑compatible language model (OpenAI, Anthropic, Cohere, etc.). |
| `Memory` (optional) | Stores conversation history for context‑aware replies. |

### 3. Extending the Bot

- **Add a new data source** – create a script that loads documents, splits them (using `RecursiveCharacterTextSplitter`), embeds them (`OpenAIEmbeddings` or any other) and upserts them into the chosen vector store.
- **Swap the LLM** – replace `OpenAI` with `ChatAnthropic`, `Cohere`, or a locally hosted model that implements LangChain's `BaseLLM` interface.
- **Custom tools** – implement LangChain `Tool` subclasses (e.g., web‑search, calculator) and add them to the `AgentExecutor` if you need tool‑use capabilities.

---

## 📂 Project Structure

```
langchain-chatbot/
├─ .env                 # environment variables (not committed)
├─ app.py               # entry‑point for the interactive demo
├─ requirements.txt     # Python dependencies
├─ src/
│   ├─ chatbot.py       # Chatbot class (core RAG logic)
│   ├─ retriever.py     # Helper to build a VectorStoreRetriever
│   └─ utils.py         # Misc helpers (document loading, chunking)
├─ tests/
│   └─ test_chatbot.py  # unit tests for the Chatbot class
├─ data/                # optional folder for raw documents
└─ README.md            # <-- you are reading this file
```

---

## 🧪 Testing

The repository includes a minimal test suite using `pytest`.

```bash
pip install pytest
pytest -q
```

Feel free to add more tests covering new data loaders, custom prompts, or alternative LLM back‑ends.

---

## 🤝 Contributing

Contributions are welcome! Follow these steps:

1. **Fork the repository** and clone your fork.
2. **Create a feature branch** (`git checkout -b feature/awesome‑feature`).
3. **Write code** and add/modify tests as needed.
4. **Run the test suite** (`pytest`).
5. **Commit** with a clear message following the Conventional Commits spec.
6. **Open a Pull Request** targeting the `main` branch.

Please adhere to the existing code style (Black, isort) and include documentation updates when adding new functionality.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 📚 Additional Resources

- **LangChain Documentation** – https://python.langchain.com/
- **RAG Primer** – https://python.langchain.com/docs/use_cases/rag
- **Vector Store Options** – FAISS, Chroma, Pinecone, Weaviate, Milvus, etc.
- **Prompt Engineering Guide** – https://python.langchain.com/docs/concepts/prompts

---

*Happy coding!*