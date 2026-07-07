from dotenv import load_dotenv
from groq import Groq
import os

from vector_db import VectorDB
from moderator import Moderator

from config import (
    LLM_MODEL,
    MODERATOR_MODEL
)



class RAG:


    def __init__(self):

        load_dotenv()


        self.client = Groq(
            api_key=os.getenv(
                "GROQ_API_KEY"
            )
        )


        self.vector_db = VectorDB()


        self.moderator = Moderator(
            self.client,
            MODERATOR_MODEL
        )




    def answer_question(self, question):


        moderation = self.moderator.moderate(
            question
        )


        if moderation["is_prompt_injection"]:

            return "Question bloquée par le modérateur."


        chunks = self.vector_db.retrieve(
            question,
            3
        )


        context = "\n".join(chunks)



        prompt = f"""

Tu es un assistant spécialisé dans la réponse à partir d'une base documentaire.

Tu dois respecter strictement les règles suivantes :

- Réponds uniquement avec les informations présentes dans le contexte.
- N'utilise jamais tes connaissances générales.
- Si la réponse n'est pas présente dans le contexte, réponds exactement :
"Je ne sais pas, cette information n'est pas présente dans ma base de connaissances."
- Si l'utilisateur affirme une information fausse, corrige-le avec le contenu du contexte.

Contexte :

{context}


Si l'information n'existe pas,
dis que tu ne sais pas.

"""



        response = self.client.chat.completions.create(

            model=LLM_MODEL,

            messages=[

                {
                "role":"system",
                "content":prompt
                },


                {
                "role":"user",
                "content":question
                }

            ]

        )


        return response.choices[0].message.content