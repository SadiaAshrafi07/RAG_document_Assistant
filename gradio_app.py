"""
Optional next step from the article: a ChatGPT-style web UI with Gradio.

Run:
    python gradio_app.py
Then open the local URL printed in the terminal.
"""

import gradio as gr

from rag_app import build_rag_chain, clean_answer

rag_chain = build_rag_chain()


def respond(message, history):
    return clean_answer(rag_chain.invoke(message))


demo = gr.ChatInterface(
    fn=respond,
    title="Chat with the TechCorp Employee Handbook",
    description="Ask anything about company policies. Answers come from the PDF via RAG.",
    examples=[
        "What days can I work from home?",
        "How much vacation do I get?",
        "What is the dress code?",
    ],
)

if __name__ == "__main__":
    demo.launch()
