import os
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import ChatOpenAI

# Configuration de l'API Openrouter (compatible OpenAI)
os.environ["OPENAI_API_KEY"] = "sk-votre_cle_openrouter"
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"  # Remplace si besoin
os.environ["OPENAI_API_MODEL"] = "openrouter/openai/gpt-3.5-turbo"

# Chargement des documents depuis le dossier ./data
documents = SimpleDirectoryReader("data").load_data()

# Création d’un index vectoriel avec LlamaIndex
index = VectorStoreIndex.from_documents(documents)

# LLM via OpenRouter compatible OpenAI
llm = ChatOpenAI(model="openai/gpt-3.5-turbo")

# Création d’un moteur de questions-réponses
query_engine = index.as_query_engine(llm=llm)

# Question posée à la base de documents
question = "Quel est le contenu principal des documents ?"
response = query_engine.query(question)

# Affichage de la réponse
print("Réponse LlamaIndex + OpenRouter :")
print(response)
