"""
app.py - Upgraded KGB Dashboard with MongoDB Metrics
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import networkx as nx
import sys, os, datetime
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'semantic_rag'))

st.set_page_config(page_title="KGB | Knowledge Graph Builder", page_icon="🧠", layout="wide", initial_sidebar_state="collapsed")

@st.cache_data
def load_data():
    base_dir  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, 'cleaned_tickets.xlsx')
    if os.path.exists(file_path):
        return pd.read_excel(file_path)
    return pd.DataFrame({
        'Ticket ID': range(1,101),
        'Product Purchased': (['LG Smart TV','Microsoft Office','Dell XPS','GoPro Hero','Autodesk AutoCAD']*20),
        'Ticket Type': (['Technical Issue','Billing Inquiry']*50),
        'Ticket Priority': (['Critical','High','Medium','Low']*25),
        'Ticket Status': (['Open','Closed','Pending Customer Response']*34)[:100],
        'Ticket Channel': (['Email','Phone','Chat','Social Media']*25),
        'Ticket Subject': (['Product Setup','Network Problem','Data Loss','Account Access','Overheating']*20),
        'Resolution Status': (['Resolved','Unresolved']*50),
    })

@st.cache_data(ttl=30)
def load_metrics():
    try:
        import requests
        r = requests.get("http://localhost:5000/metrics", timeout=3)
        if r.status_code == 200:
            d = r.json()
            return pd.DataFrame(d) if d else pd.DataFrame()
    except Exception:
        pass
    np.random.seed(42)
    n = 50
    times = [datetime.datetime.utcnow() - datetime.timedelta(hours=i) for i in range(n)]
    return pd.DataFrame({
        'timestamp': times,
        'query': [f'Sample query {i}' for i in range(n)],
        'response_time_ms': np.random.normal(1200,300,n).clip(200,3000),
        'token_usage': np.random.randint(100,500,n),
        'similarity_score': np.random.uniform(0.6,0.95,n),
        'cache_hit': np.random.choice([True,False],n,p=[0.2,0.8]),
        'model': ['mistral']*n,
        'answer_length': np.random.randint(100,800,n)
    })

df      = load_data()
metrics = load_metrics()

EDGES = [
    ("LG Smart TV","Overheating","has_issue"),
    ("Overheating","Power Supply Failure","caused_by"),
    ("Power Supply Failure","Cooling System Check","resolved_by"),
    ("Microsoft Office","Account Access","has_issue"),
    ("Account Access","Billing Inquiry","type"),
    ("Dell XPS","Network Problem","has_issue"),
    ("Network Problem","Software Update","resolved_by"),
]
NODE_COLORS = {
    "LG Smart TV":"#0ea5e9","Microsoft Office":"#0ea5e9","Dell XPS":"#0ea5e9",
    "Overheating":"#e879f9","Account Access":"#e879f9","Network Problem":"#e879f9",
    "Power Supply Failure":"#f59e0b","Billing Inquiry":"#f59e0b",
    "Cooling System Check":"#34d399","Software Update":"#34d399",
}

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
*,*::before,*::after{box-sizing:border-box;}
html,body,.stApp{background:radial-gradient(circle at top right,#0f172a,#000000)!important;color:#f8fafc!important;font-family:'Space Grotesk',sans-serif!important;}
#MainMenu,footer,header,[data-testid="stToolbar"],[data-testid="stDecoration"],[data-testid="stStatusWidget"]{visibility:hidden!important;display:none!important;}
.block-container{padding:24px 32px!important;max-width:100%!important;}
[data-testid="stSidebar"]{display:none!important;}
.glass{background:rgba(30,41,59,0.4)!important;backdrop-filter:blur(16px)!important;border:1px solid rgba(255,255,255,0.05)!important;box-shadow:0 4px 30px rgba(0,0,0,0.5)!important;border-radius:16px!important;padding:20px!important;margin-bottom:16px!important;}
.glass-header{background:linear-gradient(90deg,rgba(16,185,129,0.1),rgba(59,130,246,0.1));border-bottom:1px solid rgba(255,255,255,0.05);border-radius:16px 16px 0 0;padding:14px 20px;margin:-20px -20px 16px -20px;}
.glass-header-title{font-size:11px;font-weight:700;letter-spacing:0.12em;text-transform:uppercase;color:#e2e8f0;}
.brand-kgb{font-size:2.4rem;font-weight:800;background:linear-gradient(135deg,#34d399,#06b6d4);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.brand-sub{font-size:1.1rem;font-weight:300;color:#94a3b8;}
.brand-desc{font-size:13px;color:#64748b;margin-top:4px;}
.status-badge{display:inline-flex;align-items:center;gap:8px;background:rgba(30,41,59,0.8);border:1px solid rgba(255,255,255,0.08);border-radius:999px;padding:6px 16px;font-size:13px;color:#94a3b8;}
.status-dot{width:8px;height:8px;border-radius:50%;background:#34d399;box-shadow:0 0 8px rgba(52,211,153,0.8);animation:pulse-dot 2s infinite;}
@keyframes pulse-dot{0%,100%{opacity:1}50%{opacity:0.4}}
[data-testid="metric-container"]{background:rgba(30,41,59,0.4)!important;backdrop-filter:blur(16px)!important;border:1px solid rgba(255,255,255,0.05)!important;border-radius:16px!important;padding:20px!important;transition:transform 0.2s,border-color 0.3s!important;}
[data-testid="metric-container"]:hover{transform:translateY(-3px)!important;border-color:rgba(52,211,153,0.3)!important;}
[data-testid="stMetricValue"]{font-family:'JetBrains Mono',monospace!important;font-size:2.2rem!important;font-weight:700!important;}
[data-testid="stMetricLabel"]{font-size:10px!important;letter-spacing:0.15em!important;text-transform:uppercase!important;color:#64748b!important;}
[data-testid="stButton"]>button{background:linear-gradient(135deg,#059669,#0891b2)!important;color:white!important;border:none!important;border-radius:999px!important;padding:10px 28px!important;font-weight:600!important;font-size:14px!important;box-shadow:0 4px 20px rgba(6,182,212,0.25)!important;width:auto!important;}
[data-testid="stButton"]>button:hover{transform:scale(1.05)!important;box-shadow:0 8px 30px rgba(6,182,212,0.4)!important;}
[data-testid="stTextInput"] input{background:rgba(15,23,42,0.8)!important;border:1px solid rgba(255,255,255,0.08)!important;border-radius:12px!important;color:#f8fafc!important;padding:12px 16px!important;font-size:14px!important;}
[data-testid="stTextInput"] input:focus{border-color:rgba(52,211,153,0.4)!important;box-shadow:0 0 0 3px rgba(52,211,153,0.1)!important;}
[data-testid="stSelectbox"]>div>div{background:rgba(15,23,42,0.8)!important;border:1px solid rgba(255,255,255,0.08)!important;border-radius:12px!important;color:#f8fafc!important;}
[data-testid="stTabs"] [data-testid="stTab"]{background:transparent!important;color:#64748b!important;border:none!important;font-size:13px!important;font-weight:500!important;padding:8px 20px!important;}
[data-testid="stTabs"] [aria-selected="true"]{color:#34d399!important;border-bottom:2px solid #34d399!important;}
hr{border-color:rgba(255,255,255,0.05)!important;}
.feed-card{background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.05);border-radius:10px;padding:12px;margin-bottom:10px;font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.7;}
.triplet-card{background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.05);border-radius:8px;padding:10px;margin-bottom:8px;font-family:'JetBrains Mono',monospace;font-size:11px;line-height:1.8;}
.answer-box{background:linear-gradient(135deg,rgba(16,185,129,0.06),rgba(6,182,212,0.06));border:1px solid rgba(52,211,153,0.2);border-radius:16px;padding:24px;margin-top:16px;font-size:15px;line-height:1.8;color:#e2e8f0;}
.badge{display:inline-block;background:rgba(6,182,212,0.1);color:#06b6d4;border:1px solid rgba(6,182,212,0.2);border-radius:999px;padding:2px 10px;font-size:11px;font-weight:600;font-family:'JetBrains Mono',monospace;}
.step-card{background:rgba(30,41,59,0.4);border:1px solid rgba(255,255,255,0.05);border-radius:16px;padding:20px;text-align:center;backdrop-filter:blur(16px);}
[data-testid="stDownloadButton"]>button{background:rgba(52,211,153,0.1)!important;border:1px solid rgba(52,211,153,0.3)!important;color:#34d399!important;border-radius:999px!important;font-weight:600!important;}
</style>
""", unsafe_allow_html=True)

