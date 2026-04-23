# MichelinBot - LLM-Only Restaurant Recommendation Agent

A Michelin Guide-powered restaurant recommendation system using LangChain and ZhipuAI's GLM models.

## Features

- **LangChain Integration**: Uses LangChain's ChatOpenAI with ZhipuAI-compatible endpoint
- **Streaming Responses**: Real-time streaming via Server-Sent Events (SSE)
- **Professional Michelin Guide Persona**: Expert recommendations based on MICHELIN criteria
- **Geolocation Support**: Location-aware recommendations
- **LLM-Only Mode**: No database required - uses LLM knowledge directly

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file:

```env
ZHIPUAI_API_KEY=your_api_key_here
HOST=0.0.0.0
PORT=8000
```

### 3. Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat` | POST | Chat with restaurant recommendations |
| `/chat/stream` | GET | Stream recommendations (SSE) |
| `/docs` | GET | Interactive API documentation (Swagger UI) |
| `/health` | GET | Health check |

## Example Usage

### Regular Chat

```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"query": "Best 3-star restaurants in Paris"}'
```

### Streaming Chat

```bash
curl "http://localhost:8000/chat/stream?query=Romantic%20restaurants%20in%20Tokyo"
```

## Project Structure

```
MichlenBot/
├── app.py                 # FastAPI application
├── langchain_agent.py     # LangChain-based Michelin agent
├── llm.py                 # LLM utilities
├── geolocation.py         # Location utilities
├── models.py              # Pydantic models
├── config.py              # Configuration
├── main.py                # Entry point
├── requirements.txt       # Python dependencies
└── archived/              # Archived RAG-related files
```

## The MICHELIN Guide Five Criteria

The agent evaluates restaurants based on:

1. **Quality of Products** - Excellence of ingredients
2. **Mastery of Flavor and Cooking** - Chef's ability to create harmonious dishes
3. **The Personality of the Chef** - Unique voice expressed through cuisine
4. **Value for Money** - Experience relative to price
5. **Consistency** - Quality maintained over time and across menu

## Supported Locations

The agent has knowledge of MICHELIN-guide restaurants in:
- Europe: France, Italy, Spain, Germany, UK, Switzerland, Netherlands, Belgium
- Asia: Japan, Thailand, Singapore, Hong Kong
- Americas: USA, Brazil

## Configuration

### Model Settings

- **Default Model**: `glm-5.1` (ZhipuAI reasoning model)
- **Temperature**: 0.7
- **Max Tokens**: 2000
- **Timeout**: 180 seconds

### API Endpoint

- **Base URL**: `https://api.z.ai/api/paas/v4`
- **Compatible**: OpenAI API format

## Development

### Running in Development Mode

```bash
python main.py --reload
```

### Using Different Port

```bash
python main.py --port 8001
```

## License

MIT License
