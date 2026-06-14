import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import VisualAnalysisResult, RetrievalContext
from config.settings import OPENROUTER_BASE_URL


SYSTEM_PROMPT = """You are an expert Visual Design Analyst. You analyze UI/UX design screenshots with deep expertise in visual design principles.

Your analysis must cover:
1. **Color Analysis**: Palette harmony, contrast ratios, semantic color usage, 60-30-10 rule adherence
2. **Typography**: Type hierarchy, readability, font pairing, size scale, line height
3. **Layout & Spacing**: Grid alignment, whitespace usage, spacing consistency, 8px grid adherence
4. **Visual Hierarchy**: Eye flow, focal points, element importance ordering, above-the-fold content

You will receive:
- The design screenshot to analyze
- Reference design guidelines retrieved from a knowledge base (use these as benchmarks)

Respond with a JSON object matching this exact structure:
{
    "color_analysis": "detailed analysis of color usage",
    "typography": "detailed analysis of typography",
    "layout_and_spacing": "detailed analysis of layout and spacing",
    "visual_hierarchy": "detailed analysis of visual hierarchy",
    "score": <0-100 integer>,
    "strengths": ["strength 1", "strength 2", ...],
    "recommendations": ["actionable recommendation 1", "actionable recommendation 2", ...]
}

Be specific and actionable. Reference concrete elements in the design. Score fairly: 70-80 is good, 80-90 is excellent, 90+ is exceptional."""


def run_visual_analysis(image_base64: str, retrieval_context: RetrievalContext, api_key: str, model: str) -> VisualAnalysisResult:
    llm = ChatOpenAI(
        model=model,
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        temperature=0.3,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    guidelines_text = ""
    if retrieval_context and retrieval_context.relevant_guidelines:
        guidelines_text = "\n\n---\nRELEVANT DESIGN GUIDELINES FROM KNOWLEDGE BASE:\n"
        for g in retrieval_context.relevant_guidelines:
            guidelines_text += f"\n[{g.source} - {g.section}]\n{g.text}\n"

    content = [
        {"type": "text", "text": f"Analyze this design screenshot for visual design quality.{guidelines_text}"},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
    ]

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=content),
    ]

    try:
        response = llm.invoke(messages)
    except Exception as e:
        return VisualAnalysisResult(
            score=0,
            recommendations=[f"API error: {e}"],
        )

    try:
        data = json.loads(response.content)
        return VisualAnalysisResult(**data)
    except (json.JSONDecodeError, Exception):
        return VisualAnalysisResult(
            color_analysis=response.content,
            score=0,
            recommendations=["Failed to parse structured output"],
        )
