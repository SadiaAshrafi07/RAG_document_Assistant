"""STEP 3 - Create embeddings and store them in ChromaDB. Needs GOOGLE_API_KEY.

Run from the project root:  python steps/03_embed_and_store.py
"""
import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

load_dotenv()

document = PyPDFLoader("TechCorp_Official_Employee_Handbook.pdf").load()
chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(document)

embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
)

# Peek at what an embedding actually is: a long list of numbers
vector = embeddings.embed_query("What days can I work from home?")
print(f"Embedding length: {len(vector)} numbers")
print(f"First 8 numbers: {[round(v, 4) for v in vector[:8]]}")

print("\nCreating vector database...")
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="./chroma_db",
)
print(f"Stored {len(chunks)} chunks in ./chroma_db")
