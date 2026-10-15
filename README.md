# AI Knowledge Retrieval & Multi-Agent RAG Platform

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_Store-orange?style=for-the-badge)](https://www.trychroma.com/)
[![Groq](https://img.shields.io/badge/Groq-LPU_Inference-f55036?style=for-the-badge)](https://groq.com/)
[![Ollama](https://img.shields.io/badge/Ollama-Offline_LLM-black?style=for-the-badge)](https://ollama.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)

An enterprise-ready **Multi-Agent Retrieval-Augmented Generation (RAG) Platform** featuring intelligent document ingestion, semantic vector retrieval, multi-agent query orchestration, real-time voice interaction, response transparency with citations, query analytics, and automated knowledge-gap detection.

---

## 🌟 Key Features

- 📄 **Multi-Format Document Ingestion**: Upload and index **PDF, DOCX, TXT, and CSV** documents with automated text extraction, cleaning, and chunking.
- ⚡ **Lightning-Fast Generation**: Powered by **Groq Cloud API** (~0.5s per response) with seamless offline fallback to **local Ollama** (`llama3.2`).
- 🎙️ **Real-Time Voice Interaction**:
  - Live, streaming speech-to-text as you speak using the Web Speech API.
  - Automatic fallback to high-precision local/cloud Whisper.
  - Integrated Text-to-Speech (TTS) voice readout.
- 🔍 **Multi-Agent Query Resolution**:
  - **Query Understanding Agent**: Classifies queries into factual, procedural, comparative, or ambiguous intents.
  - **Clarification Agent**: Detects genuinely underspecified questions without interrupting clear multi-turn queries.
  - **Retrieval Agent**: Hybrid semantic search over ChromaDB embeddings (`all-MiniLM-L6-v2`) with cosine distance thresholding and re-ranking.
  - **Response Generation Agent**: Strictly grounds answers in retrieved document chunks with clear bullet points and zero hallucinations.
  - **Conversation Memory Agent**: Context resolution for multi-turn conversations and follow-up questions.
- 📊 **Query Analytics & Knowledge Gaps**:
  - Real-time dashboard tracking query types, domain categorization, response latencies, and confidence scores.
  - Automated cluster detection for knowledge gaps and low-confidence queries.
- 🛡️ **Response Transparency**: Full citation inspection showing document name, chunk ID, relevance distance, and exact matched text.

---

## 🏗️ System Architecture

```
User Query (Text or Voice)
       │
       ▼
┌─────────────────────────────────┐
│     Multi-Agent Orchestrator     │
└──────────────┬──────────────────┘
               │
       ┌───────┴─────────────────┐
       ▼                         ▼
┌───────────────┐        ┌────────────────┐
│ Clarification │        │     Query      │
│     Agent     │        │ Understanding  │
└───────────────┘        └───────┬────────┘
                                 │
                                 ▼
                         ┌────────────────┐
                         │   Retrieval    │ ◄─── ChromaDB Vector Store
                         │     Agent      │      (all-MiniLM-L6-v2)
                         └───────┬────────┘
                                 │
                                 ▼
                         ┌────────────────┐
                         │    Response    │ ◄─── Groq API / Ollama
                         │Generation Agent│      (Llama 3.2 / Qwen)
                         └───────┬────────┘
                                 │
                                 ▼
                  Final Grounded Answer + Citations
```

---

## 📁 Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── main.py                       # FastAPI application & REST endpoints
│   │   ├── orchestrator.py               # Central multi-agent coordinator
│   │   ├── query_understanding_agent.py  # Intent & query classifier
│   │   ├── clarification_agent.py        # Ambiguity detection & follow-ups
│   │   ├── retrieval_agent.py            # Vector search & chunk retrieval
│   │   ├── response_generation_agent.py  # Grounded LLM answer generator
│   │   ├── conversation_memory_agent.py  # Multi-turn conversational memory
│   │   ├── vector_store.py               # ChromaDB client & collection management
│   │   ├── document_processor.py         # PDF, DOCX, TXT, CSV extractors
│   │   ├── chunker.py                    # Semantic text chunking
│   │   ├── embeddings.py                 # Sentence-Transformers embeddings
│   │   ├── speech_to_text.py             # Whisper audio transcription
│   │   ├── query_analytics.py            # Metrics & knowledge gap analyzer
│   │   └── config.py                     # Centralized settings & env configuration
│   ├── data/
│   │   ├── uploads/                      # Ingested documents
│   │   └── analytics/                    # Query analytics logs
│   └── requirements.txt                  # Backend Python dependencies
├── frontend/
│   └── index.html                        # Modern single-page web application
├── docs/
│   ├── technical-understanding.md        # Technical specifications & design docs
│   └── architecture.drawio               # System architecture diagram
├── requirements.txt                      # Root requirements for cloud buildpacks
├── .env.example                          # Environment variable template
├── .gitignore
└── README.md
```

---

## 🚀 Quick Start (Local Setup)

### 1. Clone the Repository
```bash
git clone https://github.com/SiddarthaGalla/AI_Knowledge_Retrievel_Platform.git
cd AI_Knowledge_Retrievel_Platform
```

### 2. Set Up Python Environment
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Add your Groq API key (free at [console.groq.com](https://console.groq.com)):
```env
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=qwen/qwen3.8-27b
```
*(Optional: If running offline without Groq, ensure [Ollama](https://ollama.com) is running locally with `ollama run llama3.2`).*

### 4. Run the Servers

**Start Backend (FastAPI)**:
```bash
uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

**Start Frontend**:
Open `frontend/index.html` in your browser, or serve it using Python:
```bash
python -m http.server 5500 --directory frontend
```
Navigate to: **`http://127.0.0.1:5500`**

---

## ☁️ Cloud Deployment Guide

### Option 1: Frontend on Vercel + Backend on Render (Recommended & Free)

#### Deploy Backend on Render:
1. Push your repo to GitHub.
2. Sign in to [Render.com](https://render.com) and create a **New Web Service**.
3. Select your GitHub repository.
4. Set:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT`
5. Under **Environment Variables**, add:
   - `GROQ_API_KEY`: `your_groq_key`
6. Copy your deployed service URL (e.g., `https://my-rag-backend.onrender.com`).

#### Deploy Frontend on Vercel:
1. Sign in to [Vercel.com](https://vercel.com) and click **Add New Project**.
2. Select your repository.
3. Set **Root Directory** to `frontend`.
4. Click **Deploy**.
5. Once live, open your Vercel URL, open DevTools (`F12`), and set your backend URL once:
   ```javascript
   localStorage.setItem("API_URL", "https://my-rag-backend.onrender.com");
   location.reload();
   ```

---

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check |
| `POST` | `/upload` | Upload and vectorize document (`.pdf`, `.docx`, `.txt`, `.csv`) |
| `POST` | `/query` | Execute RAG query with multi-agent orchestration |
| `GET` | `/memory` | Retrieve recent conversation context |
| `GET` | `/memory/clear` | Reset conversation memory |
| `POST` | `/transcribe` | Transcribe voice recording via Whisper |
| `GET` | `/analytics` | Retrieve raw query logs |
| `GET` | `/analytics/summary`| Metrics summary (total queries, answer rate, avg confidence) |
| `GET` | `/analytics/knowledge-gaps` | Clustered knowledge gaps & low-confidence questions |
| `GET` | `/analytics/query-types` | Distribution of factual, procedural, comparative queries |
| `GET` | `/analytics/report` | Full markdown analytics report |

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
