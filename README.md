# ⚖️ Lawyer Chatbot

**Lawyer Chatbot** is a bilingual, Retrieval-Augmented Generation (RAG) web application that answers legal questions grounded in the **Constitution of Kenya**. It retrieves the most relevant constitutional provisions for a given question and uses a large language model to generate an accurate, context-aware response — in either English or Swahili.

**🔗 Live demo:** [bilingual-rag-chatbot-on-the-constitution-of-kenya](https://bilingual-rag-chatbot-on-the-constitution-of-kenya-w7gpfry5cr7.streamlit.app/)

---

##  Features

- **Legal Query Answering** — Ask natural-language questions about the Kenyan Constitution and get answers grounded in the actual text, not just model memory.
- **Multilingual Support** — Accepts and responds to questions in **English** or **Swahili**, with automatic language detection.
- **Retrieval-Augmented Generation (RAG)** — Retrieves the most relevant constitutional sections before generating a response, reducing hallucination and improving factual accuracy.
- **FastAPI Backend** — Exposes a lightweight REST API for querying the chatbot, served alongside a simple HTML frontend (`index.html`).
- **Vector Search with ChromaDB** — Embeds and indexes the full text of the Constitution for fast, semantic retrieval.
- **Groq API Integration** — Uses Groq's LLM inference for fast, low-latency response generation.

