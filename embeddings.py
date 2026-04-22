"""
HuggingFace embeddings wrapper for LangChain integration.

Provides efficient embedding generation using sentence-transformers models.
"""
import os
from typing import List, Optional, Dict, Any
import numpy as np

from sentence_transformers import SentenceTransformer
from langchain_core.embeddings import Embeddings
from config import get_settings

settings = get_settings()


# ============================================================================
# SENTENCE TRANSFORMERS EMBEDDINGS
# ============================================================================

class HuggingFaceEmbeddings(Embeddings):
    """HuggingFace SentenceTransformers embeddings for LangChain.

    This class wraps sentence-transformers models for use with LangChain.
    """

    model_name: str
    model: Optional[SentenceTransformer] = None
    cache_folder: Optional[str] = None
    encode_kwargs: Dict[str, Any] = None

    def __init__(
        self,
        model_name: str = None,
        cache_folder: Optional[str] = None,
        encode_kwargs: Optional[Dict[str, Any]] = None,
    ):
        """Initialize HuggingFace embeddings.

        Args:
            model_name: Name of the sentence-transformers model
            cache_folder: Folder to cache downloaded models
            encode_kwargs: Additional kwargs for model.encode()
        """
        self.model_name = model_name or settings.embedding_model
        self.cache_folder = cache_folder
        self.encode_kwargs = encode_kwargs or {
            "normalize_embeddings": True,
            "show_progress_bar": False,
        }
        self.model = None  # Lazy load

    def _load_model(self) -> SentenceTransformer:
        """Lazy load the model."""
        if self.model is None:
            self.model = SentenceTransformer(
                self.model_name,
                cache_folder=self.cache_folder
            )
        return self.model

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """Embed a list of documents.

        Args:
            texts: List of document texts

        Returns:
            List of embedding vectors
        """
        model = self._load_model()
        embeddings = model.encode(
            texts,
            **self.encode_kwargs
        )
        return embeddings.tolist()

    def embed_query(self, text: str) -> List[float]:
        """Embed a query text.

        Args:
            text: Query text

        Returns:
            Embedding vector
        """
        model = self._load_model()
        embedding = model.encode(
            text,
            **self.encode_kwargs
        )
        return embedding.tolist()


# ============================================================================
# SINGLETON CACHE
# ============================================================================

# Global cached embedding instance (singleton pattern)
_cached_embeddings: "HuggingFaceEmbeddings" = None


def get_cached_embeddings() -> "HuggingFaceEmbeddings":
    """Get the cached embedding instance (singleton).

    This ensures the model is loaded only once and reused across all calls.

    Returns:
        Cached HuggingFaceEmbeddings instance
    """
    global _cached_embeddings
    if _cached_embeddings is None:
        _cached_embeddings = create_embeddings()
        # Preload the model to avoid lazy loading on first call
        _cached_embeddings._load_model()
    return _cached_embeddings


# ============================================================================
# FACTORY FUNCTIONS
# ============================================================================

def create_embeddings(
    model_name: str = None,
    normalize: bool = True,
    cache_folder: Optional[str] = None
) -> HuggingFaceEmbeddings:
    """Create HuggingFace embeddings instance.

    Args:
        model_name: Name of the sentence-transformers model
        normalize: Whether to normalize embeddings
        cache_folder: Folder to cache downloaded models

    Returns:
        Configured HuggingFaceEmbeddings instance

    Example:
        >>> embeddings = create_embeddings()
        >>> vector = embeddings.embed_query("Japanese fine dining")
    """
    encode_kwargs = {
        "normalize_embeddings": normalize,
        "show_progress_bar": False,
    }

    return HuggingFaceEmbeddings(
        model_name=model_name or settings.embedding_model,
        cache_folder=cache_folder,
        encode_kwargs=encode_kwargs
    )


def get_embedding_dimension(model_name: str = None) -> int:
    """Get the embedding dimension for a model.

    Args:
        model_name: Name of the model (uses default if not specified)

    Returns:
        Embedding dimension size
    """
    model_name = model_name or settings.embedding_model

    # Known dimensions for common models
    MODEL_DIMENSIONS = {
        "sentence-transformers/all-MiniLM-L6-v2": 384,
        "sentence-transformers/all-mpnet-base-v2": 768,
        "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2": 384,
        "sentence-transformers/all-MiniLM-L12-v2": 384,
        "sentence-transformers/LaBSE": 768,
        "sentence-transformers/distiluse-base-multilingual-cased-v2": 512,
    }

    if model_name in MODEL_DIMENSIONS:
        return MODEL_DIMENSIONS[model_name]

    # Load model to get dimension
    model = SentenceTransformer(model_name)
    return model.get_sentence_embedding_dimension()


# ============================================================================
# BATCH EMBEDDING UTILITIES
# ============================================================================

