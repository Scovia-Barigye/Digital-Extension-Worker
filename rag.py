import os
import requests
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, StorageContext, Settings
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
import chromadb

# --- CONFIGURATION ---
DB_DIR = "chroma_db"
os.makedirs(DB_DIR, exist_ok=True)

@st.cache_resource
def init_settings():
    """Initialize LlamaIndex global settings."""
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
    Settings.llm = None
    return True

@st.cache_resource
def get_vector_store():
    """Initialize and return the ChromaDB persistent client and vector store."""
    db = chromadb.PersistentClient(path=DB_DIR)
    chroma_collection = db.get_or_create_collection("agri_manuals")
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    return vector_store

def ingest_documents(data_dir, vector_store):
    """Read PDFs from a directory and index them into the vector store."""
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    documents = SimpleDirectoryReader(data_dir).load_data()
    index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
    return index

def retrieve_context(query, vector_store):
    """Retrieve the single most relevant paragraph based on the query."""
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    retriever = index.as_retriever(similarity_top_k=1)
    
    nodes = retriever.retrieve(query)
    
    if nodes:
        best_node = nodes[0]
        context = best_node.text
        file_name = best_node.metadata.get("file_name", "Unknown File")
        page_label = best_node.metadata.get("page_label", "Unknown Page")
        source_str = f"{file_name}, Page {page_label}"
        return context, source_str
    
    return None, None

# --- SUNBIRD API PLACEHOLDERS ---
def transcribe_audio(audio_bytes, api_key):
    """Placeholder for Sunbird STT API."""
    if not api_key:
        return "Error: Sunbird STT API Key missing."
    
    # url = "https://api.sunbird.ai/tasks/stt"
    # headers = {"Authorization": f"Bearer {api_key}"}
    # files = {"audio": ("audio.wav", audio_bytes, "audio/wav")}
    # response = requests.post(url, headers=headers, files=files)
    # return response.json().get("text", "")
    
    return "This is a placeholder transcription from Sunbird STT."

def generate_answer(query, context, api_key, language):
    """Placeholder for Sunbird Sunflower API."""
    if not api_key:
        return "Error: Sunbird Sunflower API Key missing."
    
    system_prompt = f"You are a local Ugandan Agricultural Extension Worker. Answer the farmer's question based strictly on the provided context from the agricultural manual. If the answer is not in the document, politely say so. Always respond in {language}."
    
    # url = "https://api.sunbird.ai/tasks/sunflower"
    # headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    # payload = {
    #     "messages": [
    #         {"role": "system", "content": system_prompt},
    #         {"role": "user", "content": f"Context: {context}\\n\\nQuestion: {query}"}
    #     ]
    # }
    # response = requests.post(url, headers=headers, json=payload)
    # return response.json().get("choices")[0].get("message").get("content")
    
    return f"This is a placeholder generated answer in {language} based on the retrieved context."
