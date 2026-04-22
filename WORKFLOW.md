# MichelinBot - Application Workflow

## What This App Does

MichelinBot is an **AI-powered restaurant recommendation system** that helps you discover and explore Michelin-rated restaurants worldwide using natural language queries.

### Core Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| 🔍 **Semantic Search** | Find restaurants by description meaning | "Romantic spots with great views" |
| 📍 **Geolocation** | Find restaurants near a location | "3-star restaurants within 50km of Munich" |
| 🏷️ **Filtering** | Filter by cuisine, award, price | "Japanese restaurants under €€€€" |
| 🤖 **AI Recommendations** | Get intelligent, context-aware responses | "Best sushi for a special occasion" |
| 📊 **Restaurant Details** | Get complete restaurant information | "Tell me about ES:SENZ" |

---

## High-Level Workflow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER QUERY                               │
│    "3-star Japanese restaurants near Munich with great views"   │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                     API LAYER (FastAPI)                          │
│  📄 app.py │ models.py │ config.py                            │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  POST /chat (app.py)                                       │ │
│  │  • Validates request with Pydantic models (models.py)     │ │
│  │  • Loads settings (config.py)                              │ │
│  │  • Routes to agent.chat()                                  │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                   AGENT LAYER (LangGraph)                        │
│  📄 agent.py │ prompts.py                                      │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  1. ROUTER NODE (agent.py → router_node)                   │ │
│  │     • Parse query intent (prompts.py → analyze_query)      │ │
│  │     • Extract: location, cuisine, award, price             │ │
│  │     • Detect: is this a geo query?                         │ │
│  └────────────────────────────────────────────────────────────┘ │
│                                │                                 │
│           ┌─────────────────────┴─────────────────────┐        │
│           ▼                                           ▼        │
│  ┌──────────────────────┐              ┌──────────────────────┐ │
│  │   GEO RETRIEVER      │              │   VECTOR RETRIEVER   │ │
│  │   (agent.py)         │              │   (rag_pipeline.py)  │
│  └──────────────────────┘              └──────────────────────┘ │
│           │                                           │         │
│  📄 geolocation.py + database.py        📄 embeddings.py + database.py
│           │                                           │         │
│           └─────────────────────┬─────────────────────┘        │
│                               ▼                                │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  2. CONTEXT GATHERING (prompts.py → format_context)      │ │
│  │     • Retrieved restaurants from database                 │ │
│  │     • Sort by relevance/distance                          │ │
│  │     • Take top 5 results                                   │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    AI/LLM LAYER (GLM-4)                          │
│  📄 llm.py │ prompts.py                                         │
│  ┌────────────────────────────────────────────────────────────┐ │
│  │  3. RESPONSE GENERATION                                    │ │
│  │     • Format retrieved context (prompts.py)                │ │
│  │     • Apply Chain-of-Thought prompt (prompts.py)          │ │
│  │     • Call GLM-4 API (llm.py → simple_chat)               │ │
│  │     • Cite source restaurants                              │ │
│  └────────────────────────────────────────────────────────────┘ │
└───────────────────────────────┬─────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USER RESPONSE                            │
│  📄 app.py (returns ChatResponse from models.py)               │
│  {                                                              │
│    "response": "Based on your search, here are exceptional...  │
│    "sources": [...]                                            │
│    "query_analysis": {...}                                     │
│  }                                                              │
└─────────────────────────────────────────────────────────────────┘
```

---

## Detailed Workflow Steps

### STEP 1: User Sends Query

**Files:** `app.py` → `models.py` → `config.py`

**Example Request:**
```json
POST /chat
{
  "query": "Romantic 3-star restaurants near Munich",
  "user_location": {
    "latitude": 48.1351,
    "longitude": 11.5820
  }
}
```

**Flow:**
```
1. FastAPI receives POST /chat request           [app.py]
2. Validates using ChatRequest model            [models.py]
3. Loads settings from .env                     [config.py]
4. Calls agent.chat() with query                [agent.py]
```

---

### STEP 2: Query Analysis (Router Node)

**Files:** `agent.py` → `prompts.py`

The agent analyzes the query to understand intent:

```python
Query Analysis Result:
{
  "original_query": "Romantic 3-star restaurants near Munich",
  "has_location": true,
  "location_mentioned": "Munich",
  "has_award": true,
  "award_mentioned": "3 Stars",
  "has_cuisine": false,
  "is_geo_query": true,
  "distance_constraint": 50,
  "needs_user_location": false
}
```

**Flow:**
```
1. router_node() receives state                 [agent.py]
2. Calls analyze_query(query)                   [prompts.py]
3. Extracts: location, cuisine, award, price
4. Detects: geo query, distance constraint
```

**What gets extracted:**
- 📍 **Location**: Munich (or user coordinates)
- ⭐ **Award Level**: 3 Stars
- 🍽️ **Cuisine**: Not specified (any)
- 💰 **Price**: Not specified (any)
- 🎯 **Intent**: Romantic dining, nearby

---

### STEP 3: Routing Decision

**Files:** `agent.py` → `geolocation.py`

Based on analysis, the agent decides which retriever to use:

```
IF user_location provided OR location in query:
    → Use GEO RETRIEVER
    → Search within radius using Haversine distance
