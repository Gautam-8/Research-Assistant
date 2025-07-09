# 🧠 AI Research Assistant

A local, private RAG-powered Research Assistant using PDF documents and real-time web search.

---

## ✨ Features

- 📄 Upload and process long PDF files
- ✂️ Intelligent text chunking
- 🧠 Embedding via LM Studio (e.g. `nomic-embed-text-v1.5`)
- 📦 Vector store with ChromaDB
- 🔍 Semantic PDF search
- 🌐 Real-time web search (via Serper.dev)
- ⚖️ Hybrid Retrieval (PDF + Web)
- 🤖 Local LLM answer synthesis (e.g. `Gemma-3B` via LM Studio)
- 📚 Source citations from both PDF and web

---

## Setup environment

python -m venv venv
source venv/bin/activate # or venv\Scripts\activate on Windows
pip install -r requirements.txt
