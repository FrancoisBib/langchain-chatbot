import os
from llama_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from llama_index.llms import OpenRouterLLM  # Assurez-vous d'avoir la bonne version

# Configuration de l'API Openrouteur
os.environ["OPENAI_API_BASE"] = "https://openrouter.example.com/v1"
os.environ["OPENAI_API_KEY"] = "votre_api_key"

# Initialisation du LLM via Openrouteur
llm = OpenRouterLLM(model="gpt-3.5-turbo")

# Chargement des documents depuis le dossier "data"
documents = SimpleDirectoryReader("data").load_data()

# Construction d'un index vectoriel simple
index = GPTSimpleVectorIndex(documents)

# Requête RAG : résumé des informations présentes dans les documents
query = "Donne-moi un résumé des informations présentes dans les documents."
response = index.query(query, llm=llm)

print("Réponse de Llamaindex avec RAG :")
print(response)
