# LangChain Chatbot with Retrieval‑Augmented Generation (RAG)

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A minimal, production‑ready example of a **chatbot** built with **[LangChain](https://python.langchain.com/)** that leverages **Retrieval‑Augmented Generation (RAG)**. The bot can answer questions over a custom document collection while keeping the conversation context.

---

## Table of Contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the App](#running-the-app)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Customization & Extensibility](#customization--extensibility)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **RAG pipeline**: Combine a vector store (FAISS) with a language model (OpenAI `gpt-3.5-turbo` by default) to retrieve relevant chunks and generate grounded answers.
- **Conversation memory**: `ConversationBufferMemory` preserves chat history, enabling follow‑up questions.
- **Modular design**: Separate modules for data ingestion, vector store creation, and the chatbot chain.
- **CLI and Streamlit UI**: Run the bot from the command line or launch an interactive web UI.
- **Easy to extend**: Swap out the LLM, vector store, or retriever with a single line change.

---

## Architecture Overview

```
+-------------------+       +-------------------+       +-------------------+
|   Data Sources    |  -->  |  Document Loader  |  -->  |   Text Splitter   |
+-------------------+       +-------------------+       +-------------------+
                                 |                         |
                                 v                         v
                         +-------------------+   +-------------------+
                         |   Embedding Model |   |   Vector Store    |
                         +-------------------+   +-------------------+
                                 |                         |
                                 +-----------+-------------+
                                             |
                                     +-------------------+
                                     |   Retriever (FAISS) |
                                     +-------------------+
                                             |
                                     +-------------------+
                                     |   LLM (OpenAI)    |
                                     +-------------------+
                                             |
                                     +-------------------+
                                     |   RAG Chain (LLM + |
                                     |   Retriever)      |
                                     +-------------------+
                                             |
                                     +-------------------+
                                     |   Conversation    |
                                     |   Memory          |
                                     +-------------------+
                                             |
                                     +-------------------+
                                     |   UI / CLI        |
                                     +-------------------+
```

---

## Getting Started

### Prerequisites

- **Python >= 3.9**
- An **OpenAI API key** (or any other LLM provider supported by LangChain)
- (Optional) `git` if you clone the repository

### Installation

```bash
# Clone the repository
git clone https://github.com/FrancoisBib/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

> **Tip**: The `requirements.txt` pins the latest stable versions of LangChain, `openai`, `faiss-cpu`, and `streamlit`.

### Configuration

Create a `.env` file at the project root and add your OpenAI key:

```dotenv
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

The project also respects the following optional variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `EMBEDDING_MODEL` | OpenAI embedding model name | `text-embedding-ada-002` |
| `LLM_MODEL` | Chat model used for generation | `gpt-3.5-turbo` |
| `VECTORSTORE_PATH` | Directory where the FAISS index is persisted | `./vectorstore` |

### Running the App

#### CLI

```bash
python -m chatbot.cli
```

You will be prompted for a question; the bot will retrieve relevant documents and answer.

#### Streamlit UI (recommended for exploration)

```bash
streamlit run app.py
```

Open the displayed URL (usually `http://localhost:8501`) in your browser and start chatting.

---

## Project Structure

```
langchain-chatbot/
├── data/                     # Sample documents (PDF, txt, md, etc.)
├── src/
│   ├── ingestion.py          # Load and split documents, create embeddings
│   ├── vectorstore.py        # FAISS wrapper – build / load index
│   ├── chatbot.py            # RAG chain definition (LLM + Retriever + Memory)
│   └── utils.py              # Helper functions (env loading, logging)
├── app.py                    # Streamlit UI entry point
├── cli.py                    # Simple command‑line interface
├── requirements.txt
├── .env.example
└── README.md
```

---

## How It Works

1. **Ingestion** – `ingestion.load_documents()` reads every file under `data/` using LangChain loaders (`TextLoader`, `PDFMinerLoader`, …). The text is split into manageable chunks (`RecursiveCharacterTextSplitter`).
2. **Embedding** – Each chunk is embedded with `OpenAIEmbeddings` (or any other `Embeddings` implementation). The vectors are stored in a **FAISS** index on disk for fast similarity search.
3. **Retriever** – `FAISS.from_documents()` creates a `VectorStoreRetriever` that returns the *k* most similar chunks for a given query.
4. **RAG Chain** – `ConversationalRetrievalChain` combines the retriever with an LLM. The chain feeds retrieved context into the LLM prompt and appends the conversation history from `ConversationBufferMemory`.
5. **Interaction** – The UI (CLI or Streamlit) simply forwards the user query to the chain and displays the answer.

---

## Customization & Extensibility

- **Swap the vector store** – Replace `FAISS` with `Chroma`, `Pinecone`, `Weaviate`, etc., by changing the import in `src/vectorstore.py`.
- **Use a different LLM** – Change the `ChatOpenAI` instantiation in `src/chatbot.py` to any LangChain‑compatible LLM (`ChatAnthropic`, `ChatGoogleGenerativeAI`, …).
- **Advanced prompting** – Override the default prompt template by passing a custom `PromptTemplate` to `ConversationalRetrievalChain.from_llm`.
- **Document types** – Add more loaders (e.g., `UnstructuredFileLoader`) in `ingestion.py` to support CSV, DOCX, etc.
- **Fine‑tuning** – Store the retrieved chunks in a separate collection for supervised fine‑tuning of the LLM if needed.

---

## Testing

Unit tests live under `tests/`. Run them with:

```bash
pytest -v
```

The test suite covers:
- Document loading & splitting
- Vector store creation & persistence
- End‑to‑end RAG chain execution (mocked LLM responses)

---

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/your-feature`).
3. Ensure code style with `ruff` (`ruff format . && ruff check .`).
4. Add or update tests.
5. Submit a pull request with a clear description of the changes.

See `CONTRIBUTING.md` for detailed guidelines.

---

## License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.
