import os
from llama_index import SimpleDirectoryReader, VectorStoreIndex
from llama_index.llms import ChatOpenAI

# Configuration API OpenRouter
os.environ["OPENAI_API_KEY"] = "sk-votre_cle_openrouter"
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# Charger les fichiers de fine-tuning depuis le dossier "fine_data"
documents = SimpleDirectoryReader("fine_data").load_data()

# Création de l’index vectoriel avec les données de fine-tuning
index = VectorStoreIndex.from_documents(documents)

# Initialisation du LLM via OpenRouter
llm = ChatOpenAI(model="openai/gpt-3.5-turbo", temperature=0)

# Pour simuler un fine-tuning, on peut adapter le prompt de la requête en y intégrant des instructions
question = ("Prends en compte les données d'exemples fournies pour ajuster ton comportement. "
            "Explique ensuite quelle a été l'influence de la Révolution française sur l'Europe.")

# Exécution de la requête via le moteur RAG
response = index.as_query_engine(llm=llm).query(question)

print("Réponse avec LlamaIndex et fine-tuning simulé :")
print(response)
