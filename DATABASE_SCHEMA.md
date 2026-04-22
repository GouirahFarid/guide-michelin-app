# Database Schema Documentation

## Overview

MichelinBot uses **PostgreSQL** with the **pgvector** extension for vector similarity search. The database stores restaurant information from the Michelin Guide and their vector embeddings for semantic search.

---

## Database Extensions

| Extension | Purpose |
|-----------|---------|
| `pgvector` | Enables vector data type and similarity search operations |

---

## Tables

### 1. `users`

User accounts for the application (proposed schema).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique user identifier |
| `username` | VARCHAR(50) | UNIQUE, NOT NULL | Login username |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL | User email address |
| `password_hash` | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| `role_id` | INTEGER | FOREIGN KEY → roles(id) | User role reference |
| `is_active` | BOOLEAN | DEFAULT TRUE | Account active status |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Account creation date |
| `updated_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Last update timestamp |
| `last_login` | TIMESTAMP | NULLABLE | Last login timestamp |

#### Indexes
```sql
CREATE UNIQUE INDEX idx_users_username ON users(username);
CREATE UNIQUE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role_id ON users(role_id);
```

---

### 2. `roles`

User role definitions for access control (proposed schema).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique role identifier |
| `name` | VARCHAR(50) | UNIQUE, NOT NULL | Role name (e.g., 'admin', 'user', 'moderator') |
| `description` | TEXT | NULLABLE | Role description |
| `permissions` | JSONB | DEFAULT '{}' | Role permissions as JSON |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |

#### Default Roles
| Role | Permissions |
|------|-------------|
| `admin` | Full access to all resources |
| `user` | Search restaurants, view recommendations |
| `moderator` | Edit restaurant information, manage reviews |

#### Indexes
```sql
CREATE UNIQUE INDEX idx_roles_name ON roles(name);
```

---

### 3. `restaurants`

Core restaurant data from Michelin Guide.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique restaurant identifier |
| `name` | TEXT | NOT NULL | Restaurant name |
| `address` | TEXT | NULLABLE | Street address |
| `location` | TEXT | NULLABLE | City/region name |
| `price` | VARCHAR(10) | NULLABLE | Price level (€, €€, €€€, €€€€) |
| `cuisine` | TEXT | NULLABLE | Cuisine type(s) |
| `longitude` | FLOAT | NULLABLE | GPS longitude |
| `latitude` | FLOAT | NULLABLE | GPS latitude |
| `phone_number` | TEXT | NULLABLE | Contact phone |
| `url` | TEXT | NULLABLE | Michelin Guide URL |
| `website_url` | TEXT | NULLABLE | Restaurant website |
| `award` | TEXT | NULLABLE | Michelin award level |
| `green_star` | BOOLEAN | DEFAULT FALSE | Sustainable gastronomy recognition |
| `facilities_and_services` | TEXT | NULLABLE | Additional facilities info |
| `description` | TEXT | NULLABLE | Restaurant description |

#### Award Values
- `3 Stars` - Exceptional cuisine, worth a special journey
- `2 Stars` - Excellent cuisine, worth a detour
- `1 Star` - Very good cuisine in its category
- `Bib Gourmand` - Good quality at moderate prices
- `Selected Restaurants` - Quality ingredients and cooking

#### Indexes
```sql
CREATE INDEX idx_restaurants_location ON restaurants(location);
CREATE INDEX idx_restaurants_award ON restaurants(award);
CREATE INDEX idx_restaurants_cuisine ON restaurants(cuisine);
CREATE INDEX idx_restaurants_coordinates ON restaurants(latitude, longitude) WHERE latitude IS NOT NULL;
```

---

### 4. `restaurant_embeddings`

Vector embeddings for semantic search using pgvector.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | SERIAL | PRIMARY KEY | Unique embedding identifier |
| `restaurant_id` | INTEGER | FOREIGN KEY → restaurants(id) ON DELETE CASCADE | Reference to restaurant |
| `chunk_text` | TEXT | NOT NULL | Text chunk that was embedded |
| `embedding` | VECTOR(384) | NOT NULL | 384-dimensional vector (all-MiniLM-L6-v2) |
| `metadata` | JSONB | NULLABLE | Additional metadata about the chunk |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Embedding creation time |

#### Vector Index (HNSW)
```sql
CREATE INDEX idx_embeddings_hnsw 
ON restaurant_embeddings 
USING hnsw (embedding vector_cosine_ops) 
WITH (m = 16, ef_construction = 64);
```

**Index Parameters:**
- `m = 16`: Number of bidirectional links per node
- `ef_construction = 64`: Size of dynamic candidate list during construction

---

## Entity Relationship Diagram

```
┌─────────────┐         ┌─────────────┐
│    roles    │1       *│    users    │
│─────────────│─────────│─────────────│
│ id (PK)     │         │ id (PK)     │
│ name        │         │ username    │
│ permissions │         │ email       │
└─────────────┘         │ role_id (FK)│
                        │ is_active   │
                        └──────┬───────┘
                               │
                               │ (not yet implemented)
                               ▼
                        ┌───────────────┐
                        │  user_queries │
                        │───────────────│
                        │ id (PK)       │
                        │ user_id (FK)  │
                        │ query_text    │
                        └───────────────┘

