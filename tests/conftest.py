"""
Pytest configuration and fixtures.
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock


@pytest.fixture
def mock_settings():
    """Mock settings for testing."""
    from config import Settings
    return Settings(
        zhipuai_api_key="test_key",
        database_url="postgresql+psycopg://test:test@localhost:5432/test_db",
        host="localhost",
        port=8000,
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        chunk_size=500,
        chunk_overlap=50,
        top_k_retrieval=5,
    )


@pytest.fixture
def sample_restaurant():
    """Sample restaurant data for testing."""
    return {
        "id": 1,
        "name": "Test Restaurant",
        "location": "Munich, Germany",
        "cuisine": "Modern Cuisine",
        "award": "3 Stars",
        "price": "€€€€",
        "latitude": 48.1351,
        "longitude": 11.5820,
        "description": "A test restaurant with excellent food.",
        "address": "Test Street 1",
        "phone_number": "+49 123 456789",
        "url": "https://example.com",
        "website_url": "https://example.com",
        "green_star": False,
        "facilities_and_services": "Private dining, terrace",
    }


@pytest.fixture
def sample_user_location():
    """Sample user location for testing."""
    return {
        "latitude": 48.1351,
        "longitude": 11.5820,
    }


@pytest.fixture
def mock_llm_response():
    """Mock LLM response."""
    return "Based on your search, I found several excellent restaurants in Munich."


@pytest.fixture
async def mock_db_pool():
    """Mock database connection pool."""
    pool = AsyncMock()
    conn = AsyncMock()
    pool.connection.return_value.__aenter__.return_value = conn
    pool.connection.return_value.__aexit__.return_value = None
    return pool


@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
