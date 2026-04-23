# 🍽️ MichelinBot - Assistant IA Guide Michelin

Un assistant conversationnel intelligent pour découvrir et explorer les restaurants du Guide Michelin grâce à l'IA.

[![Python](https://img.shields.io/badge/Python-3.13-blue)](https://www.python.org/)
[![Vue](https://img.shields.io/badge/Vue-3.0-green)](https://vuejs.org/)
[![Nuxt](https://img.shields.io/badge/Nuxt-3.0-green)](https://nuxt.com/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Latest-red)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-0.3-orange)](https://langchain.com/)

---

## 📖 Sommaire

- [🎯 Présentation du Produit](#-présentation-du-produit)
- [✨ Fonctionnalités](#-fonctionnalités)
- [🏗️ Architecture Technique](#-architecture-technique)
- [🧠 Composants IA & LangChain](#-composants-ia--langchain)
- [🚀 Installation](#-installation)
- [⚙️ Configuration](#️-configuration)
- [🐳 Docker](#-docker)
- [📝 Développement](#-développement)
- [🌐 Production](#-production)

---

## 🎯 Présentation du Produit

### Le Problème

Trouver un restaurant correspondant à ses envies est souvent fastidieux :
- Multiplication des formulaires et filtres sur les sites de restauration
- Recommandations génériques sans personnalisation
- Difficulté à exprimer des critères complexes (ambiance, occasion, budget...)
- Barrières linguistiques lors de voyages

### Notre Solution

**MichelinBot** est un assistant conversationnel IA qui permet de rechercher des restaurants du Guide Michelin via une conversation naturelle. L'utilisateur exprime ses besoins en langage libre, et le bot comprend le contexte, extrait les critères, et fournit des recommandations pertinentes en temps réel.

### Cas d'Usage

```
Utilisateur : "Je cherche un restaurant romantique pour un anniversaire,
             avec une vue sur la Tour Eiffel, cuisine française,
             environ 50€ par personne"

MichelinBot : [Comprend : romantique + anniversaire + vue Tour Eiffel
              + français + ~50€ + Paris]

→ Recommandations de restaurants correspondants avec détails
```

---

## ✨ Fonctionnalités

### 🗣️ Recherche en Langage Naturel

- Expressions libres sans format strict
- Compréhension des critères implicites
- Contextualisation avec la conversation précédente

### 📍 Géolocalisation Intelligente

- Détection automatique du GPS (navigateur)
- Recherche par ville, quartier ou position actuelle
- Tri par distance et pertinence

### ⭐ Filtres Michelin

- **Bib Gourmand** - Bon rapport qualité-prix
- **1-3 étoiles** - Haute cuisine
- Par type de cuisine (française, japonaise, italienne...)
- Par fourchette de prix

### 🌐 Bilingue

- Réponses entièrement en français
- Compréhension des nuances culturelles françaises
- Également disponible en anglais

### ⚡ Streaming Temps Réel

- Réponses progressives via SSE (Server-Sent Events)
- Premiers résultats en <5 secondes
- Pas de rechargement de page

### 🧠 Mémoire de Conversation

- Maintien du contexte sur plusieurs échanges
- Possibilité d'affiner les critères
- Questions de clarification si nécessaire

---

## 🏗️ Architecture Technique

```
┌─────────────────────────────────────────────────────────────┐
│                        Navigateur                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Nuxt 3 Frontend (Vue 3 + TailwindCSS)        │  │
│  │  - Interface utilisateur                             │  │
│  │  - Géolocalisation automatique                       │  │
│  │  - Affichage streaming des réponses                 │  │
│  └──────────────────────┬───────────────────────────────┘  │
└───────────────────────┼──────────────────────────────────┘
                        │ HTTP/SSE
┌───────────────────────▼──────────────────────────────────┐
│                      Nginx (Reverse Proxy)                 │
│  - /api/* → Backend                                       │
│  - /* → Frontend                                          │
│  - Configuration SSE pour streaming                       │
└───────────────────────┬──────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────┐
│                  FastAPI Backend                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │              LangGraph Workflow                     │  │
│  │                                                      │  │
│  │  1. Intent Analysis Node                           │  │
│  │     - Extraction localisation                      │  │
│  │     - Extraction cuisine, prix, étoiles            │  │
│  │     - Détermination du type de requête             │  │
│  │                                                      │  │
│  │  2. Location Search (optionnel)                    │  │
│  │     - Recherche restaurants par localisation       │  │
│  │                                                      │  │
│  │  3. Response Generation                            │  │
│  │     - Construction prompt contextuel               │  │
│  │     - Appel LLM via LangChain                       │  │
│  │     - Streaming des réponses                       │  │
│  │                                                      │  │
│  └────────────────────────────────────────────────────┘  │
│                                                           │
│  - Mémoire conversationnelle (BufferMemory)              │
│  - Rate limiting                                          │
│  - Health checks                                          │
└───────────────────────┬──────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────┐
│                    ZhipuAI LLM API                        │
│  - Modèle GLM-5.1                                         │
│  - Complétion de chat streaming                          │
└───────────────────────────────────────────────────────────┘
```

### Stack Technique

| Composant | Technologie | Rôle |
|-----------|-------------|------|
| **Frontend** | Nuxt 3 + Vue 3 | Interface utilisateur réactive |
| **Styling** | TailwindCSS | Design moderne et responsive |
| **Backend** | FastAPI | API REST et SSE streaming |
| **IA Orchestration** | LangChain + LangGraph | Workflow multi-étapes |
| **LLM** | ZhipuAI GLM-5.1 | Génération de réponses |
| **Mémoire** | LangChain BufferMemory | Historique conversation |
| **Déploiement** | Docker + Nginx | Conteneurisation et proxy |
| **Streaming** | Server-Sent Events (SSE) | Réponses temps réel |

---

## 🧠 Composants IA & LangChain

### LangGraph Workflow

Nous utilisons **LangGraph** pour orchestrer un workflow multi-étapes déterministe :

```python
┌─────────────────────────────────────────────────────────┐
│                  START                                  │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│         1. INTENT_ANALYSIS_NODE                         │
│  - Analyse la requête utilisateur                      │
│  - Extrait : localisation, cuisine, prix, étoiles      │
│  - Détecte si c'est une requête géolocalisée           │
│  - Utilise : LLM avec prompt structuré                 │
└────────────────────┬────────────────────────────────────┘
                     │
            ┌────────┴────────┐
            │                 │
      Requête          Pas de localisation
      géolocalisée      dans la requête
            │                 │
            ▼                 │
┌─────────────────────┐        │
│ 2. LOCATION_SEARCH  │        │
│   (Conditionnel)    │        │
│  - Recherche        │        │
│    restaurants      │        │
│  - Filtre par      │        │
│    localisation     │        │
└──────────┬──────────┘        │
           │                   │
           └───────┬───────────┘
                   │
┌───────────────────▼──────────────────────────────────────┐
│       3. RESPONSE_GENERATION_NODE                        │
│  - Construit le prompt contextuel                       │
│  - Inclut :                                             │
│    • Historique de conversation                         │
│    • Localisation détectée                              │
│    • Restaurants trouvés (si recherche localisée)       │
│    • Critères utilisateur                               │
│  - Appel LLM via LangChain                              │
│  - Stream la réponse                                    │
└───────────────────┬──────────────────────────────────────┘
                    │
┌───────────────────▼──────────────────────────────────────┐
│                    END                                   │
└───────────────────────────────────────────────────────────┘
```

### LangChain Components

**1. ChatPromptTemplate**

```python
# Template système avec instructions françaises
MICHELIN_GUIDE_SYSTEM_PROMPT = ChatPromptTemplate.from_messages([
    ("system", "Tu es MICHELIN_GUIDE... Toujours répondre en français"),
    ("placeholder", "{chat_history}"),
    ("human", "{query}")
])
```

**2. BufferMemory**

```python
# Mémoire conversationnelle avec InMemoryChatMessageHistory
memory = BufferMemory(
    chat_memory=InMemoryChatMessageHistory(session_id=session_id),
    return_messages=True,
    max_token_limit=4000  # Conserve ~3-4 échanges
)
```

**3. Streaming LLM Chain**

```python
# Chain avec streaming pour réponses progressives
chain = prompt | llm

# Streaming token par token
async for chunk in chain.astream(inputs):
    if isinstance(chunk, AIMessageChunk):
        yield chunk.content
```

### Workflow LangGraph

```python
# Création du graph StateGraph
workflow = StateGraph(AgentState)

# Ajout des nœuds
workflow.add_node("intent_analysis", intent_analysis_node)
workflow.add_node("location_search", location_search_node)
workflow.add_node("response_generation", response_generation_node)

# Configuration des transitions
workflow.add_conditional_edges(
    START,
    should_search_location,
    {
        "location_search": "location_search",
        "response_generation": "response_generation"
    }
)

# Compilation
app = workflow.compile()
```

### Extraction Structurée

Utilisation de **Groq** pour l'extraction de critères depuis la requête utilisateur :

```python
from langchain_groq import ChatGroq

# Extraction : localisation, cuisine, prix, étoiles
extraction_prompt = """
Extrais de cette requête :
- localisation (ville, quartier, "près de moi")
- type de cuisine
- fourchette de prix
- nombre d'étoiles Michelin

Requête : {query}
"""
```

---

## 🚀 Installation

### Prérequis

- Python 3.13+
- Node.js 20+
- Docker & Docker Compose (optionnel)

### Backend

```bash
cd michelin-bot

# Créer environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Installer dépendances
pip install -r requirements.txt

# Configurer
cp .env.example .env
# Éditer .env avec votre clé API ZhipuAI

# Lancer
uvicorn app:app --reload
```

### Frontend

```bash
cd michelin-front

# Installer dépendances
npm install

# Développement
npm run dev

# Build production
npm run build
```

---

## ⚙️ Configuration

### Variables d'Environnement

**Backend (`michelin-bot/.env`) :**

```bash
# ZhipuAI API (requis)
ZHIPUAI_API_KEY=votre_clé_ici

# API
HOST=0.0.0.0
PORT=8000
DEBUG=false

# LLM
LLM_MODEL=glm-5.1
LLM_TEMPERATURE=0.7
LLM_MAX_TOKENS=2000
API_BASE_URL=https://api.z.ai/api/coding/paas/v4

# CORS (séparer par virgule)
ALLOWED_ORIGINS=http://localhost:3000,http://localhost

# Rate limiting
RATE_LIMIT_REQUESTS_PER_MINUTE=60
```

**Frontend (`michelin-front/.env`) :**

```bash
# URL de l'API (nginx route /api vers le backend)
NUXT_PUBLIC_API_BASE_URL=http://localhost
```

---

## 🐳 Docker

### Développement

```bash
docker-compose up --build
```

### Production

```bash
# Configurer .env.prod
cp .env.prod.example .env.prod
# Éditer avec vos valeurs

# Lancer production
docker compose -f docker-compose.prod.yml --env-file .env.prod up --build -d
```

---

## 📝 Développement

### Structure du Projet

```
guide-michelin/
├── michelin-bot/              # Backend FastAPI
│   ├── app.py                 # Entry point API
│   ├── config.py              # Configuration
│   ├── database.py            # Données restaurants
│   ├── llm.py                 # Client LLM ZhipuAI
│   ├── langgraph_workflow.py   # Workflow IA
│   ├── langgraph_state.py     # État du workflow
│   ├── langgraph_streaming.py # Streaming SSE
│   ├── prompts.py             # Templates prompts
│   ├── models.py              # Schémas Pydantic
│   ├── embeddings.py          # Embeddings (non utilisé)
│   ├── agent.py               # Agent legacy (non utilisé)
│   ├── ingest.py              # Ingestion données
│   ├── geolocation.py         # Géolocalisation
│   ├── sse_events.py          # Events SSE
│   ├── requirements.txt       # Dépendances Python
│   ├── Dockerfile             # Image Docker
│   └── .env.example           # Template variables
│
├── michelin-front/            # Frontend Nuxt 3
│   ├── app/
│   │   ├── pages/             # Pages (index, chat, about)
│   │   ├── components/        # Composants Vue
│   │   ├── composables/       # Composables Nuxt
│   │   │   ├── useChatStream.ts    # Streaming chat
│   │   │   └── useGeolocation.ts   # Géolocalisation
│   │   └── assets/            # Assets statiques
│   ├── nuxt.config.ts         # Configuration Nuxt
│   ├── package.json           # Dépendances Node
│   ├── Dockerfile             # Image Docker
│   └── .env.example           # Template variables
│
├── nginx/                     # Configuration Nginx
│   └── nginx.conf             # Reverse proxy + SSE
│
├── docker-compose.yml         # Développement
├── docker-compose.prod.yml    # Production
├── .env.prod                  # Variables production
├── .gitignore                 # Fichiers ignorés
├── README.md                  # Ce fichier
├── PITCH.md                   # Présentation projet
└── PITCH_FR.md                # Présentation (FR)
```

### Principaux Fichiers IA

| Fichier | Contenu |
|---------|---------|
| `langgraph_workflow.py` | Workflow complet LangGraph avec 3 nœuds |
| `langgraph_state.py` | État AgentState (messages, localisation, résultats) |
| `langgraph_streaming.py` | Génération events SSE pour streaming frontend |
| `prompts.py` | Templates système et exemples en français |
| `llm.py` | Client ZhipuAI avec configuration |

---

## 🌐 Production

### Déploiement VPS

Voir `PRODUCTION_DEPLOYMENT.md` pour le guide complet.

**Résumé :**

1. Cloner le repository
2. Configurer `.env.prod` avec clé API et domaine
3. Lancer : `docker compose -f docker-compose.prod.yml --env-file .env.prod up --build -d`
4. (Optionnel) Configurer SSL avec Certbot

### Health Check

```bash
curl http://your-domain/health
```

Réponse attendue :
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "llm_configured": true
}
```

---

## 🧪 Tests

### Test API

```bash
# Health
curl http://localhost:8000/health

# Chat simple
curl "http://localhost:8000/chat/stream?query=restaurants+parisiens"

# Avec localisation
curl "http://localhost:8000/chat/stream?query=restaurants+proches&user_lat=48.85&user_lon=2.35"
```

### Test Frontend

Ouvrir `http://localhost:3000` dans le navigateur.

---

## 🤝 Contribution

Ce projet a été développé pour le hackathon ESGI.


### Stack

- **Frontend :** Vue 3, Nuxt 3, TailwindCSS
- **Backend :** Python, FastAPI, LangChain, LangGraph
- **IA :** ZhipuAI GLM-5.1
- **DevOps :** Docker, Nginx

---


---

## 🔮 Roadmap

- [ ] Intégration vrais menus restaurants
- [ ] Réservation en ligne
- [ ] Photos restaurants
- [ ] Avis utilisateurs
- [ ] Apprentissage préférences utilisateur
- [ ] Application mobile
