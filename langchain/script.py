import os
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

# Configuration de l'API Openrouteur
os.environ["OPENAI_API_BASE"] = "https://openrouter.example.com/v1"
os.environ["OPENAI_API_KEY"] = "votre_api_key"

# Initialisation du LLM en utilisant l'API Openrouteur
llm = OpenAI(model_name="gpt-3.5-turbo", temperature=0)

# Création des embeddings pour construire le vectorstore
embeddings = OpenAIEmbeddings()

# Exemple de documents. Ici, on peut charger le contenu des fichiers du dossier "data".
# Pour simplifier, nous utilisons deux textes d'exemple.
texts = [
    "Document 1 : Ceci est un exemple de texte concernant le sujet A.",
    "Document 2 : Ceci est un autre texte qui traite du sujet B."
]

# Construction d'un index FAISS à partir des textes
vectorstore = FAISS.from_texts(texts, embeddings)

# Création du système de récupération pour le RAG
retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 2})
qa_chain = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

# Requête RAG : extraction d'informations concernant le sujet A
query = "Quelles informations peut-on extraire concernant le sujet A ?"
result = qa_chain.run(query)

print("Réponse de Langchain avec RAG :")
print(result)
