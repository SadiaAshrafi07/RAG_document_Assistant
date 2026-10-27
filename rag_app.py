"""
Chat with your PDF - a small RAG (Retrieval-Augmented Generation) app.

Pipeline:
    PDF -> load -> chunk -> embed -> store in ChromaDB
    question -> embed -> similarity search -> augment prompt -> Gemini -> answer

Run:
    python rag_app.py
"""

import os

from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

try:  # preferred, maintained package
    from langchain_chroma import Chroma
except ImportError:  # fallback used in the original tutorial
    from langchain_community.vectorstores import Chroma


# ---------------------------------------------------------------------------
# Step 1: Imports and environment setup
# ---------------------------------------------------------------------------
# load_dotenv() reads GOOGLE_API_KEY from the .env file into environment
# variables, so the key never has to be hard-coded in the source.
load_dotenv()

PDF_PATH = "TechCorp_Official_Employee_Handbook.pdf"
CHROMA_DIR = "./chroma_db"
CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-3.5-flash")
EMBEDDING_MODEL = os.getenv("GEMINI_EMBEDDING_MODEL", "gemini-embedding-001")

PROMPT_TEMPLATE = """
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.

Context: {context}

Question: {question}

Answer:
"""


def load_pdf(path):
    # Step 2: Loading the PDF document
    print("Loading PDF document...")
    loader = PyPDFLoader(path)
    return loader.load()


def chunk_documents(document):
    # Step 3: Chunking the text
    print("Chunking text...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,   # ~500 characters per chunk
        chunk_overlap=50,  # repeat last 50 chars so ideas aren't cut off
    )
    return text_splitter.split_documents(document)


def get_vector_db(embeddings):
    # Step 4: Embeddings + vector database (ChromaDB, stored on disk)
    # If a database already exists on disk we re-use it. This avoids paying
    # for the same embeddings (and storing duplicates) on every run.
    # Delete the "chroma_db" folder to force a rebuild, e.g. after the PDF changes.
    if os.path.isdir(CHROMA_DIR) and os.listdir(CHROMA_DIR):
        print("Found existing vector database, loading it...")
        return Chroma(persist_directory=CHROMA_DIR, embedding_function=embeddings)

    document = load_pdf(PDF_PATH)
    chunks = chunk_documents(document)
    print(f"Creating vector database from {len(chunks)} chunks...")
    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_DIR,
    )


def format_docs(docs):
    # Helper: stitch retrieved chunks into one block of text for the prompt
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain():
    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    vector_db = get_vector_db(embeddings)

    # Step 5: Retriever + prompt template
    # k=2 -> only the 2 most relevant chunks are sent to the LLM
    retriever = vector_db.as_retriever(search_kwargs={"k": 2})
    prompt = PromptTemplate.from_template(PROMPT_TEMPLATE)

    # Step 6: LLM + the RAG chain (LangChain Expression Language, LCEL)
    # temperature=0 -> factual, deterministic answers
    llm = ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0)

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
    )
    return rag_chain


def clean_answer(response):
    # Gemini may return a list of content blocks instead of a plain string.
    content = response.content
    if isinstance(content, list):
        return "".join(
            block["text"] if isinstance(block, dict) and "text" in block else str(block)
            for block in content
        )
    return content


def main():
    rag_chain = build_rag_chain()

    # Step 7 + 8: Ask questions in a continuous loop
    print("\n--- PDF Chatbot Initialized ---")
    print("Type 'exit' or 'quit' to stop.")

    while True:
        user_question = input("\nYour Question: ")

        if user_question.strip().lower() in ["exit", "quit"]:
            print("Shutting down chatbot. Goodbye!")
            break

        if not user_question.strip():
            continue

        response = rag_chain.invoke(user_question)
        print(f"Answer: {clean_answer(response)}")


if __name__ == "__main__":
    main()
