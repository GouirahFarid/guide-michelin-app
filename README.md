# MichelinBot - RAG Restaurant Recommendation System

An AI-powered restaurant recommendation system using **RAG (Retrieval-Augmented Generation)** with Michelin Guide data.

## Tech Stack

| Component | Technology |
|-----------|------------|
| **API Framework** | FastAPI |
| **LLM** | GLM-4 (Zhipu AI) |
| **Embeddings** | HuggingFace sentence-transformers |
| **Vector Database** | PostgreSQL + pgvector |
| **Agent Framework** | LangGraph + LangChain |
| **Containerization** | Docker Compose |

## Features

- 🤖 **RAG Pipeline**: Vector search + LLM generation with Chain-of-Thought prompts
- 📍 **Geolocation Search**: Find restaurants by location with Haversine distance
- 🧠 **LangGraph Agent**: Intent routing, query analysis, smart retrieval
- 📝 **Prompt Engineering**: CRISPE framework, few-shot examples, guardrails
- 🔍 **Hybrid Search**: Vector similarity + metadata filters

---

## Prerequisites

- **Docker Desktop** (installed and running)
- **Zhipu AI API Key** - Get from [https://open.bigmodel.cn/](https://open.bigmodel.cn/)
- **michelin_my_maps.csv** - Restaurant data file

---

## Quick Start (Docker)

### 1. Clone and Setup

```powershell
cd C:\Users\farid\PycharmProjects\LLM\MichlenBot
```

### 2. Create Environment File

Create `.env` file in the project root:

```env
ZHIPUAI_API_KEY=your_api_key_here
DATABASE_URL=postgresql+psycopg://michelin_user:root@postgres:5432/michelin_db
```

### 3. Start Services

```powershell
# Build and start
docker compose build
docker compose up -d
```

### 4. Ingest Data

```powershell
docker compose --profile ingest up ingest
```

### 5. Verify Installation

```powershell
# Check API health
curl http://localhost:8000/health

# Or in PowerShell:
Invoke-WebRequest -Uri http://localhost:8000/health

# Verify database
docker compose exec api python main.py --verify
```

### 6. Access API

- **API Docs**: http://localhost:8000/docs
- **Interactive Chat**: http://localhost:8000/docs#/chat/chat_chat_post

---

## Complete Workflow Commands

```powershell
# ──────────────────────────────────────────────────────────────
# STEP 1: Build
# ──────────────────────────────────────────────────────────────
docker compose build

# ──────────────────────────────────────────────────────────────
# STEP 2: Start Services
# ──────────────────────────────────────────────────────────────
docker compose up -d

# ──────────────────────────────────────────────────────────────
# STEP 3: Ingest Data (one-time)
# ──────────────────────────────────────────────────────────────
docker compose --profile ingest up ingest

# ──────────────────────────────────────────────────────────────
# STEP 4: Verify
# ──────────────────────────────────────────────────────────────
docker compose exec api python main.py --verify

# ──────────────────────────────────────────────────────────────
# STEP 5: Test Queries
# ──────────────────────────────────────────────────────────────
curl -X POST "http://localhost:8000/chat" `
  -H "Content-Type: application/json" `
  -d '{"query": "3-star restaurants in Munich"}'

# ──────────────────────────────────────────────────────────────
# STEP 6: View Logs
# ──────────────────────────────────────────────────────────────
docker compose logs -f api

# ──────────────────────────────────────────────────────────────
# STOP SERVICES (when done)
# ──────────────────────────────────────────────────────────────
docker compose down
```

---

## API Endpoints

### Chat (Main RAG Endpoint)

```bash
POST /chat
```

**Request:**
```json
{
  "query": "Romantic restaurants with great views near Munich",
  "user_location": {
    "latitude": 48.1351,
    "longitude": 11.5820
  }
}
```

**Response:**
```json
{
  "response": "Based on your request for romantic restaurants...",
  "sources": [
    {
      "name": "ES:SENZ",
      "location": "Grassau, Germany",
      "award": "3 Stars",
      "cuisine": "Creative, Modern Cuisine"
    }
  ],
  "query_analysis": {
    "is_geo_query": true,
    "has_award": true,
    "award_mentioned": "3 Stars"
  }
}
```

### Geolocation Search

```bash
POST /restaurants/near
```

**Request:**
```json
{
  "latitude": 48.1351,
  "longitude": 11.5820,
  "radius_km": 50,
  "filters": {
    "award": "3 Stars"
  }
}
```

### Restaurant Search

```bash
GET /restaurants?location=Munich&award=3 Stars&limit=10
```

---

## Example Queries

| Query | Description |
|-------|-------------|
| `"3-star restaurants in Munich"` | Filter by award + location |
| `"Japanese cuisine with great views"` | Semantic search |
| `"Romantic restaurants under €€€€"` | Filter by price + atmosphere |
| `"Restaurants near me within 25km"` | Geolocation with radius |
| `"Best sushi in Tokyo"` | Cuisine + location |
| `"Tell me about ES:SENZ"` | Direct name lookup |

---

## Project Structure

```
MichlenBot/
├── app.py                  # FastAPI application
├── agent.py                # LangGraph agent workflow
├── config.py               # Configuration settings
├── database.py             # PostgreSQL + pgvector functions
├── embeddings.py           # HuggingFace embeddings wrapper
├── geolocation.py          # Location & distance calculations
├── ingest.py               # CSV data ingestion
├── llm.py                  # GLM-4 (Zhipu AI) wrapper
├── main.py                 # Application entry point
├── models.py               # Pydantic models
├── prompts.py              # All prompt templates
├── rag_pipeline.py         # RAG retrieval + generation
├── docker-compose.yml      # Docker orchestration
├── Dockerfile              # Application container
├── requirements.txt        # Python dependencies
└── michelin_my_maps.csv    # Restaurant data
```

---

## Troubleshooting

### Database Connection Error

```powershell
# Check PostgreSQL is running
docker compose ps postgres

# View database logs
docker compose logs postgres
```

### API Not Responding

```powershell
# Check API logs
docker compose logs api

# Restart API
docker compose restart api
```

### Rebuild Everything

```powershell
docker compose down
docker compose build --no-cache
docker compose up -d
docker compose --profile ingest up ingest
```

### Data Not Ingested

```powershell
# Verify database contents
docker compose exec api python main.py --verify

# Re-run ingestion
docker compose --profile ingest up ingest --force-recreate
```

---

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        FastAPI                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │  POST /chat          POST /restaurants/near            │ │
│  └────────────────────────────────────────────────────────┘ │
│                          │                                   │
│                          ▼                                   │
│  ┌────────────────────────────────────────────────────────┐ │
│  │              LangGraph Agent                           │ │
│  │  ┌──────────┐   ┌──────────┐   ┌──────────┐           │ │
│  │  │  Router  │──▶│Retriever │──▶│Generator │           │ │
│  │  │ (Intent) │   │(RAG+Geo) │   │ (GLM-4)   │           │ │
│  │  └──────────┘   └──────────┘   └──────────┘           │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│                   PostgreSQL + pgvector                      │
│  ┌──────────────────┐         ┌──────────────────────────┐  │
│  │   restaurants    │         │   restaurant_embeddings  │  │
│  │   (table)        │         │   (vector: 384-dim)      │  │
│  └──────────────────┘         └──────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Configuration

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `ZHIPUAI_API_KEY` | *required* | Zhipu AI API key |
| `DATABASE_URL` | postgresql://... | PostgreSQL connection |
| `EMBEDDING_MODEL` | all-MiniLM-L6-v2 | Sentence transformer model |
| `CHUNK_SIZE` | 500 | Text chunk size for embeddings |
| `CHUNK_OVERLAP` | 50 | Overlap between chunks |
| `TOP_K_RETRIEVAL` | 5 | Number of results to retrieve |

---

## License

MIT License