ELSE:
    → Use VECTOR RETRIEVER
    → Search using semantic similarity
```

**Flow:**
```
1. Check state["analysis"]["is_geo_query"]     [agent.py]
2. If true, check for user_location or        [geolocation.py]
   extract_location_from_query()
3. Determine next_step routing
```

**For our example:**
- User mentioned "near Munich" + provided coordinates
- → **Route to GEO RETRIEVER**

---

### STEP 4: Data Retrieval

#### Option A: Geolocation Retrieval

**Files:** `agent.py` → `geolocation.py` → `database.py`

```python
# 1. Calculate bounding box around user location     [geolocation.py]
bounding_box = calculate_bounding_box(
    latitude: 48.1351,
    longitude: 11.5820,
    radius_km: 50
)
# Returns: north, south, east, west bounds

# 2. Search database for restaurants in bounds       [database.py]
restaurants = db.search_restaurants_nearby(
    latitude, longitude, radius_km
)

# 3. Calculate exact distance for each restaurant     [geolocation.py]
for restaurant in restaurants:
    distance = haversine_distance(
        user_lat, user_lon,
        restaurant.lat, restaurant.lon
    )
    restaurant.distance_km = distance

# 4. Filter by radius and sort by distance
results = [r for r in restaurants if r.distance_km <= 50]
results.sort(key=lambda x: x.distance_km)
```

#### Option B: Vector Retrieval

**Files:** `rag_pipeline.py` → `embeddings.py` → `database.py`

```python
# 1. Embed the user's query                        [embeddings.py]
query_embedding = embeddings.embed_query(query)
# Returns: [0.23, -0.45, 0.67, ...]  (384 dimensions)

# 2. Search pgvector for similar embeddings          [database.py]
similar_chunks = await search_similar(
    query_embedding,
    top_k: 5
)
# Uses cosine similarity: 1 - (embedding <=> query_vector)

# 3. Retrieve full restaurant data                  [database.py]
restaurant_ids = [chunk.restaurant_id for chunk in similar_chunks]
```

---

### STEP 5: Context Preparation

**Files:** `prompts.py` → `rag_pipeline.py`

The retrieved restaurants are formatted for the LLM:

```python
# format_context()                                   [prompts.py]
Formatted Context:
"""
**Restaurant 1**: Tohru in der Schreiberei
- Location: Munich, Germany
- Award: 3 Stars
- Cuisine: Modern Cuisine, Japanese Contemporary
- Price: €€€€
- Distance: 2.3 km

Description:
It is absolutely worth climbing the 23 steps of the beautiful steep
wooden staircase that leads to this tasteful, upscale restaurant...
"""

