"""
LangGraph workflow for MichelinBot multi-step restaurant recommendation.

Defines the workflow nodes and graph structure for processing restaurant queries
with step-by-step progress tracking and structured output for Nuxt UI.
"""
import logging
from typing import Literal, Dict, Any, Optional, List
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

from langgraph_state import MichelinAgentState
from config import get_settings
from geolocation import (
    extract_location_from_query,
    extract_distance_from_query,
    get_city_coordinates,
    CITY_COORDINATES,
)
from prompts import MICHELIN_GUIDE_SYSTEM_PROMPT

logger = logging.getLogger(__name__)
settings = get_settings()

# Centralized LLM configuration
LLM_MODEL = settings.llm_model
LLM_TEMPERATURE = settings.llm_temperature
LLM_MAX_TOKENS = settings.llm_max_tokens
API_BASE = settings.api_base_url


# ============================================================================
# WORKFLOW NODES
# ============================================================================

async def intent_analysis_node(state: MichelinAgentState) -> MichelinAgentState:
    """Analyze the user's query to extract intent, location, cuisine, and constraints.

    This is the first node in the workflow. It extracts structured information
    from the natural language query for use in subsequent nodes.

    Location priority:
    1. Location mentioned in query (e.g., "in Munich")
    2. User's GPS coordinates (auto-detected from browser)
    3. No location (general recommendations)
    """
    query = state["query"]
    logger.info(f"Analyzing query: {query}")

    # Extract location from query
    location_obj = extract_location_from_query(query)
    if location_obj:
        state["detected_location"] = location_obj.name
        # Get coordinates for the location
        coords = get_city_coordinates(location_obj.name)
        if coords:
            state["extracted_coordinates"] = {
                "latitude": coords[0],
                "longitude": coords[1]
            }
    elif state.get("user_location"):
        # No location in query, but user provided GPS coordinates
        # Use user's location as default
        state["detected_location"] = "Your current location"
        state["extracted_coordinates"] = state["user_location"]
        logger.info(f"Using user GPS location as default: {state['user_location']}")

    # Extract distance constraint
    distance = extract_distance_from_query(query)
    if distance:
        state["distance_constraint"] = distance

    # Extract cuisine type (simple keyword matching)
    cuisine_keywords = {
        "italian": ["italian", "pasta", "pizza", "risotto"],
        "french": ["french", "bistro", "brasserie"],
        "japanese": ["japanese", "sushi", "ramen", "izakaya", "kaiseki"],
        "chinese": ["chinese", "dim sum", "cantonese", "szechuan"],
        "spanish": ["spanish", "tapas", "paella"],
        "indian": ["indian", "curry", "tandoori"],
        "german": ["german", "bavarian", "sausage"],
        "mexican": ["mexican", "taco", "burrito"],
        "thai": ["thai", "pad thai", "curry"],
        "korean": ["korean", "bbq", "kimchi"],
        "mediterranean": ["mediterranean", "greek", "turkish"],
        "seafood": ["seafood", "fish", "oyster"],
        "vegetarian": ["vegetarian", "vegan", "plant-based"],
        "steakhouse": ["steak", "steakhouse", "meat"],
    }

    query_lower = query.lower()
    for cuisine, keywords in cuisine_keywords.items():
        if any(keyword in query_lower for keyword in keywords):
            state["detected_cuisine"] = cuisine.capitalize()
            break

    # Extract award level
    if "3 star" in query_lower or "three star" in query_lower or "3*" in query:
        state["detected_award"] = "3 Stars"
    elif "2 star" in query_lower or "two star" in query_lower or "2*" in query:
        state["detected_award"] = "2 Stars"
    elif "1 star" in query_lower or "one star" in query_lower or "1*" in query:
        state["detected_award"] = "1 Star"
    elif "bib gourmand" in query_lower:
        state["detected_award"] = "Bib Gourmand"
    elif "green star" in query_lower:
        state["detected_award"] = "Green Star"

    # Extract price range
    if "€€€€" in query or "$$$$" in query or "very expensive" in query_lower:
        state["detected_price"] = "€€€€"
    elif "€€€" in query or "$$$" in query or "expensive" in query_lower:
        state["detected_price"] = "€€€"
    elif "€€" in query or "$$" in query or "moderate" in query_lower:
        state["detected_price"] = "€€"

    # Determine query type
    if state.get("detected_location") or state.get("user_location"):
        state["is_geo_query"] = True
        state["query_type"] = "nearby_search"
    elif "best" in query_lower or "top" in query_lower or "recommend" in query_lower:
        state["query_type"] = "recommendation"
    else:
        state["query_type"] = "search"

    logger.info(f"Query analysis complete - type: {state['query_type']}, "
                f"location: {state.get('detected_location')}, "
                f"cuisine: {state.get('detected_cuisine')}, "
                f"award: {state.get('detected_award')}")

    return state


