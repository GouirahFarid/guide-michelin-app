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

    # Embedding Model
    embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"

    # RAG Settings
    chunk_size: int = 500
    chunk_overlap: int = 50
    top_k_retrieval: int = 5

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore"
    }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
