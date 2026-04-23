"""
FastAPI application for Michelin restaurant RAG system.

Provides REST API endpoints for restaurant queries and recommendations.

Now with LangGraph multi-step workflow and structured SSE events for Nuxt UI.
"""
import json
import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import Optional, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from config import get_settings
from langgraph_streaming import stream_workflow_execution
from models import HealthResponse, ErrorResponse, ChatMessage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Session storage (in-memory)
sessions: Dict[str, list] = {}
session_timestamps: Dict[str, float] = {}
SESSION_TIMEOUT = 3600  # 1 hour


# ============================================================================
# LIFESPAN MANAGEMENT
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    print("[MichelinBot] Starting API (LangGraph + Enhanced Streaming Mode)...")
    print("[LLM] Using ZhipuAI glm-5.1 with OpenAI-compatible endpoint")
    print("[Workflow] LangGraph multi-step workflow enabled")

    # Track start time
    app.state.start_time = time.time()

    yield

    # Shutdown
    print("[Shutdown] Closing...")
    print("[Shutdown] Complete")


# ============================================================================
# FASTAPI APP
# ============================================================================

app = FastAPI(
    title="MichelinBot API",
    description="RAG-powered restaurant recommendation system using Michelin Guide data",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS middleware - configure origins from environment
import os

_allowed_origins = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins,  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(error=exc.detail).model_dump(mode='json')
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions - log details but don't expose to client."""
    logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail="An unexpected error occurred. Please try again later."
        ).model_dump(mode='json')
    )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint for LLM-only mode."""
    uptime = time.time() - app.state.start_time

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        database_connected=False,  # Not used in LLM-only mode
        embedding_model_loaded=False,  # Not used in LLM-only mode
        llm_configured=bool(settings.zhipuai_api_key),
        uptime_seconds=uptime,
    )


# ============================================================================
# STREAMING CHAT ENDPOINT (ENHANCED WITH LANGGRAPH)
# ============================================================================

@app.get("/chat/stream", tags=["Chat"])
async def chat_stream(
    query: str = Query(..., description="User query about restaurants"),
    session_id: Optional[str] = Query(None, description="Session ID for conversation history"),
    user_lat: Optional[float] = Query(None, description="User latitude"),
    user_lon: Optional[float] = Query(None, description="User longitude")
):
    """Streaming chat endpoint using Server-Sent Events (SSE) with LangGraph workflow.

    Event Types:
    - step_start: A workflow step is starting
    - progress: Progress update (0.0-1.0)
    - query_analysis: Query analysis results (location, cuisine, award detected)
    - location_detected: Location extracted from query or user coordinates
    - token: Response text token (backward compatibility)
    - step_complete: A workflow step completed
    - done: Stream complete with summary
    - error: Error occurred

    Example:
        curl -N "http://localhost:8000/chat/stream?query=Best%20restaurants%20in%20Munich"
    """
    # Prepare user location
    user_location = None
    if user_lat is not None and user_lon is not None:
        user_location = {
            "latitude": user_lat,
            "longitude": user_lon,
        }

    # Get conversation history for this session
    history = None
    if session_id and session_id in sessions:
        history = sessions[session_id]

    async def event_generator():
        """Generate SSE events for streaming response."""
        nonlocal session_id

        try:
            # Stream workflow execution
            async for event in stream_workflow_execution(
                query=query,
                user_location=user_location,
                session_id=session_id,
                conversation_history=history
            ):
                # Update session ID from response
                if event.get("event") == "done":
                    try:
                        data = json.loads(event.get("data", "{}"))
                        session_id = data.get("session_id", session_id)
                    except:
                        pass

                yield event

        except Exception as e:
            logger.error(f"Streaming error: {type(e).__name__}: {e}", exc_info=True)
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)}, ensure_ascii=False)
            }

    return EventSourceResponse(event_generator())


# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", tags=["Root"])
async def root():
    """API root endpoint with information."""
    return {
        "name": "MichelinBot API",
        "version": "1.0.0",
        "description": "RAG-powered restaurant recommendation system",
        "endpoints": {
            "chat_stream": "/chat/stream",
            "health": "/health",
            "docs": "/docs",
        },
    }


# ============================================================================
# RUN DIRECTLY (for development)
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
