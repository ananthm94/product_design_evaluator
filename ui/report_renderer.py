import streamlit as st
from models.schemas import DesignReport
from ui.components import score_color

DETAIL_DIALOG_KEY = "active_detail_dialog"


def render_report(report: DesignReport, key_prefix: str = ""):
    if not report:
        return

    key_scope = f"{key_prefix}_" if key_prefix else ""
    detail_state_key = f"{key_scope}{DETAIL_DIALOG_KEY}"

    if report.synthesis:
        _render_synthesis_card(report.synthesis, key_scope)

    sections = []
    if report.visual_analysis:
        sections.append(("Visual", "🎨", "Visual Score", report.visual_analysis))
    if report.ux_critique:
        sections.append(("UX", "👆", "UX Score", report.ux_critique))
    if report.market_research:
        sections.append(("Market", "📊", "Market Readiness", report.market_research))

    if not sections and not report.synthesis and not report.live_research:
        st.warning("No analysis results to display.")
        return

    if sections:
        cols = st.columns(len(sections))
        for col, (label, icon, score_label, data) in zip(cols, sections):
            with col:
                _render_summary_card(label, icon, score_label, data, key_scope, detail_state_key)

    if report.live_research:
        _render_live_research_card(report.live_research, key_scope, detail_state_key)


def _render_synthesis_card(s, key_scope: str):
    score = s.overall_score
    with st.container(border=True):
        col_badge, col_label = st.columns([1, 5])
        with col_badge:
            _score_pill(score)
        with col_label:
            st.markdown(f"**Overall**")
        st.caption(_truncate(s.executive_summary, 200))

    if s.priority_actions:
        with st.expander("Priority actions"):
            for i, action in enumerate(s.priority_actions, 1):
                st.checkbox(action, key=f"{key_scope}action_{i}")


def _render_summary_card(
    label: str,
    icon: str,
    score_label: str,
    data,
    key_scope: str,
    detail_state_key: str,
):
    score = data.score
    with st.container(border=True):
        col_icon, col_label, col_score = st.columns([1, 4, 1])
        with col_icon:
            st.markdown(f"#### {icon}")
        with col_label:
            st.markdown(f"**{label}**")
        with col_score:
            _score_pill(score)

        top = data.strengths[:2] if data.strengths else []
        rec = data.recommendations[:1] if data.recommendations else []
        for s in top:
            st.markdown(f"- {s}")
        for r in rec:
            st.markdown(f"- _{r}_")

        if st.button("Details", key=f"{key_scope}btn_{label}", use_container_width=True):
            st.session_state[detail_state_key] = label

    if st.session_state.get(detail_state_key) == label:
        _open_detail_dialog(label, data, score_label, detail_state_key, key_scope)


def _render_live_research_card(data, key_scope: str, detail_state_key: str):
    with st.container(border=True):
        col_icon, col_label, col_sources = st.columns([1, 4, 2])
        with col_icon:
            st.markdown("#### 🔎")
        with col_label:
            st.markdown("**Live Research**")
        with col_sources:
            st.caption(f"{len(data.sources)} sources")

        if data.skipped_reason:
            st.info(data.skipped_reason)
        elif data.summary:
            st.caption(_truncate(data.summary, 260))

        for item in data.current_trends[:2]:
            st.markdown(f"- {item}")
        for item in data.opportunities[:1]:
            st.markdown(f"- _{item}_")

        if st.button("Details", key=f"{key_scope}btn_Live_Research", use_container_width=True):
            st.session_state[detail_state_key] = "Live Research"

    if st.session_state.get(detail_state_key) == "Live Research":
        _open_live_research_dialog(data, detail_state_key, key_scope)


