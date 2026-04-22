"""
LangGraph agent for intelligent restaurant recommendation workflow.

Orchestrates query analysis, retrieval, and response generation.
"""
from typing import TypedDict, Annotated, List, Dict, Any, Optional
from typing_extensions import Required
import operator
import logging

from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph import StateGraph, END

from config import get_settings
from rag_pipeline import (
    rag_pipeline,
    retrieve_relevant_documents,
    embed_query,
    should_use_geolocation,
    should_use_filters,
    retrieve_by_geolocation
)
from geolocation import extract_location_from_query, extract_distance_from_query, CITY_COORDINATES
from prompts import analyze_query, GEOLOCATION_DETECTION_TEMPLATE, MICHELIN_GUIDE_SYSTEM_PROMPT
from llm import simple_chat

logger = logging.getLogger(__name__)
settings = get_settings()


# ============================================================================
# AGENT STATE
# ============================================================================

class AgentState(TypedDict):
    """State for the restaurant recommendation agent."""
    messages: Annotated[List[BaseMessage], operator.add]
    query: Required[str]
    analysis: Dict[str, Any]
    context: List[Dict[str, Any]]
    filters: Dict[str, Any]
    geo_query: Optional[Dict[str, Any]]
    response: Optional[str]
    sources: List[Dict[str, Any]]
    next_step: str


# ============================================================================
# AGENT NODES
# ============================================================================

async def router_node(state: AgentState) -> AgentState:
    """Analyze query and determine routing.

    This node classifies the query intent and extracts filters.
    """
    query = state["query"]
    geo_info = state.get("geo_query", {})

    # Analyze the query
    analysis = analyze_query(query)

    # Extract filters
    filters = await should_use_filters(query)

    # Determine if geolocation is needed
    if not geo_info and analysis["is_geo_query"]:
        location = extract_location_from_query(query)
        distance = extract_distance_from_query(query)

        geo_info = {
            "is_geo_query": True,
            "location": location,
            "distance_constraint": distance,
            "needs_user_location": analysis["needs_user_location"]
        }

        # Try to get coordinates from city name
        if location and location.name:
            coords = CITY_COORDINATES.get(location.name.lower())
            if coords:
                geo_info["latitude"] = coords[0]
                geo_info["longitude"] = coords[1]
                geo_info["location_coords"] = coords

    # Update state
    state["analysis"] = analysis
    state["filters"] = filters
    state["geo_query"] = geo_info

    # Determine next step
    if geo_info and geo_info.get("needs_user_location") and not geo_info.get("user_provided"):
        state["next_step"] = "ask_location"
    elif geo_info and geo_info.get("latitude"):
        state["next_step"] = "geo_retriever"
    else:
        state["next_step"] = "retriever"

    return state


async def retriever_node(state: AgentState) -> AgentState:
    """Retrieve relevant restaurants using vector search."""
    query = state["query"]
    filters = state.get("filters", {})

    # Embed query
    query_emb = await embed_query(query)

    # Retrieve documents
    documents = await retrieve_relevant_documents(
        query=query,
        query_embedding=query_emb,
        top_k=5,
        filters=filters
    )

    # Convert to context format
    context = []
    for doc in documents:
        context.append({
            "id": doc.metadata.get("id"),
            "name": doc.metadata.get("name"),
            "location": doc.metadata.get("location"),
            "cuisine": doc.metadata.get("cuisine"),
            "award": doc.metadata.get("award"),
            "price": doc.metadata.get("price"),
            "content": doc.page_content,
            "similarity": doc.metadata.get("similarity_score", 0),
        })

    state["context"] = context
    state["sources"] = context
    state["next_step"] = "generator"

    return state


