"""
Database module for PostgreSQL with pgvector support.
Handles connection pooling and table creation.
"""
import asyncio
import logging
from typing import AsyncGenerator
from contextlib import asynccontextmanager

import psycopg
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool
from sqlalchemy import create_engine, Column, Integer, String, Float, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# SQLAlchemy setup for migrations/ORM
# Keep +psycopg for SQLAlchemy to use psycopg3 instead of psycopg2
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Restaurant(Base):
    """Restaurant ORM model."""
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String)
    location = Column(String)
    price = Column(String)
    cuisine = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
    phone_number = Column(String)
    url = Column(String)
    website_url = Column(String)
    award = Column(String)
    green_star = Column(Boolean, default=False)
    facilities_and_services = Column(Text)
    description = Column(Text, nullable=True)


# Async connection pool
_pool: AsyncConnectionPool | None = None


async def get_pool() -> AsyncConnectionPool:
    """Get or create the async connection pool."""
    global _pool
    if _pool is None:
        _pool = AsyncConnectionPool(
            conninfo=settings.database_url.replace("postgresql+psycopg://", "postgres://"),
            min_size=2,
            max_size=10,
            open=True,
        )
    return _pool


async def close_pool() -> None:
    """Close the connection pool."""
    global _pool
    if _pool:
        await _pool.close()
        _pool = None


@asynccontextmanager
async def get_connection() -> AsyncGenerator:
    """Get a database connection from the pool."""
    pool = await get_pool()
    async with pool.connection() as conn:
        yield conn


async def init_database() -> None:
    """Initialize database tables and enable pgvector."""
    try:
        async with get_connection() as conn:
            # Enable pgvector extension
            await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")

            # Create restaurants table
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS restaurants (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT,
                    location TEXT,
                    price TEXT,
                    cuisine TEXT,
                    longitude FLOAT,
                    latitude FLOAT,
                    phone_number TEXT,
                    url TEXT,
                    website_url TEXT,
                    award TEXT,
                    green_star BOOLEAN DEFAULT FALSE,
                    facilities_and_services TEXT,
                    description TEXT
                )
            """)

            # Create embeddings table with pgvector
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS restaurant_embeddings (
                    id SERIAL PRIMARY KEY,
                    restaurant_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE,
                    chunk_text TEXT NOT NULL,
                    embedding vector(384),
                    metadata JSONB,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Create indexes for faster retrieval
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_restaurants_location
                ON restaurants(location)
            """)

            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_restaurants_award
                ON restaurants(award)
            """)

            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_restaurants_cuisine
                ON restaurants(cuisine)
            """)

            # Create HNSW index for vector similarity search
            # Note: HNSW is preferred for better query performance
            await conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_embeddings_hnsw
                ON restaurant_embeddings USING hnsw (embedding vector_cosine_ops)
                WITH (m = 16, ef_construction = 64)
            """)

            await conn.commit()
            logger.info("Database initialized successfully!")
            print("Database initialized successfully!")

    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


async def insert_restaurant(restaurant_data: dict) -> int:
    """Insert a restaurant and return its ID."""
    async with get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                INSERT INTO restaurants (
                    name, address, location, price, cuisine, longitude, latitude,
                    phone_number, url, website_url, award, green_star,
                    facilities_and_services, description
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """, (
                restaurant_data.get("name"),
                restaurant_data.get("address"),
                restaurant_data.get("location"),
                restaurant_data.get("price"),
                restaurant_data.get("cuisine"),
                restaurant_data.get("longitude"),
                restaurant_data.get("latitude"),
                restaurant_data.get("phone_number"),
                restaurant_data.get("url"),
                restaurant_data.get("website_url"),
                restaurant_data.get("award"),
                restaurant_data.get("green_star", False),
                restaurant_data.get("facilities_and_services"),
                restaurant_data.get("description"),
            ))
            result = await cur.fetchone()
            await conn.commit()
            return result[0] if result else None


