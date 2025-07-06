from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from enum import Enum


class SearchType(str, Enum):
    """Search type enumeration"""
    DENSE = "dense"
    SPARSE = "sparse"
    HYBRID = "hybrid"
    WEB = "web"
    ALL = "all"


class ResultSource(str, Enum):
    """Result source enumeration"""
    DOCUMENT = "document"
    WEB = "web"
    CACHE = "cache"


class SearchQuery(BaseModel):
    """Search query model"""
    query: str = Field(..., min_length=1, max_length=1000)
    search_type: SearchType = SearchType.HYBRID
    limit: int = Field(default=10, ge=1, le=50)
    include_web: bool = True
    document_ids: Optional[List[str]] = None
    filters: Optional[Dict[str, Any]] = None
    rerank: bool = True


class SearchResult(BaseModel):
    """Individual search result model"""
    id: str
    title: str
    content: str
    source: ResultSource
    score: float
    metadata: Dict[str, Any]
    highlights: Optional[List[str]] = None
    url: Optional[str] = None  # For web results
    document_id: Optional[str] = None  # For document results


class SearchResponse(BaseModel):
    """Search response model"""
    query: str
    results: List[SearchResult]
    total_results: int
    search_type: SearchType
    processing_time: float
    sources: Dict[str, int]
    suggestions: Optional[List[str]] = None
    filters_applied: Optional[Dict[str, Any]] = None


class WebSearchResult(BaseModel):
    """Web search result model"""
    title: str
    url: str
    snippet: str
    date: Optional[str] = None
    source: str
    score: float = 0.0


class RerankResult(BaseModel):
    """Reranking result model"""
    original_index: int
    new_score: float
    relevance_score: float


class SearchSession(BaseModel):
    """Search session model for tracking user interactions"""
    session_id: str
    user_id: Optional[str] = None
    queries: List[str] = []
    results_clicked: List[str] = []
    feedback: List[Dict[str, Any]] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class SearchFeedback(BaseModel):
    """Search feedback model"""
    query: str
    result_id: str
    feedback_type: str  # 'helpful', 'not_helpful', 'irrelevant'
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow) 