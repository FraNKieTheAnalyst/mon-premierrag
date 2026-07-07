import chromadb
from sentence_transformers import SentenceTransformer


# Charger le modèle d'embeddings
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Connexion à ChromaDB
client = chromadb.PersistentClient(
    path="./chroma_db"
)


# Création de la collection
collection = client.get_or_create_collection(
    name="mon_corpus"
)


# Lecture du corpus
with open("data/corpus.txt", "r", encoding="utf-8") as file:
    documents = [
    line.strip()
    for line in file.readlines()
    if line.strip()
]
print("Nombre de documents :", len(documents))
print(documents)

# Création des embeddings
embeddings = model.encode(documents).tolist()


# Indexation dans ChromaDB
collection.add(
    documents=documents,
    embeddings=embeddings,
    ids=[str(i) for i in range(len(documents))]
)


print("Indexation terminée !")