async def embed_texts_batch(
    texts: List[str],
    model_name: str = None,
    batch_size: int = 32,
    show_progress: bool = True
) -> np.ndarray:
    """Embed a large list of texts in batches.

    Args:
        texts: List of texts to embed
        model_name: Name of the embedding model
        batch_size: Batch size for encoding
        show_progress: Whether to show progress bar

    Returns:
        NumPy array of embeddings
    """
    model_name = model_name or settings.embedding_model
    model = SentenceTransformer(model_name)

    embeddings = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=show_progress,
        normalize_embeddings=True
    )

    return embeddings


def embed_restaurant_data(
    name: str,
    description: str,
    cuisine: str,
    location: str,
    award: str,
    facilities: str = ""
) -> List[float]:
    """Create an embedding for restaurant search.

    Combines multiple fields into a single embedding vector.

    Args:
        name: Restaurant name
        description: Restaurant description
        cuisine: Cuisine type
        location: Location
        award: Award level
        facilities: Facilities and services

    Returns:
        Combined embedding vector
    """
    embeddings = create_embeddings()

    # Create a searchable text from restaurant data
    searchable_text = f"{name} {cuisine} {location} {award} {description} {facilities}"

    return embeddings.embed_query(searchable_text)


# ============================================================================
# SIMILARITY CALCULATIONS
# ============================================================================

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors.

    Args:
        vec1: First vector
        vec2: Second vector

    Returns:
        Similarity score between 0 and 1
    """
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)

    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)

    if norm1 == 0 or norm2 == 0:
        return 0.0

    return dot_product / (norm1 * norm2)


def find_most_similar(
    query_embedding: List[float],
    document_embeddings: List[List[float]],
    top_k: int = 5
) -> List[tuple[int, float]]:
    """Find the most similar documents to a query.

    Args:
        query_embedding: Query embedding vector
        document_embeddings: List of document embedding vectors
        top_k: Number of top results to return

    Returns:
        List of (index, similarity_score) tuples
    """
    similarities = []
    query_vec = np.array(query_embedding)

    for i, doc_emb in enumerate(document_embeddings):
        doc_vec = np.array(doc_emb)
        similarity = cosine_similarity(query_vec, doc_vec)
        similarities.append((i, similarity))

    # Sort by similarity (descending)
    similarities.sort(key=lambda x: x[1], reverse=True)

    return similarities[:top_k]


# ============================================================================
# MODEL RECOMMENDATIONS
# ============================================================================

EMBEDDING_MODELS = {
    "fast-multilingual": {
        "name": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "dimension": 384,
        "description": "Fast, multilingual support, good for general use",
    },
    "fast-english": {
        "name": "sentence-transformers/all-MiniLM-L6-v2",
        "dimension": 384,
        "description": "Fast, English-focused, good for simple queries",
    },
    "quality-english": {
        "name": "sentence-transformers/all-mpnet-base-v2",
        "dimension": 768,
        "description": "Higher quality for English, larger model",
    },
    "labse": {
        "name": "sentence-transformers/LaBSE",
        "dimension": 768,
        "description": "Excellent for multilingual semantic similarity",
    },
}


def get_recommended_model(
    multilingual: bool = True,
    priority: str = "speed"  # "speed" or "quality"
) -> str:
    """Get a recommended embedding model based on requirements.

    Args:
        multilingual: Whether multilingual support is needed
        priority: Whether to prioritize speed or quality

    Returns:
        Model name string
    """
    if multilingual:
        if priority == "speed":
            return EMBEDDING_MODELS["fast-multilingual"]["name"]
        else:
            return EMBEDDING_MODELS["labse"]["name"]
    else:
        if priority == "speed":
            return EMBEDDING_MODELS["fast-english"]["name"]
        else:
            return EMBEDDING_MODELS["quality-english"]["name"]


# ============================================================================
# CHUNK EMBEDDING
# ============================================================================

def embed_chunks(
    chunks: List[str],
    model_name: str = None
) -> List[List[float]]:
    """Embed text chunks for vector storage.

    Args:
        chunks: List of text chunks
        model_name: Optional model name override

    Returns:
        List of embedding vectors
    """
    embeddings = create_embeddings(model_name=model_name)
    return embeddings.embed_documents(chunks)


# ============================================================================
# CACHE MANAGEMENT
# ============================================================================

def clear_model_cache():
    """Clear the model cache to free memory."""
    import gc
    gc.collect()


# ============================================================================
# MODEL DOWNLOAD
# ============================================================================

def ensure_model_downloaded(model_name: str = None) -> str:
    """Ensure the embedding model is downloaded.

    Args:
        model_name: Name of the model

    Returns:
        Path to the downloaded model
    """
    model_name = model_name or settings.embedding_model
    model = SentenceTransformer(model_name)
    return model._model_card_path


def is_model_available(model_name: str = None) -> bool:
    """Check if a model is available (downloaded).

    Args:
        model_name: Name of the model

    Returns:
        True if model is available
    """
    try:
        model_name = model_name or settings.embedding_model
        SentenceTransformer(model_name)
        return True
    except Exception:
        return False