Similar format for all 5 retrieved restaurants.
```

**Flow:**
```
1. Documents retrieved from database              [rag_pipeline.py]
2. format_context() formats each restaurant        [prompts.py]
3. Creates structured context for LLM
```

---

### STEP 6: Response Generation (GLM-4)

**Files:** `llm.py` → `prompts.py`

The formatted context is sent to GLM-4 with a carefully crafted prompt:

```python
# simple_chat()                                      [llm.py]
System Prompt (CRISPE Framework):                  [prompts.py]
"""
You are MICHELIN_GUIDE, an expert AI assistant specializing in
Michelin-rated restaurants.

CAPACITY: Comprehensive knowledge of Michelin restaurants
IDENTITY: Professional, passionate about culinary excellence
CORE PRINCIPLES:
  1. Accuracy First - Only use provided context
  2. Transparency - Cite sources
  3. Helpfulness - Suggest alternatives
"""

User Message:
"""
## User Question
Romantic 3-star restaurants near Munich

## Retrieved Context
[5 restaurants with details]

Think step-by-step and provide a helpful response.
"""
```

**GLM-4 generates:**
```
Based on your search for romantic 3-star restaurants near Munich, I found
two exceptional options:

🌟 TOHRU IN DER SCHREIBEREI (Munich) - 3 Stars
This restaurant bridges Japanese and French cuisines...
Located in Munich's oldest town house, perfect for intimate dining...

🌟 ES:SENZ (Grassau, 40km away) - 3 Stars
Floor-to-ceiling garden views create a romantic atmosphere...
```

---

### STEP 7: Response to User

Final response is sent back with sources and analysis:

```json
{
  "response": "Based on your search for romantic 3-star restaurants...",
  "sources": [
    {
      "restaurant_id": 123,
      "name": "Tohru in der Schreiberei",
      "location": "Munich, Germany",
      "award": "3 Stars",
      "cuisine": "Modern Cuisine, Japanese Contemporary",
      "distance_km": 2.3
    },
    {
      "restaurant_id": 456,
      "name": "ES:SENZ",
      "location": "Grassau, Germany",
      "award": "3 Stars",
      "distance_km": 42.1
    }
  ],
  "query_analysis": {
    "original_query": "Romantic 3-star restaurants near Munich",
    "is_geo_query": true,
    "has_award": true,
    "award_mentioned": "3 Stars"
  },
  "geo_results": {
    "center": {"latitude": 48.1351, "longitude": 11.5820},
    "radius_km": 50,
    "restaurants_found": 2
  }
}
```

---

## Component Interaction Diagram

**Files:** `app.py` → `agent.py` → `database.py` → `llm.py` → `embeddings.py`

```
┌────────────────────────────────────────────────────────────────┐
│                        USER                                     │
└────────────────────────┬───────────────────────────────────────┘
                         │ Query
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                     FastAPI (app.py)                           │
│  📄 models.py │ config.py                                      │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  POST /chat                                              │ │
│  │  • Validates request (models.py → ChatRequest)          │ │
│  │  • Loads settings (config.py)                            │ │
│  │  • Calls agent.chat()                                    │ │
│  │  • Returns ChatResponse (models.py)                     │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────┬───────────────────────────────────────┘
                         │
                         ▼
┌────────────────────────────────────────────────────────────────┐
│                  LangGraph Agent (agent.py)                    │
│  📄 prompts.py │ rag_pipeline.py │ geolocation.py             │
│  ┌──────────────────────────────────────────────────────────┐ │
│  │  State: {query, analysis, context, response}            │ │
│  │                                                          │ │
│  │  router_node() → analyze_query() [prompts.py]           │ │
│  │       │                                                 │ │
│  │       ├── Geo query? ──→ geo_retriever_node()           │ │
│  │       │ [geolocation.py] │                             │ │
│  │       │                   ├── search_restaurants_nearby()│ │
│  │       │                   │   [database.py]             │ │
│  │       │                   └── calculate_distance()       │ │
│  │       │                       [geolocation.py]          │ │
│  │       │                                                 │ │
│  │       └── Semantic? ───→ retriever_node()                │ │
│  │                           │ [rag_pipeline.py]           │ │
│  │                           ├── embed_query()              │ │
│  │                           │   [embeddings.py]            │ │
│  │                           └── search_similar()           │ │
│  │                               [database.py]              │ │
│  │                                                          │ │
│  │  generator_node() → generate_response() [llm.py]        │ │
│  └──────────────────────────────────────────────────────────┘ │
└────────────────────────┬───────────────────────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
         ▼               ▼               ▼
