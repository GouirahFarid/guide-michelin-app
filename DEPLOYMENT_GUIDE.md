# MichelinBot - Complete Setup Guide

Step-by-step instructions to make the app fully functional.

---

## Prerequisites Checklist

- [ ] Docker Desktop installed and running
- [ ] Zhipu AI API key
- [ ] At least 4GB RAM available for Docker
- [ ] Windows PowerShell or Terminal

---

## 🔒 Security Best Practices

Before deploying, consider these security recommendations:

1. **Change Default Passwords**: In production, change the default PostgreSQL password
2. **Configure CORS**: Set `ALLOWED_ORIGINS` to your actual frontend domain
3. **Use Environment Variables**: Never commit `.env` file to version control
4. **API Key Security**: Rotate your Zhipu AI API key regularly
5. **Rate Limiting**: Consider adding rate limiting for production use

---

## STEP 1: Get Zhipu AI API Key

### 1.1 Register Account

1. Go to: **https://open.bigmodel.cn/**
2. Click **Register** (注册)
3. Sign up with phone number or email

### 1.2 Get API Key

1. Login to your account
2. Go to **API Keys** section
3. Click **Create API Key**
4. **Copy the key** (format: `id.secret`)

```
Example: a1b2c3d4.abcdef1234567890
```

---

## STEP 2: Create Environment File

### 2.1 Create `.env` File

