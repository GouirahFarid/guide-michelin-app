"""
Async streaming executor for LangGraph workflow.

Executes the LangGraph workflow node by node, yielding SSE events
for progress tracking and structured data delivery to the Nuxt UI frontend.
"""
import logging
import uuid
from typing import AsyncIterator, Dict, Any, Optional

from langgraph_workflow import (
    create_michelin_graph,
    create_llm_for_streaming,
    intent_analysis_node,
    location_search_node,
    response_generation_node,
    should_search_location,
)
from langgraph_state import MichelinAgentState
from langchain_core.messages import AIMessage

from sse_events import (
    create_step_start_event,
    create_step_complete_event,
    create_progress_event,
    create_query_analysis_event,
    create_location_detected_event,
    create_token_event,
    create_done_event,
    create_error_event,
    SSEEventType,
)

logger = logging.getLogger(__name__)


async def stream_workflow_execution(
    query: str,
    user_location: Optional[Dict[str, float]] = None,
    session_id: Optional[str] = None,
    conversation_history: Optional[list] = None
) -> AsyncIterator[Dict[str, str]]:
    """Stream workflow execution as SSE events.

    Executes the LangGraph workflow step by step, yielding SSE events
    for progress tracking, analysis results, and structured data.

    Args:
        query: User's restaurant query
        user_location: Optional GPS coordinates
        session_id: Optional session identifier
        conversation_history: Optional conversation history

    Yields:
        SSE event dictionaries with 'event' and 'data' keys
    """
    # Generate session ID if not provided
    if not session_id:
        session_id = str(uuid.uuid4())

    # Create workflow
    workflow = create_michelin_graph()

    # Build initial state
    initial_state: MichelinAgentState = {
        "query": query,
        "user_location": user_location,
        "session_id": session_id,
        "conversation_history": conversation_history,
        "messages": [],
        # Analysis results (to be populated)
        "query_type": None,
        "detected_location": None,
        "detected_cuisine": None,
        "detected_award": None,
        "detected_price": None,
        "is_geo_query": False,
        "distance_constraint": None,
        "extracted_coordinates": None,
        # Retrieval results (to be populated)
        "restaurants_found": None,
        "search_center": None,
        "search_radius": None,
        # Generation results (to be populated)
        "generated_response": None,
    }

    # Track progress
    total_steps = 3  # analysis, search (optional), generation
    current_step = 0

    try:
        # ====================================================================
        # STEP 1: Intent Analysis
        # ====================================================================
        current_step += 1
        yield create_step_start_event("intent_analysis", "Analyzing your query...")
        yield create_progress_event("analyzing", current_step / total_steps, "Understanding your request")

        # Execute intent analysis node
        state = await intent_analysis_node(initial_state)

        # Emit query analysis results
        yield create_query_analysis_event({
            "original_query": query,
            "detected_location": state.get("detected_location"),
            "detected_cuisine": state.get("detected_cuisine"),
            "detected_award": state.get("detected_award"),
            "detected_price": state.get("detected_price"),
            "is_geo_query": state.get("is_geo_query", False),
            "distance_constraint": state.get("distance_constraint"),
            "needs_user_location": False,
        })

        # Emit location detected event
        if state.get("extracted_coordinates"):
            coords = state["extracted_coordinates"]
            yield create_location_detected_event(
                location=state["detected_location"] or "Unknown",
                lat=coords["latitude"],
                lng=coords["longitude"],
                source="query_extracted"
            )

        yield create_step_complete_event("intent_analysis", "Query analysis complete")

        # ====================================================================
        # STEP 2: Location Search (conditional)
        # ====================================================================

        if should_search_location(state) == "location_search":
            current_step += 1
            yield create_step_start_event("location_search", "Searching for restaurants...")
            yield create_progress_event("searching", current_step / total_steps, "Finding the best options")

            state = await location_search_node(state)

            # Emit location confirmation if user provided coordinates
            if state.get("user_location"):
                coords = state["user_location"]
                yield create_location_detected_event(
                    location="Your location",
                    lat=coords["latitude"],
                    lng=coords["longitude"],
                    source="user_provided"
                )

            yield create_step_complete_event(
                "location_search",
                "Search complete" + (f" in {state.get('detected_location', 'your area')}" if state.get("detected_location") else "")
            )

        # ====================================================================
        # STEP 3: Response Generation
        # ====================================================================
        current_step += 1
        yield create_step_start_event("response_generation", "Generating recommendations...")
        yield create_progress_event("generating", current_step / total_steps, "Creating your personalized response")

        # Prepare generation node
        state = await response_generation_node(state)

        # Create LLM for streaming
        llm = create_llm_for_streaming()

        # Stream the response token by token
        full_response = ""
        chunks_received = False
        token_count = 0
        max_tokens = 2000  # Safety limit

        # Ensure messages is a valid list
        messages = state.get("messages", [])
        if not messages:
            logger.warning("No messages in state, creating default message")
            from langchain_core.messages import HumanMessage
            messages = [HumanMessage(content=state.get("query", "Hello"))]

        try:
            async for chunk in llm.astream(messages):
                chunks_received = True
                content = getattr(chunk, 'content', None) or ""
                if content:
                    full_response += str(content)
                    token_count += 1
                    yield create_token_event(str(content))
                    if token_count >= max_tokens:
                        logger.warning(f"Max tokens ({max_tokens}) reached, stopping stream")
                        break
        except Exception as e:
            logger.warning(f"Streaming failed: {e}, using fallback")
            # Fallback: invoke without streaming
            try:
                response = await llm.ainvoke(messages)
                content = getattr(response, 'content', None) or str(response)
                full_response = str(content)
                yield create_token_event(full_response)
            except Exception as e2:
                logger.error(f"LLM invoke also failed: {e2}")
                full_response = "I apologize, but I'm having trouble generating a response right now. Please try again."
                yield create_token_event(full_response)

        # If no chunks received, provide fallback
        if not chunks_received:
            logger.warning("No chunks received from stream, using fallback")
            full_response = "I apologize, but I'm having trouble generating a response right now. Please try again."
            yield create_token_event(full_response)

        state["generated_response"] = full_response or ""
        # Ensure messages is a list before appending
        if "messages" not in state or not isinstance(state["messages"], list):
            state["messages"] = []
        state["messages"].append(AIMessage(content=full_response or ""))

        yield create_step_complete_event("response_generation", "Response generated")

        # ====================================================================
        # DONE Event
        # ====================================================================
        yield create_done_event(
            session_id=session_id,
            response_length=len(full_response or ""),
            restaurants_count=len(state.get("restaurants_found") or []),
            query_analysis={
                "detected_location": state.get("detected_location"),
                "detected_cuisine": state.get("detected_cuisine"),
                "detected_award": state.get("detected_award"),
            }
        )

    except Exception as e:
        logger.error(f"Workflow execution error: {e}", exc_info=True)
        yield create_error_event(
            error=str(e),
            step="unknown"
        )


# ============================================================================
# BACKWARD COMPATIBILITY WRAPPER
# ============================================================================

async def legacy_stream_wrapper(
    query: str,
    user_location: Optional[Dict[str, float]] = None,
    session_id: Optional[str] = None,
    conversation_history: Optional[list] = None
) -> AsyncIterator[Dict[str, str]]:
    """Legacy streaming wrapper for backward compatibility.

    Emits only token, done, and error events for clients that don't
    support the new structured event types.
    """
    async for event in stream_workflow_execution(query, user_location, session_id, conversation_history):
        event_type = event.get("event")

        # Pass through legacy events
        if event_type in ["token", "done", "error"]:
            yield event
        # Ignore new event types for legacy clients