┌────────────────┐ ┌──────────────┐ ┌──────────────┐
│  database.py   │ │  llm.py      │ │ embeddings.py│
│                │ │              │ │              │
│ PostgreSQL     │ │ GLM-4 API    │ │ sentence-    │
│ + pgvector     │ │ Zhipu AI     │ │ transformers │
│                │ │              │ │              │
│ restaurants    │ │              │ │              │
│ embeddings     │ │              │ │              │
└────────────────┘ └──────────────┘ └──────────────┘
```

---

## Example Workflows

### Example 1: Simple Semantic Search

**Files:** `app.py` → `agent.py` → `rag_pipeline.py` → `embeddings.py` → `database.py` → `llm.py` → `prompts.py`

**Query:** `"Best sushi restaurants with views"`

```
1. Query Analysis:                                   [agent.py → prompts.py]
   - No location mentioned
   - Cuisine detected: "sushi" (Japanese)
   - Keywords: "best", "views"
   - Not a geo query

2. Routing: Vector Retriever                         [agent.py → router_node()]
   → retriever_node()

3. Retrieval:                                        [rag_pipeline.py]
   - Embed query: [384-dim vector]                   [embeddings.py]
   - Search pgvector for similar descriptions        [database.py]
   - Find restaurants mentioning "sushi", "views", "scenic"

4. Response:                                         [llm.py → prompts.py]
   "Here are exceptional sushi restaurants with beautiful views:
    - KIKUNOI HONTEN (Kyoto) - Garden views, traditional kaiseki
    - Tohru in der Schreiberei (Munich) - Counter dining with chef interaction..."
```

**Flow:**
```
User Query → [app.py → POST /chat]
    → [agent.py → router_node()]
    → [prompts.py → analyze_query()]
    → [agent.py → retriever_node()]
    → [embeddings.py → embed_query()]
    → [database.py → search_similar()]
    → [prompts.py → format_context()]
    → [llm.py → simple_chat()]
    → [app.py → ChatResponse]
```

---

### Example 2: Geolocation Search

**Files:** `app.py` → `agent.py` → `geolocation.py` → `database.py` → `llm.py` → `prompts.py`

**Query:** `"Restaurants within 25km of my location"`
+ User coordinates: `(52.5200, 13.4050)` (Berlin)

```
1. Query Analysis:                                   [agent.py → prompts.py]
   - User location provided (from request)
   - "within 25km" → radius constraint
   - Geo query detected

2. Routing: Geo Retriever                            [agent.py → router_node()]
   → geo_retriever_node()

3. Retrieval:                                        [geolocation.py → database.py]
   - Calculate bounding box around Berlin            [geolocation.py]
   - Search restaurants in bounds                    [database.py]
   - Calculate exact distances (Haversine)           [geolocation.py]
   - Filter: distance ≤ 25km
   - Sort by distance

4. Response:                                         [llm.py → prompts.py]
   "Found 5 restaurants within 25km of Berlin:
    - FACIL (Berlin) - 2 Stars, 3.2 km away
    - Schwarzwaldstube location... (if within radius)
    ..."
```

**Flow:**
```
User Query + Location → [app.py → POST /chat]
    → [agent.py → router_node()] detects geo_query=true
    → [agent.py → geo_retriever_node()]
    → [geolocation.py → calculate_bounding_box()]
    → [database.py → search_in_bounding_box()]
    → [geolocation.py → haversine_distance()] for each result
    → [prompts.py → format_context()]
    → [llm.py → simple_chat()]
    → [app.py → ChatResponse with geo_results]
```

---

### Example 3: Filtered Search

**Files:** `app.py` → `agent.py` → `rag_pipeline.py` → `database.py` → `models.py` → `llm.py` → `prompts.py`

**Query:** `"3-star Japanese restaurants under €€€€"`

```
1. Query Analysis:                                   [agent.py → prompts.py]
   - Award: "3 Stars"                                [models.py → AwardLevel]
   - Cuisine: "Japanese"
   - Price: "€€€€" (or less)                         [models.py → normalize_price_level()]