async def location_search_node(state: MichelinAgentState) -> MichelinAgentState:
    """Prepare location context for LLM recommendations.

    This node processes location information for the LLM:
    1. User-provided GPS coordinates
    2. Location extracted from the query

    Note: In LLM-only mode, this sets up context rather than database search.
    """
    logger.info("Starting location context node")

    # Determine search center
    center = None
    source = None

    if state.get("user_location"):
        center = state["user_location"]
        source = "user_provided"
    elif state.get("extracted_coordinates"):
        center = state["extracted_coordinates"]
        source = "query_extracted"

    if not center:
        logger.warning("No location available, skipping location context")
        return state

    state["search_center"] = center

    # Determine search radius
    radius = state.get("distance_constraint", 50.0)
    state["search_radius"] = radius

    # In LLM-only mode, provide context to the LLM
    state["restaurants_found"] = []

    logger.info(f"Location context prepared - center: {center}, radius: {radius}km")

    return state


async def restaurant_lookup_node(state: MichelinAgentState) -> MichelinAgentState:
    """Additional processing node (currently unused).

    This node is a placeholder for future enhancements.
    """
    logger.info("Restaurant lookup node (placeholder)")

    return state


async def response_generation_node(state: MichelinAgentState) -> MichelinAgentState:
    """Generate the final response using the LLM.

    This node:
    1. Formats the context from previous nodes
    2. Constructs messages for the LLM
    3. Streams the response (handled by caller)
    4. Stores the generated response in state
    """
    logger.info("Starting response generation node")

    # Build context string
    context_parts = []

    if state.get("detected_location"):
        location = state['detected_location']
        # If using user GPS, include coordinates for LLM context
        if location == "Your current location" and state.get("extracted_coordinates"):
            coords = state["extracted_coordinates"]
            location = f"User's GPS coordinates: {coords['latitude']}, {coords['longitude']}"
        context_parts.append(f"Location: {location}")

    if state.get("detected_cuisine"):
        context_parts.append(f"Cuisine: {state['detected_cuisine']}")

    if state.get("detected_award"):
        context_parts.append(f"Award Level: {state['detected_award']}")

    if state.get("detected_price"):
        context_parts.append(f"Price Range: {state['detected_price']}")

    if state.get("distance_constraint"):
        context_parts.append(f"Distance: within {state['distance_constraint']}km")

    context = "\n".join(context_parts) if context_parts else "General restaurant recommendations"

    # For streaming, we store the context for use by the streaming executor
    state["generation_context"] = context

    # Add system message
    system_msg = SystemMessage(content=MICHELIN_GUIDE_SYSTEM_PROMPT)
    state["messages"].append(system_msg)

    # Add user message with context
    user_msg = HumanMessage(content=f"""Query: {state['query']}

Context:
{context}

Please provide restaurant recommendations in the format specified in the system prompt.""")
    state["messages"].append(user_msg)

    logger.info("Response generation context prepared")

    return state


# ============================================================================
# CONDITIONAL ROUTING
# ============================================================================

def should_search_location(state: MichelinAgentState) -> Literal["location_search", "response_generation"]:
    """Determine if location-based search should be performed."""
    has_user_location = state.get("user_location") is not None
    has_extracted_location = state.get("extracted_coordinates") is not None

    if has_user_location or has_extracted_location:
        return "location_search"
    return "response_generation"


def should_enrich_with_vector(state: MichelinAgentState) -> Literal["restaurant_lookup", "response_generation"]:
    """Determine if additional processing is needed.

    Currently always returns 'response_generation' for direct LLM generation.
    """
    # TODO: Add additional processing logic here in the future
    return "response_generation"


# ============================================================================
# GRAPH CONSTRUCTION
# ============================================================================

def create_michelin_graph() -> StateGraph:
    """Create the LangGraph workflow for MichelinBot.

    The workflow:
    1. intent_analysis -> Extract location, cuisine, awards from query
    2. location_search (conditional) -> Prepare location context if available
    3. restaurant_lookup (conditional) -> Additional processing (placeholder)
    4. response_generation -> Generate final LLM response

    Returns:
        Compiled StateGraph ready for execution
    """
    workflow = StateGraph(MichelinAgentState)

    # Add nodes
    workflow.add_node("intent_analysis", intent_analysis_node)
    workflow.add_node("location_search", location_search_node)
    workflow.add_node("restaurant_lookup", restaurant_lookup_node)
    workflow.add_node("response_generation", response_generation_node)

    # Set entry point
    workflow.set_entry_point("intent_analysis")

    # Add conditional edges from intent_analysis
    workflow.add_conditional_edges(
        "intent_analysis",
        should_search_location,
        {
            "location_search": "location_search",
            "response_generation": "response_generation"
        }
    )

    # Add conditional edges from location_search
    workflow.add_conditional_edges(
        "location_search",
        should_enrich_with_vector,
        {
            "restaurant_lookup": "restaurant_lookup",
            "response_generation": "response_generation"
        }
    )

    # Add terminal edges
    workflow.add_edge("restaurant_lookup", "response_generation")
    workflow.add_edge("response_generation", END)

    logger.info("LangGraph workflow created successfully")

    return workflow.compile()


# ============================================================================
# LLM HELPER FUNCTIONS
# ============================================================================

def create_llm_for_streaming():
    """Create an LLM instance configured for streaming."""
    return ChatOpenAI(
        model=LLM_MODEL,
        temperature=LLM_TEMPERATURE,
        openai_api_key=settings.zhipuai_api_key,
        openai_api_base=API_BASE,
        streaming=True,
        max_tokens=LLM_MAX_TOKENS,
        timeout=settings.api_timeout,
    )
