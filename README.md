# LangChain Chatbot

## Overview

A **LangChain‑based chatbot** that demonstrates Retrieval‑Augmented Generation (RAG) for building conversational AI applications. The bot combines LLM inference with a vector store retriever, allowing it to answer questions using both its pre‑trained knowledge and external documents (e.g., PDFs, markdown files, or databases).

---

## Table of Contents

- [Features](#features)
- [Architecture Diagram](#architecture-diagram)
- [Quick Start](#quick-start)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Demo](#running-the-demo)
- [Configuration](#configuration)
- [Usage Examples](#usage-examples)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline**: Retrieve relevant chunks from a vector store and feed them to an LLM for context‑aware generation.
- **Modular components**: Easily swap out the LLM, embedding model, or vector store (e.g., OpenAI, Cohere, HuggingFace, Pinecone, Chroma, FAISS).
- **Streamlit UI** (optional) for interactive chat.
- **Extensible**: Add custom document loaders, preprocessing steps, or post‑processing callbacks.
- **Docker support** for reproducible environments.

---

## Architecture Diagram

```
+-----------------+      +-------------------+      +-------------------+
|   User Input    | ---> |   LangChain       | ---> |   LLM (e.g.,      |
| (Chat UI / API) |      |   RetrievalChain  |      |   OpenAI GPT‑4)   |
+-----------------+      +-------------------+      +-------------------+
          |                     |                         |
          |                     v                         |
          |               +------------+                  |
          |               | Vector Store| <----------------+
          |               +------------+                  |
          |                     ^                         |
          |                     |                         |
          +---------------------+-------------------------+
```

---

## Quick Start

### Prerequisites

- Python **3.9+**
- An OpenAI API key (or any other LLM provider you plan to use)
- Optional: Docker (if you prefer containerised execution)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Tip**: If you want to experiment with other LLMs or vector stores, install the extra dependencies:
>
> ```bash
> pip install "langchain[openai,cohere,chroma]"
> ```

### Running the Demo

```bash
# Set your environment variables (replace with your own keys)
export OPENAI_API_KEY=sk-*****
# If you use a different provider, set the corresponding env var (e.g., COHERE_API_KEY)

# Start the Streamlit UI (optional)
streamlit run app.py
```

Or, run the chatbot directly from the command line:

```bash
python main.py --question "Explain the concept of Retrieval‑Augmented Generation"
```

---

## Configuration

Configuration is handled via a **`config.yaml`** file (generated on first run) and environment variables.

```yaml
# config.yaml
llm:
  provider: openai          # openai | cohere | huggingface
  model_name: gpt-4
  temperature: 0.7

embeddings:
  provider: openai          # openai | huggingface
  model_name: text-embedding-ada-002

vector_store:
  type: chroma              # chroma | faiss | pinecone
  persist_directory: ./db   # used by Chroma/FAISS

retriever:
  search_type: similarity
  k: 4                       # number of retrieved documents
```

You can override any setting with an environment variable, e.g., `LLM_MODEL_NAME=gpt-3.5-turbo`.

---

## Usage Examples

### 1. Simple CLI Query

```python
from chatbot import Chatbot

bot = Chatbot()
response = bot.ask("What are the main components of a RAG pipeline?")
print(response)
```

### 2. Streamlit Chat Interface

```bash
streamlit run app.py
```

The UI provides:
- A text input box for user queries.
- A chat history view.
- Optional toggles to display retrieved document snippets.

### 3. Custom Document Loader

```python
from langchain.document_loaders import PyPDFLoader
from chatbot import Chatbot

loader = PyPDFLoader("./docs/whitepaper.pdf")
documents = loader.load_and_split()
bot = Chatbot(custom_documents=documents)
print(bot.ask("Summarize the whitepaper"))
```

---

## Testing

Unit tests are located in the `tests/` directory and use **pytest**.

```bash
pip install -r requirements-dev.txt
pytest -v
```

The test suite covers:
- LLM wrapper initialization
- Vector store CRUD operations
- Retrieval‑augmented generation flow
- CLI argument parsing

---

## Contributing

We welcome contributions! Please follow these steps:

1. **Fork** the repository.
2. Create a **feature branch**: `git checkout -b feature/your-feature`.
3. Write code and **add tests**.
4. Ensure the test suite passes: `pytest`.
5. Run the linter/formatter: `black . && flake8`.
6. Open a **Pull Request** with a clear description of the change.

### Code Style
- Use **black** for formatting.
- Follow **PEP 8** guidelines.
- Type hints are required for all public functions.

### Documentation
- Update the README or docstrings when adding new functionality.
- Provide usage examples in the `examples/` folder.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## Acknowledgements

- The **LangChain** library (https://github.com/langchain-ai/langchain) for providing the building blocks.
- **OpenAI**, **Cohere**, **HuggingFace**, and other LLM providers for their APIs.
- The open‑source community for vector‑store implementations like **Chroma** and **FAISS**.
