<div align="center">

<img src="https://img.shields.io/badge/AI-Knowledge%20Graph%20Builder-06b6d4?style=for-the-badge&logo=graphql&logoColor=white"/>

# 🧠 AI-Based Knowledge Graph Builder
### *For Enterprise Intelligence*

> **Automatically extract entities, build dynamic knowledge graphs, and enable intelligent Q&A from enterprise data — powered by Mistral LLM, FAISS, and RAG pipelines.**

<br/>

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Mistral](https://img.shields.io/badge/Mistral-LLM-7C3AED?style=flat-square&logo=openai&logoColor=white)](https://mistral.ai)
[![FAISS](https://img.shields.io/badge/FAISS-Vector%20Search-00A3E0?style=flat-square&logo=meta&logoColor=white)](https://faiss.ai)
[![NetworkX](https://img.shields.io/badge/NetworkX-Graph-orange?style=flat-square)](https://networkx.org)
[![License](https://img.shields.io/badge/License-MIT-34d399?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Live-34d399?style=flat-square&logo=circle&logoColor=white)]()

<br/>

[🚀 Live Demo](#-live-demo) · [📖 Documentation](#-how-it-works) · [⚡ Quick Start](#-quick-start) · [📊 Results](#-results--outcomes)

<br/>

---

</div>

## 🎯 What is This Project?

Enterprise organizations process **thousands of support tickets daily** but struggle to find patterns, root causes, and actionable insights buried in unstructured text.

This platform **automatically solves that problem** by:

1. 🔄 **Ingesting** raw enterprise support ticket data
2. 🤖 **Extracting** entities and relationships using Mistral LLM
3. 🕸️ **Building** a dynamic, queryable knowledge graph
4. 🔍 **Enabling** intelligent Q&A using a Semantic RAG pipeline
5. 📊 **Visualizing** everything through an interactive enterprise dashboard

<br/>

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    ENTERPRISE DATA SOURCE                        │
│                  tickets.xlsx (8,469 records)                    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                  MILESTONE 1 · DATA INGESTION                    │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │ Load & Clean │→ │ Normalize    │→ │ Enrich & Export     │   │
│  │ (Pandas)     │  │ (lowercase,  │  │ (21 columns,        │   │
│  │              │  │  strip, date)│  │  cleaned_tickets)   │   │
│  └──────────────┘  └──────────────┘  └─────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│            MILESTONE 2 · ENTITY EXTRACTION & GRAPH              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │ Mistral LLM  │→ │ NER + Rel.   │→ │ Knowledge Graph     │   │
│  │ via Ollama   │  │ Extraction   │  │ (NetworkX/Neo4j)    │   │
│  │              │  │ Triplets     │  │ Nodes + Edges       │   │
│  └──────────────┘  └──────────────┘  └─────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              MILESTONE 3 · SEMANTIC RAG PIPELINE                 │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │ Sentence     │→ │ FAISS Vector │→ │ RAG Q&A Pipeline    │   │
│  │ Transformers │  │ Store        │  │ (Retrieve + Answer) │   │
│  │ Embeddings   │  │ (384-dim)    │  │ Mistral LLM         │   │
│  └──────────────┘  └──────────────┘  └─────────────────────┘   │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│              MILESTONE 4 · DASHBOARD & DEPLOYMENT               │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────┐   │
│  │ Streamlit    │  │ Plotly       │  │ Streamlit Cloud     │   │
│  │ Web App      │  │ Graph Viz    │  │ Live Deployment     │   │
│  │ 4 Pages      │  │ Dark UI      │  │ Enterprise Access   │   │
│  └──────────────┘  └──────────────┘  └─────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

<br/>

---

## ✨ Key Features

| Feature | Description | Technology |
|---|---|---|
| 🤖 **LLM Entity Extraction** | Automatically extract entities & relationships from raw text | Mistral 7B via Ollama |
| 🕸️ **Knowledge Graph** | Build directed graphs with nodes and edges | NetworkX + Plotly |
| 🔍 **Semantic Search** | Meaning-based search, not just keywords | FAISS + Sentence Transformers |
| 💬 **RAG Q&A** | Ask natural language questions, get grounded answers | RAG Pipeline + Mistral |
| 📊 **Live Dashboard** | Interactive enterprise analytics dashboard | Streamlit + Plotly |
| 🚀 **Cloud Deployed** | Accessible from any browser, anywhere | Streamlit Cloud |

<br/>

---

## 📁 Project Structure

```
AI-Based-Knowledge-Graph-Builder/
│
├── 📓 data_ingestion.ipynb          # Milestone 1: Data cleaning & enrichment
├── 📓 llm.ipynb                     # Milestone 2: LLM NER & Neo4j graph
│
├── 📊 tickets.xlsx                  # Raw enterprise data (8,469 records)
├── 📊 cleaned_tickets.xlsx          # Processed dataset (21 columns)
├── 📊 structured_triples.csv        # Rule-based triples from ticket columns
├── 📊 llm_triples.csv               # Semantic triples from Mistral LLM
├── 📊 final_triples.csv             # Merged complete knowledge graph dataset
│
├── 📁 semantic_rag/                 # Milestone 3: RAG Pipeline
│   ├── 🐍 documents.py             # Knowledge base documents
│   ├── 🐍 embeddings.py            # Sentence transformer embeddings
│   ├── 🐍 vector.py                # FAISS vector store & search
│   ├── 🐍 rag_pipeline.py          # Complete RAG Q&A pipeline
│   └── 🐍 main.py                  # Pipeline entry point
│
└── 📁 app/                          # Milestone 4: Dashboard & API
    └── 🐍 app.py                   # Streamlit dashboard + Flask API
```

<br/>

---

## 🗺️ Milestones

### ✅ Milestone 1 — Data Ingestion & Schema Design
> *Weeks 1-2 · Connect to enterprise data sources*

- Loaded **8,469 enterprise support tickets** with 17 raw columns
- Performed text normalization (lowercase, strip whitespace)
- Handled **5,700 missing values** intelligently as workflow states
- Created **4 enrichment columns**: Ticket State, Resolution Status, Severity, Resolution Time Category
- Final dataset: **21 columns**, fully structured and clean

```python
# Key transformation
df['Resolution'] = df['Resolution'].fillna('not resolved yet')
df['Severity']   = df['Ticket Priority'].replace({
    'Low': 'Minor', 'Medium': 'Moderate',
    'High': 'Major', 'Critical': 'Critical'
})
```

---

### ✅ Milestone 2 — Entity Extraction & Graph Building
> *Weeks 3-4 · Extract entities/relationships and construct graph*

## Step 1: Structured Triple Extraction (Rules Engine)

Extracted **entity–relationship–entity triples** directly from structured ticket columns.

*Example triples:*

```
(LG Smart TV,  HAS_ISSUE,     Product Setup)
(Ticket_1,     HAS_PRIORITY,  Critical)
(Ticket_1,     SUBMITTED_VIA, Email)
(Ticket_1,     HAS_STATUS,    Open)
(Ticket_1,     IS_TYPE,       Technical Issue)
(LG Smart TV,  RAISED,        Ticket_1)
```

**Output:** `structured_triples.csv`

## Step 2: LLM-Based NER (Mistral 7B)

Used **Mistral LLM** locally via Ollama to extract semantic triples from unstructured ticket descriptions.

*Example triples:*

```
(Dell XPS,       EXPERIENCING,    Not turning on)
(Dell XPS,       REQUIRED_ACTION, Troubleshoot power issues)
(LG Smart TV,    EXPERIENCING,    Intermittent issues)
(Nintendo Switch,EXPERIENCING,    Not charging properly)
```

**Output:** `llm_triples.csv`

## Step 3: Merge All Triples

Combined structured and LLM-generated triples into one unified dataset.

**Output:** `final_triples.csv`

## Step 4: Graph Construction

Built knowledge graph using **NetworkX** (in-memory) and pushed all triples to **Neo4j Desktop** using MERGE queries.

### Graph Statistics

```
Graph Statistics
─────────────────────────────────────
Structured Triples   : 50,814+
LLM Triples          : 40+
Total Final Triples  : 50,854+
Unique Nodes         : 8,500+
Unique Relationships : 6 types

Note: Running LLM on full 8,469 tickets generates
a significantly larger, interconnected knowledge graph.
```

## Step 5: Graph Validation

Validated graph integrity using Cypher queries in Neo4j Browser:
---

### ✅ Milestone 3 — Semantic Search & RAG Pipeline
> *Weeks 5-6 · Enable intelligent search and retrieval*

- Converted knowledge base to **384-dimensional vectors** using `all-MiniLM-L6-v2`
- Built **FAISS index** for millisecond-speed similarity search
- Implemented complete **RAG pipeline**: Embed → Retrieve → Augment → Generate
- Prevents LLM hallucination by grounding answers in **real enterprise data**

```python
# Complete RAG flow
def rag_search(query):
    query_embedding  = create_embeddings([query])       # Vectorize question
    indices          = search(np.array(query_embedding)) # FAISS search
    retrieved_docs   = [documents[i] for i in indices[0]] # Get context
    context          = "\n".join(retrieved_docs)          # Build context
    response         = ollama.chat(model="mistral",       # LLM answer
        messages=[{"role":"user","content": f"Context: {context}\nQuestion: {query}"}])
    return response["message"]["content"]
```

---

### ✅ Milestone 4 — Dashboard & Deployment
> *Weeks 7-8 · Interactive dashboards and live deployment*

- Built **4-page Streamlit dashboard** with glassmorphic dark UI
- **Tab 1**: Pipeline overview with live KPI metrics + interactive charts
- **Tab 2**: Semantic search powered by RAG pipeline
- **Tab 3**: Full ontology network visualization
- **Tab 4**: Data explorer with filters + CSV export
- Deployed live on **Streamlit Cloud** for enterprise access

<br/>

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology | Purpose |
|---|---|---|
| **Language** | Python 3.11+ | Core development |
| **Data Processing** | Pandas, NumPy, OpenPyXL | Data ingestion & cleaning |
| **LLM** | Mistral 7B (Ollama) | Entity extraction & Q&A |
| **ML Framework** | PyTorch, Transformers | Model inference |
| **Embeddings** | Sentence Transformers (all-MiniLM-L6-v2) | Text vectorization |
| **Vector DB** | FAISS | Semantic similarity search |
| **Graph** | NetworkX | Knowledge graph construction |
| **Graph DB** | Neo4j | Enterprise graph storage |
| **Visualization** | Plotly, Streamlit | Interactive dashboard |
| **Backend** | Flask | REST API endpoints |
| **Deployment** | Streamlit Cloud | Live enterprise access |
| **Version Control** | Git, GitHub | Code management |

</div>

<br/>

---

## ⚡ Quick Start

### Prerequisites
```bash
Python 3.11+
Ollama (for local LLM)
```

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/vasudha0615/AI-Based-Knowledge-Graph-Builder-For-Enterprise-Intelligence.git
cd AI-Based-Knowledge-Graph-Builder-For-Enterprise-Intelligence

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull Mistral model via Ollama
ollama pull mistral

# 4. Run the dashboard
cd app
python -m streamlit run app.py
```

### Requirements
```txt
streamlit
pandas
openpyxl
plotly
networkx
sentence-transformers
faiss-cpu
numpy
ollama
torch
transformers
flask
```

<br/>

---

## 📊 Results & Outcomes

<div align="center">

| Metric | Value |
|---|---|
| 📋 Total Tickets Processed | **8,469** |
| 🏷️ Dataset Columns | **21** (17 original + 4 enriched) |
| 🧠 LLM Model | **Mistral 7B** |
| 📐 Embedding Dimensions | **384** |
| 🔍 Search Algorithm | **FAISS IndexFlatL2** |
| 🕸️ Graph Nodes | **10+** unique entities |
| 🔗 Graph Edges | **7+** relationships |
| ⏱️ Search Speed | **< 100ms** per query |
| 🌐 Deployment | **Streamlit Cloud** |

</div>

<br/>

---

## 🔍 How It Works

### The RAG Pipeline — Step by Step

```
User Question: "Why is my LG TV overheating?"
        │
        ▼
┌───────────────────┐
│  1. EMBED QUERY   │  → all-MiniLM-L6-v2 converts to [0.25, -0.43, 0.88, ...]
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  2. FAISS SEARCH  │  → Finds top-3 similar documents in milliseconds
└─────────┬─────────┘     Doc 1: "Customer reported overheating in LG Smart TV"
          │               Doc 2: "Power supply failure may cause overheating"
          │               Doc 3: "Check cooling system if TV heats excessively"
          ▼
┌───────────────────┐
│  3. BUILD CONTEXT │  → Combines retrieved docs into context block
└─────────┬─────────┘
          │
          ▼
┌───────────────────┐
│  4. MISTRAL LLM   │  → Generates grounded answer from context
└─────────┬─────────┘
          │
          ▼
"Your LG TV is likely overheating due to a power supply failure.
 Check the cooling system and ensure proper ventilation..."
```

<br/>

---

## 🎯 Business Impact

This platform delivers **real enterprise value**:

- ⚡ **Saves hours** of manual ticket analysis per day
- 🎯 **Identifies patterns** across thousands of tickets automatically
- 💡 **Surfaces root causes** that humans would miss
- 🤖 **Answers questions** in seconds instead of searching through thousands of records
- 📈 **Improves decision making** with data-driven insights
- 🔗 **Connects the dots** between products, issues, causes, and resolutions

<br/>

---

## 🚀 Live Demo

> 🌐 **[Launch Live App](https://share.streamlit.io)** ← *(Deploy to get your URL)*

**Local Demo:**
```bash
python -m streamlit run app/app.py
# Opens at http://localhost:8501
```

**Sample Queries to Try:**
```
💬 "Why is my LG TV overheating?"
💬 "How to fix network connectivity issues?"
💬 "What products have the most critical tickets?"
💬 "What causes power supply failure?"
```

<br/>

---

## 📬 Contact

<div align="center">

**Vasudha Tulla**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vasudha-tulla-95b35a335)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/vasudha0615)
[![Email](https://img.shields.io/badge/Email-Contact-EA4335?style=for-the-badge&logo=gmail&logoColor=white)](mailto:tullavasudha@gmail.com)

*Open to AI/ML Engineering · Data Science · NLP · Full Stack AI opportunities*

</div>

<br/>

---

<div align="center">

**⭐ Star this repository if you found it useful!**

*Built with ❤️ during internship · AI Knowledge Graph Builder · Enterprise Intelligence*

</div>
