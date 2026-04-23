from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Zhipu AI
    zhipuai_api_key: str

    # Hugging Face (optional, for gated models)
    hf_token: str = ""

    # Database
    database_url: str

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # API Configuration
    api_base_url: str = "https://api.z.ai/api/coding/paas/v4"
    api_timeout: int = 120

    # LLM Configuration
    llm_model: str = "glm-5.1"
    llm_temperature: float = 0.7
    llm_max_tokens: int = 2000

    # Embedding Model
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # RAG Settings
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_retrieval: int = 5

    # Rate Limiting
    rate_limit_requests_per_minute: int = 60

    # Session
    session_timeout: int = 3600  # 1 hour

    # RAG Mode
    enable_rag: bool = False  # Set to True to enable database/vector search

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
