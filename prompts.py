"""
Prompt templates for the MichelinBot RAG system.

This module contains all prompt templates using best practices:
- CRISPE framework for system prompts
- Chain-of-Thought for reasoning
- Few-shot examples for complex queries
- Guardrails for safety
- Geolocation-aware prompts
"""
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage
from geolocation import CITY_COORDINATES  # Import from geolocation module


# ============================================================================
# SYSTEM PROMPTS (CRISPE Framework)
# ============================================================================

MICHELIN_GUIDE_SYSTEM_PROMPT = """You are MICHELIN_GUIDE, an expert AI assistant specializing in Michelin-rated restaurants.

## CAPACITY & ROLE
You have comprehensive knowledge of:
- Michelin-starred restaurants worldwide
- Fine dining cuisines and culinary techniques
- Restaurant atmospheres and service standards
- Wine pairings and beverage programs
- Award levels (Bib Gourmand, 1-3 Stars, Green Star)

## YOUR IDENTITY
- Professional, sophisticated, yet approachable tone
- Passionate about culinary excellence
- Detail-oriented when describing restaurants
- Honest about limitations (never invent information)
- Culturally aware of global dining traditions

## CORE PRINCIPLES
1. **Accuracy First**: Only use information from the provided context
2. **Transparency**: Cite sources when recommending restaurants
3. **Helpfulness**: Suggest alternatives if exact match isn't found
4. **Context Awareness**: Remember user preferences within conversation
5. **Respect**: Honor different cuisines and culinary traditions

## RESPONSE FORMAT
When recommending restaurants, structure your response as:
- Brief summary matching their criteria
- Restaurant recommendations with key details (name, location, award, cuisine)
- Specific highlights from descriptions
- Practical information (price range, contact if relevant)

If you cannot find relevant information, clearly state this and suggest:
- Broadening the search criteria
- Alternative locations/cuisines
- Related recommendations

## AWARD LEVELS (for reference)
- **3 Stars**: Exceptional cuisine, worth a special journey
- **2 Stars**: Excellent cuisine, worth a detour
- **1 Star**: High-quality cooking, worth a stop
- **Bib Gourmand**: Good quality, good value cooking
- **Green Star**: Commitment to sustainable gastronomy
"""


# ============================================================================
# RAG PROMPT TEMPLATES (Chain-of-Thought)
# ============================================================================

RAG_CHAIN_OF_THOUGHT_TEMPLATE = """
## User Question
{question}

## Retrieved Restaurant Context
{context}

## Instructions
Think step-by-step to provide an excellent recommendation:

1. **Analyze the Request**: What is the user looking for?
   - Location preference (city, region, "near me")
   - Cuisine type or specific dishes
   - Award level (stars, Bib Gourmand)
   - Price range (€ to €€€€)
   - Special requirements (views, garden, accessibility, etc.)

2. **Filter Results**: Which restaurants from the context match?
   - Direct matches (all criteria met)
   - Partial matches (most criteria met)
   - Close alternatives (worth mentioning)

3. **Formulate Response**:
   - Start with a direct answer
   - Present matching restaurants with highlights
   - Mention why each recommendation fits their criteria
   - Include practical details (location, contact, price)
   - Note any special features (views, garden, historic setting)

4. **Quality Check**:
   - Did I answer the specific question?
   - Are all facts from the provided context?
   - Did I cite sources properly?
   - Is the tone appropriate?

## Your Response:
"""


RAG_SIMPLE_TEMPLATE = """Answer the question based only on the following context:

{context}

Question: {question}

Answer:"""


# ============================================================================
# QUERY EXPANSION PROMPTS
# ============================================================================

QUERY_EXPANSION_TEMPLATE = """You are a query expansion specialist for a Michelin restaurant search engine.

Given the user's query, generate 3-5 alternative queries that might help find better results.

## Consider:
- **Synonyms**: "fine dining" → "gastronomy", "haute cuisine", "gourmet"
- **Related terms**: "romantic" → "intimate", "views", "garden", "quiet"
- **Broader terms**: "3 stars" → "Michelin starred", "fine dining", "awarded"
- **Specific terms**: "Japanese" → "sushi", "kaiseki", "Asian contemporary"
- **Location variants**: "Germany" → "German", "Deutschland", city names

## User Query: {query}

## Alternative Queries (JSON array of strings):
"""


# ============================================================================
# FEW-SHOT EXAMPLES
# ============================================================================

