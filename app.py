import streamlit as st
import time
from pipeline import run_research_pipeline

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Multi-Agent AI Research System",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Root tokens ── */
:root {
    --bg:        #0a0c10;
    --surface:   #111318;
    --border:    #1e2128;
    --accent:    #00e5a0;
    --accent2:   #0088ff;
    --warn:      #ffb340;
    --text:      #e8eaf0;
    --muted:     #6b7280;
    --radius:    12px;
}

/* ── Global reset ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

.block-container { padding: 2.5rem 3rem 4rem; max-width: 1100px; }

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 1rem 2rem;
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
}
.hero-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.8rem;
}
.hero-title {
    font-size: clamp(2.4rem, 5vw, 3.6rem);
    font-weight: 800;
    line-height: 1.08;
    background: linear-gradient(135deg, #ffffff 30%, var(--accent) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin: 0 0 0.6rem;
}
.hero-sub {
    color: var(--muted);
    font-size: 1rem;
    font-weight: 400;
    max-width: 540px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--border), transparent);
    margin: 2rem 0;
}

/* ── Agent pipeline bar ── */
.pipeline-bar {
    display: flex;
    justify-content: center;
    gap: 0;
    margin: 1.5rem 0 2.5rem;
    flex-wrap: wrap;
}
.agent-badge {
    display: flex;
    align-items: center;
    gap: 0.45rem;
    padding: 0.4rem 1rem;
    border: 1px solid var(--border);
    background: var(--surface);
    font-family: 'DM Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.08em;
    color: var(--muted);
    transition: all 0.25s;
}
.agent-badge:first-child { border-radius: var(--radius) 0 0 var(--radius); }
.agent-badge:last-child  { border-radius: 0 var(--radius) var(--radius) 0; }
.agent-badge .dot { width: 7px; height: 7px; border-radius: 50%; background: var(--border); }
.agent-badge.active { border-color: var(--accent); color: var(--accent); background: rgba(0,229,160,0.07); }
.agent-badge.active .dot { background: var(--accent); box-shadow: 0 0 6px var(--accent); animation: pulse 1.2s infinite; }
.agent-badge.done   { border-color: var(--accent2); color: var(--accent2); background: rgba(0,136,255,0.07); }
.agent-badge.done .dot { background: var(--accent2); }
.arrow { color: var(--border); font-size: 1rem; align-self: center; padding: 0 2px; }

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50%       { opacity: 0.3; }
}

/* ── Search input card ── */
.input-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input {
    background: #0d0f14 !important;
    border: 1px solid #2a2d36 !important;
    border-radius: 8px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 0.75rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(0,229,160,0.15) !important;
}
.stButton > button {
    background: var(--accent) !important;
    color: #000 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    padding: 0.65rem 2rem !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    background: #00ffb3 !important;
    box-shadow: 0 0 20px rgba(0,229,160,0.35) !important;
    transform: translateY(-1px);
}

