from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Chemins du projet
BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = BASE_DIR / "data" / "corpus.txt"
CHROMA_PATH = BASE_DIR / "chroma_db"


# Modèle d'embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


# Configuration Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Modèle de génération
LLM_MODEL = "llama-3.1-8b-instant"

# Modèle de modération
MODERATOR_MODEL = "llama-3.1-8b-instant"