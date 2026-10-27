"""STEP 5 - Augment the prompt and generate the answer. Needs GOOGLE_API_KEY.

This is the "A" and "G" in RAG, written out by hand (no chain) so every
moving part is visible. rag_app.py does the same thing with an LCEL chain.

Run step 3 first, then from the project root:  python steps/05_prompt_and_answer.py
"""
import os

from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

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

template = """
Use the following pieces of retrieved context to answer the question.
If you don't know the answer, just say that you don't know.
Use three sentences maximum and keep the answer concise.

Context: {context}

Question: {question}

Answer:
"""
prompt = PromptTemplate.from_template(template)
llm = ChatGoogleGenerativeAI(
    model=os.getenv("GEMINI_CHAT_MODEL", "gemini-3.5-flash"), temperature=0
)

question = "How much vacation do I get?"

# 1. Retrieve
docs = retriever.invoke(question)
context = "\n\n".join(d.page_content for d in docs)

# 2. Augment
final_prompt = prompt.format(context=context, question=question)
print("=========== PROMPT SENT TO THE LLM ===========")
print(final_prompt)

# 3. Generate
response = llm.invoke(final_prompt)
text = response.content
if isinstance(text, list):
    text = "".join(b["text"] for b in text if isinstance(b, dict) and "text" in b)
print("=========== ANSWER ===========")
print(text)
