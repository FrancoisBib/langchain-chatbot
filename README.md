# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

![LangChain](https://raw.githubusercontent.com/langchain-ai/langchain/master/docs/assets/logo.png)

A minimal, production‑ready example of a **chatbot** built on **[LangChain](https://python.langchain.com/)** that leverages **Retrieval‑Augmented Generation (RAG)** to provide up‑to‑date, context‑aware answers.

---

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Installation](#installation)
4. [Quick Start](#quick-start)
5. [Project Structure](#project-structure)
6. [How RAG Works in This Bot](#how-rag-works-in-this-bot)
7. [Running Tests](#running-tests)
8. [Contributing](#contributing)
9. [License](#license)
10. [Acknowledgements](#acknowledgements)

---

## Features

- **LangChain** integration for prompt management, chains, and memory.
- **RAG pipeline** using a vector store (FAISS) and a LLM (OpenAI, Anthropic, or any `ChatModel` compatible with LangChain).
- **Modular design** – components (retriever, generator, memory) are easily swappable.
- **Dockerised** for reproducible local development.
- **Unit tests** covering the retrieval and generation steps.
- **Contribution guide** and CI configuration (GitHub Actions).

---

## Prerequisites

| Tool | Minimum Version |
|------|-----------------|
| Python | 3.9 |
| pip | 22.0 |
| Docker (optional) | 20.10 |

You also need an API key for a LLM provider (e.g., OpenAI). Set it in an environment variable `OPENAI_API_KEY` (or the appropriate variable for your provider).

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # on Windows use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

If you prefer Docker:

```bash
docker build -t langchain-chatbot .
docker run -e OPENAI_API_KEY=$OPENAI_API_KEY -p 8000:8000 langchain-chatbot
```

---

## Quick Start

```python
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory

# 1️⃣ Load documents (replace with your own data source)
from langchain.document_loaders import TextLoader
loader = TextLoader(Path('data/knowledge_base.txt'))
documents = loader.load()

# 2️⃣ Create a vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# 3️⃣ Initialise the LLM
llm = ChatOpenAI(model_name='gpt-4', temperature=0.2)

# 4️⃣ Build the RAG chain
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
rag_chain = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=memory,
)

# 5️⃣ Chat!
while True:
    user_input = input("🗣️ You: ")
    if user_input.lower() in {"exit", "quit"}:
        break
    response = rag_chain.run(user_input)
    print(f"🤖 Bot: {response}\n")
```

The script loads a knowledge base, builds a FAISS index, and creates a conversational RAG chain. The memory component preserves chat context across turns.

---

## Project Structure

```
langchain-chatbot/
├── data/                     # Sample knowledge‑base files
├── src/
│   ├── __init__.py
│   ├── retrieval.py          # Vector store & retriever helpers
│   ├── generation.py         # LLM wrapper & prompt templates
│   └── chatbot.py            # High‑level orchestration (example above)
├── tests/                    # Pytest suite
│   ├── test_retrieval.py
│   └── test_generation.py
├── Dockerfile
├── requirements.txt
├── .github/workflows/ci.yml  # CI pipeline (lint + tests)
└── README.md                 # <‑‑ this file
```

---

## How RAG Works in This Bot

1. **Retrieval** – The user query is embedded and used to fetch the *k* most relevant chunks from the FAISS index.
2. **Augmentation** – Retrieved chunks are concatenated with a system prompt that instructs the LLM to answer *as if* it had read the source material.
3. **Generation** – The LLM produces a response that is grounded in the retrieved context.
4. **Memory** – `ConversationBufferMemory` stores the dialogue history, allowing follow‑up questions to be answered with the same context.

This pipeline reduces hallucinations and ensures answers stay aligned with the underlying knowledge base.

---

## Running Tests

```bash
pytest -q
```

The test suite validates that:
- The retriever returns relevant documents.
- The generation step respects the retrieved context.
- The overall chain produces deterministic output when `temperature=0`.

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Write code and **add tests**.
4. Ensure linting passes: `ruff check .` (or run the CI locally).
5. Submit a **Pull Request** with a clear description of the change.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for detailed guidelines.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## Acknowledgements

- **LangChain** – the backbone of the RAG workflow.
- **FAISS** – fast similarity search.
- **OpenAI** – LLM provider used in the example.
- Community contributors for feedback and bug reports.

---
