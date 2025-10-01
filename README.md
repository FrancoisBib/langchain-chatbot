# LangChain Chatbot with Retrieval-Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-%233776AB)](https://www.python.org/)

A minimal yet extensible chatbot built on **[LangChain](https://github.com/hwchase17/langchain)** that demonstrates **Retrieval‑Augmented Generation (RAG)**. The bot can answer questions using a knowledge base (vector store) while maintaining conversational context.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
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

- **RAG pipeline**: Combine a vector store retriever with a language model to generate grounded answers.
- **Modular design**: Swap out LLMs, embeddings, or vector stores with a single line change.
- **Conversation memory**: Preserve chat history using LangChain's `ConversationBufferMemory`.
- **CLI & Streamlit UI**: Interact via terminal or a lightweight web interface.
- **Extensible**: Clear entry points for adding custom document loaders, prompt templates, or post‑processing steps.

---

## Architecture Overview

```
User Query → Prompt Template → LLM
               ↑            ↓
          Retriever ← Vector Store ← Document Loader
               ↑
          Memory (ConversationBuffer)
```

1. **Document Loader** ingests raw files (PDF, TXT, Markdown, etc.) and splits them into chunks.
2. **Embeddings** (e.g., OpenAI `text-embedding-ada-002`) turn chunks into vectors.
3. **Vector Store** (FAISS by default) stores vectors for fast similarity search.
4. **Retriever** fetches the most relevant chunks for a given query.
5. **Prompt Template** injects retrieved context and chat history into the LLM prompt.
6. **LLM** (OpenAI `gpt-3.5-turbo` by default) generates the final answer.
7. **Memory** keeps track of the dialogue so the model can refer back to previous turns.

---

## Quick Start

### Prerequisites

- Python **3.9** or newer
- An OpenAI API key (or any compatible LLM provider)
- Optional: `git` for cloning the repository

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Tip**: The project uses `poetry` as an alternative dependency manager. If you prefer poetry, run `poetry install` instead of the `pip` command.

### Running the Demo

1. **Prepare a knowledge base** – place your documents (PDF, TXT, MD) in the `data/` folder.
2. **Build the vector store** (only required the first time or when the data changes):
   ```bash
   python scripts/build_index.py --source data/ --persist_dir db/
   ```
3. **Start the chatbot** (CLI mode):
   ```bash
   python -m chatbot.cli --persist_dir db/
   ```
   Or launch the Streamlit UI:
   ```bash
   streamlit run app.py
   ```

You should now be able to ask questions and receive RAG‑augmented answers.

---

## Configuration

All configurable options are defined in `config.yaml`. Key sections:

```yaml
llm:
  provider: openai            # or "anthropic", "cohere", etc.
  model_name: gpt-3.5-turbo
  temperature: 0.2

embeddings:
  provider: openai
  model_name: text-embedding-ada-002

vector_store:
  type: faiss                 # other options: chroma, weaviate, pinecone
  persist_dir: db/

retriever:
  top_k: 4                    # number of documents to retrieve per query

memory:
  type: conversation_buffer
  window_size: 5               # how many past turns to keep
```

You can override any value via command‑line flags (see `--help` for each script) or by setting environment variables prefixed with `LC_` (e.g., `LC_LLM_MODEL_NAME`).

---

## Usage Examples

### Basic CLI Interaction

```bash
$ python -m chatbot.cli
> Hello!
Bot: Hello! How can I help you today?
> Tell me about the benefits of RAG.
Bot: Retrieval‑Augmented Generation (RAG) combines ...
```

### Streamlit UI

The UI displays the conversation history on the left and the retrieved source snippets on the right, making it easy to verify the provenance of the answer.

### Programmatic Access

You can import the core pipeline in your own code:

```python
from chatbot.pipeline import create_chatbot

chatbot = create_chatbot(persist_dir="db/")
response = chatbot.ask("What is LangChain?")
print(response)
```

---

## Testing

The repository includes unit tests for the retriever, prompt generation, and memory handling.

```bash
pytest -v
```

Run the tests after any modification to ensure the pipeline remains stable.

---

## Contributing

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Write code and accompanying tests.
4. Ensure the test suite passes.
5. Open a Pull Request with a clear description of the changes.

Please adhere to the existing coding style (Black, isort) and include docstrings for new functions.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