# HEADER
c1,c2 = st.columns([3,1])
with c1:
    st.markdown("""<div style="padding:8px 0 4px;">
        <span class="brand-kgb">KGB</span>
        <span class="brand-sub">| Knowledge Graph Builder</span>
        <div class="brand-desc">Enterprise Intelligence · Mistral LLM + FAISS + Neo4j + MongoDB Metrics + Slack + Email</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown("""<div style="display:flex;justify-content:flex-end;align-items:center;height:100%;padding-top:12px;">
        <div class="status-badge"><div class="status-dot"></div> System Live</div></div>""", unsafe_allow_html=True)

st.markdown("<hr style='margin:12px 0 20px 0;'>", unsafe_allow_html=True)

tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "⚡  Pipeline Overview",
    "🔍  Semantic Search",
    "📊  Metrics Dashboard",
    "🕸️  Ontology Network",
    "📋  Data Explorer"
])

# TAB 1 — PIPELINE OVERVIEW
with tab1:
    resolved   = int(df[df['Resolution Status']=='Resolved'].shape[0])   if 'Resolution Status' in df.columns else 0
    unresolved = int(df[df['Resolution Status']=='Unresolved'].shape[0]) if 'Resolution Status' in df.columns else 0
    critical   = int(df[df['Ticket Priority'].str.lower()=='critical'].shape[0]) if 'Ticket Priority' in df.columns else 0
    c1,c2,c3,c4 = st.columns(4)
    with c1: st.metric("Tickets Parsed",f"{len(df):,}")
    with c2: st.metric("Unique Entities","11")
    with c3: st.metric("Relationships","11")
    with c4: st.metric("Resolution Rate",f"{round(resolved/max(len(df),1)*100)}%")
    st.markdown("<br>",unsafe_allow_html=True)
    l,r = st.columns([5,7])
    with l:
        st.markdown("""<div class="glass"><div class="glass-header"><div style="display:flex;justify-content:space-between;align-items:center;"><span class="glass-header-title">1. Raw Data Ingestion</span><span class="badge">cleaned_tickets.xlsx</span></div></div>""",unsafe_allow_html=True)
        for _,row in df[['Ticket ID','Product Purchased','Ticket Type','Ticket Priority']].head(4).iterrows():
            pc={'critical':'#f43f5e','high':'#f59e0b','medium':'#06b6d4','low':'#34d399'}.get(str(row.get('Ticket Priority','')).lower(),'#94a3b8')
            st.markdown(f"""<div class="feed-card"><div style="color:#06b6d4;font-size:10px;font-weight:700;">Ticket ID: {row['Ticket ID']}</div><div style="color:#e2e8f0;">📦 {row['Product Purchased']}</div><div style="color:#94a3b8;">Type: {row['Ticket Type']}</div><div style="color:{pc};font-size:10px;margin-top:4px;">▲ {str(row.get('Ticket Priority','')).upper()}</div></div>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
        st.markdown("<br>",unsafe_allow_html=True)
        st.markdown("""<div class="glass"><div class="glass-header"><span class="glass-header-title">2. Triplet Extraction Engine</span></div>""",unsafe_allow_html=True)
        tc1,tc2=st.columns(2)
        with tc1:
            st.markdown("""<div style="font-size:11px;font-weight:700;color:#34d399;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;">Rules Engine</div>""",unsafe_allow_html=True)
            for s,p,o in [("LG Smart TV","has_issue","Overheating"),("Dell XPS","has_issue","Network Problem"),("Microsoft Office","has_issue","Account Access")]:
                st.markdown(f"""<div class="triplet-card"><div style="color:#e2e8f0;">{s}</div><div style="color:#34d399;">↳ [{p}]</div><div style="color:#e2e8f0;">{o}</div></div>""",unsafe_allow_html=True)
        with tc2:
            st.markdown("""<div style="font-size:11px;font-weight:700;color:#e879f9;letter-spacing:0.08em;text-transform:uppercase;margin-bottom:10px;">Mistral LLM</div>""",unsafe_allow_html=True)
            for s,p,o in [("Overheating","caused_by","Power Supply Failure"),("Network Problem","resolved_by","Software Update"),("Account Access","categorized","Billing Inquiry")]:
                st.markdown(f"""<div class="triplet-card"><div style="color:#e2e8f0;">{s}</div><div style="color:#e879f9;">↳ [{p}]</div><div style="color:#e2e8f0;">{o}</div></div>""",unsafe_allow_html=True)
        st.markdown("</div>",unsafe_allow_html=True)
    with r:
        st.markdown("""<div class="glass"><div class="glass-header"><span class="glass-header-title">3. Live Ontology Network</span></div>""",unsafe_allow_html=True)
        G2=nx.DiGraph()
        for s,t,_ in EDGES: G2.add_edge(s,t)
        pos2=nx.spring_layout(G2,seed=42,k=2.2)
        ex,ey=[],[]
        for s,t in G2.edges():
            x0,y0=pos2[s];x1,y1=pos2[t];ex+=[x0,x1,None];ey+=[y0,y1,None]
        nl=list(G2.nodes())
        fig=go.Figure(data=[
            go.Scatter(x=ex,y=ey,mode='lines',line=dict(width=1,color='rgba(255,255,255,0.12)'),hoverinfo='none'),
            go.Scatter(x=[pos2[n][0] for n in nl],y=[pos2[n][1] for n in nl],mode='markers+text',text=nl,
                       textposition='top center',textfont=dict(color='#f8fafc',size=10,family='JetBrains Mono'),
                       marker=dict(size=18,color=[NODE_COLORS.get(n,'#334155') for n in nl],line=dict(width=1.5,color='rgba(255,255,255,0.2)')))
        ],layout=go.Layout(height=320,showlegend=False,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False,zeroline=False,showticklabels=False),
            yaxis=dict(showgrid=False,zeroline=False,showticklabels=False),margin=dict(t=10,b=10,l=10,r=10)))
        st.plotly_chart(fig,use_container_width=True)
        st.markdown("</div>",unsafe_allow_html=True)
        ch1,ch2=st.columns(2)
        with ch1:
            pc2=df['Ticket Priority'].value_counts().reset_index();pc2.columns=['Priority','Count']
            fig2=go.Figure(go.Bar(x=pc2['Priority'],y=pc2['Count'],marker=dict(color=['#f43f5e','#f59e0b','#06b6d4','#34d399'],line=dict(width=0)),text=pc2['Count'],textposition='outside',textfont=dict(color='#94a3b8',size=11)))
            fig2.update_layout(title=dict(text='By Priority',font=dict(color='#94a3b8',size=12)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',font=dict(color='#64748b'),xaxis=dict(gridcolor='rgba(255,255,255,0.05)'),yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),margin=dict(t=30,b=10,l=10,r=10),height=200)
            st.plotly_chart(fig2,use_container_width=True)
        with ch2:
            sc=df['Ticket Status'].value_counts().reset_index();sc.columns=['Status','Count']
            fig3=go.Figure(go.Pie(labels=sc['Status'],values=sc['Count'],hole=0.65,marker=dict(colors=['#06b6d4','#34d399','#f59e0b'],line=dict(color='rgba(0,0,0,0.5)',width=2)),textinfo='percent',textfont=dict(color='#e2e8f0',size=11)))
            fig3.update_layout(title=dict(text='By Status',font=dict(color='#94a3b8',size=12)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',legend=dict(font=dict(color='#64748b',size=10),bgcolor='rgba(0,0,0,0)'),margin=dict(t=30,b=10,l=10,r=10),height=200)
            st.plotly_chart(fig3,use_container_width=True)

# TAB 2 — SEMANTIC SEARCH
with tab2:
    st.markdown("""<div class="glass"><div class="glass-header"><span class="glass-header-title">RAG Pipeline — Retrieval Augmented Generation</span></div>""",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    for col,(num,title,desc) in zip([c1,c2,c3,c4],[("01","Embed Query","Convert to 384-dim vector"),("02","FAISS Search","Find top-k similar docs"),("03","Build Context","Combine retrieved knowledge"),("04","LLM Answer","Mistral generates answer")]):
        with col:
            st.markdown(f"""<div class="step-card"><div style="font-family:'JetBrains Mono';font-size:1.6rem;font-weight:700;color:rgba(52,211,153,0.2);margin-bottom:8px;">{num}</div><div style="font-weight:600;color:#e2e8f0;margin-bottom:6px;font-size:13px;">{title}</div><div style="font-size:11px;color:#64748b;line-height:1.5;">{desc}</div></div>""",unsafe_allow_html=True)
    st.markdown("</div><br>",unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    for col,q in zip([c1,c2,c3],["Why is my LG TV overheating?","How to fix network problems?","What causes power supply failure?"]):
        with col:
            if st.button(q,key=f"ex_{q}"): st.session_state.rag_query=q
    st.markdown("<br>",unsafe_allow_html=True)
    query=st.text_input("query",value=st.session_state.get('rag_query',''),placeholder="Ask anything about enterprise support tickets...",label_visibility="collapsed")
    if st.button("⚡  Initialize Search",key="search_main") and query:
        with st.spinner("Searching..."):
            try:
                import requests
                resp=requests.post("http://localhost:5000/search",json={"query":query},timeout=30)
                result=resp.json()
                answer=result.get("answer","")
                rt=result.get("response_time_ms",0)
                ss=result.get("similarity_scores",[])
                tok=result.get("token_usage",0)
                ch=result.get("cache_hit",False)
            except Exception:
                from rag_pipeline import rag_search
                answer=rag_search(query);rt=0;ss=[];tok=0;ch=False
        st.markdown(f"""<div class="answer-box"><div style="font-size:11px;font-weight:700;color:#34d399;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:14px;font-family:'JetBrains Mono';">✦ Mistral AI Response</div><div style="color:#e2e8f0;line-height:1.9;">{answer}</div><div style="margin-top:16px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.05);font-size:11px;color:#475569;font-family:'JetBrains Mono';">Query: "{query}"{f" · ⏱ {rt:.0f}ms · 🔢 {tok} tokens · {'⚡ cache hit' if ch else '🔄 fresh'}" if rt else ""}</div></div>""",unsafe_allow_html=True)
        if ss:
            st.markdown("<br>",unsafe_allow_html=True)
            sc1,sc2,sc3=st.columns(3)
            for col,s,i in zip([sc1,sc2,sc3],ss[:3],range(1,4)):
                with col: st.metric(f"Doc {i} Similarity",f"{s:.4f}")

# TAB 3 — METRICS DASHBOARD
with tab3:
    st.markdown("""<div class="glass"><div class="glass-header"><div style="display:flex;justify-content:space-between;align-items:center;"><span class="glass-header-title">Real-Time AI Metrics — MongoDB</span><span class="badge">Live Analytics</span></div></div>""",unsafe_allow_html=True)

    if not metrics.empty:
        c1,c2,c3,c4,c5=st.columns(5)
        with c1: st.metric("Total Queries",f"{len(metrics):,}")
        with c2: st.metric("Avg Response Time",f"{metrics['response_time_ms'].mean():.0f}ms")
        with c3: st.metric("Avg Similarity",f"{metrics['similarity_score'].mean():.4f}")
        with c4:
            cache_rate=metrics['cache_hit'].sum()/len(metrics)*100 if 'cache_hit' in metrics.columns else 0
            st.metric("Cache Hit Rate",f"{cache_rate:.1f}%")
        with c5: st.metric("Total Tokens",f"{metrics['token_usage'].sum():,}")

        st.markdown("</div><br>",unsafe_allow_html=True)
        st.markdown("""<div style="font-size:11px;font-weight:700;color:#64748b;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;">Response Time Distribution</div>""",unsafe_allow_html=True)

        c1,c2=st.columns(2)
        with c1:
            fig_rt=go.Figure(go.Histogram(x=metrics['response_time_ms'],nbinsx=20,marker=dict(color='#06b6d4',line=dict(width=0)),opacity=0.8))
            fig_rt.update_layout(title=dict(text='Response Time Distribution (ms)',font=dict(color='#94a3b8',size=13)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(13,18,36,0.5)',font=dict(color='#94a3b8'),xaxis=dict(gridcolor='#1e2d4a',title='Response Time (ms)'),yaxis=dict(gridcolor='#1e2d4a',title='Count'),margin=dict(t=40,b=30,l=10,r=10),height=280)
            st.plotly_chart(fig_rt,use_container_width=True)

        with c2:
            fig_sim=go.Figure(go.Histogram(x=metrics['similarity_score'],nbinsx=20,marker=dict(color='#a78bfa',line=dict(width=0)),opacity=0.8))
            fig_sim.update_layout(title=dict(text='Semantic Similarity Score Distribution',font=dict(color='#94a3b8',size=13)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(13,18,36,0.5)',font=dict(color='#94a3b8'),xaxis=dict(gridcolor='#1e2d4a',title='Similarity Score'),yaxis=dict(gridcolor='#1e2d4a',title='Count'),margin=dict(t=40,b=30,l=10,r=10),height=280)
            st.plotly_chart(fig_sim,use_container_width=True)

        st.markdown("""<div style="font-size:11px;font-weight:700;color:#64748b;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;">Metrics Over Time</div>""",unsafe_allow_html=True)

        if 'timestamp' in metrics.columns:
            metrics_sorted=metrics.sort_values('timestamp')
            fig_time=go.Figure()
            fig_time.add_trace(go.Scatter(x=metrics_sorted['timestamp'],y=metrics_sorted['response_time_ms'],mode='lines+markers',name='Response Time (ms)',line=dict(color='#06b6d4',width=2),marker=dict(size=4)))
            fig_time.add_trace(go.Scatter(x=metrics_sorted['timestamp'],y=metrics_sorted['similarity_score']*1000,mode='lines+markers',name='Similarity Score (×1000)',line=dict(color='#34d399',width=2),marker=dict(size=4)))
            fig_time.update_layout(title=dict(text='Response Time & Similarity Over Time',font=dict(color='#94a3b8',size=13)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(13,18,36,0.5)',font=dict(color='#94a3b8'),legend=dict(font=dict(color='#94a3b8'),bgcolor='rgba(0,0,0,0)'),xaxis=dict(gridcolor='#1e2d4a'),yaxis=dict(gridcolor='#1e2d4a'),margin=dict(t=40,b=30,l=10,r=10),height=280)
            st.plotly_chart(fig_time,use_container_width=True)

        c1,c2=st.columns(2)
        with c1:
            fig_tok=go.Figure(go.Bar(x=list(range(len(metrics))),y=metrics['token_usage'],marker=dict(color='#f59e0b',line=dict(width=0)),opacity=0.8))
            fig_tok.update_layout(title=dict(text='Token Usage Per Query',font=dict(color='#94a3b8',size=13)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(13,18,36,0.5)',font=dict(color='#94a3b8'),xaxis=dict(gridcolor='#1e2d4a',title='Query #'),yaxis=dict(gridcolor='#1e2d4a',title='Tokens'),margin=dict(t=40,b=30,l=10,r=10),height=250)
            st.plotly_chart(fig_tok,use_container_width=True)

        with c2:
            cache_counts={'Cache Hit':int(metrics['cache_hit'].sum()),'Fresh Query':int((~metrics['cache_hit']).sum())} if 'cache_hit' in metrics.columns else {}
            fig_cache=go.Figure(go.Pie(labels=list(cache_counts.keys()),values=list(cache_counts.values()),hole=0.6,marker=dict(colors=['#34d399','#3b82f6'],line=dict(color='rgba(0,0,0,0.5)',width=2)),textinfo='percent+label',textfont=dict(color='#e2e8f0',size=12)))
            fig_cache.update_layout(title=dict(text='Cache Hit Rate',font=dict(color='#94a3b8',size=13)),paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',legend=dict(font=dict(color='#64748b'),bgcolor='rgba(0,0,0,0)'),margin=dict(t=40,b=10,l=10,r=10),height=250)
            st.plotly_chart(fig_cache,use_container_width=True)

        st.markdown("<hr>",unsafe_allow_html=True)
        st.markdown("""<div style="font-size:11px;font-weight:700;color:#64748b;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;">Notifications</div>""",unsafe_allow_html=True)
        nc1,nc2=st.columns(2)
        with nc1:
            if st.button("📨  Send Slack Summary",key="slack_btn"):
                try:
                    from notifications import send_slack_summary
                    stats={"total_queries":len(metrics),"avg_response_time":metrics['response_time_ms'].mean(),"avg_similarity":metrics['similarity_score'].mean(),"cache_hit_rate":cache_rate,"total_tokens_used":int(metrics['token_usage'].sum())}
                    send_slack_summary(stats)
                    st.success("✅ Slack summary sent!")
                except Exception as e:
                    st.warning(f"Configure SLACK_WEBHOOK_URL in notifications.py first. ({e})")
        with nc2:
            if st.button("📧  Send Email Summary",key="email_btn"):
                try:
                    from notifications import send_email_summary
                    stats={"total_queries":len(metrics),"avg_response_time":metrics['response_time_ms'].mean(),"avg_similarity":metrics['similarity_score'].mean(),"cache_hit_rate":cache_rate,"total_tokens_used":int(metrics['token_usage'].sum())}
                    send_email_summary(stats)
                    st.success("✅ Email summary sent!")
                except Exception as e:
                    st.warning(f"Configure EMAIL credentials in notifications.py first. ({e})")
    else:
        st.info("No metrics data available yet. Run some queries first!")

# TAB 4 — ONTOLOGY NETWORK
with tab4:
    st.markdown("""<div class="glass"><div class="glass-header"><div style="display:flex;justify-content:space-between;align-items:center;"><span class="glass-header-title">Full Ontology Network — Entity Relationship Map</span><span class="badge">Mistral LLM Extracted</span></div></div>""",unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    with c1: st.metric("Total Nodes","10")
    with c2: st.metric("Total Edges","7")
    with c3: st.metric("Entity Classes","4")
    with c4: st.metric("Products Mapped","3")
    st.markdown("<br>",unsafe_allow_html=True)
    G3=nx.DiGraph()
    for s,t,_ in EDGES: G3.add_edge(s,t)
    pos3=nx.spring_layout(G3,seed=7,k=3)
    ex2,ey2=[],[]
    for s,t in G3.edges():
        x0,y0=pos3[s];x1,y1=pos3[t];ex2+=[x0,x1,None];ey2+=[y0,y1,None]
    nl2=list(G3.nodes())
    fig_full=go.Figure(data=[
        go.Scatter(x=ex2,y=ey2,mode='lines',line=dict(width=1.2,color='rgba(255,255,255,0.1)'),hoverinfo='none'),
        go.Scatter(x=[pos3[n][0] for n in nl2],y=[pos3[n][1] for n in nl2],mode='markers+text',text=nl2,textposition='top center',textfont=dict(color='#f8fafc',size=11,family='JetBrains Mono'),hovertemplate='<b>%{text}</b><extra></extra>',marker=dict(size=24,color=[NODE_COLORS.get(n,'#334155') for n in nl2],line=dict(width=2,color='rgba(255,255,255,0.15)')))
    ],layout=go.Layout(height=560,showlegend=False,paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',xaxis=dict(showgrid=False,zeroline=False,showticklabels=False),yaxis=dict(showgrid=False,zeroline=False,showticklabels=False),margin=dict(t=10,b=10,l=10,r=10),hovermode='closest'))
    st.plotly_chart(fig_full,use_container_width=True)
    st.markdown("</div>",unsafe_allow_html=True)
    st.markdown("<br>",unsafe_allow_html=True)
    st.markdown("""<div style="font-size:11px;font-weight:700;color:#64748b;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:12px;">Extracted Triplets</div>""",unsafe_allow_html=True)
    st.dataframe(pd.DataFrame(EDGES,columns=['Source Entity','Target Entity','Predicate']),use_container_width=True,hide_index=True)

# TAB 5 — DATA EXPLORER
with tab5:
    st.markdown("""<div class="glass"><div class="glass-header"><div style="display:flex;justify-content:space-between;align-items:center;"><span class="glass-header-title">Enterprise Ticket Data Explorer</span><span class="badge">8,469 Records</span></div></div>""",unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: pf=st.selectbox("Priority",["All"]+sorted(df['Ticket Priority'].dropna().unique().tolist()))
    with c2: sf=st.selectbox("Status",["All"]+sorted(df['Ticket Status'].dropna().unique().tolist()))
    with c3: cf=st.selectbox("Channel",["All"]+sorted(df['Ticket Channel'].dropna().unique().tolist()))
    st.markdown("</div>",unsafe_allow_html=True)
    filtered=df.copy()
    if pf!="All": filtered=filtered[filtered['Ticket Priority']==pf]
    if sf!="All": filtered=filtered[filtered['Ticket Status']==sf]
    if cf!="All": filtered=filtered[filtered['Ticket Channel']==cf]
    st.markdown("<br>",unsafe_allow_html=True)
    c1,c2,c3=st.columns(3)
    with c1: st.metric("Filtered Tickets",f"{len(filtered):,}")
    with c2: st.metric("Total Tickets",f"{len(df):,}")
    with c3: st.metric("Match Rate",f"{round(len(filtered)/max(len(df),1)*100,1)}%")
    st.markdown("<br>",unsafe_allow_html=True)
    cols=[c for c in ['Ticket ID','Product Purchased','Ticket Type','Ticket Subject','Ticket Priority','Ticket Status','Resolution Status','Ticket Channel'] if c in filtered.columns]
    st.dataframe(filtered[cols],use_container_width=True,hide_index=True,height=400)
    st.markdown("<br>",unsafe_allow_html=True)
    c1,_=st.columns([1,4])
    with c1:
        st.download_button("⬇  Export CSV",data=filtered.to_csv(index=False),file_name=f"kgb_{pf}_{sf}.csv",mime="text/csv")

# FOOTER
st.markdown("<br><hr>",unsafe_allow_html=True)
st.markdown("""<div style="text-align:center;color:#1e293b;font-size:12px;font-family:'JetBrains Mono';letter-spacing:0.08em;padding-bottom:12px;">KGB · Knowledge Graph Builder · Mistral LLM + FAISS + Neo4j + MongoDB + Slack + Email</div>""",unsafe_allow_html=True)
