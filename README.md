# 🚀 Multi-Agent AI Research Assistant

**(Google ADK + Ollama + Gemini)**

---

## 📌 Overview

A scalable **multi-agent AI system** that performs intelligent research by combining **local LLMs (Ollama)** with **cloud models (Gemini)**.
It automates the full pipeline from **query understanding → data retrieval → verification → report generation**.

---

## ✨ Features

* 🧠 **Multi-Agent Architecture**

  * Planner, Search, Research, Summarizer, Verification, Writer

* 🔀 **Hybrid AI System**

  * Local LLM: **Ollama (Mistral)**
  * Cloud LLM: **Gemini API**

* 🌐 **Real-Time Data Retrieval**

  * Web Search
  * arXiv Papers
  * News Sources

* 📄 **Intelligent Summarization**

  * Context-aware chunking and summarization

* 🧾 **Structured Report Generation**

  * Clean, readable, and well-organized outputs

* 🛡️ **Fault-Tolerant Pipeline**

  * Retry mechanisms
  * API fallback strategies

---

## 🧠 Architecture

```plaintext
User Query
   ↓
Planner Agent
   ↓
Search Agent (Web + arXiv + News)
   ↓
Research Agent (Scraping + Chunking)
   ↓
Summarizer Agent (Ollama)
   ↓
Verification Agent
   ↓
Writer Agent (Gemini)
```

---

## ⚙️ Tech Stack

* **Backend:** Python, FastAPI
* **AI Framework:** Google ADK
* **Local LLM:** Ollama (Mistral)
* **Cloud LLM:** Gemini API
* **Web Scraping:** BeautifulSoup, Requests

---

## 📂 Project Structure

```plaintext
multi_agent_research_system/
│
├── agents/
│   ├── planner_agent.py
│   ├── search_agent.py
│   ├── research_agent.py
│   ├── summarizer_agent.py
│   ├── verification_agent.py
│   └── writer_agent.py
│
├── tools/
│   ├── google_search.py
│   ├── arxiv_search.py
│   ├── news_search.py
│   └── scraper.py
│
├── app.py
├── requirements.txt
└── README.md
```

---

## ▶️ How to Run

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Start Ollama Server

```bash
ollama serve
```

### 3️⃣ Run ADK Web Interface

```bash
adk web
```

---

## ⚡ Workflow

1. User enters a research query
2. Planner Agent breaks down the problem
3. Search Agent fetches relevant sources
4. Research Agent extracts and chunks data
5. Summarizer Agent (Ollama) processes content
6. Verification Agent validates information
7. Writer Agent (Gemini) generates final report

---

## 🔥 Key Highlights

* 🚀 Combines **RAG + Multi-Agent Systems**
* ⚡ Reduces API cost using **local LLMs**
* 🧩 Modular and extensible architecture
* 📊 Suitable for research, analysis, and automation

---

## 📌 Future Improvements

* Add **vector database (FAISS / Pinecone)**
* Integrate **memory-based agents**
* Add **UI dashboard (React / Next.js)**
* Implement **real-time streaming responses**

---

## 👨‍💻 Author

**Jeeban Mohanty**
AI Engineer | Full Stack Developer | Data Engineer