/* ── Result cards ── */
.result-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.6rem 1.8rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.result-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
}
.card-search::before  { background: var(--accent); }
.card-scraped::before { background: var(--accent2); }
.card-report::before  { background: var(--warn); }
.card-critic::before  { background: #ff5f87; }

.card-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.card-label.search  { color: var(--accent); }
.card-label.scraped { color: var(--accent2); }
.card-label.report  { color: var(--warn); }
.card-label.critic  { color: #ff5f87; }

.card-content {
    font-family: 'DM Mono', monospace;
    font-size: 0.82rem;
    line-height: 1.75;
    color: #c8cdd8;
    white-space: pre-wrap;
    max-height: 340px;
    overflow-y: auto;
}
.card-content::-webkit-scrollbar { width: 4px; }
.card-content::-webkit-scrollbar-track { background: transparent; }
.card-content::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }

/* ── Status log ── */
.status-log {
    background: #080a0e;
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1rem 1.2rem;
    font-family: 'DM Mono', monospace;
    font-size: 0.78rem;
    color: var(--muted);
    line-height: 1.8;
    margin-bottom: 1.5rem;
}
.log-line { display: block; }
.log-ok   { color: var(--accent); }
.log-run  { color: var(--warn); }
.log-err  { color: #ff5f87; }

/* ── Success banner ── */
.success-banner {
    background: rgba(0,229,160,0.07);
    border: 1px solid rgba(0,229,160,0.25);
    border-radius: var(--radius);
    padding: 1rem 1.4rem;
    text-align: center;
    color: var(--accent);
    font-size: 0.9rem;
    font-weight: 600;
    margin-bottom: 1.5rem;
    letter-spacing: 0.04em;
}

/* ── Tab overrides ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--surface) !important;
    border-radius: 10px 10px 0 0 !important;
    border: 1px solid var(--border) !important;
    border-bottom: none !important;
    gap: 0 !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.1em !important;
    padding: 0.65rem 1.2rem !important;
    color: var(--muted) !important;
    background: transparent !important;
    border-bottom: 2px solid transparent !important;
}
.stTabs [aria-selected="true"] {
    color: var(--accent) !important;
    border-bottom-color: var(--accent) !important;
}
.stTabs [data-baseweb="tab-panel"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 10px 10px !important;
    padding: 1.4rem 1.6rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Session state ────────────────────────────────────────────────────────────
if "results"       not in st.session_state: st.session_state.results       = None
if "running"       not in st.session_state: st.session_state.running       = False
if "active_step"   not in st.session_state: st.session_state.active_step   = -1
if "error"         not in st.session_state: st.session_state.error         = None


# ── Helper: pipeline stage badges ────────────────────────────────────────────
STAGES = [
    ("🔍", "Search Agent"),
    ("📄", "Reader Agent"),
    ("✍️", "Writer Chain"),
    ("🧐", "Critic Chain"),
]

def render_pipeline_bar(active: int = -1, done_up_to: int = -1):
    parts = []
    for i, (icon, name) in enumerate(STAGES):
        if i < done_up_to:
            cls = "done"
        elif i == active:
            cls = "active"
        else:
            cls = ""
        parts.append(f'<div class="agent-badge {cls}"><span class="dot"></span>{icon} {name}</div>')
        if i < len(STAGES) - 1:
            parts.append('<span class="arrow">›</span>')
    st.markdown(f'<div class="pipeline-bar">{"".join(parts)}</div>', unsafe_allow_html=True)


# ── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">⬡ Multi-Agent System</div>
    <h1 class="hero-title">Research Intelligence<br>Pipeline</h1>
    <p class="hero-sub">Four specialized AI agents — search, scrape, write, critique — working in sequence to produce deep research reports.</p>
</div>
<div class="divider"></div>
""", unsafe_allow_html=True)


# ── Pipeline bar ─────────────────────────────────────────────────────────────
active_step = st.session_state.active_step
done_up_to  = active_step if not st.session_state.running else active_step

if st.session_state.results:
    render_pipeline_bar(active=-1, done_up_to=4)
else:
    render_pipeline_bar(active=active_step, done_up_to=active_step)


# ── Input card ───────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)
col1, col2 = st.columns([5, 1])
with col1:
    topic = st.text_input(
        label="Research Topic",
        placeholder="e.g.  Advances in quantum computing 2024",
        label_visibility="collapsed",
        key="topic_input",
    )
with col2:
    run_btn = st.button("▶ Run", disabled=st.session_state.running)
st.markdown("</div>", unsafe_allow_html=True)


# ── Run pipeline ─────────────────────────────────────────────────────────────
if run_btn and topic.strip():
    st.session_state.running     = True
    st.session_state.results     = None
    st.session_state.error       = None
    st.session_state.active_step = 0

    log_placeholder      = st.empty()
    progress_placeholder = st.empty()

    log_lines = []

    def log(msg: str, kind: str = ""):
        cls = {"ok": "log-ok", "run": "log-run", "err": "log-err"}.get(kind, "")
        log_lines.append(f'<span class="log-line {cls}">{msg}</span>')
        log_placeholder.markdown(
            f'<div class="status-log">{"".join(log_lines)}</div>',
            unsafe_allow_html=True,
        )

    try:
        log(f"$ research-pipeline --topic \"{topic}\"")
        log("")

        # Monkey-patch pipeline to track stages
        import pipeline as _pl
        import agents as _ag

        original_run = _pl.run_research_pipeline

        def patched_run(t):
            state = {}

            # Step 1 – Search
            log("[ 1/4 ]  Search Agent  →  querying the web ...", "run")
            st.session_state.active_step = 0
            search_agent = _ag.build_search_agent()
            sr = search_agent.invoke({"messages": [("user",
                f"Conduct a web search to gather recent, reliable and detailed information on the topic: {t}")]})
            state["search_results"] = sr["messages"][-1].content
            log("         ✓ search results collected", "ok")

            # Step 2 – Reader
            log("[ 2/4 ]  Reader Agent  →  scraping top URLs ...", "run")
            st.session_state.active_step = 1
            reader_agent = _ag.build_reader_agent()
            rr = reader_agent.invoke({"messages": [("user",
                f"Based on the following search results about '{t}', "
                f"pick the most relevant URLs and scrape their content for deeper insights."
                f"Search Results:\n{state['search_results'][:800]}")]})
            state["scraped_content"] = rr["messages"][-1].content
            log("         ✓ web content scraped", "ok")

            # Step 3 – Writer
            log("[ 3/4 ]  Writer Chain  →  drafting report ...", "run")
            st.session_state.active_step = 2
            combined = (
                f"SEARCH RESULTS:\n{state['search_results']}\n\n"
                f"DETAILED SCRAPED CONTENT:\n{state['scraped_content']}"
            )
            state["writer_report"] = _ag.writer_chain.invoke({"topic": t, "research_data": combined})
            log("         ✓ report drafted", "ok")

            # Step 4 – Critic
            log("[ 4/4 ]  Critic Chain  →  reviewing report ...", "run")
            st.session_state.active_step = 3
            state["critic_feedback"] = _ag.critic_chain.invoke({"topic": t, "research_data": combined, "report": state["writer_report"]})
            log("         ✓ critique complete", "ok")

            log("")
            log("✓  Pipeline finished successfully.", "ok")
            return state

        results = patched_run(topic.strip())
        st.session_state.results     = results
        st.session_state.active_step = 4

    except Exception as e:
        st.session_state.error   = str(e)
        st.session_state.running = False
        log(f"✗  Error: {e}", "err")

    finally:
        st.session_state.running = False

elif run_btn and not topic.strip():
    st.warning("Please enter a research topic before running.")


# ── Error state ───────────────────────────────────────────────────────────────
if st.session_state.error:
    st.markdown(
        f'<div class="result-card card-critic"><div class="card-label critic">⚠ Error</div>'
        f'<div class="card-content">{st.session_state.error}</div></div>',
        unsafe_allow_html=True,
    )


# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results

    st.markdown(
        '<div class="success-banner">✓ &nbsp; Research complete — all four agents finished successfully</div>',
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔍  Search Results",
        "📄  Scraped Content",
        "✍️  Research Report",
        "🧐  Critic Feedback",
    ])

    with tab1:
        st.markdown(
            f'<div class="card-label search">● Search Agent Output</div>'
            f'<div class="card-content">{r.get("search_results","—")}</div>',
            unsafe_allow_html=True,
        )

    with tab2:
        st.markdown(
            f'<div class="card-label scraped">● Reader Agent Output</div>'
            f'<div class="card-content">{r.get("scraped_content","—")}</div>',
            unsafe_allow_html=True,
        )

    with tab3:
        report = r.get("writer_report", "—")
        st.markdown(
            f'<div class="card-label report">● Writer Chain — Final Report</div>',
            unsafe_allow_html=True,
        )
        st.markdown(report)          # render markdown natively for the report
        st.download_button(
            label="⬇  Download Report (.md)",
            data=report,
            file_name=f"research_report_{int(time.time())}.md",
            mime="text/markdown",
        )

    with tab4:
        st.markdown(
            f'<div class="card-label critic">● Critic Chain Feedback</div>'
            f'<div class="card-content">{r.get("critic_feedback","—")}</div>',
            unsafe_allow_html=True,
        )