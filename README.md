# Digital-Extension-Worker
markdown
# 🌾 Digital Extension Worker
The **Digital Extension Worker** is a local, AI-powered agricultural advisory system built to provide fast, localized, and verified farming advice. It uses the power of **Retrieval-Augmented Generation (RAG)** to "read" local agricultural PDF manuals and answer farmer queries accurately, without making up information.
Built with a "Uganda-First" accessible design, the application can take in both text and voice questions, process them using **Sunbird AI's API**, and ground its answers directly in your uploaded PDF documents.
## 🌟 Key Features
- **Offline Document Knowledge**: Ingests and memorizes agricultural PDF manuals locally using **LlamaIndex** and **ChromaDB**.
- **Voice & Text Inputs**: Farmers can type their questions or speak directly into their device. Audio is transcribed via the **Sunbird STT API**.
- **Verified Answers**: The system uses the **Sunbird Sunflower** text generation model. Every answer provided includes the exact source document name and page number for easy verification.
- **Multilingual Support**: Supports providing extension advice in multiple local languages (English, Luganda, Runyankole, Swahili).
- **Responsive UI**: A gorgeous, lightweight frontend built completely in **Streamlit** and styled with a custom Tailwind-inspired theme.
## 🛠️ Architecture
- **Frontend**: Streamlit
- **Vector Database**: ChromaDB (Running locally on your machine)
- **Embeddings**: HuggingFace (`BAAI/bge-small-en-v1.5`)
- **Document Pipeline**: LlamaIndex core
- **Inference**: Sunbird AI APIs (Speech-to-Text & Sunflower)
## 🚀 How to Run Locally
1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/digital-extension-worker.git
   cd digital-extension-worker
Install the dependencies:

bash
   pip install -r requirements.txt
Start the application:

bash
   streamlit run app.py
Use it:

Add your Sunbird API keys into the Streamlit sidebar.
Upload any agricultural PDF manual.
Click "Process & Index Documents".
