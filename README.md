# LangChain Chatbot

## 📖 Description

**LangChain‑Chatbot** est un exemple de bot conversationnel basé sur **LangChain** et la technique **RAG (Retrieval‑Augmented Generation)**. Le projet montre comment combiner un modèle de génération de texte (LLM) avec un moteur de recherche de documents afin d’enrichir les réponses du bot avec du contexte provenant de sources externes (documents PDF, bases de connaissances, etc.).

---

## ✨ Fonctionnalités principales

- **Intégration LangChain** : utilisation des chaînes (`Chains`), des agents (`Agents`) et des `Retrievers`.
- **RAG complet** : indexation de documents, recherche sémantique et injection du texte récupéré dans le prompt LLM.
- **Support de multiples LLM** (OpenAI, Anthropic, Ollama, etc.) via l’interface unifiée de LangChain.
- **Configuration via fichier YAML** – facile à adapter pour différents modèles, bases de données vectorielles et sources de documents.
- **Docker** : image prête à être déployée en local ou sur le cloud.
- **Tests unitaires** pour les composants critiques (indexation, récupération, chaîne de génération).

---

## 🛠️ Prérequis

| Outil | Version minimale |
|-------|------------------|
| Python | 3.9 |
| pip | 22.0 |
| Docker (optionnel) | 20.10 |
| Une clé API pour le LLM choisi (ex. `OPENAI_API_KEY`) |

---

## 🚀 Installation

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/your‑org/langchain-chatbot.git
cd langchain-chatbot
```

### 2️⃣ Créer un environnement virtuel
```bash
python -m venv .venv
source .venv/bin/activate   # sous Linux/macOS
# .venv\Scripts\activate   # sous Windows
```

### 3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4️⃣ Configurer les variables d’environnement
Créez un fichier `.env` à la racine du projet :
```dotenv
# Exemple pour OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
# Si vous utilisez un autre LLM, ajoutez les variables correspondantes
# Exemple pour Cohere
COHERE_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5️⃣ (Optionnel) Lancer avec Docker
```bash
docker build -t langchain‑chatbot .
docker run -p 8000:8000 --env-file .env langchain‑chatbot
```

---

## 📚 Utilisation

### Indexation de documents
Le script `scripts/index_documents.py` parcourt le répertoire `data/` et crée un index vectoriel (FAISS par défaut).
```bash
python scripts/index_documents.py --source data/ --index_path indexes/faiss.idx
```

### Démarrer le serveur de chatbot
```bash
uvicorn app.main:app --reload
```
Le bot sera disponible sur `http://127.0.0.1:8000/docs` (Swagger UI) où vous pourrez tester les endpoints.

### Exemple d’appel via `curl`
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Quelles sont les étapes pour créer un pipeline RAG avec LangChain ?"}'
```

### Interaction via interface web (facultatif)
Le répertoire `frontend/` contient une petite application React qui consomme l’API. Après avoir installé les dépendances (`npm install`) et lancé `npm start`, vous pouvez discuter avec le bot directement depuis votre navigateur.

---

## 🏗️ Architecture du projet

```
langchain-chatbot/
├─ app/                # API FastAPI
│   ├─ main.py         # Point d’entrée
│   └─ router.py       # Endpoints /chat, /health
├─ core/               # Logique métier LangChain
│   ├─ rag_chain.py    # Chaîne RAG complète
│   ├─ retriever.py   # Wrapper autour du vecteur store
│   └─ llm_provider.py # Sélection du LLM selon la config
├─ data/               # Documents sources (PDF, txt, markdown…)
├─ indexes/            # Indexes vectoriels générés
├─ scripts/            # Outils CLI (indexation, nettoyage)
├─ tests/              # Tests unitaires & d’intégration
├─ requirements.txt    # Dépendances Python
├─ Dockerfile          # Image Docker
└─ README.md           # ← Vous êtes ici
```

- **`core.rag_chain.RAGChain`** orchestre : récupération → formatage du contexte → appel LLM.
- **`core.retriever.Retriever`** encapsule la logique du vecteur store (FAISS, Chroma, Pinecone, …) et expose une méthode `get_relevant_documents(query, k)`.
- **`core.llm_provider.LLMProvider`** charge dynamiquement le modèle à partir du fichier `config.yaml`.

---

## 🤝 Contribuer

Les contributions sont les bienvenues ! Voici comment commencer :

1. **Fork** le dépôt et créez une branche feature (`git checkout -b feature/ma‑nouvelle‑fonction`).
2. Installez les dépendances de développement :
   ```bash
   pip install -r dev-requirements.txt
   ```
3. Assurez‑vous que les tests passent :
   ```bash
   pytest -q
   ```
4. Ouvrez une **Pull Request** décrivant le problème résolu ou la fonctionnalité ajoutée.
5. Respectez le style de code : `black`, `isort` et `flake8` sont configurés dans le repo.

### Guide de contribution rapide
- **Documentation** : mettez à jour le `README.md` ou les docstrings si vous ajoutez de nouvelles fonctions.
- **Tests** : chaque nouvelle logique doit être couverte par au moins un test unitaires.
- **CI** : le pipeline GitHub Actions exécute les tests et le linting automatiquement.

---

## 📄 Licence

Ce projet est distribué sous licence **MIT** – voir le fichier `LICENSE` pour plus de détails.

---

## 🙏 Remerciements

- **LangChain** – pour la bibliothèque puissante qui simplifie la création de pipelines LLM.
- **FAISS** – pour le moteur de recherche vectorielle ultra‑rapide.
- La communauté open‑source qui contribue aux modèles de langage et aux outils RAG.

---

*Pour toute question, n’hésitez pas à ouvrir une issue ou à contacter les mainteneurs via le tableau des contributeurs.*
