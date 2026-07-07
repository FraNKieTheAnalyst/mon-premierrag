from vector_db import VectorDB


db = VectorDB()


questions = [
    "Quelle est la couleur du chat de Bob ?",
    "Comment s'appelle le chien d'Alice ?"
]


for q in questions:

    print("\nQUESTION :", q)

    results = db.retrieve(q)

    print(results)