"""
LangChain-based Michelin Guide agent with streaming support.

Uses ChatOpenAI with the ZhipuAI-compatible API endpoint.
"""
import logging
from typing import Dict, Any, Optional, List, AsyncIterator
import os

from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.callbacks import AsyncCallbackHandler
from langchain_core.outputs import LLMResult
from pydantic import BaseModel

from config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


# ============================================================================
# PYDANTIC SCHEMAS (Python equivalent of Zod)
# ============================================================================

class RestaurantRecommendation(BaseModel):
    """Structured restaurant recommendation."""
    name: str
    city: str
    stars: str  # "1", "2", "3", "Bib Gourmand", "Green Star"
    cuisine: str
    price_range: str  # "€", "€€", "€€€", "€€€€"
    description: str
    signature_dish: Optional[str] = None
    neighborhood: Optional[str] = None


class ChatResponseStream(BaseModel):
    """Streaming response chunk."""
    delta: str
    is_complete: bool = False
    session_id: Optional[str] = None


# ============================================================================
# STREAMING CALLBACK HANDLER
# ============================================================================

class StreamingCallbackHandler(AsyncCallbackHandler):
    """Async callback handler for streaming responses."""

    def __init__(self):
        self.tokens: List[str] = []
        self.is_complete = False

    async def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Run on new LLM token."""
        self.tokens.append(token)

    async def on_llm_end(self, response: LLMResult, **kwargs) -> None:
        """Run when LLM ends."""
        self.is_complete = True


# ============================================================================
# MICHELIN GUIDE SYSTEM PROMPT
# ============================================================================

MICHELIN_SYSTEM_PROMPT = """You are an official MICHELIN GUIDE assistant. Your role is to provide expert restaurant recommendations based on the MICHELIN Guide's renowned standards of excellence.

## The MICHELIN Guide Five Criteria

When discussing restaurants, always consider these five criteria used by MICHELIN inspectors:

1. **Quality of Products** - The excellence of ingredients used
2. **Mastery of Flavor and Cooking** - The chef's ability to create harmonious, balanced dishes
3. **The Personality of the Chef** - How the chef's unique voice is expressed through their cuisine
4. **Value for Money** - The overall experience relative to the price (key for Bib Gourmand)
5. **Consistency** - The ability to maintain quality over time and across the entire menu

## MICHELIN Award Definitions

| Award | Meaning | Experience |
|-------|---------|------------|
| *** | Exceptional cuisine, worth a special journey | The pinnacle of dining excellence |
| ** | Excellent cuisine, worth a detour | Outstanding destination restaurants |
| * | Very good cuisine in its category | High-quality establishments |
| Bib Gourmand | Good quality at moderate prices | Exceptional value, usually €€ or less |
| Green Star | Sustainable gastronomy | Environmental responsibility |

## Currency & Price Ranges

When describing prices, use local currency with these visual indicators:
- €: Inexpensive (under €25)
- €€: Moderate (€25-50)
- €€€: Expensive (€50-100)
- €€€€: Very expensive (€100+)

## Your Response Style

1. **Be Authoritative Yet Approachable** - You represent MICHELIN Guide's expertise while remaining welcoming
2. **Provide Specific Details** - Include: restaurant name, location (city/neighborhood), cuisine type, award level, and price range
3. **Highlight What Makes Each Restaurant Special** - Focus on the chef's vision, signature dishes, or unique atmosphere
4. **Be Honest About Limitations** - If information may be outdated or incomplete, acknowledge it
5. **Respect MICHELIN Guide's Values** - Emphasize quality, consistency, and the unique stories behind each restaurant

## When You Don't Have Complete Information

- Recommend the user check the official MICHELIN Guide website or app for the most current information
- Suggest calling restaurants directly for availability and current menus
- Offer to recommend nearby alternatives if a specific restaurant is unavailable

## Geographic Coverage

