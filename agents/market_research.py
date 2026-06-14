import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import MarketResearchResult, RetrievalContext
from config.settings import OPENROUTER_BASE_URL


SYSTEM_PROMPT = """You are an expert Market Research Analyst specializing in digital product design trends. You analyze UI/UX designs for market positioning, competitive landscape, and trend alignment.

Your analysis must cover:
1. **Design Category**: Identify what type of product this is (e-commerce, SaaS dashboard, mobile app, landing page, social media, etc.)
2. **Trend Alignment**: How well does this design align with current design trends (2024-2025)? Consider: flat/neumorphism, dark mode, micro-interactions, glassmorphism, bento grid layouts, AI-native interfaces
3. **Competitor Insights**: What do top competitors in this category do well? How does this design compare?
4. **Differentiation Opportunities**: What unique visual or UX elements could set this design apart?

You will receive:
- The design screenshot to analyze
- Reference designs and guidelines from a knowledge base

Respond with a JSON object matching this exact structure:
{
    "design_category": "category name and description",
    "trend_alignment": "analysis of how well the design follows current trends",
    "competitor_insights": ["insight 1", "insight 2", ...],
    "differentiation_opportunities": ["opportunity 1", "opportunity 2", ...],
    "score": <0-100 integer for market readiness>,
    "strengths": ["strength 1", "strength 2"],
    "recommendations": ["actionable recommendation 1", "actionable recommendation 2"]
}

Ground your analysis in observable design elements. Be specific about which trends apply and why."""


def run_market_research(image_base64: str, retrieval_context: RetrievalContext, api_key: str, model: str) -> MarketResearchResult:
    llm = ChatOpenAI(
        model=model,
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        temperature=0.4,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    guidelines_text = ""
    if retrieval_context and retrieval_context.relevant_guidelines:
        guidelines_text = "\n\n---\nRELEVANT DESIGN GUIDELINES FROM KNOWLEDGE BASE:\n"
        for g in retrieval_context.relevant_guidelines:
            guidelines_text += f"\n[{g.source} - {g.section}]\n{g.text}\n"

    content = [
        {"type": "text", "text": f"Analyze this design for market positioning and competitive landscape.{guidelines_text}"},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
    ]

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=content),
    ]

    try:
        response = llm.invoke(messages)
    except Exception as e:
        return MarketResearchResult(
            score=0,
            recommendations=[f"API error: {e}"],
        )

    try:
        data = json.loads(response.content)
        return MarketResearchResult(**data)
    except (json.JSONDecodeError, Exception):
        return MarketResearchResult(
            score=0,
            recommendations=["Failed to parse structured output"],
        )