┌───────────────┐1               *┌─────────────────────────┐
│  restaurants  │─────────────────│ restaurant_embeddings   │
│───────────────│                 │─────────────────────────│
│ id (PK)       │                 │ id (PK)                 │
│ name          │                 │ restaurant_id (FK)      │
│ location      │                 │ chunk_text              │
│ cuisine       │                 │ embedding (vector)      │
│ award         │                 │ metadata (JSONB)        │
│ latitude      │                 └─────────────────────────┘
│ longitude     │
└───────────────┘
```

---

## SQL Schema Creation Script

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create roles table
CREATE TABLE IF NOT EXISTS roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    permissions JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role_id INTEGER REFERENCES roles(id) ON DELETE SET NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Create restaurants table
CREATE TABLE IF NOT EXISTS restaurants (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    location TEXT,
    price VARCHAR(10),
    cuisine TEXT,
    longitude FLOAT,
    latitude FLOAT,
    phone_number TEXT,
    url TEXT,
    website_url TEXT,
    award TEXT,
    green_star BOOLEAN DEFAULT FALSE,
    facilities_and_services TEXT,
    description TEXT
);

-- Create restaurant_embeddings table
CREATE TABLE IF NOT EXISTS restaurant_embeddings (
    id SERIAL PRIMARY KEY,
    restaurant_id INTEGER REFERENCES restaurants(id) ON DELETE CASCADE,
    chunk_text TEXT NOT NULL,
    embedding vector(384),
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for roles
CREATE UNIQUE INDEX IF NOT EXISTS idx_roles_name ON roles(name);

-- Create indexes for users
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_role_id ON users(role_id);

-- Create indexes for restaurants
CREATE INDEX IF NOT EXISTS idx_restaurants_location ON restaurants(location);
CREATE INDEX IF NOT EXISTS idx_restaurants_award ON restaurants(award);
CREATE INDEX IF NOT EXISTS idx_restaurants_cuisine ON restaurants(cuisine);
CREATE INDEX IF NOT EXISTS idx_restaurants_coordinates 
    ON restaurants(latitude, longitude) 
    WHERE latitude IS NOT NULL;

-- Create HNSW index for vector similarity search
CREATE INDEX IF NOT EXISTS idx_embeddings_hnsw
    ON restaurant_embeddings 
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

---

## Vector Operations

### Cosine Similarity Search

```sql
-- Search for similar restaurant chunks
SELECT 
    re.id,
    re.restaurant_id,
    re.chunk_text,
    r.name,
    r.location,
    r.cuisine,
    1 - (re.embedding <=> '[<query_vector>]'::vector) as similarity
FROM restaurant_embeddings re
JOIN restaurants r ON re.restaurant_id = r.id
ORDER BY re.embedding <=> '[<query_vector>]'::vector
LIMIT 5;
```

### Insert Embedding

```sql
-- Insert a new embedding vector
INSERT INTO restaurant_embeddings (restaurant_id, chunk_text, embedding)
VALUES (
    123,
    'Excellent modern cuisine with local ingredients',
    '[0.1, -0.2, 0.3, ...]'::vector
);
```

---

## Migration Status

| Table | Status | Notes |
|-------|--------|-------|
| `restaurants` | ✅ Implemented | In `database.py` |
| `restaurant_embeddings` | ✅ Implemented | In `database.py` |
| `users` | ❌ Not Implemented | Proposed for future |
| `roles` | ❌ Not Implemented | Proposed for future |

---

## Future Enhancements

1. **User Favorites**: Add `user_favorites` junction table
2. **User Reviews**: Add reviews and ratings system
3. **Query History**: Track user search history for personalization
4. **Sessions**: Store conversation sessions
5. **Audit Logs**: Track changes to restaurant data

---

## Database Connection

**Connection String Format:**
```
postgresql+psycopg://username:password@host:port/database
```

**Example (.env):**
```
DATABASE_URL=postgresql+psycopg://michelin_user:password@localhost:5432/michelin_db
```

---

## Maintenance Commands

```sql
-- Analyze tables for query optimization
ANALYZE restaurants;
ANALYZE restaurant_embeddings;

-- Reindex HNSW index (maintenance)
REINDEX INDEX CONCURRENTLY idx_embeddings_hnsw;

-- Check table sizes
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE tablename LIKE '%restaurant%'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Vector similarity stats
SELECT 
    COUNT(*) as total_embeddings,
    pg_size_pretty(pg_total_relation_size('restaurant_embeddings')) as table_size
FROM restaurant_embeddings;
```
