# LangChain Chatbot

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a Retrieval‑Augmented Generation (RAG) chatbot built on top of **LangChain**. It demonstrates how to combine vector stores, LLMs, and prompt engineering to build a conversational AI that can answer questions using both its internal knowledge and external document sources.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Running the Bot Locally](#running-the-bot-locally)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline**: Retrieve relevant passages from a vector store and augment LLM generation.
- **Modular components**: Easy to swap out LLM providers, embedding models, or vector databases.
- **Streaming responses**: Real‑time token streaming for a smooth chat experience.
- **Config‑driven**: All major parameters (model, temperature, top‑k, etc.) are configurable via a single `config.yaml`.
- **Extensible**: Clear interfaces for adding custom retrievers, memory modules, or post‑processing steps.

---

## Architecture Overview

```mermaid
flowchart TD
    A[User Message] --> B[Prompt Template]
    B --> C[Retriever (VectorStore)]
    C --> D[Relevant Documents]
    D --> E[LLM (LangChain)]
    E --> F[Chatbot Response]
    F --> A
```

1. **Prompt Template** – A LangChain `PromptTemplate` that injects the retrieved context into the LLM prompt.
2. **Retriever** – Uses embeddings (e.g., OpenAI `text-embedding-ada-002`) stored in a vector DB (FAISS, Chroma, Pinecone, …).
3. **LLM** – Any LangChain‑compatible LLM (OpenAI, Anthropic, Llama‑Cpp, etc.).
4. **Streaming** – The response is streamed back to the client using LangChain's `StreamingStdOutCallbackHandler` (or a custom WebSocket handler).

---

## Prerequisites

- Python **3.9** or newer
- An OpenAI API key (or credentials for the LLM provider you intend to use)
- Optional: Docker & Docker‑Compose if you prefer containerised execution

---

## Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Tip**: The `requirements.txt` pins versions that are known to work together. If you need the latest LangChain features, bump the version and run `pip install -r requirements.txt` again.

---

## Quick Start

Below is a minimal script (`run_chat.py`) that launches the chatbot in the console:

```python
import os
from pathlib import Path
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

# Load environment variables (e.g., OPENAI_API_KEY)
from dotenv import load_dotenv
load_dotenv()

# 1️⃣ Load documents & create vector store (run once)
# docs = ...  # load your own text files
# embeddings = OpenAIEmbeddings()
# vectorstore = FAISS.from_documents(docs, embeddings)
# vectorstore.save_local("./vectorstore")

# 2️⃣ Load the persisted vector store
vectorstore = FAISS.load_local("./vectorstore", OpenAIEmbeddings())

# 3️⃣ Define a simple RAG prompt
prompt = PromptTemplate(
    input_variables=["question", "context"],
    template="""You are a helpful assistant. Use the following context to answer the question.

Context: {context}\n\nQuestion: {question}\nAnswer:""",
)

# 4️⃣ Build the RetrievalQA chain
qa = RetrievalQA.from_chain_type(
    llm=OpenAI(temperature=0),
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    chain_type="stuff",
    return_source_documents=True,
    combine_documents_chain_kwargs={"prompt": prompt},
)

# 5️⃣ Interactive loop
print("🤖 LangChain RAG Chatbot – type 'exit' to quit")
while True:
    query = input("\nYou: ")
    if query.lower() in {"exit", "quit"}:
        break
    resp = qa(query)
    print("\nBot:", resp["result"], "\n")
```

1. **Create the vector store** the first time you run the script (uncomment the block that loads documents).
2. Subsequent runs will load the persisted store from `./vectorstore`.
3. Adjust the LLM, temperature, or `k` (number of retrieved chunks) in the script to suit your use‑case.

---

## Running the Bot Locally (Web UI)

A lightweight FastAPI + React front‑end is provided in the `web/` folder. To launch the full stack:

```bash
# From the repository root
docker compose up --build
```

- The API will be available at `http://localhost:8000`.
- The UI can be accessed at `http://localhost:3000`.

Configuration is read from `config.yaml`. Example snippet:

```yaml
llm:
  provider: openai
  model: gpt-3.5-turbo
  temperature: 0.2
retriever:
  top_k: 5
vectorstore:
  type: faiss
  path: ./vectorstore
```

---

## Testing

```bash
pytest tests/  # Run the unit and integration tests
```

The test suite covers:
- Document ingestion and embedding
- Retriever correctness (top‑k results)
- Prompt template rendering
- End‑to‑end QA flow with a mock LLM

---

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the repository** and clone your fork.
2. Create a feature branch: `git checkout -b feat/your-feature`.
3. Make your changes, ensuring that:
   - Code follows the existing style (PEP 8, type hints).
   - New functionality is covered by tests.
   - The README is updated if you add public‑facing features.
4. Run the test suite locally: `pytest`.
5. Commit with a clear message and push to your fork.
6. Open a Pull Request against the `main` branch.

> **Code of Conduct**: Please adhere to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md).

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
