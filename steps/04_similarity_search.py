"""STEP 4 - Semantic search WITHOUT the LLM. Needs GOOGLE_API_KEY.

Shows exactly which chunks the retriever hands to the LLM. Great for debugging
bad answers: if the right chunk isn't here, the problem is retrieval, not the LLM.

Run step 3 first, then from the project root:  python steps/04_similarity_search.py
"""
import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

try:
    from langchain_chroma import Chroma
except ImportError:
    from langchain_community.vectorstores import Chroma

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model=os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")
)
vector_db = Chroma(persist_directory="./chroma_db", embedding_function=embeddings)

retriever = vector_db.as_retriever(search_kwargs={"k": 2})

question = input("Ask something about the handbook: ") or "What days can I work from home?"
docs = retriever.invoke(question)

for i, doc in enumerate(docs, start=1):
    print(f"\n=== Retrieved chunk {i} (page {doc.metadata.get('page')}) ===")
    print(doc.page_content)
