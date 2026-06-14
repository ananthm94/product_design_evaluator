import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import (
    LiveResearchResult,
    MarketResearchResult,
    SynthesisResult,
    UXCritiqueResult,
    VisualAnalysisResult,
)
from config.settings import OPENROUTER_BASE_URL


SYSTEM_PROMPT = """You are a Senior Design Director synthesizing findings from multiple specialist analysts. Your job is to create an executive summary that combines visual analysis, UX critique, market research, and optional live web research into a unified, actionable report.

You will receive the detailed outputs from specialist agents. Synthesize them into:

1. **Executive Summary**: 2-3 paragraph overview of the design's overall quality and market readiness
2. **Overall Score**: Weighted average considering scored specialist outputs only (0-100). Live web research has no score and should inform recommendations without dragging the score up or down.
3. **Top Strengths**: The 3-5 most impactful strengths across all analyses
4. **Top Recommendations**: The 3-5 highest-priority improvements, ordered by impact
5. **Priority Actions**: Immediate next steps the design team should take

Respond with a JSON object:
{
    "executive_summary": "comprehensive 2-3 paragraph summary",
    "overall_score": <0-100 integer>,
    "top_strengths": ["strength 1", "strength 2", ...],
    "top_recommendations": ["recommendation 1", "recommendation 2", ...],
    "priority_actions": ["action 1", "action 2", ...]
}

Focus on actionable insights. Avoid repeating the same finding from different agents — synthesize and deduplicate."""


def run_synthesis(
    visual_result: VisualAnalysisResult | None,
    ux_result: UXCritiqueResult | None,
    market_result: MarketResearchResult | None,
    live_research_result: LiveResearchResult | None,
    api_key: str,
    model: str,
) -> SynthesisResult:
    llm = ChatOpenAI(
        model=model,
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        temperature=0.3,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    agent_outputs = []

    if visual_result:
        agent_outputs.append(f"""## Visual Analysis Agent (Score: {visual_result.score}/100)
Color: {visual_result.color_analysis}
Typography: {visual_result.typography}
Layout: {visual_result.layout_and_spacing}
Hierarchy: {visual_result.visual_hierarchy}
Strengths: {', '.join(visual_result.strengths)}
Recommendations: {', '.join(visual_result.recommendations)}""")

    if ux_result:
        violations = ""
        for v in ux_result.heuristic_violations:
            violations += f"\n- [{v.severity.upper()}] {v.heuristic_id} {v.heuristic_name}: {v.description}"
        agent_outputs.append(f"""## UX Critique Agent (Score: {ux_result.score}/100)
Heuristic Violations:{violations}
Accessibility Issues: {', '.join(ux_result.accessibility_issues)}
Strengths: {', '.join(ux_result.strengths)}
Recommendations: {', '.join(ux_result.recommendations)}""")

    if market_result:
        agent_outputs.append(f"""## Market Research Agent (Score: {market_result.score}/100)
Category: {market_result.design_category}
Trend Alignment: {market_result.trend_alignment}
Competitor Insights: {', '.join(market_result.competitor_insights)}
Differentiation: {', '.join(market_result.differentiation_opportunities)}
Strengths: {', '.join(market_result.strengths)}
Recommendations: {', '.join(market_result.recommendations)}""")

    if live_research_result and not live_research_result.skipped_reason:
        sources = "\n".join(
            f"- {source.title}: {source.url}"
            for source in live_research_result.sources[:8]
        )
        agent_outputs.append(f"""## Live Web Research Agent (No numeric score)
Summary: {live_research_result.summary}
Current Trends: {', '.join(live_research_result.current_trends)}
Competitor Findings: {', '.join(live_research_result.competitor_findings)}
Opportunities: {', '.join(live_research_result.opportunities)}
Sources:
{sources}""")

    if not agent_outputs:
        return SynthesisResult(
            executive_summary="No completed analysis outputs were available to synthesize.",
            overall_score=0,
        )

    combined = "\n\n".join(agent_outputs)

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Synthesize these specialist agent findings into an executive report:\n\n{combined}"),
    ]

    try:
        response = llm.invoke(messages)
    except Exception as e:
        return SynthesisResult(
            executive_summary=f"API error: {e}",
            overall_score=0,
        )

    try:
        data = json.loads(response.content)
        return SynthesisResult(**data)
    except (json.JSONDecodeError, Exception):
        return SynthesisResult(
            executive_summary=response.content,
            overall_score=0,
        )
