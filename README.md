# LangChain Chatbot

## 📖 Overview

**LangChain‑Chatbot** is a lightweight, extensible example project that demonstrates how to build a conversational AI assistant using **LangChain**, **OpenAI** (or any compatible LLM), and **Retrieval‑Augmented Generation (RAG)**.  The repository showcases:
- Integration of a language model with a vector store for document retrieval.
- A modular pipeline that can be extended with custom tools, memory, and callbacks.
- Clear entry points for running the bot locally or deploying it as an API.

The goal is to provide developers with a solid, production‑ready foundation that they can clone, adapt, and contribute to.

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Recommended Version |
|-------------|----------------------|
| Python | `>=3.9` |
| pip | latest (use `python -m pip install --upgrade pip`) |
| OpenAI API key* or compatible LLM endpoint | – |
| `git` | – |

> **Note**: The asterisk denotes that you need an API key from OpenAI (or an equivalent provider) to run the LLM.  Store it in an environment variable named `OPENAI_API_KEY` (or configure a custom provider as described in the *Configuration* section).

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/langchain-chatbot.git
cd langchain-chatbot

# Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file at the project root (or export the variables in your shell) with the following keys:

```dotenv
# LLM configuration
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Optional: model name (defaults to gpt-3.5-turbo)
OPENAI_MODEL=gpt-3.5-turbo

# Vector store configuration (we use Chroma by default)
CHROMA_PATH=./vectorstore

# Retrieval settings
TOP_K=4   # number of retrieved documents per query
```

You can also override the defaults programmatically when constructing the `Chatbot` class – see the *Advanced Usage* section.

---

## 🛠️ Usage

### Run the interactive CLI

```bash
python -m chatbot.cli
```

You will be greeted with a prompt where you can type natural‑language questions.  The bot will:
1. Retrieve the most relevant chunks from the vector store.
2. Pass the retrieved context to the LLM.
3. Return a response that is grounded in the source material.

### Launch the FastAPI server

The repository includes a minimal FastAPI wrapper for serving the chatbot over HTTP.

```bash
uvicorn api.main:app --reload
```

The API exposes a single endpoint:
- `POST /chat` – expects JSON `{ "message": "Your question" }` and returns `{ "response": "LLM answer" }`.

### Adding your own documents

1. Place your source files (PDF, TXT, Markdown, etc.) in the `data/` directory.
2. Run the ingestion script to index them:
   ```bash
   python -m scripts.ingest
   ```
   This will:
   - Split documents into chunks (default: 500 tokens, 100 token overlap).
   - Embed each chunk using the selected embedding model.
   - Persist the embeddings in the configured vector store (`CHROMA_PATH`).

After ingestion, the chatbot will automatically retrieve from the newly added knowledge base.

---

## 📚 Core Concepts

### LangChain

LangChain provides abstractions for:
- **LLM wrappers** – uniform interface for OpenAI, Azure, HuggingFace, etc.
- **Prompt templates** – reusable prompt construction.
- **Chains** – composable sequences of calls (e.g., retrieval → LLM).
- **Memory** – persisting conversational state across turns.

The chatbot primarily uses the `RetrievalQA` chain, which couples a retriever (vector store) with a language model.

### Retrieval‑Augmented Generation (RAG)

RAG improves factuality by grounding LLM outputs in external data:
1. **Retriever** fetches the top‑k most relevant document chunks.
2. **Prompt** is built with those chunks as context.
3. **LLM** generates a response that references the retrieved information.

This pattern reduces hallucinations and enables domain‑specific assistants without fine‑tuning the model.

---

## 🧩 Project Structure

```
langchain-chatbot/
├─ api/                # FastAPI entry point
│   └─ main.py
├─ chatbot/            # Core library
│   ├─ __init__.py
│   ├─ bot.py          # High‑level Chatbot class
│   └─ prompts.py      # Prompt templates
├─ data/               # Sample documents (add yours here)
├─ scripts/            # Utility scripts (ingest, evaluate, etc.)
│   └─ ingest.py
├─ tests/              # Unit / integration tests
├─ .env.example        # Example env file
├─ requirements.txt    # Python dependencies
└─ README.md           # <-- you're reading it!
```

---

## 🧪 Testing

Run the test suite with:

```bash
pytest -q
```

The tests cover:
- Document ingestion and vector store creation.
- Retrieval correctness (top‑k results).
- End‑to‑end chatbot responses for a few canned queries.

Feel free to add new tests when extending functionality.

---

## 🤝 Contributing

Contributions are welcome!  Follow these steps:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feat/awesome-feature`).
3. Ensure the code passes linting and tests (`flake8`, `pytest`).
4. Open a Pull Request with a clear description of the change.

### Coding Standards

- Use **black** for formatting (`black .`).
- Type‑hint all public functions and classes.
- Keep the public API stable; deprecate with warnings when necessary.

---

## 📄 License

This project is licensed under the **MIT License** – see the `LICENSE` file for details.

---

## 📚 Further Reading

- **LangChain Documentation** – https://python.langchain.com/
- **RAG Primer** – https://arxiv.org/abs/2005.11401
- **OpenAI API Reference** – https://platform.openai.com/docs/api-reference

---

*Happy coding!*