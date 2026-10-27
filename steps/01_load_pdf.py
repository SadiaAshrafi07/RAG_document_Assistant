"""STEP 1 - Load the PDF. No API key needed.

Run from the project root:  python steps/01_load_pdf.py
"""
from langchain_community.document_loaders import PyPDFLoader

print("Loading PDF document...")
loader = PyPDFLoader("TechCorp_Official_Employee_Handbook.pdf")
document = loader.load()

print(f"Pages loaded: {len(document)}")
print("\n--- Text of page 1 ---")
print(document[0].page_content)
