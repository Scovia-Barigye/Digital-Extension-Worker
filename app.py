import os
import streamlit as st

# Import all RAG and API functions from rag.py
from rag import (
    init_settings, 
    get_vector_store, 
    ingest_documents, 
    retrieve_context, 
    transcribe_audio, 
    generate_answer
)

# --- CONFIGURATION ---
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Initialize global LLM settings and DB from rag.py
init_settings()
vector_store = get_vector_store()

# --- STREAMLIT UI ---
st.set_page_config(page_title="Digital Extension Worker", page_icon="🌾", layout="wide")

# Tailwind / Custom CSS injection for Uganda-First Theme
st.markdown("""
<style>
    /* Main Background: slate-900 */
    .stApp {
        background-color: #0f172a;
        color: #f8fafc;
    }
    
    /* Sidebar Background: slate-800 */
    [data-testid="stSidebar"] {
        background-color: #1e293b;
    }
    
    /* Headers and Text */
    h1, h2, h3, p, div {
        color: #f8fafc;
    }
    
    /* Buttons: orange-600 */
    .stButton>button {
        background-color: #ea580c !important;
        color: white !important;
        border: none !important;
        border-radius: 0.375rem !important;
        padding: 0.5rem 1rem !important;
        font-weight: 600 !important;
    }
    .stButton>button:hover {
        background-color: #c2410c !important; /* orange-700 on hover */
    }
    
    /* Accents & Highlights: amber-500 */
    .stFileUploader>div>div>div>button {
        color: #f59e0b !important;
    }
    
    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: #1e293b;
        border-radius: 0.5rem;
        padding: 1rem;
        margin-bottom: 1rem;
        border-left: 4px solid #f59e0b; /* amber-500 accent */
    }
    
    /* Chat Input Background */
    [data-testid="stChatInput"] {
        background-color: #334155 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🌾 Digital Extension Worker")
st.markdown("Ask agricultural questions based on verified local manuals.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    sunbird_stt_key = st.text_input("Sunbird STT API Key", type="password", key="stt_key")
    sunbird_sunflower_key = st.text_input("Sunbird Sunflower API Key", type="password", key="sunflower_key")
    response_language = st.selectbox("Response Language", ["English", "Luganda", "Runyankole", "Swahili"])
    
    st.divider()
    
    st.header("📄 Upload Manuals")
    uploaded_files = st.file_uploader("Upload PDF Manuals", type=["pdf"], accept_multiple_files=True)
    
    if st.button("Process & Index Documents"):
        if uploaded_files:
            with st.spinner("Processing documents..."):
                # Save uploaded files to the DATA_DIR
                for uploaded_file in uploaded_files:
                    file_path = os.path.join(DATA_DIR, uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # Ingest data using rag.py
                ingest_documents(DATA_DIR, vector_store)
                st.success(f"Successfully indexed {len(uploaded_files)} document(s)!")
        else:
            st.warning("Please upload PDF files first.")

# --- CHAT STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "source" in message:
            st.caption(f"**Source:** {message['source']}")

# --- INPUT HANDLING ---
query_text = st.chat_input("Type your question here...")
audio_bytes = st.experimental_audio_input("Or ask via voice") if hasattr(st, "experimental_audio_input") else st.audio_input("Or ask via voice")

query = None

if audio_bytes:
    with st.spinner("Transcribing audio..."):
        query = transcribe_audio(audio_bytes.getvalue(), sunbird_stt_key)
        if "Error" in query:
            st.error(query)
            query = None
elif query_text:
    query = query_text

# --- RETRIEVAL & GENERATION ---
if query:
    # 1. Add user query to chat history
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
        
    # 2. Retrieve context and generate answer
    with st.chat_message("assistant"):
        with st.spinner("Searching manuals and generating answer..."):
            try:
                # Retrieve from rag.py
                context, source_str = retrieve_context(query, vector_store)
                
                if context:
                    # Generate Answer via Sunbird from rag.py
                    answer = generate_answer(query, context, sunbird_sunflower_key, response_language)
                    
                    st.markdown(answer)
                    st.caption(f"**Source:** {source_str}")
                    
                    st.session_state.messages.append({
                        "role": "assistant", 
                        "content": answer,
                        "source": source_str
                    })
                else:
                    msg = "I couldn't find relevant information in the manuals."
                    st.warning("No relevant information found in the uploaded manuals for this query.")
                    st.session_state.messages.append({"role": "assistant", "content": msg})
                    
            except Exception as e:
                st.error(f"Error during retrieval: {e}")
                if "empty" in str(e).lower() or "not found" in str(e).lower():
                    st.info("Please upload and index some PDF manuals first via the sidebar.")