async def geo_retriever_node(state: AgentState) -> AgentState:
    """Retrieve restaurants using geolocation."""
    query = state["query"]
    filters = state.get("filters", {})
    geo_info = state["geo_query"]

    if not geo_info:
        state["next_step"] = "retriever"
        return state

    lat = geo_info.get("latitude")
    lon = geo_info.get("longitude")
    radius = geo_info.get("distance_constraint", 50)

    if lat is None or lon is None:
        state["next_step"] = "retriever"
        return state

    # Retrieve nearby restaurants
    documents = await retrieve_by_geolocation(
        query=query,
        latitude=lat,
        longitude=lon,
        radius_km=radius,
        filters=filters
    )

    # Convert to context format
    context = []
    for doc in documents:
        context.append({
            "id": doc.metadata.get("id"),
            "name": doc.metadata.get("name"),
            "location": doc.metadata.get("location"),
            "cuisine": doc.metadata.get("cuisine"),
            "award": doc.metadata.get("award"),
            "price": doc.metadata.get("price"),
            "distance_km": doc.metadata.get("distance_km"),
            "content": doc.page_content,
        })

    state["context"] = context
    state["sources"] = context
    state["next_step"] = "generator"

    return state


async def ask_location_node(state: AgentState) -> AgentState:
    """Ask user for their location."""
    response = ("I'd be happy to help you find nearby restaurants! "
                "Could you please provide your location? You can share:\n"
                "- Your city name\n"
                "- Your coordinates (latitude, longitude)\n"
                "- Or allow location access")

    state["response"] = response
    state["next_step"] = END

    return state


async def generator_node(state: AgentState) -> AgentState:
    """Generate response using retrieved context."""
    query = state["query"]
    context = state["context"]
    geo_info = state.get("geo_query")

    # Build context string
    if context:
        context_str = "## Relevant Restaurants\n\n"
        for i, ctx in enumerate(context[:5], 1):
            distance_info = f" ({ctx['distance_km']:.1f}km away)" if ctx.get('distance_km') else ""
            context_str += f"**{i}. {ctx['name']}**{distance_info}\n"
            context_str += f"- Location: {ctx['location']}\n"
            context_str += f"- Award: {ctx['award']} | Cuisine: {ctx['cuisine']}\n"
            if ctx.get('price'):
                context_str += f"- Price: {ctx['price']}\n"
            context_str += f"- Description: {ctx['content'][:200]}...\n\n"
    else:
        context_str = "No specific restaurants found. You may want to broaden your search criteria."

    # Add location context if geo query
    if geo_info and geo_info.get("location"):
        context_str += f"\n*Search area: {geo_info['location'].name} within {geo_info.get('distance_constraint', 50)}km*\n"

    # Generate response using GLM-4 with proper system prompt from prompts.py
    response = simple_chat(
        user_message=f"Question: {query}\n\n{context_str}",
        system_message=MICHELIN_GUIDE_SYSTEM_PROMPT
    )

    state["response"] = response
    state["next_step"] = END

    return state


# ============================================================================
# GRAPH BUILDING
# ============================================================================

def build_graph() -> StateGraph:
    """Build the LangGraph agent workflow.

    Returns:
        Compiled StateGraph
    """
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("router", router_node)
    workflow.add_node("retriever", retriever_node)
    workflow.add_node("geo_retriever", geo_retriever_node)
    workflow.add_node("ask_location", ask_location_node)
    workflow.add_node("generator", generator_node)

    # Set entry point
    workflow.set_entry_point("router")

    # Add conditional edges from router
    workflow.add_conditional_edges(
        "router",
        lambda s: s["next_step"],
        {
            "ask_location": "ask_location",
            "geo_retriever": "geo_retriever",
            "retriever": "retriever",
        }
    )

    # Add edges from retrievers to generator
    workflow.add_edge("retriever", "generator")
    workflow.add_edge("geo_retriever", "generator")

    # Add edges from ask_location and generator to END
    workflow.add_edge("ask_location", END)
    workflow.add_edge("generator", END)

    return workflow.compile()


# ============================================================================
# AGENT INTERFACE
# ============================================================================

