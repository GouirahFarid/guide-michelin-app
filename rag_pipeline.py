"""
RAG Pipeline for restaurant recommendations.

Combines retrieval from PostgreSQL/pgvector with GLM-4 generation.
"""
import asyncio
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from config import get_settings
from database import (
    search_similar,
    search_restaurants,
    search_restaurants_nearby,
    get_restaurant_by_id
)
from embeddings import create_embeddings, get_embedding_dimension
from llm import create_glm4_for_rag, simple_chat
from geolocation import extract_location_from_query, extract_distance_from_query
from prompts import (
    create_rag_prompt,
    create_simple_rag_prompt,
    format_context,
    analyze_query,
    MICHELIN_GUIDE_SYSTEM_PROMPT
)

settings = get_settings()


# ============================================================================
# RAG PIPELINE CONFIGURATION
# ============================================================================

@dataclass
class RAGConfig:
    """Configuration for RAG pipeline."""
    top_k: int = 5
    chunk_size: int = 500
    chunk_overlap: int = 50
    min_similarity: float = 0.5
    use_geo: bool = True


# ============================================================================
# DOCUMENT CREATION
# ============================================================================

def restaurant_to_document(restaurant: Dict[str, Any]) -> Document:
    """Convert a restaurant dictionary to a LangChain Document.

    Args:
        restaurant: Restaurant data from database

    Returns:
        LangChain Document with metadata
    """
    # Create page content from description and key info
    content_parts = []
    if restaurant.get('description'):
        content_parts.append(restaurant['description'])
    if restaurant.get('cuisine'):
        content_parts.append(f"Cuisine: {restaurant['cuisine']}")
    if restaurant.get('award'):
        content_parts.append(f"Award: {restaurant['award']}")

    page_content = " | ".join(content_parts)

    # Create metadata
    metadata = {
        'id': restaurant.get('id'),
        'name': restaurant.get('name'),
        'location': restaurant.get('location'),
        'cuisine': restaurant.get('cuisine'),
        'award': restaurant.get('award'),
        'price': restaurant.get('price'),
        'address': restaurant.get('address'),
        'phone': restaurant.get('phone_number'),
        'url': restaurant.get('url'),
        'green_star': restaurant.get('green_star', False),
        'facilities': restaurant.get('facilities_and_services'),
        'longitude': restaurant.get('longitude'),
        'latitude': restaurant.get('latitude'),
    }

    return Document(page_content=page_content, metadata=metadata)


async def create_documents_from_results(
    results: List[Dict[str, Any]]
) -> List[Document]:
    """Convert database results to LangChain Documents.

    Args:
        results: List of restaurant dictionaries

    Returns:
        List of LangChain Documents
    """
    return [restaurant_to_document(r) for r in results]


# ============================================================================
# QUERY EMBEDDING
# ============================================================================

async def embed_query(query: str) -> List[float]:
    """Embed a query for vector search.

    Args:
        query: Query text

    Returns:
        Embedding vector
    """
    embeddings = create_embeddings()
    return embeddings.embed_query(query)


async def expand_query(query: str) -> List[str]:
    """Expand a query into multiple search queries.

    Uses simple expansion for now. Can be enhanced with LLM-based expansion.

    Args:
        query: Original query

    Returns:
        List of expanded queries
    """
    queries = [query]

    # Simple expansion based on analysis
    analysis = analyze_query(query)

    # Add location-specific query if location mentioned
    if analysis['has_location'] and analysis['location_mentioned']:
        queries.append(f"{query} {analysis['location_mentioned']}")

    # Add cuisine-specific query
    if analysis['has_cuisine'] and analysis['cuisine_mentioned']:
        queries.append(f"{analysis['cuisine_mentioned']} restaurant {query}")

    # Add award-specific query
    if analysis['has_award'] and analysis['award_mentioned']:
        queries.append(f"{analysis['award_mentioned']} restaurant {query}")

    return list(set(queries))  # Remove duplicates


# ============================================================================
# RETRIEVAL
# ============================================================================

