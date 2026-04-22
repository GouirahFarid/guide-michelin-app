# Changelog

All notable changes to MichelinBot will be documented in this file.

## [Unreleased] - 2026-04-22

### Security Fixes
- **CORS Configuration**: Changed from `allow_origins=["*"]` to environment-based configuration via `ALLOWED_ORIGINS`
- **Database Password**: Changed from hardcoded password to environment variable `POSTGRES_PASSWORD`
- **Error Handling**: Stack traces no longer exposed to API clients
- **SQL Injection Prevention**: Verified parameterized queries are used throughout

### Bug Fixes
- **Duplicate CITY_COORDINATES**: Removed duplicate dictionary in `prompts.py`, now imports from `geolocation.py`
- **Session Memory Leak**: Added session timestamp tracking and cleanup function with 1-hour timeout
- **Query Mutation**: Removed side-effect that modified user query in agent.py
- **Stub Classes**: Removed empty `UserLocation` and `SearchFilters` class stubs, using forward references instead
- **API Timeouts**: Added default 30-second timeout to all Zhipu AI API calls

### Performance Improvements
- **Vector Index**: Changed from IVFFlat to HNSW index for better query performance
- **Connection Pooling**: Improved database connection error handling
- **Health Check**: Now actually verifies database connection instead of returning hardcoded `True`

### Code Quality
- **Type Hints**: Added `from __future__ import annotations` for better forward reference support
- **Logging**: Added structured logging throughout the application
- **Docker Compatibility**: Removed interactive `input()` calls that would hang in Docker
- **Docker Compose**: Added health checks, restart policies, and environment variable support
- **Unused Imports**: Removed unused `asyncio` import from llm.py
- **System Prompt**: Agent now uses `MICHELIN_GUIDE_SYSTEM_PROMPT` from prompts.py instead of hardcoded string

### New Features
- **Session Cleanup**: Automatic cleanup of expired sessions
- **Non-Interactive Mode**: Added `--start-after-ingest` flag for Docker/Ci environments
- **Environment Configuration**: Added `ALLOWED_ORIGINS`, `API_TIMEOUT`, and database configuration options
- **Testing Infrastructure**: Added basic test suite with pytest fixtures

### Documentation
- **Security Section**: Added security best practices to DEPLOYMENT_GUIDE.md
- **Environment Variables**: Updated .env.example with all new configuration options

### Breaking Changes
- **Environment Variables**: `POSTGRES_PASSWORD` and `ALLOWED_ORIGINS` now required for Docker deployment
- **Session Management**: Sessions now expire after 1 hour of inactivity

---

## [1.0.0] - Initial Release

### Features
- RAG-powered restaurant recommendations
- Geolocation-based search with Haversine distance
- LangGraph agent workflow orchestration
- GLM-4 LLM integration
- PostgreSQL + pgvector for vector storage
- Local embeddings with sentence-transformers
- FastAPI REST API
- Docker Compose deployment
