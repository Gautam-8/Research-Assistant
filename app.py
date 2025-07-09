# app.py

import streamlit as st
import os
import dotenv
from ragpipe import RAGPipeline
from websearch import WebSearch

# Load Serper API key
dotenv.load_dotenv()
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY is not set")
searcher = WebSearch(api_key=SERPER_API_KEY)

# Set up page
st.set_page_config(page_title="🧠 Research Assistant", layout="wide")
st.title("📄 AI Research Assistant")

# Upload PDF
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])
rag = RAGPipeline()  # initialize outside for reuse

if uploaded_file:
    # Save the PDF to disk
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("PDF uploaded successfully!")

    # Button to process and index
    if st.button("🔍 Process PDF"):
        with st.spinner("Extracting & indexing..."):
            chunks = rag.load_and_split_pdf(file_path)
            rag.index_chunks(chunks)
        st.success(f"✅ Indexed {len(chunks)} chunks from the PDF.")

# PDF Semantic Search
st.markdown("---")
st.subheader("📄 Ask a Question from PDF")
query = st.text_input("Ask a question based on the uploaded PDF:")
if query and st.button("🔍 Search PDF"):
    with st.spinner("Searching..."):
        results = rag.query_pdf(query)
        answer = rag.synthesize_answer(query, results)
        st.markdown("### 🔍 Top PDF Results")
        st.write(answer)
        st.markdown("### 📚 Sources (from PDF)")
        for doc in results:
            source = doc.metadata.get("source", "PDF")
            page = doc.metadata.get("page")
            if page:
                st.markdown(f"- 📄 {source}, Page {page}")
            else:
                st.markdown(f"- 📄 {source}")


# Web Search
st.markdown("---")
st.subheader("🌐 Real-Time Web Search")
web_query = st.text_input("Search the web for latest information:")
if web_query and st.button("🌎 Search Web"):
    with st.spinner("Searching the web..."):
        results = searcher.search(web_query)
    st.markdown("### 🌐 Web Search Results")
    for i, item in enumerate(results):
        st.markdown(f"**{i+1}. [{item['title']}]({item['link']})**")
        st.write(item["snippet"])

# Hybrid Search and Answer
st.markdown("---")
st.subheader("🧠 Hybrid RAG (PDF + Web)")
hybrid_query = st.text_input("Ask your research question:")
if hybrid_query and st.button("🧪 Run Hybrid RAG"):
    with st.spinner("Running hybrid search..."):
        web_results = searcher.search(hybrid_query)
        hybrid_docs = rag.hybrid_search(hybrid_query, web_results)
        answer = rag.synthesize_answer(hybrid_query, hybrid_docs)

    st.markdown("### ✅ Final Answer")
    st.write(answer)

    st.markdown("### 📚 Sources")
    for doc in hybrid_docs:
        source = doc.metadata.get("source")
        page = doc.metadata.get("page")
        title = doc.metadata.get("title", source)

        if source and source.startswith("uploads/"):  # PDF file
            label = f"📄 {source}"
            if page: label += f" (Page {page})"
        else:  # Web
            label = f"🌐 [{title}]({source})"

        st.markdown(f"- {label}")