async def retrieve_relevant_documents(
    query: str,
    query_embedding: List[float],
    top_k: int = 5,
    filters: Dict[str, Any] = None
) -> List[Document]:
    """Retrieve relevant restaurant documents.

    Args:
        query: Original query text
        query_embedding: Embedded query vector
        top_k: Number of results to retrieve
        filters: Optional metadata filters

    Returns:
        List of relevant Documents
    """
    # First, try vector search
    vector_results = await search_similar(query_embedding, top_k=top_k * 2)

    # Then, apply metadata filters
    if filters:
        filtered_results = await search_restaurants(filters or {})
        # Combine results, prioritizing vector matches
        seen_ids = {r['restaurant_id'] for r in vector_results}
        for r in filtered_results:
            if r['id'] not in seen_ids:
                vector_results.append({
                    'restaurant_id': r['id'],
                    'chunk_text': r.get('description', ''),
                    'metadata': r,
                    'similarity': 0.5,
                    'name': r['name'],
                    'location': r['location'],
                    'cuisine': r['cuisine'],
                    'award': r['award'],
                    'price': r['price'],
                })

    # Convert to Documents
    documents = []
    for r in vector_results[:top_k]:
        doc = Document(
            page_content=r.get('chunk_text', ''),
            metadata={
                'id': r.get('restaurant_id'),
                'name': r.get('name'),
                'location': r.get('location'),
                'cuisine': r.get('cuisine'),
                'award': r.get('award'),
                'price': r.get('price'),
                'similarity_score': r.get('similarity', 0),
            }
        )
        documents.append(doc)

    return documents


async def retrieve_by_geolocation(
    query: str,
    latitude: float,
    longitude: float,
    radius_km: float = 50,
    filters: Dict[str, Any] = None
) -> List[Document]:
    """Retrieve restaurants by geolocation.

    Args:
        query: Original query text
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Search radius
        filters: Optional additional filters

    Returns:
        List of relevant Documents sorted by distance
    """
    results = await search_restaurants_nearby(
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km,
        filters=filters,
        limit=20
    )

    documents = await create_documents_from_results(results)

    # Sort by distance (already sorted from search_restaurants_nearby)
    return documents


# ============================================================================
# RESPONSE GENERATION
# ============================================================================

async def generate_response(
    query: str,
    context: str,
    use_simple_prompt: bool = False
) -> str:
    """Generate a response using GLM-4.

    Args:
        query: User's query
        context: Retrieved context string
        use_simple_prompt: Whether to use simple prompt

    Returns:
        Generated response
    """
    if use_simple_prompt:
        return simple_chat(
            user_message=f"Context: {context}\n\nQuestion: {query}",
            system_message="You are MICHELIN_GUIDE, an expert restaurant assistant. Answer based only on the provided context."
        )

    # Use full RAG prompt
    return simple_chat(
        user_message=f"## User Question\n{query}\n\n## Retrieved Context\n{context}\n\nProvide a helpful, detailed response.",
        system_message=MICHELIN_GUIDE_SYSTEM_PROMPT
    )


# ============================================================================
# FULL RAG PIPELINE
# ============================================================================

@dataclass
class RAGResult:
    """Result from RAG pipeline."""
    response: str
    sources: List[Dict[str, Any]]
    query_analysis: Dict[str, Any]
    documents_used: int
    geo_results: Optional[Dict[str, Any]] = None


async def rag_pipeline(
    query: str,
    filters: Dict[str, Any] = None,
    user_location: Optional[Dict[str, float]] = None,
    config: RAGConfig = None
) -> RAGResult:
    """Full RAG pipeline for restaurant recommendations.

    Args:
        query: User's query
        filters: Optional search filters
        user_location: Optional user location dict with 'latitude' and 'longitude'
        config: RAG configuration

    Returns:
        RAGResult with response and sources
    """
    config = config or RAGConfig()

    # Analyze query
    query_analysis = analyze_query(query)

    documents = []
    geo_info = None

    # Route to appropriate retrieval
    if user_location and (query_analysis['is_geo_query'] or query_analysis['needs_user_location']):
        # Geolocation-based retrieval
        radius = query_analysis.get('distance_constraint', 50)
        documents = await retrieve_by_geolocation(
            query=query,
            latitude=user_location['latitude'],
            longitude=user_location['longitude'],
            radius_km=radius,
            filters=filters
        )

        geo_info = {
            'center': user_location,
            'radius_km': radius,
            'count': len(documents)
        }

    elif query_analysis['is_geo_query'] and query_analysis.get('location_coords'):
        # Location extracted from query
        lat, lon = query_analysis['location_coords']
        radius = query_analysis.get('distance_constraint', 50)
        documents = await retrieve_by_geolocation(
            query=query,
            latitude=lat,
            longitude=lon,
            radius_km=radius,
            filters=filters
        )

        geo_info = {
            'center': {'latitude': lat, 'longitude': lon},
            'radius_km': radius,
            'count': len(documents)
        }

    else:
        # Standard vector retrieval
        query_emb = await embed_query(query)
        documents = await retrieve_relevant_documents(
            query=query,
            query_embedding=query_emb,
            top_k=config.top_k,
            filters=filters
        )

    # Fallback: if no documents from vector search, try metadata-only search
    if not documents and filters:
        results = await search_restaurants(filters)
        documents = await create_documents_from_results(results[:config.top_k])

    # Format context
    context = format_context(documents) if documents else "No restaurant information found."

    # Generate response
    response = await generate_response(query, context)

    # Extract sources
    sources = []
    for doc in documents[:5]:
        sources.append({
            'restaurant_id': doc.metadata.get('id'),
            'name': doc.metadata.get('name'),
            'location': doc.metadata.get('location'),
            'award': doc.metadata.get('award'),
            'cuisine': doc.metadata.get('cuisine'),
            'relevance_score': doc.metadata.get('similarity_score', 0.0),
            'distance_km': doc.metadata.get('distance_km'),
        })

    return RAGResult(
        response=response,
        sources=sources,
        query_analysis=query_analysis,
        documents_used=len(documents),
        geo_results=geo_info
    )


