"""
Pydantic models for API request/response validation.

Provides type safety and validation for all API endpoints.
"""
from __future__ import annotations

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum


# ============================================================================
# ENUMS
# ============================================================================

class AwardLevel(str, Enum):
    """Michelin award levels."""
    THREE_STARS = "3 Stars"
    TWO_STARS = "2 Stars"
    ONE_STAR = "1 Star"
    BIB_GOURMAND = "Bib Gourmand"
    SELECTED = "Selected Restaurants"
    ANY = "Any"


class PriceLevel(str, Enum):
    """Price range levels - generic, currency-agnostic.

    The actual price in the database will use local currency symbols:
    - Europe: €, €€, €€€, €€€€
    - Japan: ¥, ¥¥, ¥¥¥, ¥¥¥¥
    - UAE/USA: $, $$, $$$, $$$$
    """
    ONE = "1"     # € / ¥ / $ (inexpensive)
    TWO = "2"     # €€ / ¥¥ / $$ (moderate)
    THREE = "3"   # €€€ / ¥¥¥ / $$$ (expensive)
    FOUR = "4"    # €€€€ / ¥¥¥¥ / $$$$ (very expensive)


# ============================================================================
# CHAT MODELS
# ============================================================================

class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    query: str = Field(..., description="User's question or query", min_length=1)
    session_id: Optional[str] = Field(None, description="Session ID for conversation history")
    user_location: Optional[UserLocation] = Field(None, description="User's location for geo queries")
    filters: Optional[SearchFilters] = Field(None, description="Optional search filters")
    max_results: int = Field(5, description="Maximum number of results", ge=1, le=20)

    model_config = {"validate_assignment": True}

    @field_validator('query')
    @classmethod
    def query_not_empty(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Query cannot be empty")
        return v.strip()


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="AI-generated response")
    sources: List[RestaurantSource] = Field(default_factory=list, description="Source restaurants")
    query_analysis: QueryAnalysis = Field(..., description="Analysis of the user's query")
    geo_results: Optional[GeoResults] = Field(None, description="Geolocation search results if applicable")
    session_id: str = Field(..., description="Session ID for conversation continuity")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatMessage(BaseModel):
    """Chat message in conversation history."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class Message(BaseModel):
    """Chat message in conversation history."""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# RESTAURANT MODELS
# ============================================================================

class RestaurantResponse(BaseModel):
    """Restaurant data model."""
    id: int
    name: str
    address: Optional[str] = None
    location: str
    price: Optional[str] = None
    cuisine: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    phone_number: Optional[str] = None
    url: Optional[str] = None
    website_url: Optional[str] = None
    award: Optional[str] = None
    green_star: bool = False
    facilities_and_services: Optional[str] = None
    description: Optional[str] = None
    distance_km: Optional[float] = Field(None, description="Distance from query location")


class RestaurantSource(BaseModel):
    """Source reference for restaurant recommendations."""
    restaurant_id: int
    name: str
    location: str
    award: Optional[str] = None
    cuisine: Optional[str] = None
    relevance_score: Optional[float] = Field(None, description="Relevance score (0-1)")
    snippet: Optional[str] = Field(None, description="Relevant text snippet")


# ============================================================================
# SEARCH & FILTER MODELS
# ============================================================================

class SearchFilters(BaseModel):
    """Search filters for restaurant queries."""
    location: Optional[str] = None
    cuisine: Optional[str] = None
    award: Optional[str] = None
    price: Optional[str] = None
    green_star_only: bool = False
    has_facilities: Optional[List[str]] = Field(None, description="Required facilities")


class QueryAnalysis(BaseModel):
    """Analysis of user query intent and components."""
    original_query: str
    has_location: bool
    location_mentioned: Optional[str] = None
    has_cuisine: bool
    cuisine_mentioned: Optional[str] = None
    has_award: bool
    award_mentioned: Optional[str] = None
    has_price: bool
    price_mentioned: Optional[str] = None
    is_geo_query: bool
    distance_constraint: Optional[float] = None
    needs_user_location: bool
    detected_filters: Dict[str, Any] = Field(default_factory=dict)


# ============================================================================
# GEOLOCATION MODELS
# ============================================================================

class UserLocation(BaseModel):
    """User's location for geolocation queries."""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in decimal degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in decimal degrees")
    city: Optional[str] = Field(None, description="City name (optional)")


class GeoSearchRequest(BaseModel):
    """Request for geolocation-based restaurant search."""
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(50.0, description="Search radius in kilometers", ge=1, le=500)
    filters: Optional[SearchFilters] = None
    max_results: int = Field(10, ge=1, le=50)


class GeoResults(BaseModel):
    """Results from geolocation search."""
    center: UserLocation
    radius_km: float
    restaurants_found: int
    restaurants: List[RestaurantResponse]


