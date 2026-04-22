"""
FastAPI application for Michelin restaurant RAG system.

Provides REST API endpoints for restaurant queries and recommendations.
"""
import json
import logging
import time
from contextlib import asynccontextmanager
from typing import Optional, Dict

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse

from config import get_settings
from langchain_agent import create_langchain_michelin_agent
from models import HealthResponse, ErrorResponse

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()
agent = None  # LangChain Michelin agent


# ============================================================================
# LIFESPAN MANAGEMENT
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    global agent

    # Startup
    print("[MichelinBot] Starting API (LangChain + Streaming Mode)...")
    print("[LLM] Using ZhipuAI glm-5.1 with OpenAI-compatible endpoint")

    # Initialize LangChain Michelin agent
    agent = create_langchain_michelin_agent(
        model="glm-5.1",
        temperature=0.7,
        streaming=True
    )
    print("[Agent] LangChain Michelin agent initialized")

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
# STREAMING CHAT ENDPOINT
# ============================================================================

@app.get("/chat/stream", tags=["Chat"])
async def chat_stream(
    query: str = Query(..., description="User query about restaurants"),
    session_id: Optional[str] = Query(None, description="Session ID for conversation history"),
    user_lat: Optional[float] = Query(None, description="User latitude"),
    user_lon: Optional[float] = Query(None, description="User longitude")
):
    """Streaming chat endpoint using Server-Sent Events (SSE).

    Returns restaurant recommendations as streaming tokens for real-time display.

    Example:
        curl "http://localhost:8003/chat/stream?query=Best%20restaurants%20in%20Munich"
    """
    global agent

    async def event_generator():
        """Generate SSE events for streaming response."""
        try:
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
                history = [
                    {"role": msg.role, "content": msg.content}
                    for msg in sessions[session_id]
                ]

            # Stream response from LangChain agent
            full_response = ""
            async for token in agent.chat_stream(
                query=query,
                user_location=user_location,
                conversation_history=history
            ):
                full_response += token
                # Send SSE event with the token
                yield {
                    "event": "token",
                    "data": json.dumps({"content": token}, ensure_ascii=False)
                }

            # Send completion event
            yield {
                "event": "done",
                "data": json.dumps({
                    "session_id": session_id or str(uuid.uuid4()),
                    "response_length": len(full_response)
                }, ensure_ascii=False)
            }

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
