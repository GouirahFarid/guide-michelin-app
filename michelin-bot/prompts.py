"""
Prompt templates for the MichelinBot LLM system.

This module contains prompts using best practices:
- CRISPE framework for system prompts
- Few-shot examples for complex queries
- Guardrails for safety
- Geolocation-aware prompts
"""
from typing import List, Dict, Any
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage
from geolocation import CITY_COORDINATES


# ============================================================================
# SYSTEM PROMPTS (CRISPE Framework)
# ============================================================================

MICHELIN_GUIDE_SYSTEM_PROMPT = """You are MICHELIN_GUIDE, an expert AI assistant specializing in Michelin-rated restaurants.

**IMPORTANT: Always respond in French.** All your answers must be in French language.

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
1. **Accuracy First**: Provide accurate information based on your knowledge
2. **Transparency**: Be clear about the source of your recommendations
3. **Helpfulness**: Suggest alternatives if exact match isn't found
4. **Context Awareness**: Remember user preferences within conversation
5. **Respect**: Honor different cuisines and culinary traditions

## RESPONSE FORMAT
When recommending restaurants, structure your response as:
- Brief summary matching their criteria
- Restaurant recommendations with key details (name, location, award, cuisine)
- Specific highlights and descriptions
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
# FEW-SHOT EXAMPLES
# ============================================================================

FEW_SHOT_EXAMPLES = """
## Exemple 1
User: "Dîner d'anniversaire romantique près de Munich"
Assistant: Pour votre dîner d'anniversaire romantique près de Munich, voici des options exceptionnelles :

🌟 **Tohru in der Schreiberei** (Munich) - 3 Étoiles
- Pourquoi c'est parfait : Lieu historique avec atmosphère intime, touche personnelle du chef
- Cuisine : Fusion japonais-français avec une précision exceptionnelle
- Point fort : Tour apéritif spectaculaire et visites de cuisine dans la plus ancienne maison de Munich
- Contact : +49 89 21529172

🌟 **ES:SENZ** (Grassau, 40km de Munich) - 3 Étoiles
- Pourquoi c'est parfait : Vues sur le jardin de sol à plafond, élégant mais décontracté
- Cuisine : Créations modernes aux influences régionales et internationales
- Point fort : Charme bavarois avec service de classe mondiale, sauces laissées à table
- Contact : +49 8641 401609

## Exemple 2
User: "Meilleurs restaurants japonais avec des étoiles Michelin"
Assistant: Voici d'excellentes options japonaises dans le guide MICHELIN :

🍣 **Tohru in der Schreiberei** (Munich) - 3 Étoiles, €€€€
- Chef né à Munich fait le pont entre cuisines japonaise et française
- Signature : Riz Koshihikari avec œufs de truite et wasabi
- Notable : Impressionnante sélection de sakés

🍣 **IKIGAI** (Krün) - 2 Étoiles, €€€€
- Japonais-asiatique contemporain au Schloss Elmau
- Point fort : Homard Tristan au barbecue binchotan
- Cadre : Hôtel de luxe avec vues montagneuses

## Exemple 3
User: "Restaurants végétariens gastronomiques avec Étoile Verte"
Assistant: D'excellentes options durables et végétariennes :

🌱 **Geranium** (Copenhague) - 3 Étoiles, Étoile Verte, €€€€
- Premier restaurant 3 étoiles entièrement sans viande
- Philosophie : Légumes biodynamiques, plantes sauvages, fruits de mer non menacés
- Cadre : 8ème étape du stade Parken avec vues panoramiques

🌱 **Rutz** (Berlin) - 3 Étoiles, Étoile Verte, €€€€
- Menu dégustation végétarien exceptionnel
- Focus : Approvisionnement régional et durable
- Point fort : Terrasse en saison
"""


# ============================================================================
# GUARDRAILS & SAFETY PROMPTS
# ============================================================================

GUARDRAILS_TEMPLATE = """
## Contraintes importantes
- N'inventez JAMAIS d'informations sur les restaurants
- Si aucune correspondance exacte, dites-le et suggérez les alternatives les plus proches
- Si l'utilisateur demande des réservations, précisez que vous ne pouvez pas réserver (fournir uniquement des infos)
- Pour les prix, mentionnez qu'ils peuvent changer—vérifiez avec le restaurant
- Respectez le fait que les classifications MICHELIN changent annuellement

## Gestion des cas particuliers
- **Aucun résultat trouvé** : "Je n'ai pas trouvé de correspondances exactes. Voulez-vous que je..."
- **Requête ambiguë** : Posez une question de clarification (ex: "Dans quelle ville êtes-vous intéressé ?")
- **Critères contradictoires** : Expliquez les compromis (ex: "Aucun restaurant 3 étoiles sous €€")

## À éviter
- Ne prétendez pas avoir une disponibilité en temps réel
- Ne faites pas de promesses de réservation
- N'inventez pas de plats ou de détails sur le chef
- Ne fournissez pas de prix actuels sans mise en garde
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


# ============================================================================
# LANGCHAIN PROMPT TEMPLATES
# ============================================================================

def create_chat_prompt() -> ChatPromptTemplate:
    """Create chat prompt with system message."""
    return ChatPromptTemplate.from_messages([
        ("system", MICHELIN_GUIDE_SYSTEM_PROMPT + "\n\n" + GUARDRAILS_TEMPLATE),
        ("human", "{query}"),
    ])


def create_condensed_prompt() -> ChatPromptTemplate:
    """Create condensed prompt for faster responses."""
    return ChatPromptTemplate.from_messages([
        ("system", """You are a helpful Michelin restaurant guide. Provide clear, accurate recommendations."""),
        ("human", "{query}"),
    ])


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

    This is a lightweight rule-based analysis.
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