In the project folder (`C:\Users\farid\PycharmProjects\LLM\MichlenBot\`), create a file named `.env`:

```powershell
# Open PowerShell in project folder
cd C:\Users\farid\PycharmProjects\LLM\MichlenBot

# Create .env file
notepad .env
```

### 2.2 Paste Configuration

```env
# Zhipu AI (GLM-4) API Key - REPLACE WITH YOUR KEY
ZHIPUAI_API_KEY=your_actual_api_key_here

# Database (Docker - configure for production)
POSTGRES_DB=michelin_db
POSTGRES_USER=michelin_user
POSTGRES_PASSWORD=root  # CHANGE THIS IN PRODUCTION!

# Server
HOST=0.0.0.0
PORT=8000

# CORS - Configure your allowed origins
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:8000

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# RAG Settings
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K_RETRIEVAL=5
```

### 2.3 Save and Close

Save the file and close Notepad.

---

## STEP 3: Verify CSV File Exists

### 3.1 Check File Location

```powershell
# Check if CSV exists in project folder
Test-Path "C:\Users\farid\PycharmProjects\LLM\MichlenBot\michelin_my_maps.csv"
```

Expected output: `True`

If `False`, make sure `michelin_my_maps.csv` is in the project folder.

---

## STEP 4: Start PostgreSQL (Docker)

### 4.1 Start Docker Desktop

Make sure Docker Desktop is running on Windows.

### 4.2 Launch PostgreSQL Container

```powershell
cd C:\Users\farid\PycharmProjects\LLM\MichlenBot

# Start only PostgreSQL first
docker compose up -d postgres
```

### 4.3 Verify PostgreSQL is Running

```powershell
# Check container status
docker compose ps
```

Expected output:
```
NAME                STATUS
michelinbot-db      Up (healthy)
```

### 4.4 Test Database Connection (Optional)

```powershell
# Connect to PostgreSQL
docker compose exec postgres psql -U michelin_user -d michelin_db

# You should see psql prompt:
# michelin_db=#

# Exit by typing: \q
```

---

## STEP 5: Initialize Database Schema

### 5.1 Run Database Initialization

```powershell
# This will create tables and enable pgvector extension
docker compose exec api python -c "
import asyncio
from database import init_database
asyncio.run(init_database())
print('Database initialized!')
"
```

Expected output:
```
Database initialized successfully!
```

---

## STEP 6: Ingest Restaurant Data

### 6.1 Run Data Ingestion

```powershell
# Start ingestion (this may take 5-15 minutes)
docker compose --profile ingest up ingest
```

### 6.2 Monitor Progress

You should see progress like:
```
🍽️  Michelin Restaurant Data Ingestion
📁 CSV Path: michelin_my_maps.csv
🔧 Chunk Size: 500, Overlap: 50
--------------------------------------------------
📊 Initializing database...
✅ Database initialized
📖 Loading data from michelin_my_maps.csv...

📦 Processing batch 1 (50 restaurants)...
 100%|████████████████| 50/50
   ✅ Processed: 50/50 restaurants

...
--------------------------------------------------
📊 INGESTION SUMMARY
==================================================
✅ Restaurants Processed: [number]
➕ Restaurants Added: [number]
🔢 Embeddings Created: [number]
⏱️  Duration: [seconds]
```

### 6.3 Verify Ingestion

```powershell
docker compose exec api python main.py --verify
```

Expected output:
```
🔍 Verifying installation...
✅ Database initialized

📊 Database Contents:
   Restaurants: [number > 0]
   Embeddings: [number > 0]

🏆 Award Distribution:
   3 Stars: [number]
   2 Stars: [number]
   1 Star: [number]
   ...
```

---

## STEP 7: Start the API Server

### 7.1 Build and Start API

```powershell
# Build the API container
docker compose build api

# Start the API
docker compose up -d api
```

### 7.2 Check All Services

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

## STEP 8: Test the Application

### 8.1 Health Check

```powershell
# PowerShell
Invoke-WebRequest -Uri http://localhost:8000/health | Select-Object -ExpandProperty Content
```

Expected output:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database_connected": true,
  "embedding_model_loaded": true,
  "llm_configured": true,
  "uptime_seconds": ...
}
```

### 8.2 Open API Documentation

Open your browser and go to:
```
http://localhost:8000/docs
```

You should see the interactive Swagger UI.

---

## STEP 9: Test Chat Endpoint

### 9.1 Test Simple Query (PowerShell)

```powershell
# Test 1: Basic query
$body = @{
    query = "3-star restaurants in Munich"
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://localhost:8000/chat" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body | Select-Object -ExpandProperty Content
```

### 9.2 Test Geolocation Query

```powershell
# Test 2: Location-based query
$body = @{
    query = "Restaurants near me"
    user_location = @{
        latitude = 48.1351
        longitude = 11.5820
    }
} | ConvertTo-Json -Depth 3

Invoke-WebRequest -Uri "http://localhost:8000/chat" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body | Select-Object -ExpandProperty Content
```

### 9.3 Test with Filters

```powershell
# Test 3: With filters
$body = @{
    query = "Fine dining restaurants"
    filters = @{
        award = "3 Stars"
        cuisine = "Japanese"
    }
} | ConvertTo-Json -Depth 3

Invoke-WebRequest -Uri "http://localhost:8000/chat" `
  -Method POST `
  -ContentType "application/json" `
  -Body $body | Select-Object -ExpandProperty Content
```

---

## STEP 10: Test Using Swagger UI

### 10.1 Open Swagger UI

Navigate to: **http://localhost:8000/docs**

### 10.2 Try Chat Endpoint

1. Find `POST /chat` endpoint
2. Click **Try it out**
3. Enter a query:
   ```json
   {
     "query": "Romantic restaurants with great views in Germany"
   }
   ```
4. Click **Execute**
5. View the response

---

## Troubleshooting

### Problem: Port 8000 Already in Use

```powershell
# Find what's using port 8000
netstat -ano | findstr :8000

# Kill the process (replace PID)
taskkill /PID [PID] /F
```

### Problem: Container Won't Start

```powershell
# View detailed logs
docker compose logs api

# Rebuild without cache
docker compose build --no-cache api
docker compose up -d
```

### Problem: API Key Error

```powershell
# Verify .env file exists
Get-Content .env

# Check ZHIPUAI_API_KEY is set correctly
# No extra spaces, correct format
```

### Problem: Database Connection Failed

```powershell
# Restart PostgreSQL
docker compose restart postgres

# Wait for healthy status
docker compose ps postgres
```

### Problem: No Data in Response

```powershell
# Verify data was ingested
docker compose exec api python main.py --verify

# Re-run ingestion if needed
docker compose --profile ingest up ingest --force-recreate
```

---

## View Logs

### All Services
```powershell
docker compose logs -f
```

### API Only
```powershell
docker compose logs -f api
```

### Database Only
```powershell
docker compose logs -f postgres
```

---

## Stop Services

```powershell
# Stop all services
docker compose down

# Stop and remove volumes (deletes data!)
docker compose down -v
```

---

## Quick Reference Commands

| Command | Purpose |
|---------|---------|
| `docker compose up -d` | Start all services |
| `docker compose down` | Stop all services |
| `docker compose logs -f api` | View API logs |
| `docker compose restart api` | Restart API |
| `docker compose exec api python main.py --verify` | Verify data |
| `docker compose --profile ingest up ingest` | Load data |

---

## Next Steps

Once everything is running:

1. **Try the Swagger UI** at http://localhost:8000/docs
2. **Test different queries**:
   - `"Best sushi restaurants in Tokyo"`
   - `"3-star restaurants with gardens"`
   - `"Romantic dinner spots under €€€€"`
3. **Explore the API documentation** in `/docs`

---

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ZHIPUAI_API_KEY not set` | Check `.env` file exists and has your key |
| `Database connection failed` | Ensure PostgreSQL container is running |
| `No restaurants found` | Run ingestion: `docker compose --profile ingest up ingest` |
| `Port 8000 in use` | Change port in `docker-compose.yml` or stop conflicting app |
| `Container exits immediately` | Check logs: `docker compose logs api` |