async def batch_insert_restaurants(restaurants: list[dict], batch_size: int = 100) -> list[int]:
    """Insert multiple restaurants in batches for better performance.

    Args:
        restaurants: List of restaurant dictionaries
        batch_size: Number of restaurants per batch

    Returns:
        List of inserted restaurant IDs in order
    """
    if not restaurants:
        return []

    inserted_ids = []

    async with get_connection() as conn:
        async with conn.cursor() as cur:
            for i in range(0, len(restaurants), batch_size):
                batch = restaurants[i:i + batch_size]

                # Build multi-value INSERT
                values_template = "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values_clauses = ", ".join([values_template] * len(batch))

                query = f"""
                    INSERT INTO restaurants (
                        name, address, location, price, cuisine, longitude, latitude,
                        phone_number, url, website_url, award, green_star,
                        facilities_and_services, description
                    ) VALUES {values_clauses}
                    RETURNING id
                """

                # Flatten params
                params = []
                for r in batch:
                    params.extend([
                        r.get("name"), r.get("address"), r.get("location"),
                        r.get("price"), r.get("cuisine"),
                        r.get("longitude"), r.get("latitude"),
                        r.get("phone_number"), r.get("url"), r.get("website_url"),
                        r.get("award"), r.get("green_star", False),
                        r.get("facilities_and_services"), r.get("description"),
                    ])

                await cur.execute(query, params)
                batch_ids = await cur.fetchall()
                inserted_ids.extend([row[0] for row in batch_ids])
                await conn.commit()

    return inserted_ids


async def insert_embedding(restaurant_id: int, chunk_text: str, embedding: list, metadata: dict = None) -> None:
    """Insert an embedding for a restaurant chunk."""
    async with get_connection() as conn:
        async with conn.cursor() as cur:
            # Convert list to vector string format
            vector_str = f"[{','.join(map(str, embedding))}]"
            await cur.execute("""
                INSERT INTO restaurant_embeddings (restaurant_id, chunk_text, embedding, metadata)
                VALUES (%s, %s, %s::vector, %s)
            """, (restaurant_id, chunk_text, vector_str, metadata))
            await conn.commit()


async def batch_insert_embeddings(embeddings_data: list[tuple], batch_size: int = 500) -> None:
    """Insert multiple embeddings in batches for better performance.

    Args:
        embeddings_data: List of (restaurant_id, chunk_text, embedding_vector, metadata) tuples
        batch_size: Number of embeddings per batch
    """
    if not embeddings_data:
        return

    async with get_connection() as conn:
        async with conn.cursor() as cur:
            for i in range(0, len(embeddings_data), batch_size):
                batch = embeddings_data[i:i + batch_size]

                # Build multi-value INSERT
                values_template = "(%s, %s, %s::vector, %s)"
                values_clauses = ", ".join([values_template] * len(batch))

                query = f"""
                    INSERT INTO restaurant_embeddings (restaurant_id, chunk_text, embedding, metadata)
                    VALUES {values_clauses}
                """

                # Prepare params with vector strings
                params = []
                for restaurant_id, chunk_text, embedding, metadata in batch:
                    vector_str = f"[{','.join(map(str, embedding))}]"
                    params.extend([restaurant_id, chunk_text, vector_str, metadata])

                await cur.execute(query, params)
                await conn.commit()


async def search_similar(query_embedding: list, top_k: int = 5) -> list:
    """Search for similar restaurant chunks using cosine similarity."""
    async with get_connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            vector_str = f"[{','.join(map(str, query_embedding))}]"
            await cur.execute("""
                SELECT
                    re.id,
                    re.restaurant_id,
                    re.chunk_text,
                    re.metadata,
                    r.name,
                    r.location,
                    r.cuisine,
                    r.award,
                    r.price,
                    r.description,
                    1 - (re.embedding <=> %s::vector) as similarity
                FROM restaurant_embeddings re
                JOIN restaurants r ON re.restaurant_id = r.id
                ORDER BY re.embedding <=> %s::vector
                LIMIT %s
            """, (vector_str, vector_str, top_k))
            results = await cur.fetchall()
            return results


async def get_restaurant_by_id(restaurant_id: int) -> dict | None:
    """Get a restaurant by ID."""
    async with get_connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            await cur.execute("SELECT * FROM restaurants WHERE id = %s", (restaurant_id,))
            result = await cur.fetchone()
            return result


async def search_restaurants(filters: dict) -> list:
    """Search restaurants with filters."""
    async with get_connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            query = "SELECT * FROM restaurants WHERE 1=1"
            params = []

            if filters.get("location"):
                query += " AND location ILIKE %s"
                params.append(f"%{filters['location']}%")

            if filters.get("cuisine"):
                query += " AND cuisine ILIKE %s"
                params.append(f"%{filters['cuisine']}%")

            if filters.get("award"):
                query += " AND award = %s"
                params.append(filters['award'])

            if filters.get("price"):
                query += " AND price = %s"
                params.append(filters['price'])

            if filters.get("min_rating"):
                # Parse award for rating
                query += " AND award IN (%s, %s, %s)"
                params.extend(["3 Stars", "2 Stars", "1 Star"])

            await cur.execute(query, params)
            results = await cur.fetchall()
            return results


