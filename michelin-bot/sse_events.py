"""
SSE (Server-Sent Events) event models for streaming.

Defines structured event types for real-time communication with Nuxt UI frontend.
Compatible with Nuxt UI UCard components and progress indicators.
"""
import json
from enum import Enum
from typing import Optional, Dict, Any, Literal
from pydantic import BaseModel, Field, field_validator


class SSEEventType(str, Enum):
    """SSE event types for streaming."""
    # Legacy (for backward compatibility)
    TOKEN = "token"
    DONE = "done"
    ERROR = "error"

    # Progress tracking
    PROGRESS = "progress"
    STEP_START = "step_start"
    STEP_COMPLETE = "step_complete"

    # Structured data for UI
    RESTAURANT_CARD = "restaurant_card"
    METADATA = "metadata"

    # Analysis results
    QUERY_ANALYSIS = "query_analysis"
    LOCATION_DETECTED = "location_detected"


class ProgressEvent(BaseModel):
    """Progress update event for UI progress indicators."""
    step: str = Field(..., description="Current step identifier (e.g., 'analyzing', 'searching', 'generating')")
    progress: float = Field(..., ge=0.0, le=1.0, description="Progress from 0.0 to 1.0")
    message: str = Field(..., description="Human-readable progress message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional step details")


class RestaurantCardEvent(BaseModel):
    """Structured restaurant card data for Nuxt UI UCard rendering.

    Designed to be compatible with UCard component:
    - title: Main title displayed
    - subtitle: Secondary text
    - badge: Award badge display
    - Additional fields for rich card content
    """
    # Core restaurant data
    id: int
    name: str
    award: Optional[str] = None
    cuisine: Optional[str] = None
    price: Optional[str] = None
    location: str
    distance_km: Optional[float] = None

    # Description
    description: Optional[str] = None
    signature_dish: Optional[str] = None
    facilities: Optional[str] = None

    # UI rendering helpers - computed from core data
    title: Optional[str] = Field(None, description="Computed title for UCard")
    subtitle: Optional[str] = Field(None, description="Computed subtitle for UCard")
    badge_text: Optional[str] = Field(None, description="Badge text (e.g., '3 Stars')")
    badge_color: Optional[str] = Field(None, description="Badge color for UBadge")

    # Links
    url: Optional[str] = None
    website_url: Optional[str] = None

    @field_validator('title', mode='before')
    @classmethod
    def compute_title(cls, v: Optional[str], info) -> str:
        """Compute title from name and award if not explicitly set."""
        if v is not None:
            return v
        name = info.data.get('name', '')
        award = info.data.get('award', '')
        return f"{name} ({award})" if award else name

    @field_validator('subtitle', mode='before')
    @classmethod
    def compute_subtitle(cls, v: Optional[str], info) -> Optional[str]:
        """Compute subtitle from cuisine and location if not explicitly set."""
        if v is not None:
            return v
        cuisine = info.data.get('cuisine')
        location = info.data.get('location', '')
        parts = [p for p in [cuisine, location] if p]
        return " | ".join(parts) if parts else None

    @field_validator('badge_text', mode='before')
    @classmethod
    def compute_badge_text(cls, v: Optional[str], info) -> Optional[str]:
        """Compute badge text from award if not explicitly set."""
        if v is not None:
            return v
        return info.data.get('award')

    @field_validator('badge_color', mode='before')
    @classmethod
    def compute_badge_color(cls, v: Optional[str], info) -> Optional[str]:
        """Compute Nuxt UI badge color from award level."""
        if v is not None:
            return v
        award = info.data.get('award', '')
        if '3 Stars' in award or '3 star' in award:
            return 'yellow'
        elif '2 Stars' in award or '2 star' in award:
            return 'orange'
        elif '1 Star' in award or '1 star' in award:
            return 'amber'
        elif 'Bib Gourmand' in award:
            return 'red'
        elif 'Green Star' in award or 'green' in award.lower():
            return 'green'
        return 'primary'


class QueryAnalysisEvent(BaseModel):
    """Query analysis results event.

    Shows what the agent detected from the user's query.
    Useful for displaying filters and confirming understanding.
    """
    original_query: str
    detected_location: Optional[str] = None
    detected_cuisine: Optional[str] = None
    detected_award: Optional[str] = None
    detected_price: Optional[str] = None
    is_geo_query: bool
    distance_constraint: Optional[float] = None
    needs_user_location: bool = False


class LocationDetectedEvent(BaseModel):
    """Location detected event.

    Shows the location that was extracted from the query or provided by user.
    Useful for map visualization and confirmation.
    """
    location: str
    latitude: float
    longitude: float
    source: Literal["user_provided", "query_extracted", "city_database"]


class SSEMetadata(BaseModel):
    """Metadata event for stream session."""
    session_id: str
    query: str
    workflow_version: str = "2.0"


# ============================================================================
# SSE Event Factory Functions
# ============================================================================

def create_sse_event(event_type: SSEEventType, data: Dict[str, Any]) -> Dict[str, str]:
    """Create an SSE event dictionary.

    Args:
        event_type: The type of SSE event
        data: The event data payload (will be JSON serialized)

    Returns:
        Dictionary with 'event' and 'data' keys for SSE formatting
    """
    return {
        "event": event_type.value,
        "data": json.dumps(data, ensure_ascii=False)
    }


def create_token_event(content: str) -> Dict[str, str]:
    """Create a token event for streaming text."""
    return create_sse_event(SSEEventType.TOKEN, {"content": content})


def create_progress_event(step: str, progress: float, message: str, details: Optional[Dict] = None) -> Dict[str, str]:
    """Create a progress event."""
    return create_sse_event(SSEEventType.PROGRESS, {
        "step": step,
        "progress": progress,
        "message": message,
        "details": details
    })


def create_step_start_event(step: str, message: str) -> Dict[str, str]:
    """Create a step start event."""
    return create_sse_event(SSEEventType.STEP_START, {
        "step": step,
        "message": message
    })


def create_step_complete_event(step: str, message: str) -> Dict[str, str]:
    """Create a step complete event."""
    return create_sse_event(SSEEventType.STEP_COMPLETE, {
        "step": step,
        "message": message
    })


def create_restaurant_card_event(restaurant_data: Dict[str, Any]) -> Dict[str, str]:
    """Create a restaurant card event from raw data."""
    card = RestaurantCardEvent(**restaurant_data)
    return create_sse_event(SSEEventType.RESTAURANT_CARD, card.model_dump())


def create_query_analysis_event(analysis_data: Dict[str, Any]) -> Dict[str, str]:
    """Create a query analysis event."""
    return create_sse_event(SSEEventType.QUERY_ANALYSIS, analysis_data)


def create_location_detected_event(location: str, lat: float, lng: float, source: str) -> Dict[str, str]:
    """Create a location detected event."""
    return create_sse_event(SSEEventType.LOCATION_DETECTED, {
        "location": location,
        "latitude": lat,
        "longitude": lng,
        "source": source
    })


def create_done_event(session_id: str, response_length: int, **kwargs) -> Dict[str, str]:
    """Create a completion event."""
    return create_sse_event(SSEEventType.DONE, {
        "session_id": session_id,
        "response_length": response_length,
        **kwargs
    })


def create_error_event(error: str, step: Optional[str] = None) -> Dict[str, str]:
    """Create an error event."""
    return create_sse_event(SSEEventType.ERROR, {
        "error": error,
        "step": step
    })