# ============================================================================
# SIMPLIFIED PIPELINES
# ============================================================================

async def simple_rag(query: str) -> str:
    """Simple RAG pipeline with default settings.

    Args:
        query: User's query

    Returns:
        Generated response
    """
    result = await rag_pipeline(query)
    return result.response


async def chat_with_restaurants(
    query: str,
    conversation_history: List[Dict[str, str]] = None
) -> str:
    """Chat with context from conversation history.

    Args:
        query: Current user query
        conversation_history: List of previous messages

    Returns:
        Generated response
    """
    # Build context from history
    history_context = ""
    if conversation_history:
        recent = conversation_history[-3:]
        history_context = "\n".join([
            f"{msg['role']}: {msg['content']}" for msg in recent
        ])
        history_context = f"\n## Previous Conversation\n{history_context}\n"

    result = await rag_pipeline(query)

    return result.response


# ============================================================================
# HYBRID SEARCH (Vector + Metadata)
# ============================================================================

async def hybrid_search(
    query: str,
    filters: Dict[str, Any] = None,
    top_k: int = 5
) -> List[Document]:
    """Hybrid search combining vector and metadata search.

    Args:
        query: Search query
        filters: Metadata filters
        top_k: Number of results

    Returns:
        Combined and reranked results
    """
    # Vector search
    query_emb = await embed_query(query)
    vector_docs = await retrieve_relevant_documents(query, query_emb, top_k * 2)

    # Metadata search
    metadata_results = await search_restaurants(filters or {})
    metadata_docs = await create_documents_from_results(metadata_results[:top_k * 2])

    # Combine and deduplicate
    seen_ids = set()
    combined = []

    for doc in vector_docs + metadata_docs:
        doc_id = doc.metadata.get('id')
        if doc_id and doc_id not in seen_ids:
            seen_ids.add(doc_id)
            combined.append(doc)

    return combined[:top_k]


# ============================================================================
# QUERY ANALYSIS & ROUTING
# ============================================================================

async def should_use_geolocation(query: str) -> bool:
    """Determine if query should use geolocation."""
    analysis = analyze_query(query)
    return analysis['is_geo_query']


async def should_use_filters(query: str) -> Dict[str, Any]:
    """Extract filters from query."""
    analysis = analyze_query(query)

    filters = {}
    if analysis['has_location'] and analysis['location_mentioned']:
        filters['location'] = analysis['location_mentioned']
    if analysis['has_cuisine'] and analysis['cuisine_mentioned']:
        filters['cuisine'] = analysis['cuisine_mentioned']
    if analysis['has_award'] and analysis['award_mentioned']:
        filters['award'] = analysis['award_mentioned']
    if analysis['has_price'] and analysis['price_mentioned']:
        filters['price'] = analysis['price_mentioned']

    return filters


# ============================================================================
# BATCH PROCESSING
# ============================================================================

async def batch_embed_queries(queries: List[str]) -> List[List[float]]:
    """Embed multiple queries efficiently.

    Args:
        queries: List of query strings

    Returns:
        List of embedding vectors
    """
    embeddings = create_embeddings()
    return embeddings.embed_documents(queries)


async def batch_rag(
    queries: List[str],
    filters: Dict[str, Any] = None
) -> List[RAGResult]:
    """Run RAG pipeline on multiple queries.

    Args:
        queries: List of queries
        filters: Shared filters

    Returns:
        List of RAG results
    """
    # Embed all queries at once
    query_embeddings = await batch_embed_queries(queries)

    # Process each query
    results = []
    for query, embedding in zip(queries, query_embeddings):
        documents = await retrieve_relevant_documents(
            query=query,
            query_embedding=embedding,
            top_k=5,
            filters=filters
        )

        context = format_context(documents)
        response = await generate_response(query, context)

        results.append(RAGResult(
            response=response,
            sources=[{
                'restaurant_id': doc.metadata.get('id'),
                'name': doc.metadata.get('name'),
                'location': doc.metadata.get('location'),
            } for doc in documents],
            query_analysis=analyze_query(query),
            documents_used=len(documents)
        ))

    return results
