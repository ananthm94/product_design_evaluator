from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Optional


class RetrievedTextChunk(BaseModel):
    text: str
    source: str
    section: str = ""
    score: float = 0.0


class RetrievedImage(BaseModel):
    image_path: str
    source: str
    category: str = ""
    caption: str = ""
    score: float = 0.0


class RetrievalContext(BaseModel):
    similar_images: list[RetrievedImage] = Field(default_factory=list)
    relevant_guidelines: list[RetrievedTextChunk] = Field(default_factory=list)


class VisualAnalysisResult(BaseModel):
    color_analysis: str = ""
    typography: str = ""
    layout_and_spacing: str = ""
    visual_hierarchy: str = ""
    score: int = Field(default=0, ge=0, le=100)
    strengths: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class HeuristicViolation(BaseModel):
    heuristic_id: str
    heuristic_name: str
    severity: str = "medium"
    description: str = ""
    recommendation: str = ""


class UXCritiqueResult(BaseModel):
    heuristic_violations: list[HeuristicViolation] = Field(default_factory=list)
    accessibility_issues: list[str] = Field(default_factory=list)
    interaction_patterns: list[str] = Field(default_factory=list)
    score: int = Field(default=0, ge=0, le=100)
    strengths: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class MarketResearchResult(BaseModel):
    design_category: str = ""
    trend_alignment: str = ""
    competitor_insights: list[str] = Field(default_factory=list)
    differentiation_opportunities: list[str] = Field(default_factory=list)
    score: int = Field(default=0, ge=0, le=100)
    strengths: list[str] = Field(default_factory=list)
    recommendations: list[str] = Field(default_factory=list)


class WebResearchSource(BaseModel):
    title: str = ""
    url: str = ""
    content: str = ""
    score: float = 0.0


class LiveResearchResult(BaseModel):
    summary: str = ""
    current_trends: list[str] = Field(default_factory=list)
    competitor_findings: list[str] = Field(default_factory=list)
    opportunities: list[str] = Field(default_factory=list)
    sources: list[WebResearchSource] = Field(default_factory=list)
    skipped_reason: Optional[str] = None


class SynthesisResult(BaseModel):
    executive_summary: str = ""
    overall_score: int = Field(default=0, ge=0, le=100)
    top_strengths: list[str] = Field(default_factory=list)
    top_recommendations: list[str] = Field(default_factory=list)
    priority_actions: list[str] = Field(default_factory=list)


class DesignReport(BaseModel):
    visual_analysis: Optional[VisualAnalysisResult] = None
    ux_critique: Optional[UXCritiqueResult] = None
    market_research: Optional[MarketResearchResult] = None
    live_research: Optional[LiveResearchResult] = None
    synthesis: Optional[SynthesisResult] = None
    retrieval_context: Optional[RetrievalContext] = None


class HistoryRecord(BaseModel):
    id: str
    timestamp: str = ""
    model: str = ""
    overall_score: int = 0
    summary: str = ""
    category: str = ""
    thumb_path: str = ""  # local LanceDB backend stores a file path
    thumb_b64: str = ""  # Qdrant backend stores the thumbnail inline (base64 PNG)
    report: Optional[DesignReport] = None
    score: float = 0.0  # retrieval distance when returned from a search


class GraphState(BaseModel):
    image_base64: str = ""
    retrieval_context: Optional[RetrievalContext] = None
    visual_result: Optional[VisualAnalysisResult] = None
    ux_result: Optional[UXCritiqueResult] = None
    market_result: Optional[MarketResearchResult] = None
    live_research_result: Optional[LiveResearchResult] = None
    synthesis: Optional[SynthesisResult] = None
    api_key: str = ""
    model: str = ""
    tavily_api_key: str = ""
