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

from fastapi import FastAPI, HTTPException, Query, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from sse_starlette.sse import EventSourceResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.sessions import SessionMiddleware

from config import get_settings
from langgraph_streaming import stream_workflow_execution
from models import HealthResponse, ErrorResponse, ChatMessage
import secrets

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

# ============================================================================
# RATE LIMITING
# ============================================================================

from collections import defaultdict
from datetime import datetime, timedelta

class RateLimiter:
    """Simple in-memory rate limiter."""
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if request is allowed for this client."""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id]
            if req_time > minute_ago
        ]

        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False

        self.requests[client_id].append(now)
        return True

rate_limiter = RateLimiter(requests_per_minute=60)


# ============================================================================
# CSP MIDDLEWARE
# ============================================================================

class CSPMiddleware(BaseHTTPMiddleware):
    """Content Security Policy middleware for XSS protection."""

    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' 'unsafe-eval'; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: https:; "
            "font-src 'self'; "
            "connect-src 'self' http://localhost:* http://127.0.0.1:*; "
            "frame-ancestors 'none'; "
            "base-uri 'self'; "
            "form-action 'self';"
        )
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        return response


# ============================================================================
# MEMORY STORAGE (LangChain BufferMemory)
# ============================================================================

from memory import memory_store, build_messages_with_memory


# ============================================================================
# LIFESPAN MANAGEMENT
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    print("[MichelinBot] Starting API (LangGraph + Enhanced Streaming Mode)...")
    print("[LLM] Using ZhipuAI with OpenAI-compatible endpoint")
    print("[Workflow] LangGraph multi-step workflow enabled")
    print("[Security] Rate limiting and CSP enabled")

    # Validate required settings
    if not settings.zhipuai_api_key or settings.zhipuai_api_key == "your_zhipuai_api_key_here":
        print("[WARNING] ZHIPUAI_API_KEY not configured!")

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
    description="AI-powered restaurant recommendation system using Michelin Guide data",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CSP middleware
app.add_middleware(CSPMiddleware)

# Add GZip middleware for response compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=secrets.token_urlsafe(32),
    session_cookie="michelin_session",
    max_age=3600,
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
    """Health check endpoint."""
    uptime = time.time() - app.state.start_time

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        llm_configured=bool(settings.zhipuai_api_key),
        uptime_seconds=uptime,
    )


# ============================================================================
# STREAMING CHAT ENDPOINT (ENHANCED WITH LANGGRAPH)
# ============================================================================

def get_client_identifier(request: Request) -> str:
    """Get client identifier for rate limiting."""
    # Try to get from session first
    session_id = getattr(request.state, "session_id", None)
    if session_id:
        return f"session:{session_id}"

    # Fall back to IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return f"ip:{forwarded.split(',')[0].strip()}"
    return f"ip:{request.client.host}"


@app.get("/chat/stream", tags=["Chat"])
async def chat_stream(
    request: Request,
    query: str = Query(
        ...,
        description="User query about restaurants",
        min_length=1,
        max_length=500
    ),
    session_id: Optional[str] = Query(None, description="Session ID for conversation history"),
    user_lat: Optional[float] = Query(None, ge=-90, le=90, description="User latitude"),
    user_lon: Optional[float] = Query(None, ge=-180, le=180, description="User longitude")
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
    logger.info(f"Received chat stream request - query: '{query[:50]}...', session_id: {session_id}")

    # Rate limiting
    client_id = get_client_identifier(request)
    if not rate_limiter.is_allowed(client_id):
        logger.warning(f"Rate limit exceeded for {client_id}")
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later."
        )

    # Prepare user location
    user_location = None
    if user_lat is not None and user_lon is not None:
        user_location = {
            "latitude": user_lat,
            "longitude": user_lon,
        }

    # Get conversation history for this session
    history = None
    if session_id:
        history = memory_store.get_history(session_id)

    async def event_generator():
        """Generate SSE events for streaming response."""
        nonlocal session_id
        current_session_id = session_id
        full_assistant_response = ""

        try:
            # Stream workflow execution
            async for event in stream_workflow_execution(
                query=query,
                user_location=user_location,
                session_id=session_id,
                conversation_history=history
            ):
                # Collect tokens for memory storage
                if event.get("event") == "token":
                    try:
                        data = json.loads(event.get("data", "{}"))
                        full_assistant_response += data.get("content", "")
                    except json.JSONDecodeError:
                        pass

                # Update session ID from response
                if event.get("event") == "done":
                    try:
                        data = json.loads(event.get("data", "{}"))
                        current_session_id = data.get("session_id", current_session_id)
                    except json.JSONDecodeError:
                        pass

                yield event

            # Store session in LangChain memory for continuity
            if current_session_id:
                memory_store.add_message(current_session_id, "user", query)
                if full_assistant_response:
                    memory_store.add_message(current_session_id, "assistant", full_assistant_response)

        except HTTPException as e:
            raise  # Re-raise HTTP exceptions
        except Exception as e:
            logger.error(f"Streaming error: {type(e).__name__}: {e}", exc_info=True)
            yield {
                "event": "error",
                "data": json.dumps({
                    "error": "An error occurred processing your request",
                    "detail": str(e) if settings.debug else None
                }, ensure_ascii=False)
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
        "description": "AI-powered restaurant recommendation system",
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
