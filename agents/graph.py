from __future__ import annotations
from typing import Optional, Annotated
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from models.schemas import (
    LiveResearchResult,
    MarketResearchResult,
    RetrievalContext,
    SynthesisResult,
    UXCritiqueResult,
    VisualAnalysisResult,
)
from PIL import Image
import base64
import io


def _replace(a, b):
    return b if b is not None else a


class AgentState(TypedDict, total=False):
    image_base64: str
    api_key: str
    model: str
    tavily_api_key: str
    retrieval_context: Annotated[Optional[RetrievalContext], _replace]
    visual_result: Annotated[Optional[VisualAnalysisResult], _replace]
    ux_result: Annotated[Optional[UXCritiqueResult], _replace]
    market_result: Annotated[Optional[MarketResearchResult], _replace]
    live_research_result: Annotated[Optional[LiveResearchResult], _replace]
    synthesis: Annotated[Optional[SynthesisResult], _replace]


def _retrieve_node(state: AgentState) -> dict:
    from retrieval.retriever import retrieve_context
    from knowledge_base.ingest import is_knowledge_base_ready

    if not is_knowledge_base_ready():
        return {"retrieval_context": RetrievalContext()}

    img_bytes = base64.b64decode(state["image_base64"])
    image = Image.open(io.BytesIO(img_bytes)).convert("RGB")
    ctx = retrieve_context(image)
    return {"retrieval_context": ctx}


def _get_retrieval_context(state: AgentState) -> RetrievalContext:
    ctx = state.get("retrieval_context")
    if ctx and isinstance(ctx, dict):
        return RetrievalContext(**ctx)
    return ctx or RetrievalContext()


def _visual_node(state: AgentState) -> dict:
    from agents.visual_analysis import run_visual_analysis

    result = run_visual_analysis(
        state["image_base64"],
        _get_retrieval_context(state),
        state["api_key"],
        state["model"],
    )
    return {"visual_result": result}


def _ux_node(state: AgentState) -> dict:
    from agents.ux_critique import run_ux_critique

    result = run_ux_critique(
        state["image_base64"],
        _get_retrieval_context(state),
        state["api_key"],
        state["model"],
    )
    return {"ux_result": result}


def _market_node(state: AgentState) -> dict:
    from agents.market_research import run_market_research

    result = run_market_research(
        state["image_base64"],
        _get_retrieval_context(state),
        state["api_key"],
        state["model"],
    )
    return {"market_result": result}


def _live_research_node(state: AgentState) -> dict:
    from agents.live_research import run_live_research

    result = run_live_research(
        state["image_base64"],
        _get_retrieval_context(state),
        state["api_key"],
        state["model"],
        state.get("tavily_api_key", ""),
    )
    return {"live_research_result": result}


def _synthesize_node(state: AgentState) -> dict:
    from agents.synthesizer import run_synthesis

    visual = state.get("visual_result")
    if visual and isinstance(visual, dict):
        visual = VisualAnalysisResult(**visual)

    ux = state.get("ux_result")
    if ux and isinstance(ux, dict):
        ux = UXCritiqueResult(**ux)

    market = state.get("market_result")
    if market and isinstance(market, dict):
        market = MarketResearchResult(**market)

    live_research = state.get("live_research_result")
    if live_research and isinstance(live_research, dict):
        live_research = LiveResearchResult(**live_research)

    result = run_synthesis(visual, ux, market, live_research, state["api_key"], state["model"])
    return {"synthesis": result}


def build_graph(enabled_agents: list[str]):
    graph = StateGraph(AgentState)

    graph.add_node("retrieve", _retrieve_node)
    graph.add_edge(START, "retrieve")

    agent_nodes = []
    if "visual" in enabled_agents:
        graph.add_node("visual", _visual_node)
        graph.add_edge("retrieve", "visual")
        agent_nodes.append("visual")

    if "ux" in enabled_agents:
        graph.add_node("ux", _ux_node)
        graph.add_edge("retrieve", "ux")
        agent_nodes.append("ux")

    if "market" in enabled_agents:
        graph.add_node("market", _market_node)
        graph.add_edge("retrieve", "market")
        agent_nodes.append("market")

    if "live_research" in enabled_agents:
        graph.add_node("live_research", _live_research_node)
        graph.add_edge("retrieve", "live_research")
        agent_nodes.append("live_research")

    graph.add_node("synthesize", _synthesize_node)

    for node_name in agent_nodes:
        graph.add_edge(node_name, "synthesize")

    graph.add_edge("synthesize", END)

    return graph.compile()
