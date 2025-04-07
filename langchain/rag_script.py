import os
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA

# Configuration API Openrouter compatible OpenAI
os.environ["OPENAI_API_KEY"] = "sk-votre_cle_openrouter"
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# Chargement des fichiers .txt depuis ./data/
documents = []
for filename in os.listdir("data"):
    if filename.endswith(".txt"):
        loader = TextLoader(os.path.join("data", filename))
        documents.extend(loader.load())

# Découpage des textes
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
texts = text_splitter.split_documents(documents)

# Embedding & vectorisation avec FAISS
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(texts, embeddings)

# Création de la chaîne RAG
retriever = db.as_retriever()
llm = ChatOpenAI(model="openai/gpt-3.5-turbo")
qa_chain = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

# Poser une question
query = "Que contiennent les documents ?"
result = qa_chain.run(query)

# Affichage
print("Réponse LangChain + OpenRouter :")
print(result)
