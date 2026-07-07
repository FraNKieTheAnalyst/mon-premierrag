from rag import RAG


rag = RAG()


while True:

    question = input(
        "\n> : "
    )


    answer = rag.answer_question(
        question
    )


    print(
        "\nRéponse :",
        answer
    )