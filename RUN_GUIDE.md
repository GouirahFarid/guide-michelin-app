# Quick Start Guide - Run MichelinBot Step by Step

## STEP 1: Prerequisites

You need:
- ✅ Docker Desktop installed and running
- ✅ Zhipu AI API key (get from https://open.bigmodel.cn/)
- ✅ At least 4GB RAM available

---

## STEP 2: Create .env File

Open PowerShell in your project folder:

```powershell
cd C:\Users\farid\PycharmProjects\LLM\MichlenBot
```

Create the `.env` file:

```powershell
notepad .env
```

Paste this content:

```env
ZHIPUAI_API_KEY=your_actual_api_key_here

POSTGRES_DB=michelin_db
POSTGRES_USER=michelin_user
POSTGRES_PASSWORD=root

ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

HOST=0.0.0.0
PORT=8000

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RETRIEVAL=5
API_TIMEOUT=30
```

**Replace `your_actual_api_key_here` with your actual Zhipu AI key!**

Save and close.

---

## STEP 3: Verify CSV File Exists

Make sure `michelin_my_maps.csv` is in the project folder.

---

## STEP 4: Start Docker

Open Docker Desktop and make sure it's running.

---

## STEP 5: Start PostgreSQL Database

```powershell
docker compose up -d postgres
```

Wait until you see "healthy" status:

```powershell
docker compose ps
```

Expected output:
```
NAME                STATUS
michelinbot-db      Up (healthy)
```

---

## STEP 6: Initialize Database

```powershell
docker compose exec api python -c "import asyncio; from database import init_database; asyncio.run(init_database())"
```

Expected output:
```
Database initialized successfully!
```

---

## STEP 7: Ingest Restaurant Data

This loads the CSV data into the database (takes 5-15 minutes):

```powershell
docker compose --profile ingest up ingest
```

You'll see progress like:
```
🍽️  Michelin Restaurant Data Ingestion
✅ Restaurants Processed: 500+
🔢 Embeddings Created: 2000+
```

---

## STEP 8: Verify Data Ingestion

```powershell
docker compose exec api python main.py --verify
```

Expected output:
```
📊 Database Contents:
   Restaurants: 500+
   Embeddings: 2000+
```

---

## STEP 9: Start the API Server

```powershell
docker compose up -d api
```

Check all services are running:

```powershell
docker compose ps
```

Expected output:
```
NAME                STATUS
michelinbot-api     Up
michelinbot-db      Up (healthy)
```

---

## STEP 10: Test the Application

### Option A: Test with PowerShell

```powershell
# Health check
Invoke-WebRequest -Uri http://localhost:8000/health | Select-Object -ExpandProperty Content

# Chat query
$body = @{
    query = "3-star restaurants in Munich"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/chat" -Method POST -ContentType "application/json" -Body $body | Select-Object -ExpandProperty Content
```

### Option B: Use Swagger UI (Recommended)

1. Open your browser
2. Go to: **http://localhost:8000/docs**
3. Find `POST /chat` endpoint
4. Click **Try it out**
5. Enter a query and click **Execute**

---

## STEP 11: Try Example Queries

- `"3-star restaurants in Munich"`
- `"Japanese restaurants with great views"`
- `"Romantic restaurants under €€€€"`
- `"Restaurants near me"` (with location)

---

## View Logs

```powershell
# View all logs
docker compose logs -f

# View API logs only
docker compose logs -f api
```

---

## Stop Services

```powershell
docker compose down
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Port 8000 in use | Change `PORT=8001` in .env |
| API key error | Check .env file has correct key |
| No data found | Run ingestion again (STEP 7) |
| Container won't start | Run `docker compose logs api` |

---

## Quick Commands Reference

| Command | Purpose |
|---------|---------|
| `docker compose up -d` | Start all services |
| `docker compose down` | Stop all services |
| `docker compose logs -f api` | View API logs |
| `docker compose restart api` | Restart API |
| `docker compose --profile ingest up ingest` | Load data |
| `docker compose exec api python main.py --verify` | Check data |