2. Routing: Hybrid (Vector + Metadata)              [agent.py → router_node()]
   → retriever_node() with filters

3. Retrieval:                                        [rag_pipeline.py → database.py]
   - First: Vector search for "Japanese fine dining" [embeddings.py]
   - Second: Apply metadata filters                  [database.py]
     - award IN ('3 Stars', '2 Stars', '1 Star')
     - cuisine ILIKE '%Japanese%'
     - price IN ('€', '€€', '€€€')
   - Combine results, prioritize vector matches

4. Response:                                         [llm.py → prompts.py]
   "Here are Japanese restaurants within your criteria:
    - Tohru in der Schreiberei (3 Stars, €€€€)
    - IKIGAI (2 Stars, €€€€)
    ..."
```

**Flow:**
```
User Query → [app.py → POST /chat]
    → [models.py → ChatRequest with filters]
    → [agent.py → router_node()] extracts filters
    → [agent.py → retriever_node()] with filter params
    → [database.py → search_with_filters()]
    → [prompts.py → format_context()]
    → [llm.py → simple_chat()]
    → [app.py → ChatResponse with sources]
```

---

## Data Flow Summary

**Files:** `ingest.py` → `database.py` → `embeddings.py` → `app.py` → `agent.py` → `llm.py` → `prompts.py`

```
CSV File (michelin_my_maps.csv)
    ↓
[Ingestion Process]                               [ingest.py]
    ├── load_csv_data()
    ├── chunk_text()
    ├── generate_embeddings()                     [embeddings.py]
    └── store_in_db()                             [database.py]
    ↓
PostgreSQL Database                               [database.py]
    ├── restaurants (500+ rows)
    └── restaurant_embeddings (2000+ chunks)
        ↓
[User Query]                                      [app.py → POST /chat]
        ↓
    [LangGraph Agent]                             [agent.py]
        ├── Analyze Query                         [prompts.py → analyze_query()]
        ├── Route to Retriever                    [agent.py → router_node()]
        │
        ├── [Geo Path]                            [geolocation.py → database.py]
        │   ├── Get coordinates
        │   ├── Search nearby
        │   └── Calculate distances (Haversine)
        │
        └── [Vector Path]                         [rag_pipeline.py]
            ├── Embed query                       [embeddings.py]
            ├── Search pgvector                   [database.py]
            └── Get similar chunks
        ↓
    [GLM-4 LLM]                                   [llm.py]
        ├── Format context                        [prompts.py → format_context()]
        ├── Apply prompt template                 [prompts.py → RAG_PROMPT_TEMPLATE]
        └── Generate response
        ↓
    [User Response with Sources]                  [app.py → ChatResponse]
```

---

## Key Technologies in Workflow

| Component | Files | Technology | Role |
|-----------|-------|------------|------|
| **API Server** | `app.py`, `models.py`, `config.py` | FastAPI | Handle HTTP requests, validation |
| **Agent Framework** | `agent.py`, `rag_pipeline.py` | LangGraph | Orchestrate workflow, state management |
| **LLM** | `llm.py` | GLM-4 (Zhipu AI) | Generate intelligent responses |
| **Embeddings** | `embeddings.py` | sentence-transformers | Convert text to 384-dim vectors |
| **Vector DB** | `database.py` | PostgreSQL + pgvector | Store and search embeddings |
| **Distance Calc** | `geolocation.py` | Haversine formula | Calculate distances between coordinates |
| **Prompts** | `prompts.py` | Custom templates | Guide LLM behavior (CRISPE, CoT) |
| **Ingestion** | `ingest.py` | CSV Parser + ETL | Load restaurant data into database |

---

## Why This Architecture?

| Design Choice | Benefit |
|---------------|---------|
| **LangGraph Agent** | Explicit workflow, easy to debug and extend |
| **Local Embeddings** | No API cost, fast, privacy-preserving |
| **pgvector in PostgreSQL** | Single database for all data, SQL + vectors |
| **GLM-4** | Good multilingual support, reasonable pricing |
| **Chain-of-Thought Prompts** | Better reasoning, fewer hallucinations |
| **Hybrid Search** | Vector similarity + precise filters |
