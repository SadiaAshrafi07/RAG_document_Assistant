"""STEP 2 - Split the text into chunks. No API key needed.

Try changing chunk_size / chunk_overlap live and watch how many chunks you get.

Run from the project root:  python steps/02_chunking.py
"""
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

document = PyPDFLoader("TechCorp_Official_Employee_Handbook.pdf").load()

print("Chunking text...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(document)

print(f"Total chunks: {len(chunks)}")
print("\n--- Chunk 0 ---")
print(chunks[0].page_content)
print("\n--- Chunk 1 (note the 50-character overlap with chunk 0) ---")
print(chunks[1].page_content)
