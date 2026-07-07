import os
import chromadb

from sentence_transformers import SentenceTransformer
from config import EMBEDDING_MODEL


class VectorDB:

    def __init__(self, db_path="./chroma_db", corpus_path="./data/corpus.txt"):

        self.db_path = db_path

        self.client = chromadb.PersistentClient(
            path=db_path
        )

        # Si collection existe
        collections = [
            c.name for c in self.client.list_collections()
        ]

        if "knowledge" in collections:

            print("Chargement de la base existante")

            self.collection = self.client.get_collection(
                "knowledge"
            )

            model_name = self.collection.metadata["embedding_model"]

            self.model = SentenceTransformer(model_name)


        else:

            print("Création de la base")

            self.model = SentenceTransformer(
                EMBEDDING_MODEL
            )

            self.collection = self.client.create_collection(
                name="knowledge",
                metadata={
                    "embedding_model": EMBEDDING_MODEL
                }
            )

            self.create_database(corpus_path)



    def create_database(self, corpus_path):

        with open(
            corpus_path,
            "r",
            encoding="utf-8"
        ) as f:

            texts = [
                line.strip()
                for line in f.readlines()
                if line.strip()
            ]


        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )


        ids = [
            f"chunk_{i}"
            for i in range(len(texts))
        ]


        metadatas = [
            {
                "source":"corpus.txt"
            }
            for _ in texts
        ]


        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas
        )


        print("Base créée avec succès")



    def retrieve(self, question, n_results=3):

        query_embedding = self.model.encode(
            question,
            normalize_embeddings=True
        )


        results = self.collection.query(
            query_embeddings=[
                query_embedding.tolist()
            ],
            n_results=n_results
        )


        documents = results["documents"][0]


        return documents