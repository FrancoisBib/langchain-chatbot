import os
import sys
from langchain.chat_models import ChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Configuration API OpenRouter
os.environ["OPENAI_API_KEY"] = "sk-votre_cle_openrouter"
os.environ["OPENAI_API_BASE"] = "https://openrouter.ai/api/v1"

# Charger les fichiers de fine-tuning depuis le dossier "fine_data"
documents = []
data_path = "fine_data"
if not os.path.isdir(data_path):
    sys.exit(f"Le dossier '{data_path}' est introuvable.")

for filename in os.listdir(data_path):
    if filename.endswith(".txt"):
        loader = TextLoader(os.path.join(data_path, filename))
        documents.extend(loader.load())

# Découpage des documents en morceaux (pour optimiser la récupération)
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs_split = text_splitter.split_documents(documents)

# Création d'un index vectoriel avec FAISS
embeddings = OpenAIEmbeddings()
db = FAISS.from_documents(docs_split, embeddings)

# Création du retriever
retriever = db.as_retriever()

# Définition d'un prompt personnalisé pour influencer le comportement
prompt_template = """Tu es un assistant expert qui prend en compte des données supplémentaires issues d'un fine-tuning simulé.
Voici quelques informations contextuelles :
{context}

En t'appuyant sur ces informations, répond de manière détaillée à la question suivante :
{question}"""

custom_prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

# Initialisation du LLM via OpenRouter
llm = ChatOpenAI(model="openai/gpt-3.5-turbo", temperature=0)

# Création de la chaîne RAG avec le prompt personnalisé
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": custom_prompt}
)

# Exemple de question qui bénéficiera des données supplémentaires
question = "Explique en quoi la Révolution française a influencé l'Europe en prenant en compte les données fournies."
result = qa_chain.run(question)

print("Réponse avec LangChain et fine-tuning simulé :")
print(result)