@st.dialog("Analysis Details", width="large")
def _open_detail_dialog(label: str, data, score_label: str, detail_state_key: str, key_scope: str):
    _score_pill(data.score)
    st.markdown(f"### {score_label}")
    st.divider()

    if label == "Visual":
        _detail_visual(data)
    elif label == "UX":
        _detail_ux(data)
    elif label == "Market":
        _detail_market(data)

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if data.strengths:
            st.markdown("**Strengths**")
            for s in data.strengths:
                st.markdown(f"- {s}")
    with col2:
        if data.recommendations:
            st.markdown("**Recommendations**")
            for i, r in enumerate(data.recommendations, 1):
                st.markdown(f"{i}. {r}")

    if st.button("Close", key=f"{key_scope}close_dialog_{label}", use_container_width=True):
        st.session_state[detail_state_key] = None
        st.rerun()


@st.dialog("Live Research Details", width="large")
def _open_live_research_dialog(data, detail_state_key: str, key_scope: str):
    st.markdown("### Live Research")
    if data.skipped_reason:
        st.info(data.skipped_reason)

    if data.summary:
        st.markdown(data.summary)

    col1, col2 = st.columns(2)
    with col1:
        if data.current_trends:
            st.markdown("##### Current Trends")
            for trend in data.current_trends:
                st.markdown(f"- {trend}")
        if data.competitor_findings:
            st.markdown("##### Competitor Findings")
            for finding in data.competitor_findings:
                st.markdown(f"- {finding}")
    with col2:
        if data.opportunities:
            st.markdown("##### Opportunities")
            for opportunity in data.opportunities:
                st.markdown(f"- {opportunity}")

    if data.sources:
        st.divider()
        st.markdown("##### Sources")
        for source in data.sources:
            title = source.title or source.url
            st.markdown(f"- [{title}]({source.url})")
            if source.content:
                st.caption(_truncate(source.content, 220))

    if st.button("Close", key=f"{key_scope}close_dialog_Live_Research", use_container_width=True):
        st.session_state[detail_state_key] = None
        st.rerun()


def _detail_visual(v):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("##### Color Analysis")
        st.markdown(v.color_analysis)
        st.markdown("##### Typography")
        st.markdown(v.typography)
    with col2:
        st.markdown("##### Layout & Spacing")
        st.markdown(v.layout_and_spacing)
        st.markdown("##### Visual Hierarchy")
        st.markdown(v.visual_hierarchy)


def _detail_ux(u):
    if u.heuristic_violations:
        st.markdown("##### Heuristic Violations")
        for v in u.heuristic_violations:
            sev_color = {"high": "red", "medium": "orange", "low": "blue"}.get(
                v.severity, "gray"
            )
            with st.expander(
                f":{sev_color}[{v.severity.upper()}] {v.heuristic_id}: {v.heuristic_name}"
            ):
                st.markdown(f"**Issue:** {v.description}")
                st.markdown(f"**Fix:** {v.recommendation}")

    if u.accessibility_issues:
        st.markdown("##### Accessibility Issues")
        for issue in u.accessibility_issues:
            st.markdown(f"- {issue}")

    if u.interaction_patterns:
        st.markdown("##### Interaction Patterns")
        for p in u.interaction_patterns:
            st.markdown(f"- {p}")


def _detail_market(m):
    st.markdown(f"**Design Category:** {m.design_category}")
    st.markdown(f"**Trend Alignment:** {m.trend_alignment}")

    col1, col2 = st.columns(2)
    with col1:
        if m.competitor_insights:
            st.markdown("##### Competitor Insights")
            for ins in m.competitor_insights:
                st.markdown(f"- {ins}")
    with col2:
        if m.differentiation_opportunities:
            st.markdown("##### Differentiation Opportunities")
            for opp in m.differentiation_opportunities:
                st.markdown(f"- {opp}")


def _score_pill(score: int):
    color = score_color(score)
    st.markdown(
        f'<span style="background:{color}; color:white; padding:4px 12px;'
        f' border-radius:10px; font-weight:600; font-size:0.95em;">{score}</span>',
        unsafe_allow_html=True,
    )


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."