class RestaurantAgent:
    """Agent for restaurant recommendations using LangGraph."""

    def __init__(self):
        """Initialize the agent with compiled graph."""
        self.graph = build_graph()

    async def chat(
        self,
        query: str,
        user_location: Optional[Dict[str, float]] = None,
        conversation_history: Optional[List[BaseMessage]] = None
    ) -> Dict[str, Any]:
        """Chat with the agent.

        Args:
            query: User's query
            user_location: Optional user location (lat, lon)
            conversation_history: Optional conversation history

        Returns:
            Agent response with sources and analysis
        """
        # Build initial state
        initial_state: AgentState = {
            "messages": conversation_history or [],
            "query": query,
            "analysis": {},
            "context": [],
            "filters": {},
            "geo_query": {},
            "response": None,
            "sources": [],
            "next_step": "router",
        }

        # Override with user location if provided
        if user_location:
            initial_state["geo_query"] = {
                "is_geo_query": True,
                "latitude": user_location.get("latitude"),
                "longitude": user_location.get("longitude"),
                "needs_user_location": False,
                "user_provided": True,  # Flag to indicate user provided location
            }
            # Don't modify query - use geo_query flag to trigger geo retriever

        # Run the graph
        result = await self.graph.ainvoke(initial_state)

        return {
            "response": result.get("response", "I apologize, but I couldn't process that request."),
            "sources": result.get("sources", []),
            "analysis": result.get("analysis", {}),
            "geo_info": result.get("geo_query"),
        }

    async def stream(
        self,
        query: str,
        user_location: Optional[Dict[str, float]] = None
    ):
        """Stream agent responses.

        Args:
            query: User's query
            user_location: Optional user location

        Yields:
            Intermediate states
        """
        initial_state: AgentState = {
            "messages": [],
            "query": query,
            "analysis": {},
            "context": [],
            "filters": {},
            "geo_query": {},
            "response": None,
            "sources": [],
            "next_step": "router",
        }

        if user_location:
            initial_state["geo_query"] = {
                "is_geo_query": True,
                "latitude": user_location.get("latitude"),
                "longitude": user_location.get("longitude"),
                "needs_user_location": False,
            }

        async for event in self.graph.astream(initial_state):
            yield event


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_agent() -> RestaurantAgent:
    """Create a new restaurant agent instance.

    Returns:
        Configured RestaurantAgent
    """
    return RestaurantAgent()


# ============================================================================
# HIGH-LEVEL INTERFACE
# ============================================================================

async def get_restaurant_recommendations(
    query: str,
    user_location: Optional[Dict[str, float]] = None
) -> Dict[str, Any]:
    """Get restaurant recommendations using the agent.

    This is the main interface for the application.

    Args:
        query: User's query about restaurants
        user_location: Optional user location with 'latitude' and 'longitude'

    Returns:
        Dictionary with response, sources, and metadata

    Example:
        >>> result = await get_restaurant_recommendations(
        ...     "3-star restaurants near me",
        ...     user_location={"latitude": 48.1351, "longitude": 11.5820}
        ... )
        >>> print(result['response'])
        >>> for source in result['sources']:
        ...     print(f"- {source['name']} ({source['location']})")
    """
    agent = create_agent()
    return await agent.chat(query, user_location)


async def ask_agent(
    query: str,
    location: Optional[str] = None,
    latitude: Optional[float] = None,
    longitude: Optional[float] = None
) -> str:
    """Simple ask interface for the agent.

    Args:
        query: User's question
        location: Optional city name
        latitude: Optional latitude
        longitude: Optional longitude

    Returns:
        Agent's response text
    """
    user_location = None

    if latitude and longitude:
        user_location = {"latitude": latitude, "longitude": longitude}
    elif location:
        coords = CITY_COORDINATES.get(location.lower())
        if coords:
            user_location = {"latitude": coords[0], "longitude": coords[1]}

    result = await get_restaurant_recommendations(query, user_location)
    return result["response"]
