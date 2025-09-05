# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

## 📖 Overview

**LangChain‑Chatbot** is a reference implementation of a conversational AI assistant built on top of **[LangChain](https://github.com/langchain-ai/langchain)**.  It demonstrates how to combine:

- **LLM inference** (OpenAI, Anthropic, Llama 2, etc.)
- **Vector stores** for semantic search (FAISS, Chroma, Pinecone, …)
- **Retrieval‑Augmented Generation (RAG)** to ground responses in your own documents
- **Tool‑use** (web search, calculator, custom APIs) via LangChain agents

The repo is intentionally minimal yet fully functional, making it an ideal starting point for developers who want to:

- Spin up a local chatbot quickly
- Extend the pipeline with custom data sources or tools
- Contribute improvements back to the community

---

## 🚀 Quick Start

> **Prerequisites**
> - Python 3.9 – 3.12
> - An OpenAI API key (or any other LLM provider supported by LangChain)
> - `git` and `pip` installed on your machine

```bash
# 1️⃣ Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# 2️⃣ Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# 3️⃣ Install dependencies
pip install -r requirements.txt

# 4️⃣ Set your environment variables
export OPENAI_API_KEY=sk-...   # Linux/macOS
# set OPENAI_API_KEY=sk-...   # Windows PowerShell

# 5️⃣ Run the demo chatbot (uses a small set of sample documents)
python app.py
```

You should see a prompt like:
```
> Hello! How can I help you today?
``` 
Type a question – the assistant will retrieve relevant passages from the embedded documents and generate a response.

---

## 📂 Project Structure

```
langchain-chatbot/
├─ data/                 # Sample PDFs / txt files used for the demo
├─ embeddings/           # Cached vector store (FAISS) – generated on first run
├─ src/
│   ├─ agents.py         # Agent definitions (tool usage, custom logic)
│   ├─ retrieval.py      # Vector‑store setup and retrieval helpers
│   ├─ llm.py            # LLM wrapper (OpenAI, Anthropic, etc.)
│   └─ chatbot.py        # High‑level orchestration of RAG pipeline
├─ app.py                # Simple CLI entry‑point (can be swapped for FastAPI/Gradio)
├─ requirements.txt      # Python dependencies
└─ README.md             # <-- you are reading it!
```

---

## 🛠️ Core Components

### 1. LLM Wrapper (`src/llm.py`)
Encapsulates the chosen language model.  By default it uses `ChatOpenAI` from LangChain, but you can switch to any provider that implements the `BaseChatModel` interface.

```python
from langchain.chat_models import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
```

### 2. Retrieval (`src/retrieval.py`)
Creates a **FAISS** vector store from the documents in `data/`.  The embeddings are generated with `OpenAIEmbeddings` (or any `Embeddings` implementation).

```python
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(docs, embeddings)
```

### 3. Agent (`src/agents.py`)
A `ConversationalRetrievalChain` couples the LLM with the retriever.  It also adds optional tools (e.g., a calculator) that the model can invoke.

```python
from langchain.chains import ConversationalRetrievalChain

qa_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True,
)
```

### 4. Orchestration (`src/chatbot.py`)
Handles the chat loop, maintains conversation history, and formats the final answer.

---

## 📦 Installation Guide

### Using Poetry (recommended for reproducibility)
```bash
pip install poetry
poetry install
poetry shell
```

### Using Conda
```bash
conda create -n lc-chatbot python=3.11
conda activate lc-chatbot
pip install -r requirements.txt
```

### Adding New Documents
1. Place your `.pdf`, `.txt`, or `.md` files inside the `data/` directory.
2. Run the ingestion script to rebuild the vector store:
   ```bash
   python src/ingest.py
   ```
   (The script is tiny – it loads files with `UnstructuredLoader` and persists the FAISS index under `embeddings/`.)

---

## 🧪 Testing

The repository includes a minimal pytest suite covering:
- Document loading
- Embedding generation
- Retrieval correctness
- End‑to‑end conversation flow

Run the tests with:
```bash
pytest -q
```

---

## 🤝 Contributing

We welcome contributions!  Follow these steps:

1. **Fork** the repository.
2. **Create a branch** for your feature or bug‑fix:
   ```bash
   git checkout -b feat/your‑feature
   ```
3. **Write tests** for new functionality.
4. **Run the full test suite** to ensure nothing breaks.
5. **Submit a Pull Request** with a clear description of the change.

### Code Style
- Use **black** for formatting (`black .`).
- Type hints are required for all public functions.
- Keep the public API surface minimal – expose only what is needed in `src/__init__.py`.

---

## 📚 Further Reading & Resources

- **LangChain Documentation** – https://python.langchain.com/
- **Retrieval‑Augmented Generation** – https://arxiv.org/abs/2005.11401
- **FAISS – Efficient Similarity Search** – https://github.com/facebookresearch/faiss
- **OpenAI Embeddings** – https://platform.openai.com/docs/guides/embeddings

---

## 📄 License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

---

## 🙏 Acknowledgments

- The LangChain team for providing a robust framework for LLM‑centric applications.
- The open‑source community behind FAISS, Chroma, and the many document loaders used in this repo.

---

*Happy coding!*