class NearbyRestaurantsResponse(BaseModel):
    """Response for nearby restaurants endpoint."""
    location: UserLocation
    radius_km: float
    count: int
    results: List[RestaurantResponse]


# ============================================================================
# INGESTION MODELS
# ============================================================================

class IngestRequest(BaseModel):
    """Request to trigger data ingestion."""
    file_path: Optional[str] = Field(None, description="Path to CSV file (default: michelin_my_maps.csv)")
    chunk_size: int = Field(500, description="Character chunk size for embeddings", ge=100, le=2000)
    chunk_overlap: int = Field(50, description="Character overlap between chunks", ge=0, le=500)
    skip_existing: bool = Field(True, description="Skip restaurants already in database")


class IngestResponse(BaseModel):
    """Response from data ingestion."""
    status: str
    message: str
    restaurants_processed: int
    restaurants_added: int
    restaurants_skipped: int
    embeddings_created: int
    errors: List[str] = Field(default_factory=list)
    duration_seconds: float


class IngestProgress(BaseModel):
    """Progress update during ingestion."""
    current: int
    total: int
    percentage: float
    current_restaurant: Optional[str] = None


# ============================================================================
# HEALTH & STATUS MODELS
# ============================================================================

class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "healthy"
    version: str = "1.0.0"
    database_connected: bool
    embedding_model_loaded: bool
    llm_configured: bool
    uptime_seconds: float


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


# ============================================================================
# RESTAURANT SEARCH MODELS
# ============================================================================

class RestaurantSearchRequest(BaseModel):
    """Request for direct restaurant search."""
    query: Optional[str] = Field(None, description="Search query (name, cuisine, location)")
    filters: Optional[SearchFilters] = None
    limit: int = Field(20, ge=1, le=100)
    offset: int = Field(0, ge=0, le=1000)
    sort_by: Optional[str] = Field(None, description="Sort field: name, award, location")
    sort_order: str = Field("asc", description="Sort order: asc or desc")

    @field_validator('sort_order')
    @classmethod
    def validate_sort_order(cls, v: str) -> str:
        if v not in ['asc', 'desc']:
            raise ValueError("sort_order must be 'asc' or 'desc'")
        return v


class RestaurantListResponse(BaseModel):
    """Response for restaurant list endpoint."""
    count: int
    total: int
    limit: int
    offset: int
    results: List[RestaurantResponse]


# ============================================================================
# COMPARISON MODELS
# ============================================================================

class RestaurantComparison(BaseModel):
    """Comparison of multiple restaurants."""
    restaurants: List[RestaurantResponse]
    comparison_points: Dict[str, List[str]] = Field(..., description="Key comparison points")
    recommendation: Optional[str] = None


# ============================================================================
# VALIDATION HELPERS
# ============================================================================

def validate_coordinates(latitude: float, longitude: float) -> bool:
    """Validate latitude and longitude are within valid ranges."""
    return -90 <= latitude <= 90 and -180 <= longitude <= 180


def sanitize_query(query: str) -> str:
    """Sanitize user query to prevent injection."""
    # Remove any potentially harmful characters
    allowed = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .,!?-'@")
    return "".join(c for c in query if c in allowed)


# ============================================================================
# PRICE & CURRENCY HELPERS
# ============================================================================

def normalize_price_level(price_str: str) -> Optional[str]:
    """Normalize any currency symbol to a generic price level (1-4).

    Examples:
        "€" → "1",  "€€" → "2",  "€€€" → "3",  "€€€€" → "4"
        "$" → "1",  "$$" → "2",  "$$$" → "3",  "$$$$" → "4"
        "¥" → "1",  "¥¥" → "2",  "¥¥¥" → "3",  "¥¥¥¥" → "4"
    """
    if not price_str:
        return None

    # Count currency symbols (first character repeated)
    if len(price_str) > 0:
        symbol = price_str[0]
        count = len(price_str)

        # Map to price level
        if count == 1:
            return "1"
        elif count == 2:
            return "2"
        elif count == 3:
            return "3"
        elif count >= 4:
            return "4"

    return None


def detect_currency(price_str: str) -> str:
    """Detect the currency symbol from price string.

    Returns: 'EUR', 'USD', 'JPY', or 'UNKNOWN'
    """
    if not price_str:
        return 'UNKNOWN'

    symbol = price_str[0]

    currency_map = {
        '€': 'EUR',
        '$': 'USD',
        '¥': 'JPY',
        '£': 'GBP',
        '₹': 'INR',
    }

    return currency_map.get(symbol, 'UNKNOWN')


CURRENCY_SYMBOLS = {
    'EUR': '€',
    'USD': '$',
    'JPY': '¥',
    'GBP': '£',
    'UNKNOWN': ''
}
