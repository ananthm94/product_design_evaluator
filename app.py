import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import base64
import hashlib
import io
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
load_dotenv()

from config.settings import AVAILABLE_MODELS, DEFAULT_LLM_MODEL
from utils.image_utils import resize_image, image_to_base64
from ui.report_renderer import render_report
from ui.components import render_reference_gallery, score_color
from models.schemas import DesignReport, GraphState

st.set_page_config(
    page_title="Design Analysis Suite",
    page_icon="🎨",
    layout="wide",
)

# Friendly labels for each LangGraph node, shown live as the graph streams.
NODE_LABELS = {
    "retrieve": "Retrieving relevant design guidelines",
    "visual": "Analyzing visual design",
    "ux": "Evaluating UX & accessibility",
    "market": "Researching market & competitors",
    "live_research": "Running live web research",
    "synthesize": "Synthesizing executive report",
}

st.markdown(
    """
    <style>
      .block-container { padding-top: 2.2rem; max-width: 1200px; }
      h1, h2, h3 { font-weight: 650; letter-spacing: -0.01em; }
      [data-testid="stSidebar"] { background: #f5f6fa; }
      .stButton > button { border-radius: 10px; font-weight: 600; }
      [data-testid="stMetricValue"] { font-weight: 650; }
      .ref-caption { color: #6b7280; font-size: 0.82rem; margin-top: 2px; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Multimodal AI Design Analysis Suite")
st.caption("AI-powered design critique with image RAG, multi-agent analysis, and a shared design memory")

if "design_report" not in st.session_state:
    st.session_state.design_report = None
if "report_signature" not in st.session_state:
    st.session_state.report_signature = None
if "uploaded_file_signature" not in st.session_state:
    st.session_state.uploaded_file_signature = None
if "history_selected" not in st.session_state:
    st.session_state.history_selected = None

with st.sidebar:
    st.header("Settings")

    api_key = st.text_input(
        "OpenRouter API Key",
        type="password",
        value=os.getenv("OPENROUTER_API_KEY", ""),
        help="Get your key at openrouter.ai",
    )

    default_model_index = AVAILABLE_MODELS.index(DEFAULT_LLM_MODEL) if DEFAULT_LLM_MODEL in AVAILABLE_MODELS else 0
    model = st.selectbox("Model", AVAILABLE_MODELS, index=default_model_index)

    with st.expander("Optional API keys"):
        tavily_api_key = st.text_input(
            "Tavily API Key",
            type="password",
            value=os.getenv("TAVILY_API_KEY", ""),
            help="Enables Live Research",
        )
        if tavily_api_key:
            os.environ["TAVILY_API_KEY"] = tavily_api_key

        langsmith_key = st.text_input(
            "LangSmith API Key",
            type="password",
            value=os.getenv("LANGSMITH_API_KEY", ""),
        )
        if langsmith_key:
            os.environ["LANGSMITH_API_KEY"] = langsmith_key
            os.environ["LANGSMITH_TRACING"] = "true"
            os.environ["LANGSMITH_PROJECT"] = "design-analysis-suite"


def _run_analysis(resized_image, image_b64, model, api_key, tavily_api_key, enabled_agents):
    """Stream the LangGraph flow, surfacing each node as it runs."""
    from agents.graph import build_graph

    graph = build_graph(enabled_agents)
    initial_state = GraphState(
        image_base64=image_b64,
        api_key=api_key,
        model=model,
        tavily_api_key=tavily_api_key,
    )

    result = {}
    with st.status("Analyzing design...", expanded=True) as status:
        try:
            for chunk in graph.stream(initial_state.model_dump(), stream_mode="updates"):
                for node_name, node_output in chunk.items():
                    label = NODE_LABELS.get(node_name, node_name)
                    st.write(f"✓ {label}")
                    status.update(label=f"{label}...")
                    if isinstance(node_output, dict):
                        result.update(node_output)
        except Exception as e:
            status.update(label="Analysis failed", state="error")
            st.error(f"Error during analysis: {e}")
            return None
        status.update(label="Analysis complete", state="complete")

    report = DesignReport(
        visual_analysis=result.get("visual_result"),
        ux_critique=result.get("ux_result"),
        market_research=result.get("market_result"),
        live_research=result.get("live_research_result"),
        synthesis=result.get("synthesis"),
        retrieval_context=result.get("retrieval_context"),
    )

    # Persist to the shared design memory so others can learn from it.
    try:
        from knowledge_base.history_store import get_history_store

        get_history_store().save_design(resized_image, report, model)
    except Exception as e:
        st.warning(f"Could not save to design history: {e}")

    return report


tab_analyze, tab_library, tab_history = st.tabs(
    ["Analyze", "Reference Library", "Past Designs"]
)

# ---------------------------------------------------------------- Analyze tab
with tab_analyze:
    uploaded_file = st.file_uploader(
        "Upload a design screenshot",
        type=["png", "jpg", "jpeg", "webp"],
        help="Upload a product or app design for analysis",
    )

    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        file_digest = hashlib.sha256(file_bytes).hexdigest()
        file_signature = f"{uploaded_file.name}:{file_digest}"

        if st.session_state.uploaded_file_signature != file_signature:
            st.session_state.uploaded_file_signature = file_signature
            st.session_state.design_report = None
            st.session_state.report_signature = None
            st.session_state.active_detail_dialog = None

        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        resized = resize_image(image)

        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(resized, caption="Uploaded Design", use_container_width=True)

        with col2:
            st.markdown("**Analysis agents**")
            c1, c2, c3, c4 = st.columns(4)
            run_visual = c1.checkbox("Visual", value=True)
            run_ux = c2.checkbox("UX", value=True)
            run_market = c3.checkbox("Market", value=True)
            run_live_research = c4.checkbox("Live Research", value=True)

            enabled_agents = []
            if run_visual:
                enabled_agents.append("visual")
            if run_ux:
                enabled_agents.append("ux")
            if run_market:
                enabled_agents.append("market")
            if run_live_research:
                enabled_agents.append("live_research")

            tavily_key_signature = (
                hashlib.sha256(tavily_api_key.encode()).hexdigest() if tavily_api_key else ""
            )
            current_signature = (file_signature, model, tuple(enabled_agents), tavily_key_signature)

            if not api_key:
                st.warning("Enter your OpenRouter API key in the sidebar.")
            if not enabled_agents:
                st.error("Enable at least one agent.")

            analyze_btn = st.button(
                "Analyze Design",
                type="primary",
                use_container_width=True,
                disabled=not api_key or not enabled_agents,
            )

            if analyze_btn:
                image_b64 = image_to_base64(resized)
                report = _run_analysis(
                    resized, image_b64, model, api_key, tavily_api_key, enabled_agents
                )
                if report is not None:
                    st.session_state.design_report = report
                    st.session_state.report_signature = current_signature
                    st.session_state.active_detail_dialog = None

        report = st.session_state.design_report
        if report:
            if st.session_state.report_signature != current_signature:
                st.info(
                    "The displayed report was generated with different image, model, or agent "
                    "settings. Click Analyze Design to refresh it."
                )

            if report.retrieval_context and report.retrieval_context.similar_images:
                st.subheader("Retrieved Reference Designs")
                render_reference_gallery(report.retrieval_context.similar_images)

            render_report(report)
    else:
        st.info("Upload a screenshot to begin, then pick which agents to run.")


# -------------------------------------------------------- Reference Library tab
with tab_library:
    from retrieval.retriever import search_reference_images, list_reference_images

    st.subheader("Reference Library")
    st.caption("Search a library of real, well-designed websites used as visual references.")

    query = st.text_input(
        "Search references",
        placeholder="e.g. minimal dashboard, bold landing page, ecommerce product grid",
        key="library_query",
    )

    if query:
        images = search_reference_images(query, limit=8)
    else:
        images = list_reference_images(limit=24)

    if not images:
        st.info(
            "No reference images yet. Build the library with "
            "`python knowledge_base/scraper.py`."
        )
    else:
        render_reference_gallery(images)


# ------------------------------------------------------------- Past Designs tab
with tab_history:
    from knowledge_base.history_store import get_history_store

    st.subheader("Past Designs")
    st.caption("A shared memory of every analyzed design — search and learn from previous reviews.")

    store = get_history_store()
    hquery = st.text_input(
        "Search past designs",
        placeholder="e.g. fintech app, low contrast, onboarding screen",
        key="history_query",
    )

    records = store.search_designs(query_text=hquery, limit=12) if hquery else store.list_recent(limit=24)

    if not records:
        st.info("No past designs yet. Analyze a design and it will appear here.")
    else:
        cols = st.columns(4)
        for i, rec in enumerate(records):
            with cols[i % 4]:
                with st.container(border=True):
                    try:
                        if rec.thumb_b64:
                            st.image(base64.b64decode(rec.thumb_b64), use_container_width=True)
                        elif rec.thumb_path:
                            st.image(rec.thumb_path, use_container_width=True)
                        else:
                            st.caption("(no thumbnail)")
                    except Exception:
                        st.caption("(thumbnail unavailable)")
                    color = score_color(rec.overall_score)
                    st.markdown(
                        f'<span style="background:{color}; color:white; padding:2px 10px;'
                        f' border-radius:8px; font-weight:600; font-size:0.85em;">'
                        f'{rec.overall_score}/100</span>'
                        f' <span class="ref-caption">{rec.category}</span>',
                        unsafe_allow_html=True,
                    )
                    if rec.summary:
                        st.caption(rec.summary[:120] + ("..." if len(rec.summary) > 120 else ""))
                    if st.button("View report", key=f"hist_{rec.id}", use_container_width=True):
                        st.session_state.history_selected = rec.id

        selected_id = st.session_state.history_selected
        if selected_id:
            match = next((r for r in records if r.id == selected_id), None)
            if match and match.report:
                st.divider()
                st.markdown(f"### Report — {match.category} · {match.timestamp[:10]}")
                if st.button("Close report", key="close_history_report"):
                    st.session_state.history_selected = None
                    st.rerun()
                render_report(match.report)
