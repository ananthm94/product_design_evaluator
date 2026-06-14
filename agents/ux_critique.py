import json
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from models.schemas import UXCritiqueResult, HeuristicViolation, RetrievalContext
from config.settings import OPENROUTER_BASE_URL


SYSTEM_PROMPT = """You are an expert UX Researcher and Usability Analyst. You evaluate UI designs against established usability heuristics and accessibility standards.

Your analysis must cover:
1. **Nielsen's Heuristic Violations**: Identify specific violations of the 10 usability heuristics:
   - H1: Visibility of System Status
   - H2: Match Between System and Real World
   - H3: User Control and Freedom
   - H4: Consistency and Standards
   - H5: Error Prevention
   - H6: Recognition Rather Than Recall
   - H7: Flexibility and Efficiency of Use
   - H8: Aesthetic and Minimalist Design
   - H9: Help Users Recognize, Diagnose, and Recover from Errors
   - H10: Help and Documentation

2. **Accessibility Issues**: WCAG compliance concerns visible from the screenshot (contrast, touch targets, text size, color-only information)

3. **Interaction Patterns**: Evaluate navigation, feedback mechanisms, input methods

You will receive:
- The design screenshot to evaluate
- Reference design guidelines from a knowledge base

Respond with a JSON object matching this exact structure:
{
    "heuristic_violations": [
        {
            "heuristic_id": "H1",
            "heuristic_name": "Visibility of System Status",
            "severity": "high|medium|low",
            "description": "specific violation found",
            "recommendation": "actionable fix"
        }
    ],
    "accessibility_issues": ["issue 1", "issue 2"],
    "interaction_patterns": ["observation 1", "observation 2"],
    "score": <0-100 integer>,
    "strengths": ["strength 1", "strength 2"],
    "recommendations": ["actionable recommendation 1", "actionable recommendation 2"]
}

Be specific. Reference concrete UI elements. Only flag real violations you can observe."""


def run_ux_critique(image_base64: str, retrieval_context: RetrievalContext, api_key: str, model: str) -> UXCritiqueResult:
    llm = ChatOpenAI(
        model=model,
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        temperature=0.3,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    guidelines_text = ""
    if retrieval_context and retrieval_context.relevant_guidelines:
        guidelines_text = "\n\n---\nRELEVANT USABILITY GUIDELINES FROM KNOWLEDGE BASE:\n"
        for g in retrieval_context.relevant_guidelines:
            guidelines_text += f"\n[{g.source} - {g.section}]\n{g.text}\n"

    content = [
        {"type": "text", "text": f"Evaluate this design for usability and accessibility.{guidelines_text}"},
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
    ]

    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=content),
    ]

    try:
        response = llm.invoke(messages)
    except Exception as e:
        return UXCritiqueResult(
            score=0,
            recommendations=[f"API error: {e}"],
        )

    try:
        data = json.loads(response.content)
        if "heuristic_violations" in data:
            data["heuristic_violations"] = [
                HeuristicViolation(**v) for v in data["heuristic_violations"]
            ]
        return UXCritiqueResult(**data)
    except (json.JSONDecodeError, Exception):
        return UXCritiqueResult(
            score=0,
            recommendations=["Failed to parse structured output"],
        )