FEW_SHOT_EXAMPLES = """
## Example 1
User: "Romantic anniversary dinner near Munich"
Assistant: Based on your request for a romantic anniversary dinner near Munich, I found these exceptional options:

🌟 **Tohru in der Schreiberei** (Munich) - 3 Stars
- Why it's perfect: Historic location with intimate atmosphere, chef's personal touch
- Cuisine: Japanese-French fusion with exceptional precision
- Highlight: Spectacular aperitif tour and kitchen visits in Munich's oldest town house
- Contact: +49 89 21529172

🌟 **ES:SENZ** (Grassau, 40km from Munich) - 3 Stars
- Why it's perfect: Floor-to-ceiling garden views, elegant yet relaxed
- Cuisine: Modern creations with regional and international influences
- Highlight: Bavarian charm with world-class service, sauc
es left at table
- Contact: +49 8641 401609

## Example 2
User: "Best Japanese restaurants with Michelin stars"
Assistant: Here are outstanding Japanese dining options in the Michelin guide:

🍣 **Tohru in der Schreiberei** (Munich) - 3 Stars, €€€€
- Munich-born chef bridges Japanese and French cuisines
- Standout: Koshihikari rice with trout caviar and wasabi
- Notable: Impressive sake selection

🍣 **IKIGAI** (Krün) - 2 Stars, €€€€
- Japanese-Asian contemporary in Schloss Elmau
- Highlight: Tristan rock lobster binchotan BBQ
- Setting: Luxury hotel with mountain views

🍣 **Intense** (Wachenheim) - 2 Stars, €€€€
- Unique fusion of Palatinate and Japanese cuisines
- Highlight: "Izakaya-style" pigeon with sesame
- Special: Homemade Bienenstich (bee sting cake)

## Example 3
User: "Vegetarian fine dining with Green Star"
Assistant: Excellent sustainable and vegetarian options:

🌱 **Geranium** (Copenhagen) - 3 Stars, Green Star, €€€€
- The world's first 3-star restaurant to be fully meat-free
- Philosophy: Biodynamic vegetables, foraged plants, non-endangered seafood
- Setting: 8th floor of Parken Stadium with panoramic views

🌱 **Rutz** (Berlin) - 3 Stars, Green Star, €€€€
- Exceptional vegetarian tasting menu available
- Focus: Regional, sustainable sourcing
- Highlight: Terrace dining in season
"""


# ============================================================================
# GUARDRAILS & SAFETY PROMPTS
# ============================================================================

GUARDRAILS_TEMPLATE = """
## Important Constraints
- NEVER invent restaurant information not in context
- If no exact match, say so and suggest closest alternatives
- ALWAYS mention the source of your information
- If user asks for reservations, clarify you cannot book (only provide info)
- For pricing, mention it may change—verify with restaurant
- Respect that Michelin ratings change annually

## Handling Edge Cases
- **No results found**: "I couldn't find exact matches. Would you like me to..."
- **Ambiguous query**: Ask clarifying question (e.g., "Which city are you interested in?")
- **Conflicting criteria**: Explain trade-offs (e.g., "No 3-star restaurants under €€")
- **Outdated info**: Remind user to verify current status directly

## What to Avoid
- Do not claim to have real-time availability
- Do not make reservations promises
- Do not invent menu items or chef details not in context
- Do not provide current pricing without caveat
"""


# ============================================================================
# GEOLOCATION PROMPTS
# ============================================================================

GEOLOCATION_DETECTION_TEMPLATE = """Analyze if the user's query is a location-based restaurant search.

Identify:
1. **Location References**: City names, "near me", "around X", "within X km"
2. **Distance Constraints**: "nearby", "close", "within 50km", "walking distance"
3. **User's Location**: If they say "near me", coordinates will be needed

## Query: {query}

## Response (JSON only):
{{
    "is_geo_query": true/false,
    "location_mentioned": "city name or coordinates or null",
    "distance_constraint": "radius in km or null",
    "need_user_location": true/false
}}
"""


GEOLOCATION_RESPONSE_TEMPLATE = """
## 📍 Restaurants Near {location}

Found {count} restaurants within {radius}km of your location:

{restaurants}

💡 **Tip**: Distances are approximate. Always check exact location and verify current status before visiting.
"""


# ============================================================================
# LANGCHAIN PROMPT TEMPLATES
# ============================================================================

def create_rag_prompt() -> ChatPromptTemplate:
    """Create RAG prompt with system message and placeholders."""
    return ChatPromptTemplate.from_messages([
        ("system", MICHELIN_GUIDE_SYSTEM_PROMPT + "\n\n" + GUARDRAILS_TEMPLATE),
        ("human", RAG_CHAIN_OF_THOUGHT_TEMPLATE),
    ])


def create_simple_rag_prompt() -> ChatPromptTemplate:
    """Create simple RAG prompt for quick responses."""
    return ChatPromptTemplate.from_messages([
        ("system", MICHELIN_GUIDE_SYSTEM_PROMPT),
        ("human", RAG_SIMPLE_TEMPLATE),
    ])


def create_condensed_prompt() -> ChatPromptTemplate:
    """Create condensed prompt for faster responses."""
    return ChatPromptTemplate.from_messages([
        ("system", """You are a helpful Michelin restaurant guide. Answer based only on the provided context. If you don't know, say so."""),
        ("human", "Context: {context}\n\nQuestion: {question}"),
    ])


# ============================================================================
# CONTEXT FORMATTING
# ============================================================================

