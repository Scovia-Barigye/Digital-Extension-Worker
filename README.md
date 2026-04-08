# Digital Extension Worker

> **Empowering farmers with fast, localized, and verified agricultural advice through AI.**

## Overview

The **Digital Extension Worker** is a local, AI-powered agricultural advisory system built to deliver accurate and accessible farming advice. Designed with a "Uganda-First" approach, it bridges the knowledge gap by using **Retrieval-Augmented Generation (RAG)** to "read" local agricultural PDF manuals and provide hyper-specific, hallucination-free answers to farmer queries. 

Whether interacting via text or voice, farmers receive actionable advice in local languages, grounded entirely in trusted documentary sources.

---

##  Table of Contents

- [Core Features](#-core-features)
- [Tech Stack](#-tech-stack)
- [Installation \& Setup](#-installation--setup)
- [Usage Guide](#-usage-guide)
- [Roadmap](#-roadmap)
- [Contributing](#-contributing)

---

##  Core Features

- **Offline Document Knowledge**: Ingests and memorizes agricultural PDF manuals locally without relying on external cloud databases, utilizing **LlamaIndex** and **ChromaDB**.
- **Multimodal Voice & Text Inputs**: Farmers can type their questions or speak directly into their devices. Audio is seamlessly transcribed via the **Sunbird STT API**.
- **Verified, Grounded Answers**: Powered by the **Sunbird Sunflower** text generation model. Every answer cites the exact source document name and page number, ensuring complete transparency and verifiability.
- **Multilingual Support**: Breaks localization barriers by offering extension advice in **English, Luganda, Runyankole, and Swahili**.
- **Responsive & Accessible UI**: Features a gorgeous, lightweight frontend built completely in **Streamlit**, styled with a custom responsive "Ruixen" dark-theme design.

---

## Tech Stack

- **Frontend / UI**: [Streamlit](https://streamlit.io/) with custom CSS injection.
- **Data Ingestion & RAG**: [LlamaIndex](https://www.llamaindex.ai/) core pipeline.
- **Vector Database**: [ChromaDB](https://www.trychroma.com/) (Local persistent storage).
- **Embeddings**: HuggingFace (`BAAI/bge-small-en-v1.5`).
- **AI Models**: [Sunbird AI APIs](https://sunbird.ai/) (Speech-to-Text & Sunflower Qwen).
- **Language**: Python 3.9+

---

##  Installation & Setup

Get the Digital Extension Worker running locally in under 5 minutes.

### Prerequisites

- **Python 3.9+** installed on your system.
- **Git** installed.
- Valid API keys from **Sunbird AI** (for STT and Sunflower).

### Setup Steps

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/Digital-Extension-Worker.git
   cd Digital-Extension-Worker
   ```

2. **Create a virtual environment (Recommended)**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install the dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the application**

   ```bash
   streamlit run app.py
   ```

---

##  Usage Guide

1. Open the application in your browser (usually `http://localhost:8501`).
2. Navigate to the sidebar and **enter your Sunbird API keys**.
3. Select your preferred **Response Language** (English, Luganda, Runyankole, or Swahili).
4. **Upload** one or more agricultural PDF manuals and click **"Process & Index Documents"**.
5. Once indexed, use the chat interface to **ask questions** either by typing or using the voice input feature!

---

##  Roadmap

- [X] Initial UI and custom styling implementation
- [X] Integrate LlamaIndex for local PDF ingestion
- [X] Set up local ChromaDB vector storage
- [X] Integrate Sunbird STT and Sunflower APIs
- [X] Add multilingual translation support
- [ ] Implement query logging for analytics
- [ ] Add support for additional document formats (e.g., DOCX, TXT)
- [ ] Containerize the application using Docker for easier deployment
- [ ] Expand local language support

---

##  Contributing

We welcome contributions to make the Digital Extension Worker even better!

To ensure a smooth collaboration process:
1. Please **open an issue** to discuss your proposed changes or feature requests before submitting a Pull Request (PR).
2. Follow the project's existing coding standards and architectural patterns.
3. Keep PRs focused and include a clear description of the modifications made.

---

*Harvesting intelligence for better agricultural yields.* 
