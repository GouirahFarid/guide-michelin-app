"""
FastAPI application for Michelin restaurant RAG system.

Provides REST API endpoints for restaurant queries and recommendations.
"""
import asyncio
import logging
import time
import uuid
from contextlib import asynccontextmanager
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Query, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config import get_settings
from database import (
    init_database,
    close_pool,
    search_restaurants,
    search_restaurants_nearby,
    get_restaurant_by_id,
)
from agent import RestaurantAgent, get_restaurant_recommendations
from ingest import ingest_data, IngestConfig, verify_ingestion
from models import (
    ChatRequest,
    ChatResponse,
    ChatMessage,
    RestaurantResponse,
    RestaurantSearchRequest,
    RestaurantListResponse,
    GeoSearchRequest,
    NearbyRestaurantsResponse,
    UserLocation,
    IngestRequest,
    IngestResponse,
    HealthResponse,
    ErrorResponse,
    QueryAnalysis,
    RestaurantSource,
    GeoResults,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Store for conversation sessions with TTL
sessions: Dict[str, List[ChatMessage]] = {}
SESSION_TIMEOUT = 3600  # 1 hour
session_timestamps: Dict[str, float] = {}
agent: Optional[RestaurantAgent] = None


# ============================================================================
# SESSION CLEANUP
# ============================================================================

async def cleanup_expired_sessions():
    """Remove sessions that have exceeded timeout."""
    current_time = time.time()
    expired = [
        session_id for session_id, timestamp in session_timestamps.items()
        if current_time - timestamp > SESSION_TIMEOUT
    ]
    for session_id in expired:
        del sessions[session_id]
        del session_timestamps[session_id]
    if expired:
        logger.info(f"Cleaned up {len(expired)} expired sessions")


# ============================================================================
# LIFESPAN MANAGEMENT
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    global agent

    # Startup
    print("🍽️  Starting MichelinBot API...")
    print(f"📊 Database: {settings.database_url}")
    print(f"🤖 Embedding Model: {settings.embedding_model}")

    try:
        await init_database()
        print("✅ Database initialized")
    except Exception as e:
        print(f"⚠️  Database initialization warning: {e}")

    # Initialize agent
    agent = RestaurantAgent()
    print("✅ Agent initialized")

    # Track start time
    app.state.start_time = time.time()

    yield

    # Shutdown
    print("👋 Shutting down...")
    await close_pool()
    print("✅ Connections closed")


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
        content=ErrorResponse(error=exc.detail, timestamp=None).dict()
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions - log details but don't expose to client."""
    logger.error(f"Unhandled exception: {type(exc).__name__}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail="An unexpected error occurred. Please try again later.",
            timestamp=None
        ).dict()
    )


