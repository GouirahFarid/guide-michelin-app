"""
LangGraph state schema for MichelinBot workflow.

Defines the TypedDict state that flows through the workflow nodes.
"""
from typing import TypedDict, List, Dict, Any, Optional, Annotated
from langgraph.graph import add_messages


class MichelinAgentState(TypedDict):
    """State for LangGraph multi-step restaurant recommendation workflow.

    This state flows through each node in the workflow, accumulating
    analysis results, retrieved restaurants, and generated responses.
    """
    # ========================================================================
    # INPUT FIELDS (provided by user)
    # ========================================================================
    query: str
    """The user's original query about restaurants."""

    user_location: Optional[Dict[str, float]]
    """User's GPS coordinates if provided: {'latitude': float, 'longitude': float}"""

    session_id: Optional[str]
    """Session identifier for conversation history."""

    conversation_history: Optional[List[Dict[str, str]]]
    """Previous messages in the conversation: [{'role': 'user|assistant', 'content': str}]"""

    # ========================================================================
    # ANALYSIS RESULTS (populated by intent_analysis_node)
    # ========================================================================
    query_type: Optional[str]
    """Type of query: 'search', 'recommend', 'nearby', 'details'"""

    detected_location: Optional[str]
    """Location name extracted from query (e.g., 'Paris', 'Munich')"""

    detected_cuisine: Optional[str]
    """Cuisine type extracted from query (e.g., 'Italian', 'Japanese')"""

    detected_award: Optional[str]
    """Award level extracted from query (e.g., '3 Stars', 'Bib Gourmand')"""

    detected_price: Optional[str]
    """Price range extracted from query (e.g., '€€€€', '$$$')"""

    is_geo_query: bool
    """Whether the query requires geographic search."""

    distance_constraint: Optional[float]
    """Maximum distance in km for search (e.g., 10.0 for 'within 10km')"""

    extracted_coordinates: Optional[Dict[str, float]]
    """Coordinates for extracted location: {'latitude': float, 'longitude': float}"""

    # ========================================================================
    # RETRIEVAL RESULTS (populated by location_search_node and restaurant_lookup_node)
    # ========================================================================
    restaurants_found: Optional[List[Dict[str, Any]]]
    """List of restaurants found from database/vector search.
    Each dict contains: id, name, location, award, cuisine, price, etc.
    """

    search_center: Optional[Dict[str, float]]
    """The center point used for geographic search."""

    search_radius: Optional[float]
    """The radius used for search in km."""

    # ========================================================================
    # GENERATION RESULTS (populated by response_generation_node)
    # ========================================================================
    generated_response: Optional[str]
    """The final generated response text."""

    # ========================================================================
    # LANGGRAPH MESSAGES (for LangGraph's built-in message handling)
    # ========================================================================
    messages: Annotated[List, add_messages]
    """Message history for LangGraph's message passing mechanism."""
