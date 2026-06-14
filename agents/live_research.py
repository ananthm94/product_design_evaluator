import json
import os
from datetime import date

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI

from config.settings import OPENROUTER_BASE_URL
from models.schemas import LiveResearchResult, RetrievalContext, WebResearchSource


QUERY_PLANNER_PROMPT = """You are a design research strategist. Inspect the screenshot and create concise web search queries that will find current competitor and UI trend context.

Return JSON only:
{
    "product_category": "short category name",
    "queries": ["query 1", "query 2", "query 3"]
}

Rules:
- Produce exactly 3 queries.
- Keep queries specific to observable product category, UI pattern, and market/design benchmark needs.
- Include current year or recent/current wording where helpful."""


SUMMARY_PROMPT = """You are a live market and design research analyst. Use the supplied web search snippets to summarize current design trends, competitor patterns, and opportunities for the uploaded UI.

Return JSON only:
{
    "summary": "short synthesis of the live research",
    "current_trends": ["trend 1", "trend 2", "trend 3"],
    "competitor_findings": ["finding 1", "finding 2", "finding 3"],
    "opportunities": ["opportunity 1", "opportunity 2", "opportunity 3"]
}

Ground every point in the snippets. Do not invent companies or claims that are not supported by the search results."""


def run_live_research(
    image_base64: str,
    retrieval_context: RetrievalContext,
    api_key: str,
    model: str,
    tavily_api_key: str,
) -> LiveResearchResult:
    if not tavily_api_key:
        return LiveResearchResult(
            skipped_reason="Live Research skipped because no Tavily API key was provided.",
        )

    try:
        from langchain_tavily import TavilySearch
    except ImportError:
        return LiveResearchResult(
            skipped_reason="Live Research skipped because langchain-tavily is not installed.",
        )

    queries = _plan_queries(image_base64, retrieval_context, api_key, model)
    sources = _run_tavily_searches(queries, tavily_api_key, TavilySearch)

    if not sources:
        return LiveResearchResult(
            summary="Live research ran, but Tavily returned no usable sources.",
            skipped_reason="No usable Tavily search results were returned.",
        )

    return _summarize_sources(sources, image_base64, api_key, model)


def _plan_queries(
    image_base64: str,
    retrieval_context: RetrievalContext,
    api_key: str,
    model: str,
) -> list[str]:
    llm = ChatOpenAI(
        model=model,
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        temperature=0,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    guideline_hint = _guideline_hint(retrieval_context)
    content = [
        {
            "type": "text",
            "text": (
                f"Today's date is {date.today().isoformat()}. "
                "Create live web research queries for this UI screenshot."
                f"{guideline_hint}"
            ),
        },
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
    ]

    try:
        response = llm.invoke([
            SystemMessage(content=QUERY_PLANNER_PROMPT),
            HumanMessage(content=content),
        ])
        data = json.loads(response.content)
        queries = data.get("queries", [])
        queries = [str(q).strip() for q in queries if str(q).strip()]
        if queries:
            return _normalize_queries(queries)
    except Exception:
        pass

    return _fallback_queries()


def _run_tavily_searches(queries: list[str], tavily_api_key: str, tavily_search_cls) -> list[WebResearchSource]:
    os.environ["TAVILY_API_KEY"] = tavily_api_key
    tool = tavily_search_cls(
        max_results=5,
        topic="general",
        search_depth="basic",
        include_answer=False,
        include_raw_content=False,
    )

    by_url: dict[str, WebResearchSource] = {}
    for query in queries:
        try:
            result = tool.invoke({"query": query})
        except Exception:
            continue

        for row in _extract_result_rows(result):
            url = str(row.get("url", "")).strip()
            if not url or url in by_url:
                continue
            by_url[url] = WebResearchSource(
                title=str(row.get("title", "")).strip(),
                url=url,
                content=_truncate(str(row.get("content", "")).strip(), 700),
                score=float(row.get("score") or 0.0),
            )

    return list(by_url.values())[:12]


def _summarize_sources(
    sources: list[WebResearchSource],
    image_base64: str,
    api_key: str,
    model: str,
) -> LiveResearchResult:
    llm = ChatOpenAI(
        model=model,
        base_url=OPENROUTER_BASE_URL,
        api_key=api_key,
        temperature=0.2,
        model_kwargs={"response_format": {"type": "json_object"}},
    )

    source_text = "\n\n".join(
        f"[{i}] {s.title}\nURL: {s.url}\nSnippet: {s.content}"
        for i, s in enumerate(sources, 1)
    )
    content = [
        {
            "type": "text",
            "text": (
                f"Today's date is {date.today().isoformat()}.\n\n"
                "Search snippets:\n"
                f"{source_text}"
            ),
        },
        {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64}"}},
    ]

    try:
        response = llm.invoke([
            SystemMessage(content=SUMMARY_PROMPT),
            HumanMessage(content=content),
        ])
        data = json.loads(response.content)
        return LiveResearchResult(
            summary=data.get("summary", ""),
            current_trends=_as_string_list(data.get("current_trends")),
            competitor_findings=_as_string_list(data.get("competitor_findings")),
            opportunities=_as_string_list(data.get("opportunities")),
            sources=sources,
        )
    except Exception as e:
        return LiveResearchResult(
            summary=f"Live research sources were retrieved, but summarization failed: {e}",
            sources=sources,
        )


def _guideline_hint(retrieval_context: RetrievalContext) -> str:
    if not retrieval_context or not retrieval_context.relevant_guidelines:
        return ""
    chunks = retrieval_context.relevant_guidelines[:3]
    lines = [f"- {g.source}: {_truncate(g.text, 220)}" for g in chunks]
    return "\n\nRelevant local design context:\n" + "\n".join(lines)


def _fallback_queries() -> list[str]:
    year = date.today().year
    return [
        f"current UI design trends for digital product interfaces {year}",
        f"best competitor app UI design benchmarks {year}",
        f"digital product UX patterns and market differentiation {year}",
    ]


def _normalize_queries(queries: list[str]) -> list[str]:
    normalized = []
    for query in queries:
        if query not in normalized:
            normalized.append(query)
    while len(normalized) < 3:
        normalized.extend(_fallback_queries())
        normalized = list(dict.fromkeys(normalized))
    return normalized[:3]


def _extract_result_rows(result) -> list[dict]:
    if isinstance(result, dict):
        rows = result.get("results", [])
        return rows if isinstance(rows, list) else []
    if isinstance(result, list):
        return result
    return []


def _as_string_list(value) -> list[str]:
    if not isinstance(value, list):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _truncate(text: str, limit: int) -> str:
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0] + "..."