# ============================================================================
# HEALTH CHECK
# ============================================================================

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint with actual database verification."""
    uptime = time.time() - app.state.start_time

    # Check database connection
    db_connected = False
    try:
        from database import get_pool
        pool = await get_pool()
        async with pool.connection() as conn:
            await conn.execute("SELECT 1")
        db_connected = True
    except Exception as e:
        logger.error(f"Database health check failed: {e}")

    # Check embedding model
    embedding_loaded = False
    try:
        from embeddings import create_embeddings
        embeddings = create_embeddings()
        # Trigger lazy load
        _ = embeddings._load_model()
        embedding_loaded = True
    except Exception as e:
        logger.error(f"Embedding model health check failed: {e}")

    return HealthResponse(
        status="healthy",
        version="1.0.0",
        database_connected=db_connected,
        embedding_model_loaded=embedding_loaded,
        llm_configured=bool(settings.zhipuai_api_key),
        uptime_seconds=uptime,
    )


# ============================================================================
# CHAT ENDPOINT
# ============================================================================

@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    """Main chat endpoint for restaurant recommendations.

    This is the primary endpoint for querying the RAG system.
    It supports natural language queries about Michelin restaurants.

    Examples:
        - "3-star restaurants in Munich"
        - "Japanese fine dining with great views"
        - "Romantic restaurants under €€€€"
    """
    global agent, sessions

    # Generate or retrieve session
    session_id = request.session_id or str(uuid.uuid4())

    # Store message in session
    if session_id not in sessions:
        sessions[session_id] = []
    sessions[session_id].append(
        ChatMessage(role="user", content=request.query)
    )
    # Update session timestamp
    session_timestamps[session_id] = time.time()

    # Periodically cleanup expired sessions
    await cleanup_expired_sessions()

    try:
        # Prepare user location
        user_location = None
        if request.user_location:
            user_location = {
                "latitude": request.user_location.latitude,
                "longitude": request.user_location.longitude,
            }

        # Prepare filters
        filters = request.filters.dict() if request.filters else {}

        # Get recommendations from agent
        result = await agent.chat(
            query=request.query,
            user_location=user_location,
        )

        # Store assistant response
        sessions[session_id].append(
            ChatMessage(role="assistant", content=result["response"])
        )

        # Build response
        sources = []
        for src in result.get("sources", []):
            sources.append(RestaurantSource(
                restaurant_id=src.get("id"),
                name=src.get("name"),
                location=src.get("location"),
                award=src.get("award"),
                cuisine=src.get("cuisine"),
                relevance_score=src.get("similarity") or src.get("relevance_score"),
            ))

        # Build query analysis
        analysis_data = result.get("analysis", {})
        query_analysis = QueryAnalysis(
            original_query=request.query,
            has_location=analysis_data.get("has_location", False),
            location_mentioned=analysis_data.get("location_mentioned"),
            has_cuisine=analysis_data.get("has_cuisine", False),
            cuisine_mentioned=analysis_data.get("cuisine_mentioned"),
            has_award=analysis_data.get("has_award", False),
            award_mentioned=analysis_data.get("award_mentioned"),
            has_price=analysis_data.get("has_price", False),
            price_mentioned=analysis_data.get("price_mentioned"),
            is_geo_query=analysis_data.get("is_geo_query", False),
            distance_constraint=analysis_data.get("distance_constraint"),
            needs_user_location=analysis_data.get("needs_user_location", False),
        )

        # Build geo results if applicable
        geo_results = None
        if result.get("geo_info"):
            geo_info = result["geo_info"]
            geo_results = GeoResults(
                center=UserLocation(
                    latitude=geo_info.get("latitude", 0),
                    longitude=geo_info.get("longitude", 0),
                ),
                radius_km=geo_info.get("distance_constraint", 50),
                restaurants_found=len(result.get("sources", [])),
            )

        return ChatResponse(
            response=result["response"],
            sources=sources,
            query_analysis=query_analysis,
            geo_results=geo_results,
            session_id=session_id,
        )

    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        logger.error(f"Chat endpoint error: {type(e).__name__}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail="An error occurred processing your request. Please try again."
        )


# ============================================================================
# RESTAURANT SEARCH ENDPOINTS
# ============================================================================

@app.get("/restaurants", response_model=RestaurantListResponse, tags=["Restaurants"])
async def search_restaurants_endpoint(
    query: Optional[str] = Query(None, description="Search query"),
    location: Optional[str] = Query(None, description="Filter by location"),
    cuisine: Optional[str] = Query(None, description="Filter by cuisine"),
    award: Optional[str] = Query(None, description="Filter by award level"),
    price: Optional[str] = Query(None, description="Filter by price range"),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    """Search restaurants with filters."""
    filters = {}
    if location:
        filters["location"] = location
    if cuisine:
        filters["cuisine"] = cuisine
    if award:
        filters["award"] = award
    if price:
        filters["price"] = price

    results = await search_restaurants(filters)

    # Apply pagination
    total = len(results)
    paginated = results[offset:offset + limit]

    return RestaurantListResponse(
        count=len(paginated),
        total=total,
        limit=limit,
        offset=offset,
        results=[RestaurantResponse(**r) for r in paginated],
    )


@app.get("/restaurants/{restaurant_id}", response_model=RestaurantResponse, tags=["Restaurants"])
async def get_restaurant(restaurant_id: int):
    """Get a specific restaurant by ID."""
    restaurant = await get_restaurant_by_id(restaurant_id)

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    return RestaurantResponse(**restaurant)


# ============================================================================
# GEOLOCATION ENDPOINTS
# ============================================================================

@app.post("/restaurants/near", response_model=NearbyRestaurantsResponse, tags=["Restaurants"])
async def find_nearby_restaurants(request: GeoSearchRequest):
    """Find restaurants near a location.

    Uses the Haversine formula to calculate distances.
    """
    # Build filters
    filters = request.filters.dict() if request.filters else {}

    # Search nearby
    results = await search_restaurants_nearby(
        latitude=request.latitude,
        longitude=request.longitude,
        radius_km=request.radius_km,
        filters=filters,
        limit=request.max_results,
    )

    return NearbyRestaurantsResponse(
        location=UserLocation(
            latitude=request.latitude,
            longitude=request.longitude,
        ),
        radius_km=request.radius_km,
        count=len(results),
        results=[RestaurantResponse(**r) for r in results],
    )


# ============================================================================
# INGESTION ENDPOINTS
# ============================================================================

@app.post("/ingest", response_model=IngestResponse, tags=["Admin"])
async def trigger_ingestion(
    background_tasks: BackgroundTasks,
    request: IngestRequest = None,
):
    """Trigger data ingestion from CSV file.

    This is an admin endpoint for loading data into the database.
    """
    if request is None:
        request = IngestRequest()

    config = IngestConfig(
        csv_path=request.file_path or "michelin_my_maps.csv",
        chunk_size=request.chunk_size,
        chunk_overlap=request.chunk_overlap,
        skip_existing=request.skip_existing,
        create_embeddings=True,
    )

    # Run ingestion in background
    async def run_ingestion():
        return await ingest_data(config)

    # For simplicity, run synchronously (in production, use background tasks)
    result = await run_ingestion()

    return IngestResponse(
        status=result["status"],
        message=result["message"],
        restaurants_processed=result["restaurants_processed"],
        restaurants_added=result["restaurants_added"],
        restaurants_skipped=result.get("restaurants_skipped", 0),
        embeddings_created=result["embeddings_created"],
        errors=result.get("errors", []),
        duration_seconds=result["duration_seconds"],
    )


@app.get("/ingest/verify", tags=["Admin"])
async def verify_data():
    """Verify that data was ingested correctly."""
    verification = await verify_ingestion()
    return {
        "restaurant_count": verification["restaurant_count"],
        "embedding_count": verification["embedding_count"],
        "award_distribution": verification["award_distribution"],
        "top_locations": verification["top_locations"],
    }


# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

@app.delete("/sessions/{session_id}", tags=["Chat"])
async def clear_session(session_id: str):
    """Clear a chat session."""
    if session_id in sessions:
        del sessions[session_id]
        return {"message": "Session cleared"}
    raise HTTPException(status_code=404, detail="Session not found")


@app.get("/sessions/{session_id}", tags=["Chat"])
async def get_session(session_id: str):
    """Get session history."""
    if session_id in sessions:
        return {"session_id": session_id, "messages": sessions[session_id]}
    raise HTTPException(status_code=404, detail="Session not found")


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
            "chat": "/chat",
            "restaurants": "/restaurants",
            "restaurants_nearby": "/restaurants/near",
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
