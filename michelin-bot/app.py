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

from fastapi import FastAPI, HTTPException, Query, Depends
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
# SESSION STORAGE WITH CLEANUP
# ============================================================================

from threading import Thread
import asyncio

class SessionStore:
    """Thread-safe session storage with automatic cleanup."""

    def __init__(self, timeout_seconds: int = 3600):
        self.sessions: Dict[str, list] = {}
        self.timestamps: Dict[str, float] = {}
        self.timeout = timeout_seconds
        self._cleanup_task: Optional[Thread] = None

    def get(self, session_id: str) -> Optional[list]:
        """Get session data, updating timestamp."""
        if session_id in self.sessions:
            self.timestamps[session_id] = time.time()
            return self.sessions[session_id]
        return None

    def set(self, session_id: str, data: list) -> None:
        """Set session data with current timestamp."""
        self.sessions[session_id] = data
        self.timestamps[session_id] = time.time()

    def cleanup_expired(self) -> int:
        """Remove expired sessions. Returns count of removed sessions."""
        now = time.time()
        expired = [
            sid for sid, timestamp in self.timestamps.items()
            if now - timestamp > self.timeout
        ]
        for sid in expired:
            del self.sessions[sid]
            del self.timestamps[sid]
        return len(expired)

    def start_cleanup_task(self) -> None:
        """Start background cleanup task."""
        if self._cleanup_task is None:
            self._cleanup_task = Thread(target=self._cleanup_loop, daemon=True)
            self._cleanup_task.start()

    def _cleanup_loop(self) -> None:
        """Run cleanup every 5 minutes."""
        import logging
        logger = logging.getLogger(__name__)
        while True:
            time.sleep(300)  # 5 minutes
            removed = self.cleanup_expired()
            if removed > 0:
                logger.info(f"Cleaned up {removed} expired sessions")

session_store = SessionStore(timeout_seconds=3600)
session_store.start_cleanup_task()


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
    description="RAG-powered restaurant recommendation system using Michelin Guide data",
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

    # Check database if RAG is enabled
    database_connected = False
    embedding_model_loaded = False
    if settings.enable_rag:
        try:
            from database import get_pool
            pool = await get_pool()
            database_connected = pool is not None
            embedding_model_loaded = True  # Assume loaded if DB is connected
        except Exception as e:
            logger.warning(f"Database health check failed: {e}")

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        database_connected=database_connected if settings.enable_rag else None,
        embedding_model_loaded=embedding_model_loaded if settings.enable_rag else None,
        llm_configured=bool(settings.zhipuai_api_key),
        uptime_seconds=uptime,
    )


# ============================================================================
# STREAMING CHAT ENDPOINT (ENHANCED WITH LANGGRAPH)
# ============================================================================

def get_client_identifier(request) -> str:
    """Get client identifier for rate limiting."""
    # Try to get from session first
    session_id = request.state.get("session_id")
    if session_id:
        return f"session:{session_id}"

    # Fall back to IP
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return f"ip:{forwarded.split(',')[0].strip()}"
    return f"ip:{request.client.host}"


@app.get("/chat/stream", tags=["Chat"])
async def chat_stream(
    request,
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
        history = session_store.get(session_id)

    async def event_generator():
        """Generate SSE events for streaming response."""
        nonlocal session_id
        current_session_id = session_id

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
                        current_session_id = data.get("session_id", current_session_id)
                    except json.JSONDecodeError:
                        pass

                yield event

            # Store session for continuity
            if current_session_id:
                # Initialize or update session
                existing_history = session_store.get(current_session_id) or []
                existing_history.append({"role": "user", "content": query})
                existing_history.append({"role": "assistant", "content": ""})  # Will be updated
                session_store.set(current_session_id, existing_history[-20:])  # Keep last 20 messages

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
