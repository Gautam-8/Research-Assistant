# ragpipe.py

import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
import requests
from openai import OpenAI


# Embeddings from LM Studio
class LMStudioEmbeddings(Embeddings):
    def __init__(self, endpoint_url: str = "http://localhost:1234/v1/embeddings", model_name: str = "text-embedding-nomic-embed-text-v1.5"):
        self.endpoint_url = endpoint_url
        self.model_name = model_name

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        payload = {"model": self.model_name, "input": texts}
        headers = {"Content-Type": "application/json"}
        response = requests.post(self.endpoint_url, json=payload, headers=headers)
        response.raise_for_status()
        return [item['embedding'] for item in response.json()["data"]]

    def embed_query(self, text: str) -> List[float]:
        return self.embed_documents([text])[0]


class RAGPipeline:
    def __init__(self, persist_dir="db"):
        self.persist_dir = persist_dir
        self.embeddings = LMStudioEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        self.llm = OpenAI(
            base_url="http://localhost:1234/v1",
            api_key="not-needed"
        )

    def load_and_split_pdf(self, pdf_path: str) -> List[Document]:
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        chunks = self.text_splitter.split_documents(documents)
        return chunks

    def index_chunks(self, chunks: List[Document]):
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=self.embeddings,
            persist_directory=self.persist_dir
        )
        vectordb.persist()
        return vectordb

    def query_pdf(self, query: str, top_k=3) -> List[Document]:
        vectordb = Chroma(persist_directory=self.persist_dir, embedding_function=self.embeddings)
        return vectordb.as_retriever(search_kwargs={"k": top_k}).get_relevant_documents(query)

    def hybrid_search(self, query: str, web_results: list, top_k_pdf=3) -> List[Document]:
        vectordb = Chroma(persist_directory=self.persist_dir, embedding_function=self.embeddings)
        pdf_chunks = vectordb.as_retriever(search_kwargs={"k": top_k_pdf}).get_relevant_documents(query)

        # Convert web results into Document-like format
        web_chunks = [
            Document(
                page_content=item["snippet"],
                metadata={"source": item["link"], "title": item["title"]}
            )
            for item in web_results
        ]

        return pdf_chunks + web_chunks

    def synthesize_answer(self, query: str, sources: List[Document]) -> str:
        context = "\n\n".join([doc.page_content for doc in sources])
        prompt = f"Answer the question using the following context:\n\n{context}\n\nQuestion: {query}"

        response = self.llm.chat.completions.create(
            model="google/gemma-3-1b",
            messages=[
                {"role": "system", "content": "You are an expert research assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        if response.choices[0].message.content:
            return response.choices[0].message.content
        else:
            return "No answer found"
