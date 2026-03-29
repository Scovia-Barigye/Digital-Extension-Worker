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

# Tailwind / Custom CSS injection for "Ruixen Agric" Theme
st.markdown("""
<style>
    /* Main Background: Dark Agricultural Cinematic */
    .stApp {
        background: linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), 
                    url('https://images.unsplash.com/photo-1464226184884-fa280b87c399?auto=format&fit=crop&q=80&w=2070');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #f0fdf4;
    }
    
    /* Ruixen-style Glassmorphism for Sidebars */
    [data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Headers & Text Style */
    h1 {
        font-weight: 700 !important;
        letter-spacing: -1px !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5);
    }
    
    /* Ruixen-Style Buttons (Quick Actions) */
    .stButton>button {
        background-color: rgba(0, 0, 0, 0.5) !important;
        color: #d1d5db !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 9999px !important; /* Full pill shape */
        padding: 0.4rem 1rem !important;
        font-size: 0.8rem !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: white !important;
        border-color: rgba(255, 255, 255, 0.3) !important;
        transform: translateY(-1px);
    }
    
    /* Chat Messages: Layered styling */
    [data-testid="stChatMessage"] {
        background-color: rgba(0, 0, 0, 0.6) !important;
        backdrop-filter: blur(8px);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
    }
    
    /* User: Ruixen Neutral Border */
    [data-testid="stChatMessage"]:has([data-testid="stChatUser"]) {
        border-left: 4px solid #4ade80; /* Green accent */
    }

    /* Assistant: Golden Sunbird Border */
    [data-testid="stChatMessage"]:has([data-testid="stChatAssistant"]) {
        border-left: 4px solid #facc15; /* Yellow accent */
    }
    
    /* Chat Input Background */
    [data-testid="stChatInput"] {
        background-color: rgba(0, 0, 0, 0.7) !important;
        border-radius: 12px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        backdrop-filter: blur(12px);
    }
</style>
""", unsafe_allow_html=True)

# Centered AI Branding similar to Ruixen Moon
st.markdown("<div style='text-align: center; padding: 50px 0;'>", unsafe_allow_html=True)
st.markdown("<h1 style='font-size: 3.5rem; margin-bottom: 10px;'>🌾 Digital Extension</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #9ca3af; font-size: 1.2rem;'>Harvest intelligence — ask your agricultural questions below.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- QUICK ACTIONS (Ruixen Style) ---
cols = st.columns(4)
with cols[0]:
    if st.button(" Crop Advice"): st.session_state.messages.append({"role": "user", "content": "How do I maximize crop yield?"})
with cols[1]:
    if st.button(" Pest Control"): st.session_state.messages.append({"role": "user", "content": "Tell me about common pest management."})
with cols[2]:
    if st.button(" Weather Tips"): st.session_state.messages.append({"role": "user", "content": "How does current weather affect planting?"})
with cols[3]:
    if st.button(" Manual Search"): st.session_state.messages.append({"role": "user", "content": "Search the manuals for soil prep."})

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