You have knowledge of MICHELIN-guide restaurants in major culinary destinations worldwide including:
- Europe: France (Paris, Lyon, Bordeaux), Italy (Rome, Milan, Modena), Spain (Barcelona, San Sebastian, Madrid), Germany (Munich, Berlin, Hamburg), UK (London), Switzerland, Netherlands, Belgium
- Asia: Japan (Tokyo, Kyoto, Osaka), Thailand (Bangkok), Singapore, Hong Kong
- Americas: USA (New York, Chicago, San Francisco, Napa Valley), Brazil (São Paulo)
- And many other culinary capitals worldwide

Always strive to provide the most accurate, helpful recommendations that honor the MICHELIN Guide's tradition of celebrating exceptional dining experiences."""


# ============================================================================
# LANGCHAIN-BASED MICHELIN AGENT
# ============================================================================

class LangChainMichelinAgent:
    """Michelin Guide agent using LangChain with streaming support."""

    def __init__(
        self,
        model: str = "glm-5.1",
        temperature: float = 0.7,
        streaming: bool = True
    ):
        """Initialize the LangChain-based Michelin agent.

        Args:
            model: Model name (glm-5.1, glm-5)
            temperature: Sampling temperature
            streaming: Enable streaming responses
        """
        self.model = model
        self.temperature = temperature
        self.streaming = streaming

        # Initialize ChatOpenAI with ZhipuAI-compatible endpoint
        self.llm = ChatOpenAI(
            model=model,
            temperature=temperature,
            openai_api_key=settings.zhipuai_api_key,
            openai_api_base="https://api.z.ai/api/coding/paas/v4",
            streaming=streaming,
            max_tokens=2000,
            timeout=180.0,  # 3 minutes timeout for reasoning models
        )

        logger.info(f"LangChain Michelin Agent initialized with model: {model}")

    def _build_messages(
        self,
        query: str,
        location_context: Optional[str] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> List:
        """Build message list for the LLM.

        Args:
            query: User's query
            location_context: Optional location information
            conversation_history: Optional conversation history

        Returns:
            List of LangChain messages
        """
        messages = [SystemMessage(content=MICHELIN_SYSTEM_PROMPT)]

        # Add conversation history if provided
        if conversation_history:
            for turn in conversation_history[-5:]:  # Keep last 5 turns
                if turn.get("role") == "user":
                    messages.append(HumanMessage(content=turn["content"]))
                elif turn.get("role") == "assistant":
                    messages.append(AIMessage(content=turn["content"]))

        # Build current user message
        user_content = query

        if location_context:
            user_content += f"\n\n## Context Information:\n{location_context}"

        user_content += """

Please provide your recommendations in this format:

### 🍽️ [Restaurant Name] ([Stars])
**Location:** City, Neighborhood (if known)
**Cuisine:** Type of cuisine
**Price:** € range
**Why It's Special:** [Brief description of what makes this restaurant exceptional]
**Signature Dish:** [If applicable]

---
*For the most current information and reservations, please visit guide.michelin.com or contact restaurants directly.*
"""

        messages.append(HumanMessage(content=user_content))

        return messages

    async def chat(
        self,
        query: str,
        user_location: Optional[Dict[str, float]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None,
        stream_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """Get restaurant recommendations.

        Args:
            query: User's query
            user_location: Optional user location (lat, lon)
            conversation_history: Optional conversation history
            stream_callback: Optional callback for streaming tokens

        Returns:
            Response dictionary with recommendations and metadata
        """
        from geolocation import (
            CITY_COORDINATES,
            extract_location_from_query,
            extract_distance_from_query
        )

        # Extract location information
        location_in_query = extract_location_from_query(query)
        distance_constraint = extract_distance_from_query(query)

        # Build location context
        location_context_parts = []
        geo_info = None

        if user_location:
            location_context_parts.append(
                f"User coordinates: {user_location.get('latitude')}, "
                f"{user_location.get('longitude')}"
            )
            geo_info = {
                "center": user_location,
                "radius_km": 50,
                "type": "user_provided"
            }

        if location_in_query and location_in_query.name:
            city_name = location_in_query.name
            location_context_parts.append(f"User mentioned city: {city_name}")
            if location_in_query.latitude and location_in_query.longitude:
                location_context_parts.append(
                    f"City coordinates: {location_in_query.latitude}, "
                    f"{location_in_query.longitude}"
                )
                geo_info = {
                    "center": {
                        "latitude": location_in_query.latitude,
                        "longitude": location_in_query.longitude
                    },
                    "radius_km": distance_constraint or 50,
                    "city": city_name
                }

        if distance_constraint:
            location_context_parts.append(f"Distance constraint: within {distance_constraint}km")

        location_context = "\n".join(location_context_parts) if location_context_parts else None

        # Build messages
        messages = self._build_messages(query, location_context, conversation_history)

        # Get response
        if self.streaming and stream_callback:
            # Streaming mode
            response_text = ""
            callback = StreamingCallbackHandler()

            async for chunk in self.llm.astream(messages):
                if hasattr(chunk, 'content'):
                    token = chunk.content
                    response_text += token
                    await stream_callback(token)

            response_text = response_text or "".join(callback.tokens)

        else:
            # Non-streaming mode
            response = await self.llm.ainvoke(messages)
            response_text = response.content

        # Handle reasoning models (glm-5.1 puts content in reasoning_content)
        if not response_text.strip() or response_text.strip().startswith("1."):
            # The model might have returned reasoning instead of content
            # Re-invoke with simpler prompt
            messages = [
                SystemMessage(content="You are a helpful Michelin Guide assistant. Provide concise restaurant recommendations."),
                HumanMessage(content=query)
            ]
            response = await self.llm.ainvoke(messages)
            response_text = getattr(response, 'content', '') or getattr(response, 'reasoning_content', str(response))

        return {
            "response": response_text,
            "sources": [],
            "query_analysis": {
                "original_query": query,
                "mode": "langchain_streaming",
                "has_location": bool(location_in_query or user_location),
                "location_mentioned": location_in_query.name if location_in_query else None,
                "distance_constraint": distance_constraint
            },
            "geo_info": geo_info
        }

    async def chat_stream(
        self,
        query: str,
        user_location: Optional[Dict[str, float]] = None,
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> AsyncIterator[str]:
        """Stream restaurant recommendations.

        Args:
            query: User's query
            user_location: Optional user location
            conversation_history: Optional conversation history

        Yields:
            Response tokens as they arrive
        """
        from geolocation import (
            extract_location_from_query,
            extract_distance_from_query
        )

        # Extract location information
        location_in_query = extract_location_from_query(query)
        distance_constraint = extract_distance_from_query(query)

        # Build location context
        location_context_parts = []

        if user_location:
            location_context_parts.append(
                f"User coordinates: {user_location.get('latitude')}, "
                f"{user_location.get('longitude')}"
            )

        if location_in_query and location_in_query.name:
            location_context_parts.append(f"User mentioned city: {location_in_query.name}")

        if distance_constraint:
            location_context_parts.append(f"Distance constraint: within {distance_constraint}km")

        location_context = "\n".join(location_context_parts) if location_context_parts else None

        # Build messages
        messages = self._build_messages(query, location_context, conversation_history)

        # Stream response
        async for chunk in self.llm.astream(messages):
            if hasattr(chunk, 'content'):
                yield chunk.content


# ============================================================================
# FACTORY FUNCTION
# ============================================================================

def create_langchain_michelin_agent(
    model: str = "glm-5.1",
    temperature: float = 0.7,
    streaming: bool = True
) -> LangChainMichelinAgent:
    """Create a new LangChain-based Michelin agent.

    Args:
        model: Model name (glm-5.1, glm-5)
        temperature: Sampling temperature
        streaming: Enable streaming responses

    Returns:
        Configured LangChainMichelinAgent instance
    """
    return LangChainMichelinAgent(
        model=model,
        temperature=temperature,
        streaming=streaming
    )