# ============================================================================
# GEOLOCATION FUNCTIONS
# ============================================================================

async def search_restaurants_nearby(
    latitude: float,
    longitude: float,
    radius_km: float = 50,
    filters: dict = None,
    limit: int = 50
) -> list:
    """Search for restaurants within a radius of a point.

    Args:
        latitude: Center point latitude
        longitude: Center point longitude
        radius_km: Search radius in kilometers
        filters: Optional filters (award, cuisine, price, etc.)
        limit: Maximum number of results

    Returns:
        List of restaurants with distance_km field, sorted by distance
    """
    from geolocation import calculate_bounding_box, haversine_distance_km

    # Calculate bounding box for efficient filtering
    bbox = calculate_bounding_box(latitude, longitude, radius_km)

    async with get_connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            # Base query with bounding box filter
            query = """
                SELECT *,
                       latitude AS lat,
                       longitude AS lon
                FROM restaurants
                WHERE latitude IS NOT NULL
                  AND longitude IS NOT NULL
                  AND latitude BETWEEN %s AND %s
                  AND longitude BETWEEN %s AND %s
            """
            params = [bbox.south, bbox.north, bbox.west, bbox.east]

            # Add additional filters
            filter_index = 5
            if filters:
                if filters.get("award"):
                    query += " AND award = %s"
                    params.append(filters['award'])
                    filter_index += 1

                if filters.get("cuisine"):
                    query += " AND cuisine ILIKE %s"
                    params.append(f"%{filters['cuisine']}%")
                    filter_index += 1

                if filters.get("price"):
                    query += " AND price = %s"
                    params.append(filters['price'])
                    filter_index += 1

                if filters.get("green_star_only"):
                    query += " AND green_star = TRUE"
                    filter_index += 1

            # Add limit
            query += " LIMIT %s"
            params.append(limit * 2)  # Get more candidates, will filter by exact distance

            await cur.execute(query, params)
            results = await cur.fetchall()

    # Calculate exact distances and filter by radius
    restaurants_with_distance = []
    for r in results:
        if r.get('latitude') and r.get('longitude'):
            distance = haversine_distance_km(
                latitude, longitude,
                r['latitude'], r['longitude']
            )
            r['distance_km'] = distance
            if distance <= radius_km:
                restaurants_with_distance.append(r)

    # Sort by distance and limit
    restaurants_with_distance.sort(key=lambda x: x['distance_km'])
    return restaurants_with_distance[:limit]


async def get_restaurant_coordinates(restaurant_id: int) -> tuple | None:
    """Get restaurant coordinates.

    Returns:
        Tuple of (latitude, longitude) or None
    """
    async with get_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute(
                "SELECT latitude, longitude FROM restaurants WHERE id = %s",
                (restaurant_id,)
            )
            result = await cur.fetchone()
            return result if result and result[0] is not None else None


async def search_in_bounding_box(
    north: float,
    south: float,
    east: float,
    west: float,
    filters: dict = None
) -> list:
    """Search for restaurants within a bounding box.

    Args:
        north: Northern boundary
        south: Southern boundary
        east: Eastern boundary
        west: Western boundary
        filters: Optional filters

    Returns:
        List of restaurants in the bounding box
    """
    async with get_connection() as conn:
        async with conn.cursor(row_factory=dict_row) as cur:
            query = """
                SELECT * FROM restaurants
                WHERE latitude IS NOT NULL
                  AND longitude IS NOT NULL
                  AND latitude BETWEEN %s AND %s
                  AND longitude BETWEEN %s AND %s
            """
            params = [south, north, west, east]

            if filters:
                if filters.get("award"):
                    query += " AND award = %s"
                    params.append(filters['award'])

                if filters.get("cuisine"):
                    query += " AND cuisine ILIKE %s"
                    params.append(f"%{filters['cuisine']}%")

            await cur.execute(query, params)
            return await cur.fetchall()


async def get_nearby_cities(latitude: float, longitude: float, radius_km: float = 100) -> list:
    """Get cities near a location (for context).

    Returns list of city names within radius.
    """
    from geolocation import CITY_COORDINATES, haversine_distance_km

    nearby = []
    for city, (city_lat, city_lon) in CITY_COORDINATES.items():
        distance = haversine_distance_km(latitude, longitude, city_lat, city_lon)
        if distance <= radius_km:
            nearby.append((city.title(), distance))

    nearby.sort(key=lambda x: x[1])
    return nearby[:10]
