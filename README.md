# My RAG Project - Chat with a PDF

A small, readable Retrieval-Augmented Generation (RAG) app. It answers questions about a PDF
(a sample company employee handbook) using **Python, LangChain, Google Gemini, and ChromaDB**.

Based on the freeCodeCamp article
[RAG Explained Simply with a Real Project](https://www.freecodecamp.org/news/rag-explained-simply-with-a-real-project/)
by Ashutosh Krishna.

## How it works

```
INDEXING (once)
PDF -> PyPDFLoader -> RecursiveCharacterTextSplitter -> Gemini embeddings -> ChromaDB

QUERYING (every question)
question -> embed -> ChromaDB similarity search (top k=2 chunks)
         -> fill prompt template {context} + {question} -> Gemini -> answer
```

## Project layout

```
my-rag-project/
├── rag_app.py                 # the complete app (terminal chatbot)
├── gradio_app.py              # optional web UI on top of rag_app.py
├── create_sample_pdf.py       # regenerates the sample handbook PDF
├── TechCorp_Official_Employee_Handbook.pdf
├── steps/                     # one small script per pipeline stage (for teaching)
│   ├── 01_load_pdf.py
│   ├── 02_chunking.py
│   ├── 03_embed_and_store.py
│   ├── 04_similarity_search.py
│   └── 05_prompt_and_answer.py
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

1. **Create a virtual environment**

   macOS / Linux:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   Windows (Command Prompt):
   ```bat
   python -m venv venv
   venv\Scripts\activate
   ```
   Windows (PowerShell):
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies**
   ```bash
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

3. **Add your Gemini API key** (free from https://aistudio.google.com/app/api-keys)
   ```bash
   cp .env.example .env      # Windows: copy .env.example .env
   ```
   Then edit `.env` and set `GOOGLE_API_KEY`.

## Run it

```bash
python rag_app.py
```

Example questions:

- What days can I work from home?
- How much vacation do I get?
- What is the dress code?
- How much is the home office allowance?

Type `exit` or `quit` to stop.

Optional web UI:

```bash
python gradio_app.py
```

## Step-by-step scripts (great for a live session)

Run from the project root. Steps 1 and 2 need no API key.

| Script | What it shows |
|---|---|
| `python steps/01_load_pdf.py` | Extract raw text from the PDF |
| `python steps/02_chunking.py` | Split into 500-character chunks with 50 overlap |
| `python steps/03_embed_and_store.py` | Turn chunks into vectors and store them in ChromaDB |
| `python steps/04_similarity_search.py` | See which chunks the retriever finds (no LLM) |
| `python steps/05_prompt_and_answer.py` | See the final augmented prompt and the answer |

## Notes and troubleshooting

- **Model names.** Defaults are `gemini-3.5-flash` (chat) and `gemini-embedding-001` (embeddings),
  matching the article's final code. If your key doesn't have access to a model, set
  `GEMINI_CHAT_MODEL` / `GEMINI_EMBEDDING_MODEL` in `.env`.
- **Existing database.** `rag_app.py` re-uses `./chroma_db` if it exists, so the PDF isn't embedded
  twice. **Delete the `chroma_db` folder after you change the PDF** to rebuild the index.
- **Answer printed as a list?** Gemini can return content blocks; `clean_answer()` extracts the text.
- **Use your own document.** Replace the PDF, update `PDF_PATH` in `rag_app.py`, delete `chroma_db/`.
- **Free-tier rate limits.** If you hit a quota error, wait a minute and retry.
