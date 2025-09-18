# LangChain‑Chatbot

**LangChain‑Chatbot** is a minimal yet extensible reference implementation of a Retrieval‑Augmented Generation (RAG) chatbot built on top of **[LangChain](https://python.langchain.com/)**.  It demonstrates how to combine large language models (LLMs), vector stores, and custom tooling to create a conversational AI that can answer questions with up‑to‑date knowledge from arbitrary document collections.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Demo](#running-the-demo)
- [Usage Guide](#usage-guide)
  - [Creating a Vector Store](#creating-a-vector-store)
  - [Defining the Retrieval Chain](#defining-the-retrieval-chain)
  - [Running a Conversation](#running-a-conversation)
- [Configuration](#configuration)
- [Testing](#testing)
- [Contributing](#contributing)
- [Roadmap](#roadmap)
- [License](#license)

---

## Features

- **RAG‑enabled chatbot** – queries are enriched with relevant document snippets retrieved from a vector store.
- **Modular LangChain components** – easy to swap LLMs, embeddings, retrievers, or memory back‑ends.
- **Support for multiple document types** – PDF, Markdown, plain text, and CSV out of the box.
- **Dockerised development environment** – reproducible builds and isolated dependencies.
- **Extensive unit‑test suite** – ensures reliability when extending the code base.
- **Clear contribution guidelines** – encourages community extensions and bug fixes.

---

## Architecture Overview

```mermaid
flowchart TD
    A[User Input] --> B[Chat Prompt Template]
    B --> C[LLM (e.g., OpenAI, Anthropic)]
    C --> D[LangChain Chain]
    D --> E[Retriever]
    E --> F[Vector Store (FAISS / Pinecone / Chroma)]
    F --> G[Document Embeddings]
    D --> H[Conversation Memory]
    H --> I[Response Formatting]
    I --> A
```

1. **User Input** – The raw message entered by the user.
2. **Prompt Template** – Constructs a prompt that includes retrieved context and conversation history.
3. **LLM** – Generates a response based on the enriched prompt.
4. **Retriever** – Pulls the most relevant documents from the vector store.
5. **Vector Store** – Stores embeddings of the source documents for fast similarity search.
6. **Memory** – Persists conversation state across turns (optional).

---

## Getting Started

### Prerequisites

- **Python ≥ 3.9**
- **Poetry** (or pip) for dependency management
- An API key for the LLM you plan to use (e.g., `OPENAI_API_KEY`)
- Optional: Docker & Docker‑Compose if you prefer containerised execution

### Installation

```bash
# Clone the repository
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot

# Install dependencies using Poetry (recommended)
poetry install
# Or with pip
pip install -r requirements.txt
```

### Running the Demo

The repository ships with a small demo dataset (`data/faq.md`).  To start the chatbot locally:

```bash
# Build the vector store from the demo documents
python scripts/build_vector_store.py --source data/faq.md

# Launch the interactive CLI chatbot
python scripts/chat_cli.py
```

You should see a prompt like `>>>`.  Type a question and watch the RAG‑augmented response.

---

## Usage Guide

### Creating a Vector Store

```python
from langchain.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS

# Load and split documents
loader = TextLoader('data/faq.md')
documents = loader.load()
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(documents)

# Generate embeddings and store them
embeddings = OpenAIEmbeddings()
vector_store = FAISS.from_documents(chunks, embeddings)
vector_store.save_local('vector_store')
```

### Defining the Retrieval Chain

```python
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

retriever = vector_store.as_retriever(search_kwargs={"k": 4})
prompt = PromptTemplate.from_template(
    "Answer the question using the provided context.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:" 
)

qa_chain = RetrievalQA.from_chain_type(
    llm=OpenAI(),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt},
)
```

### Running a Conversation

```python
while True:
    user_input = input(">>> ")
    if user_input.lower() in {"exit", "quit"}:
        break
    result = qa_chain({"query": user_input})
    print("\nAnswer:", result["result"], "\n")
    # Optional: display source snippets for debugging
    for doc in result["source_documents"]:
        print("-", doc.page_content[:200], "…")
```

---

## Configuration

All configurable options are stored in `config.yaml`.  Example snippet:

```yaml
llm:
  provider: openai
  model: gpt-4o-mini
  temperature: 0.0

retriever:
  top_k: 4
  distance_metric: cosine

vector_store:
  type: faiss
  persist_directory: vector_store
```

You can override any setting at runtime via environment variables (e.g., `LLM_MODEL=gpt-4o`).  See `scripts/configure.py` for the parsing logic.

---

## Testing

The project includes a pytest suite covering the core RAG pipeline.

```bash
poetry run pytest
```

Add new tests in the `tests/` directory to cover custom retrievers or prompt templates.

---

## Contributing

We welcome contributions!  Follow these steps:

1. **Fork** the repository and create a feature branch.
2. Install the development dependencies (`poetry install --with dev`).
3. Ensure all tests pass (`poetry run pytest`).
4. Add or update documentation as needed – the README should always reflect the current state of the code.
5. Submit a **Pull Request** with a clear description of the change.

Please adhere to the **PEP 8** style guide and run `black .` before committing.

---

## Roadmap

- [ ] Support for hybrid retrieval (BM25 + vector similarity).
- [ ] Integration with **LangChain Hub** for reusable chain components.
- [ ] Web UI built with **Streamlit** for non‑technical users.
- [ ] Automated deployment scripts for AWS Lambda / Azure Functions.

---

## License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

*Happy coding!*
