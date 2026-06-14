import streamlit as st
from pathlib import Path
from PIL import Image
from models.schemas import RetrievedImage


def score_color(score: int) -> str:
    """Calm, semantic score palette used across the app."""
    if score >= 80:
        return "#15803d"
    if score >= 60:
        return "#0f766e"
    if score >= 40:
        return "#b45309"
    return "#b91c1c"


def render_score_badge(score: int, label: str = "Score"):
    color = score_color(score)
    st.markdown(
        f"""<div style="display:inline-block; background:{color}; color:white;
        padding:8px 16px; border-radius:10px; font-weight:600; font-size:1.05em;">
        {label}: {score}/100</div>""",
        unsafe_allow_html=True,
    )


def render_strengths(strengths: list[str]):
    if not strengths:
        return
    st.markdown("**Strengths**")
    for s in strengths:
        st.markdown(f"- {s}")


def render_recommendations(recommendations: list[str]):
    if not recommendations:
        return
    st.markdown("**Recommendations**")
    for i, r in enumerate(recommendations, 1):
        st.markdown(f"{i}. {r}")


def render_reference_gallery(images: list[RetrievedImage]):
    if not images:
        st.info("No reference images found in the knowledge base. Add images to knowledge_base/sources/reference_images/")
        return

    cols = st.columns(min(len(images), 5))
    for i, img_ref in enumerate(images):
        with cols[i % len(cols)]:
            try:
                img = Image.open(img_ref.image_path)
                st.image(img, caption=img_ref.caption or img_ref.source, use_container_width=True)
            except Exception:
                st.caption(f"{img_ref.caption} (image not found)")
