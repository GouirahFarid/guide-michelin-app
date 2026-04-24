# Documentation Technique & Fonctionnelle — Guide Michelin AI Frontend

> Hackaton Skolae 2026 · ICAN / ESGI / ECITV / EFET CREA

---

## Table des matières

1. [Contexte & Problématique](#1-contexte--problématique)
2. [Solution apportée par le projet](#2-solution-apportée-par-le-projet)
3. [Vue d'ensemble du projet](#3-vue-densemble-du-projet)
4. [Architecture technique](#4-architecture-technique)
5. [Structure des fichiers](#5-structure-des-fichiers)
6. [Organisation des composants](#6-organisation-des-composants)
7. [Pages & Routing](#7-pages--routing)
8. [Gestion d'état](#8-gestion-détat)
9. [Flux de données & Communication avec le backend](#9-flux-de-données--communication-avec-le-backend)
10. [Système de design & Charte graphique](#10-système-de-design--charte-graphique)
11. [TypeScript — Interfaces & Types](#11-typescript--interfaces--types)
12. [Dépendances](#12-dépendances)
13. [Déploiement & Configuration](#13-déploiement--configuration)
14. [État d'avancement & Pistes d'évolution](#14-état-davancement--pistes-dévolution)

---

## 1. Contexte & Problématique

### Le Guide Michelin en 2026

Fondé en 1900 par André et Édouard Michelin, le Guide Michelin est historiquement la référence mondiale de la gastronomie.

### La Problématique

> **"Comment le Guide Michelin peut-il regagner du terrain face aux réseaux sociaux, aux plateformes et aux influenceurs, pour conquérir un marché plus jeune et redevenir le guide prescripteur de référence ?"**

L'émergence d'acteurs numériques (TripAdvisor, The Fork, Le Fooding, influenceurs food, réseaux sociaux) a fragmenté la prescription gastronomique et éloigné le public jeune du guide rouge.

---

## 2. Solution apportée par le projet

### Positionnement

`michelin-front` est une **interface conversationnelle mobile-first** qui repositionne le Guide Michelin comme un outil de recommandation quotidien, accessible, personnalisé et moderne — répondant directement à la problématique du hackaton.

### Réponse aux enjeux identifiés

| Problème                                        | Solution implémentée                                          |
| ----------------------------------------------- | ------------------------------------------------------------- |
| Guide perçu comme élitiste et difficile d'accès | Interface conversationnelle intuitive en langage naturel      |
| Perte de pertinence face aux influenceurs       | Assistant IA qui dialogue comme un expert de confiance        |
| Public jeune peu engagé                         | UX mobile-first avec navigation                               |
| Manque de dynamisme face aux réseaux sociaux    | Streaming temps réel des réponses (SSE) pour un effet vivant  |
| Complexité de la sélection Michelin             | Cards restaurants enrichies avec badge, award, prix, distance |

### Concept central : l'assistant gastronomique IA

L'utilisateur peut poser des questions en langage naturel ("un restaurant étoilé à moins de 5km avec de la cuisine japonaise") et recevoir en temps réel :

- Une **analyse de sa requête** (lieu détecté, cuisine, distinction)
- Des **fiches restaurant** structurées et enrichies
- Un **texte de réponse streamé** avec contexte gastronomique
- Une **continuité de session** pour un dialogue naturel

Cette approche transforme le Guide Michelin d'un annuaire consulté passivement en un **compagnon gastronomique interactif**.

---

## 3. Vue d'ensemble du projet

| Attribut            | Valeur                                     |
| ------------------- | ------------------------------------------ |
| **Nom**             | michelin-front                             |
| **Type**            | Application web mobile-first (SPA/SSR)     |
| **Framework**       | Nuxt 4.4.2 + Vue 3                         |
| **Langage**         | TypeScript                                 |
| **Build tool**      | Vite (intégré Nuxt)                        |
| **Package manager** | npm                                        |
| **Backend attendu** | API REST + SSE sur `http://localhost:8000` |
| **Port dev**        | 3000                                       |
| **Déploiement**     | Docker                                     |

---

## 4. Architecture technique

### Vue d'ensemble

```
┌─────────────────────────────────────────────────────────┐
│                    NAVIGATEUR / MOBILE                   │
│                                                         │
│  ┌──────────────────────────────────────────────────┐   │
│  │                  Nuxt 4 (Vue 3)                  │   │
│  │                                                  │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  │   │
│  │  │  app.vue   │  │ default.vue│  │  Pages     │  │   │
│  │  │  (root)    │  │ (layout)   │  │  (routes)  │  │   │
│  │  └────────────┘  └────────────┘  └────────────┘  │   │
│  │                                                  │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │             Composables (logique)           │  │   │
│  │  │         useChatStream.ts (SSE client)       │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  │                                                  │   │
│  │  ┌────────────────────────────────────────────┐  │   │
│  │  │           Composants réutilisables          │  │   │
│  │  │  BadgeCard │ ChatWidget │ CreatorCard │ ... │  │   │
│  │  └────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────┘   │
│                          │ fetch SSE                     │
│  ┌───────────────────────▼──────────────────────────┐   │
│  │         Proxy Vite → http://localhost:8000        │   │
│  │         /api/chat/stream?query=...                │   │
│  └──────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
                          │
            ┌─────────────▼──────────────┐
            │      Backend Python        │
            │   (FastAPI / autre)        │
            │  SSE streaming endpoint    │
            └────────────────────────────┘
```

### Pattern architectural

Le projet suit une architecture **Feature-per-Page** avec des composables partagés :

- **Pages** : chaque route est une unité autonome
- **Composables** : logique métier réutilisable extraite des composants
- **Composants** : UI découplée de la logique, props-driven
- **Layout** : navigation commune injectée via `default.vue`

---

## 5. Structure des fichiers

```
michelin-front/
├── app/                            # Code source principal
│   ├── app.vue                     # Racine de l'application (NuxtPage + ChatWidget global)
│   ├── assets/
│   │   └── css/
│   │       └── main.css            # Tailwind CSS + Nuxt UI + variables CSS marque
│   │
│   ├── components/                 # Composants réutilisables
│   │   ├── BadgeCard.vue           # Affichage des badges/récompenses
│   │   ├── ChatWidget.vue          # Widget chat flottant (disponible sur toutes les pages)
│   │   ├── CreatorCard.vue         # Carte profil créateur de contenu
│   │   ├── MenuItem.vue            # Élément de menu dans les paramètres profil
│   │   ├── NavBar.vue              # Barre de navigation (legacy, non utilisée)
│   │   ├── StatCard.vue            # Carte statistiques profil utilisateur
│   │   └── TasteTag.vue            # Tag de préférence gustative
│   │
│   ├── composables/
│   │   └── useChatStream.ts        # Client SSE — cœur de la logique IA
│   │
│   ├── layouts/
│   │   └── default.vue             # Layout avec bottom navigation fixe
│   │
│   └── pages/                      # Routing file-based (auto-routing Nuxt)
│       ├── index.vue               # / — Landing page
│       ├── chat/
│       │   └── index.vue           # /chat — Interface chat plein écran
│       ├── assistant/
│       │   └── index.vue           # /assistant — Assistant IA (page dédiée)
│       ├── explore/
│       │   └── index.vue           # /explore — Exploration restaurants
│       ├── creators/
│       │   └── index.vue           # /creators — Profils créateurs
│       └── profile/
│           └── index.vue           # /profile — Profil utilisateur
│
├── public/                         # Assets statiques servis directement
├── nuxt.config.ts                  # Configuration Nuxt (proxy, modules, runtime)
├── tsconfig.json                   # Configuration TypeScript
├── eslint.config.mjs               # Linting
├── Dockerfile                      # Image Docker production
├── .env.example                    # Template variables d'environnement
├── package.json                    # Dépendances & scripts
├── LOGO_GUIDE.md                   # Guide des assets marque
└── README.md                       # Documentation rapide
```

---

## 6. Organisation des composants

### Arbre de composants

```
app.vue (racine)
├── <NuxtLayout> (default.vue)
│   ├── <slot /> → <NuxtPage> (page active)
│   │   ├── pages/index.vue
│   │   ├── pages/chat/index.vue
│   │   │   └── useChatStream() [composable]
│   │   ├── pages/assistant/index.vue
│   │   ├── pages/explore/index.vue
│   │   ├── pages/creators/index.vue
│   │   │   └── <CreatorCard /> (×N)
│   │   └── pages/profile/index.vue
│   │       ├── <StatCard /> (×3)
│   │       ├── <BadgeCard /> (×N)
│   │       ├── <TasteTag /> (×N)
│   │       └── <MenuItem /> (×N)
│   └── [Bottom Navigation Bar]
│       └── <NuxtLink> (×5 routes)
│
└── <ChatWidget /> (global, Teleport → <body>)
    ├── Bouton flottant (toggle)
    └── Panel chat
        ├── Header
        ├── Liste messages (scroll)
        │   ├── Message utilisateur
        │   └── Message assistant
        │       ├── Texte streamé (markdown)
        │       ├── Query analysis chips
        │       ├── Progress bar
        │       └── RestaurantCard (×N)
        └── Input + bouton envoi
```

### Catalogue des composants

#### `ChatWidget.vue`

**Type** : Feature component (logique + UI)
**Rôle** : Widget de chat flottant disponible sur toutes les pages. Gère l'état de visibilité, l'historique des messages, le streaming SSE et le rendu des cards restaurants.
**Props** : `buttonClass?`, `icon?`
**État interne** : `isOpen`, `messages[]`, `sessionId`, `isLoading`, `form`
**Dépendance** : `useChatStream` composable

#### `CreatorCard.vue`

**Type** : Presentational component
**Rôle** : Affiche la carte d'un créateur de contenu (influenceur food, chef, chroniqueur) avec avatar, stats, spécialités.

#### `BadgeCard.vue`

**Type** : Presentational component
**Rôle** : Affiche un badge/récompense utilisateur (gamification du profil).
**Props** : `icon`, `title`, `subtitle`, `active`

#### `StatCard.vue`

**Type** : Presentational component
**Rôle** : Carte statistique sur la page profil (restaurants visités, étoiles vues, etc.)

#### `TasteTag.vue`

**Type** : Presentational component
**Rôle** : Tag de préférence culinaire (japonais, végétarien, bistrots, etc.)

#### `MenuItem.vue`

**Type** : Presentational component
**Rôle** : Ligne de menu avec icône pour les paramètres du profil.

---

## 7. Pages & Routing

### Configuration

Nuxt 4 utilise le **file-based routing** : la structure du dossier `pages/` génère automatiquement les routes Vue Router.

```typescript
// nuxt.config.ts
pages: true;
```

### Table des routes

| Route        | Fichier                     | Rôle                                                                 | Statut       |
| ------------ | --------------------------- | -------------------------------------------------------------------- | ------------ |
| `/`          | `pages/index.vue`           | Landing page — présentation de l'assistant IA et des fonctionnalités | Fonctionnel  |
| `/chat`      | `pages/chat/index.vue`      | Interface chat plein écran avec streaming SSE                        | Fonctionnel  |
| `/assistant` | `pages/assistant/index.vue` | Page assistant IA dédiée                                             | UI partielle |
| `/explore`   | `pages/explore/index.vue`   | Navigation dans la sélection restaurants                             | Squelette UI |
| `/creators`  | `pages/creators/index.vue`  | Profils des créateurs de contenu                                     | Squelette UI |
| `/profile`   | `pages/profile/index.vue`   | Profil utilisateur avec statistiques et badges                       | UI statique  |

### Navigation

La navigation principale est assurée par une **bottom navigation bar fixe** dans `layouts/default.vue` :

```
[Accueil]  [Explorer]  [Assistant]  [Créateurs]  [Profil]
```

Cette approche mobile-first reproduit les codes UX des apps comme Instagram ou TikTok, directement ciblés dans la problématique du hackaton.

---

## 8. Gestion d'état

### Stratégie adoptée : état local + composables

Le projet n'utilise **pas de store centralisé** (Pinia est installé mais aucun store n'est défini). La gestion d'état repose sur :

1. **`ref()` / `reactive()`** Vue 3 dans chaque composant
2. **Composables** pour la logique partagée

> Pinia (`@pinia/nuxt@^0.11.3`) est disponible et prêt à être utilisé si l'état doit être partagé entre plusieurs pages.

### Cartographie de l'état par composant

| Composant/Composable   | Variable      | Type                       | Rôle                              |
| ---------------------- | ------------- | -------------------------- | --------------------------------- |
| `ChatWidget.vue`       | `isOpen`      | `Ref<boolean>`             | Visibilité du widget              |
| `ChatWidget.vue`       | `messages`    | `Ref<Message[]>`           | Historique de la conversation     |
| `ChatWidget.vue`       | `sessionId`   | `Ref<string \| undefined>` | Continuité de session API         |
| `ChatWidget.vue`       | `isLoading`   | `Ref<boolean>`             | État de chargement                |
| `ChatWidget.vue`       | `form`        | `reactive({query})`        | Valeur de l'input utilisateur     |
| `pages/chat/index.vue` | `messages`    | `Ref<Message[]>`           | Même état, page dédiée            |
| `pages/chat/index.vue` | `sessionId`   | `Ref<string>`              | Session persistante sur la page   |
| `useChatStream.ts`     | _(stateless)_ | —                          | Composable pur, pas d'état propre |

### Type `Message`

```typescript
interface Message {
  role: "user" | "assistant";
  content: string;
  loading?: boolean;
  progress?: { value: number; message: string };
  queryAnalysis?: QueryAnalysisData;
  restaurantCards?: RestaurantCardData[];
  location?: { lat: number; lng: number; location: string };
}
```

### Schéma du flux d'état

```
[User input]
     │
     ▼
form.query (reactive)
     │
     ▼ submitMessage()
messages.push({ role: 'user', content })
messages.push({ role: 'assistant', loading: true })
     │
     ▼ useChatStream()
  SSE stream ouvert
     │
     ├── onToken      → messages[last].content += token
     ├── onProgress   → messages[last].progress = { value, message }
     ├── onQueryAnalysis → messages[last].queryAnalysis = data
     ├── onRestaurantCard → messages[last].restaurantCards.push(card)
     └── onDone       → sessionId = data.session_id
                        isLoading = false
```

---

## 9. Flux de données & Communication avec le backend

### Protocole : Server-Sent Events (SSE)

Le projet utilise le **streaming SSE** (Server-Sent Events) plutôt que REST classique pour deux raisons :

- Affichage progressif token par token (effet "machine à écrire")
- Mise à jour incrémentale des données (progress, cards, analyse)

### Endpoint

```
GET /api/chat/stream
  ?query=<requête utilisateur>
  &session_id=<id session optionnel>
  &user_lat=<latitude GPS optionnel>
  &user_lon=<longitude GPS optionnel>
```

Le préfixe `/api` est **proxifié** par Vite vers le backend :

```typescript
// nuxt.config.ts
vite: {
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
}
```

### Événements SSE reçus

| Événement           | Payload                                          | Usage                                       |
| ------------------- | ------------------------------------------------ | ------------------------------------------- |
| `token`             | `{ content: string }`                            | Ajout progressif au message assistant       |
| `progress`          | `{ step, progress, message }`                    | Barre de progression pendant le traitement  |
| `step`              | `{ step, status: 'start'\|'complete', message }` | Indicateurs d'étapes                        |
| `query_analysis`    | `QueryAnalysisData`                              | Chips "détecté : Paris, japonais, 1 étoile" |
| `restaurant_card`   | `RestaurantCardData`                             | Carte restaurant enrichie                   |
| `location_detected` | `LocationData`                                   | Notification de géolocalisation             |
| `done`              | `DoneData`                                       | Fin du stream + session_id                  |
| `error`             | `{ message: string }`                            | Gestion des erreurs                         |

### Composable `useChatStream`

```typescript
// Signature
function streamChat(options: ChatStreamOptions): Promise<void>;

// Utilisation
await streamChat({
  query: "restaurant étoilé à Lyon",
  session_id: sessionId.value,
  user_lat: 45.75,
  user_lon: 4.83,
  onToken: (content) => {
    /* append to message */
  },
  onRestaurantCard: (card) => {
    /* push to cards */
  },
  onDone: (data) => {
    sessionId.value = data.session_id;
  },
});
```

---

## 10. Système de design & Charte graphique

### Stack UI

| Couche               | Technologie               |
| -------------------- | ------------------------- |
| Framework CSS        | Tailwind CSS v4           |
| Composants           | Nuxt UI v4 (headless)     |
| Icônes               | Heroicons (via `UIcon`)   |
| Typographie markdown | `@tailwindcss/typography` |

### Variables CSS marque

```css
:root {
  --ui-michelin-red: #ba0b2f; /* Rouge Michelin principal */
  --ui-michelin-black: #191919; /* Noir texte */
  --ui-michelin-dark-gray: #757575; /* Gris foncé */
  --ui-michelin-light-gray: #d2d2d2; /* Gris clair */
}
```

### Palette utilisée

| Usage            | Couleur                              |
| ---------------- | ------------------------------------ |
| Primaire / CTA   | Rouge Michelin `#c41e3a` / `#ba0b2f` |
| Fond clair       | `gray-50` / `white`                  |
| Texte principal  | `gray-900` / `#191919`               |
| Texte secondaire | `gray-500` / `#757575`               |
| Badges étoiles   | `amber-*` / `yellow-*`               |
| Bib Gourmand     | `red-*`                              |
| Prix             | `green-*`                            |

### Philosophie UX

- **Mobile-first** : conçu pour smartphone, adapté desktop
- **Bottom navigation** : codes UX apps modernes (Instagram, TikTok)
- **Couleurs Michelin** : rouge dominant, sobriété typographique
- **Cards restaurants** : information dense mais lisible
- **Animations** : transitions Vue pour fluidité du widget chat

---

## 11. TypeScript — Interfaces & Types

### Interfaces principales (`useChatStream.ts`)

```typescript
interface ChatStreamOptions {
  query: string;
  session_id?: string;
  user_lat?: number;
  user_lon?: number;
  onError?: (error: string) => void;
  onProgress?: (step: string, progress: number, message: string) => void;
  onStep?: (
    step: string,
    status: "start" | "complete",
    message: string,
  ) => void;
  onToken?: (content: string) => void;
  onQueryAnalysis?: (analysis: QueryAnalysisData) => void;
  onLocationDetected?: (location: LocationData) => void;
  onRestaurantCard?: (card: RestaurantCardData) => void;
  onDone?: (data: DoneData) => void;
}

interface RestaurantCardData {
  id: number;
  name: string;
  award?: string; // ex: "1 étoile Michelin", "Bib Gourmand"
  cuisine?: string; // ex: "Japonaise contemporaine"
  price?: string; // ex: "€€€"
  location: string;
  distance_km?: number;
  description?: string;
  signature_dish?: string;
  badge_text?: string;
  badge_color?: string;
  url?: string;
  website_url?: string;
}

interface QueryAnalysisData {
  original_query: string;
  detected_location?: string;
  detected_cuisine?: string;
  detected_award?: string;
  detected_price?: string;
  is_geo_query: boolean;
  distance_constraint?: number;
  needs_user_location: boolean;
}

interface DoneData {
  session_id: string;
  response_length: number;
  restaurants_count?: number;
  query_analysis?: object;
}
```

---

## 12. Dépendances

### Production

| Package                   | Version | Rôle                                           |
| ------------------------- | ------- | ---------------------------------------------- |
| `nuxt`                    | ^4.4.2  | Framework fullstack                            |
| `vue`                     | ^3.5.32 | Framework UI                                   |
| `vue-router`              | ^5.0.4  | Routing                                        |
| `@nuxt/ui`                | ^4.6.1  | Composants headless (UButton, UInput, UIcon…)  |
| `@nuxt/image`             | ^2.0.0  | Optimisation images                            |
| `@pinia/nuxt`             | ^0.11.3 | Store (installé, non utilisé)                  |
| `@nuxtjs/i18n`            | ^10.2.4 | Internationalisation (installé, non configuré) |
| `nuxt-mapbox`             | ^1.6.4  | Cartes Mapbox (installé, non utilisé)          |
| `marked`                  | ^15.0.4 | Parsing Markdown → HTML                        |
| `dompurify`               | ^3.4.1  | Sanitisation HTML (sécurité XSS)               |
| `@tailwindcss/typography` | ^0.5.19 | Styles prose pour le markdown                  |

### Développement

| Package            | Version | Rôle                       |
| ------------------ | ------- | -------------------------- |
| `@nuxt/eslint`     | ^1.15.2 | Linting intégré Nuxt       |
| `@types/dompurify` | ^3.0.5  | Types TypeScript DOMPurify |

---

## 13. Déploiement & Configuration

### Variables d'environnement

```env
# .env.example
NUXT_PUBLIC_API_BASE_URL=http://localhost:8000   # URL du backend
PORT=3000                                         # Port du frontend
```

### Scripts npm

```bash
npm run dev          # Serveur de développement (port 3000)
npm run build        # Build production
npm run preview      # Prévisualisation du build
npm run generate     # Génération statique
npm run postinstall  # Préparation Nuxt (auto)
```

### Docker

Le projet inclut un `Dockerfile` pour la containerisation. Build multi-stage optimisé Node.js.

```bash
docker build -t michelin-front .
docker run -p 3000:3000 michelin-front
```

---

## 14. État d'avancement & Pistes d'évolution

### Pages fonctionnelles

| Page         | Fonctionnel | Notes                                        |
| ------------ | ----------- | -------------------------------------------- |
| `/`          | Oui         | Landing avec présentation des features       |
| `/chat`      | Oui         | Chat SSE complet avec cards restaurants      |
| `/assistant` | Partiel     | UI présente, logique à brancher              |
| `/explore`   | Squelette   | Navigation restaurants à implémenter         |
| `/creators`  | Squelette   | Cartes créateurs à connecter à une API       |
| `/profile`   | UI statique | Données hardcodées, authentification absente |

### Modules installés non configurés

- **Pinia** : prêt à être utilisé dès que l'état doit être partagé entre pages (ex: profil utilisateur connecté, favoris)
- **i18n (`@nuxtjs/i18n`)** : à activer pour supporter le multi-langue (FR/EN minimum, cohérent avec la stratégie d'internationalisation Michelin)
- **nuxt-mapbox** : à utiliser sur `/explore` pour une carte interactive des restaurants

### Améliorations architecturales suggérées

1. **Store Pinia `useUserStore`** : centraliser le profil, l'historique de chat, les favoris
2. **Store Pinia `useRestaurantStore`** : cache des fiches restaurants chargées
3. **Authentification** : OAuth ou session backend pour personnalisation réelle
4. **Page `/explore`** : intégrer la carte Mapbox avec clustering des restaurants Michelin
5. **Page `/creators`** : brancher une API créateurs (profils, contenus, abonnements)
6. **PWA** : configurer `@nuxtjs/pwa` pour une expérience installable sur mobile
7. **Harmonisation langue** : uniformiser FR/EN selon la cible visée

---

_Documentation générée le 24 avril 2026 — Hackaton Skolae 2026_
