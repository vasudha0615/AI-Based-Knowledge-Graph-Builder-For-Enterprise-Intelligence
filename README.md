# 🧠 (KGB) AI-Based Knowledge Graph Builder for Enterprise Intelligence

## **Developed as part of the Infosys Springboard Internship Program**
## **Author:** Vasudha Tulla
## **Live Demo:** [🚀 Launch App on Render](https://kgb-01.onrender.com)

[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Mistral](https://img.shields.io/badge/Mistral_LLM-7C3AED?style=for-the-badge)](https://mistral.ai)
[![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-00A3E0?style=for-the-badge&logo=meta&logoColor=white)](https://faiss.ai)
[![Neo4j](https://img.shields.io/badge/Neo4j-018bff?style=for-the-badge&logo=neo4j&logoColor=white)](https://neo4j.com)
[![MongoDB](https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://mongodb.com)
[![Slack](https://img.shields.io/badge/Slack-4A154B?style=for-the-badge&logo=slack&logoColor=white)](https://slack.com)

---

# 📖 Project Overview

This project builds an enterprise-level **AI-powered Knowledge Graph system** from structured and unstructured customer support ticket data.

The system extracts entities and relationships from support tickets using Mistral LLM, stores a **dynamic knowledge graph in Neo4j**, enables **intelligent semantic search via a RAG pipeline**, logs all AI metrics to **MongoDB in real time**, and sends **daily summaries via Slack and Email** — all deployed live on Render.com.

---

# 🎯 Objective

- **Automated extraction** of entities and relationships using Mistral LLM (NER)
- **Dynamic knowledge graph** stored in Neo4j with Cypher query support
- **Semantic search** over 8,469 tickets using FAISS vector embeddings
- **RAG-powered Q&A** grounded in real enterprise data
- **Real-time metrics** — response time, tokens, similarity scores → MongoDB
- **Slack + Email alerts** for daily metric summaries
- **Interactive dashboard** deployed live for enterprise access

---

# 🏗️ System Architecture

```
Raw Dataset (tickets.xlsx — 8,469 records)
      ↓
Data Cleaning & Enrichment (Pandas) → cleaned_tickets.xlsx
      ↓
┌─────────────────────────────────┐
│  Structured Triple Extraction   │  Rules Engine
│  (6 relation types from cols)   │  → structured_triples.csv
└──────────────┬──────────────────┘
               ↓
┌──────────────────────────────────┐
│  LLM-Based NER (Mistral 7B)      │  AI Engine
│  EXPERIENCING + REQUIRED_ACTION  │  → llm_triples.csv
└──────────────┬───────────────────┘
               ↓
         Merge → final_triples.csv
               ↓
    ┌──────────┴──────────┐
    ▼                     ▼
NetworkX Graph        Neo4j Desktop
(In-Memory)           (Persistent DB)
               ↓
Sentence Transformers (all-MiniLM-L6-v2)
→ 384-dim vectors → FAISS Index
               ↓
RAG Pipeline: Embed → Search → Context → Mistral → Answer
               ↓
Flask API → Metrics Logged to MongoDB (timestamp, response time,
           tokens, similarity score, cache hit rate)
               ↓
Streamlit Dashboard (5 Tabs)
+ Slack Webhook + Email (smtplib)
               ↓
Live on Render.com 🚀
```

---

# 🚀 Technologies Used

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11+ | Core development |
| **Data Processing** | Pandas, NumPy, OpenPyXL | Data ingestion & cleaning |
| **LLM** | Mistral 7B (Ollama) | NER, relation extraction, Q&A |
| **Graph (Memory)** | NetworkX | In-memory graph construction |
| **Graph Database** | Neo4j Desktop | Persistent graph storage |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) | 384-dim vectors |
| **Vector DB** | FAISS | Semantic similarity search |
| **Backend API** | Flask | REST endpoints + metrics logging |
| **Metrics DB** | MongoDB | Real-time query metrics storage |
| **Dashboard** | Streamlit + Plotly | Interactive enterprise UI |
| **Notifications** | Slack Webhook + smtplib | Daily metric summaries |
| **Deployment** | Render.com | Live cloud deployment |

---

# ✅ Milestone 1 — Data Ingestion & Schema Design

### Tasks Completed
- Loaded **8,469 enterprise support tickets** from `tickets.xlsx`
- Handled **5,700 missing values** as meaningful workflow states
- Applied text normalization — lowercase, strip whitespace, datetime conversion
- Created **4 enrichment columns**: Ticket State, Resolution Status, Severity, Resolution Time Category

### Output: `cleaned_tickets.xlsx` — 8,469 rows × 21 columns

---

# ✅ Milestone 2 — Entity Extraction & Graph Building

## Step 1: Structured Triple Extraction

```
(LG Smart TV,  HAS_ISSUE,     Product Setup)
(Ticket_1,     HAS_PRIORITY,  Critical)
(Ticket_1,     SUBMITTED_VIA, Email)
```
**Output:** `structured_triples.csv` — 50,814+ triples

## Step 2: LLM-Based NER (Mistral 7B)

```
(Dell XPS,       EXPERIENCING,    Not turning on)
(Dell XPS,       REQUIRED_ACTION, Troubleshoot power issues)
```
**Output:** `llm_triples.csv` — 40+ semantic triples

## Step 3: Merge + Neo4j Storage

```python
def create_graph(tx, subject, predicate, obj):
    relationship = clean_relationship(predicate)
    query = f"""
    MERGE (a:Entity {{name: $subject}})
    MERGE (b:Entity {{name: $object}})
    MERGE (a)-[r:{relationship}]->(b)
    """
    tx.run(query, subject=str(subject), object=str(obj))
```

### Graph Statistics
```
Total Nodes         : 8,500+
Total Relationships : 50,000+
Relation Types      : 8 types
```

---

# ✅ Milestone 3 — Semantic Search & RAG Pipeline

```
User Query → Embed (384-dim) → FAISS Search (top-3) →
Retrieve Context → Mistral LLM → Grounded Answer
```

```python
def rag_search(query):
    query_embedding  = create_embeddings([query])
    indices          = search(np.array(query_embedding))
    retrieved_docs   = [documents[i] for i in indices[0]]
    context          = "\n".join(retrieved_docs)
    response         = ollama.chat(model='mistral',
                         messages=[{"role":"user",
                         "content":f"Context:\n{context}\nQuestion:\n{query}"}])
    return response["message"]["content"]
```

---

# ✅ Milestone 4 — Dashboard, Metrics & Deployment

## Metrics Collection Layer (Flask + MongoDB)

Every query is automatically logged:
```python
metric_doc = {
    "timestamp":        datetime.datetime.utcnow(),
    "query":            query,
    "response_time_ms": response_time_ms,
    "token_usage":      token_usage,
    "similarity_score": avg_similarity,
    "cache_hit":        cache_hit,
    "model":            "mistral"
}
col.insert_one(metric_doc)
```

## Flask API Endpoints

| Endpoint | Method | Purpose |
|---|---|---|
| `/tickets` | GET | All 8,469 tickets as JSON |
| `/stats` | GET | Ticket statistics for KPI cards |
| `/search` | POST | RAG search + metrics logging |
| `/metrics` | GET | All logged metrics from MongoDB |
| `/metrics/summary` | GET | Aggregated stats summary |
| `/graph` | GET | Knowledge graph nodes and edges |
| `/health` | GET | System health check |

## Streamlit Dashboard (5 Tabs)

| Tab | Content |
|---|---|
| ⚡ Pipeline Overview | Ticket feed + triplet extraction + ontology graph + charts |
| 🔍 Semantic Search | RAG Q&A with response time + similarity score display |
| 📊 Metrics Dashboard | MongoDB charts — response time distribution, similarity, tokens, cache |
| 🕸️ Ontology Network | Full interactive knowledge graph |
| 📋 Data Explorer | Filter + export 8,469 tickets |

## Slack + Email Notifications

```python
# Daily Slack Summary
send_slack_summary(stats)   # Rich block format

# Daily Email Summary
send_email_summary(stats)   # HTML email via smtplib
```

---

# ⚙️ Installation & Setup

```bash
# 1. Clone the repository
git clone https://github.com/vasudha0615/AI-Based-Knowledge-Graph-Builder-For-Enterprise-Intelligence.git
cd AI-Based-Knowledge-Graph-Builder-For-Enterprise-Intelligence

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull Mistral model
ollama pull mistral

# 4. Start Neo4j Desktop and update password in llm.ipynb

# 5. Run Flask API
python app/flask_api.py

# 6. Run Streamlit Dashboard
python -m streamlit run app/app.py
```

---

# 📁 Project Structure

```
AI-Based-Knowledge-Graph-Builder/
│
├── 📓 data_ingestion.ipynb          # Milestone 1: Data cleaning & enrichment
├── 📓 llm.ipynb                     # Milestone 2: LLM NER + Neo4j graph
│
├── 📊 tickets.xlsx                  # Raw data (8,469 records)
├── 📊 cleaned_tickets.xlsx          # Processed dataset (21 columns)
├── 📊 structured_triples.csv        # Rule-based triples
├── 📊 llm_triples.csv               # LLM-extracted triples
├── 📊 final_triples.csv             # Merged knowledge graph dataset
│
├── 📁 semantic_rag/                 # Milestone 3
│   ├── documents.py                 # Knowledge base
│   ├── embeddings.py                # Sentence transformer embeddings
│   ├── vector.py                    # FAISS vector store
│   ├── rag_pipeline.py              # RAG Q&A pipeline
│   └── main.py                      # Entry point
│
├── 📁 app/                          # Milestone 4
│   ├── app.py                       # Streamlit dashboard (5 tabs)
│   ├── flask_api.py                 # Flask REST API (7 endpoints)
│   ├── metrics.py                   # MongoDB metrics logger
│   └── notifications.py             # Slack + Email alerts
│
├── requirements.txt                 # Dependencies
├── render.yaml                      # Render.com deployment config
└── README.md
```

---

# 📊 Current Status

```
Milestone 1 ✅ Data Ingestion & Schema Design    — Completed
Milestone 2 ✅ Entity Extraction & Graph Building — Completed
Milestone 3 ✅ Semantic Search & RAG Pipeline     — Completed
Milestone 4 ✅ Dashboard + Metrics + Deployment   — Completed
```

---

# 🌐 Deployment — How to Get Live Link (Render.com)

```
1. Push code to GitHub
2. Go to render.com → New Web Service
3. Connect GitHub repo
4. Build Command: pip install -r requirements.txt
5. Start Command: python -m streamlit run app/app.py --server.port $PORT --server.address 0.0.0.0
6. Click Deploy → Get live URL!
```

---

# 🤖 Example Interaction

**Query:** *"Why is my LG TV overheating?"*

**Response:**
> Based on the enterprise knowledge base:
> 1. Likely caused by **Power Supply Failure**
> 2. Check **cooling system** for blockages
> 3. Ensure proper **ventilation**
> 4. Consider a **factory reset**

**Logged Metrics:**
```json
{
  "response_time_ms": 1247,
  "token_usage": 312,
  "similarity_score": 0.8734,
  "cache_hit": false,
  "model": "mistral"
}
```

---

# 👩‍💻 Author

**Vasudha Tulla**
*B.Tech CSE (AI & ML) · Global Institute of Engineering & Technology, Hyderabad*

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vasudha-tulla-95b35a335)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vasudha0615)
[![Email](https://img.shields.io/badge/Email-Contact-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tullavasudha@gmail.com)


---

⭐ **Star this repository if you found it useful!**