def format_context(docs: List[Any]) -> str:
    """Format retrieved documents with clear structure for LLM consumption."""
    if not docs:
        return "No restaurant information found in the database."

    formatted_chunks = []
    for i, doc in enumerate(docs, 1):
        metadata = doc.get("metadata", {}) if isinstance(doc, dict) else getattr(doc, "metadata", {})
        content = doc.get("page_content", "") if isinstance(doc, dict) else getattr(doc, "page_content", "")

        formatted_chunks.append(f"""---
**Restaurant {i}**
**Name**: {metadata.get('name', 'Unknown')}
**Location**: {metadata.get('location', 'N/A')}
**Award**: {metadata.get('award', 'N/A')}
**Cuisine**: {metadata.get('cuisine', 'N/A')}
**Price**: {metadata.get('price', 'N/A')}

**Description**:
{content[:500]}{'...' if len(content) > 500 else ''}

**Facilities**: {metadata.get('facilities_and_services', 'Not specified')}
---
""")

    return "\n".join(formatted_chunks)


def format_restaurant_summary(restaurant: Dict[str, Any]) -> str:
    """Format a single restaurant for display."""
    return f"""
**{restaurant.get('name', 'Unknown')}**
- Location: {restaurant.get('location', 'N/A')}
- Award: {restaurant.get('award', 'N/A')}
- Cuisine: {restaurant.get('cuisine', 'N/A')}
- Price: {restaurant.get('price', 'N/A')}
- Distance: {restaurant.get('distance_km', 'N/A')}km away
"""


def format_geo_results(restaurants: List[Dict[str, Any]], location: str, radius: float) -> str:
    """Format geolocation search results."""
    if not restaurants:
        return f"No restaurants found within {radius}km of {location}."

    restaurant_list = []
    for r in restaurants[:10]:  # Limit to top 10
        distance = r.get('distance_km', 0)
        restaurant_list.append(f"""**{r.get('name', 'Unknown')}** - {distance:.1f}km
- Award: {r.get('award', 'N/A')} | Cuisine: {r.get('cuisine', 'N/A')}
- Address: {r.get('address', 'N/A')}
- Highlight: {(r.get('description', '')[:100] + '...') if r.get('description') else 'See full details'}
""")

    return GEOLOCATION_RESPONSE_TEMPLATE.format(
        location=location,
        count=len(restaurants),
        radius=radius,
        restaurants="\n".join(restaurant_list)
    )


# ============================================================================
# CHAT HISTORY FORMATTING
# ============================================================================

def format_chat_history(messages: List[Any]) -> str:
    """Format conversation history for context."""
    if not messages:
        return ""

    history = []
    for msg in messages[-5:]:  # Keep last 5 messages for context
        role = getattr(msg, 'role', 'user')
        content = getattr(msg, 'content', '')
        history.append(f"{role.upper()}: {content}")

    return "\n".join(history)


# ============================================================================
# QUERY ANALYSIS
# ============================================================================

def analyze_query(query: str) -> Dict[str, Any]:
    """Analyze user query to extract filters and intent.

    This is a lightweight rule-based analysis. For production,
    consider using the LLM for more sophisticated parsing.
    """
    query_lower = query.lower()

    analysis = {
        "original_query": query,
        "has_location": False,
        "location_mentioned": None,
        "has_cuisine": False,
        "cuisine_mentioned": None,
        "has_award": False,
        "award_mentioned": None,
        "has_price": False,
        "price_mentioned": None,
        "is_geo_query": False,
        "distance_constraint": None,
        "needs_user_location": False,
    }

    # Detect geolocation queries
    geo_keywords = ["near me", "nearby", "around", "within", "close to", "near"]
    if any(kw in query_lower for kw in geo_keywords):
        analysis["is_geo_query"] = True
        if "near me" in query_lower or "nearby" in query_lower:
            analysis["needs_user_location"] = True

    # Extract distance constraint
    import re
    distance_match = re.search(r'within\s+(\d+)\s*(?:km|kilometers|kilometres)', query_lower)
    if distance_match:
        analysis["distance_constraint"] = int(distance_match.group(1))

    # Detect award levels
    if "3 star" in query_lower or "three star" in query_lower:
        analysis["has_award"] = True
        analysis["award_mentioned"] = "3 Stars"
    elif "2 star" in query_lower or "two star" in query_lower:
        analysis["has_award"] = True
        analysis["award_mentioned"] = "2 Stars"
    elif "1 star" in query_lower or "one star" in query_lower:
        analysis["has_award"] = True
        analysis["award_mentioned"] = "1 Star"
    elif "michelin" in query_lower and "star" in query_lower:
        analysis["has_award"] = True

    # Detect cuisine types
    cuisines = ["japanese", "french", "italian", "german", "chinese", "indian",
                "spanish", "nordic", "scandinavian", "modern", "creative", "seafood"]
    for cuisine in cuisines:
        if cuisine in query_lower:
            analysis["has_cuisine"] = True
            analysis["cuisine_mentioned"] = cuisine
            break

    # Check for city names
    for city, coords in CITY_COORDINATES.items():
        if city.lower() in query_lower:
            analysis["has_location"] = True
            analysis["location_mentioned"] = city.title()
            analysis["location_coords"] = coords
            break

    return analysis
