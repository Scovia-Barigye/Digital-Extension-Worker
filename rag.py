import os
import requests
import json
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
    """Call Sunbird STT API to transcribe audio."""
    if not api_key:
        return "Error: Sunbird STT API Key missing."
    
    url = "https://api.sunbird.ai/tasks/stt"
    headers = {"Authorization": f"Bearer {api_key}"}
    files = {"audio": ("audio.wav", audio_bytes, "audio/wav")}
    
    try:
        response = requests.post(url, headers=headers, files=files, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data.get("text", "Error: Transcription not found in response.")
    except Exception as e:
        return f"Error transcribing audio: {str(e)}"

def generate_answer(query, context, api_key, language):
    """Call Sunbird Sunflower API to generate a grounded answer."""
    if not api_key:
        return "Error: Sunbird Sunflower API Key missing."
    
    # Sanitize input to handle non-ASCII characters (like em-dashes \u2014) 
    # that can cause 'latin-1' encoding errors in some environments.
    def sanitize(text):
        if not text: return ""
        # Specifically replace problematic dashes which are common in PDF extracts
        text = text.replace('\u2014', '-').replace('\u2013', '-')
        # If there are other non-ascii, ignore them for safety or stay UTF-8
        return text.encode("utf-8", errors="ignore").decode("utf-8")
    
    clean_query = sanitize(query)
    clean_context = sanitize(context)
    
    system_prompt = (
        "You are a local Ugandan Agricultural Extension Worker. "
        "Answer the farmer's question based strictly on the provided context from the agricultural manual. "
        "If the answer is not in the document, politely say so. Keep the tone helpful and professional. "
        f"Always respond in {language}."
    )
    
    url = "https://api.sunbird.ai/tasks/sunflower_inference"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8"
    }
    payload = {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Context: {clean_context}\n\nQuestion: {clean_query}"}
        ],
        "model_type": "qwen",
        "temperature": 0.3
    }
    
    try:
        # Manually encode payload to UTF-8 to bypass potential encoding issues in requests/urllib3
        payload_json = json.dumps(payload).encode("utf-8")
        response = requests.post(url, headers=headers, data=payload_json, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        # Debugging: handle both dict and list responses
        if isinstance(data, list) and len(data) > 0:
            data = data[0]
            
        if isinstance(data, dict):
            # Prioritize standard Sunbird keys, then fall back to others
            for key in ["content", "response", "text", "result", "output", "answer"]:
                if key in data:
                    return data[key]
            
            # OpenAI / LLM style nested response
            if "choices" in data and len(data["choices"]) > 0:
                choice = data["choices"][0]
                if isinstance(choice, dict):
                    if "message" in choice and "content" in choice["message"]:
                        return choice["message"]["content"]
                    elif "text" in choice:
                        return choice["text"]
            
            # If we reach here, we found a dict but no recognized key
            found_keys = list(data.keys())
            return f"Error: Recognized key not found in API response. Found keys: {found_keys}"
        
        return f"Error: Unexpected response format from Sunbird API: {type(data).__name__}"
            
    except Exception as e:
        return f"Error generating answer: {str(e)}"
