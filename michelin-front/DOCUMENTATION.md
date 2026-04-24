# Michelin Guide — Documentation Complète du Projet

> **Hackathon Skolae 2026** · ICAN · ESGI · ECITV · EFET CREA

---

## Table des matières

1. [Contexte & Problématique](#1-contexte--problématique)
2. [Installation & Lancement](#2-installation--lancement)
3. [Stack technique](#3-stack-technique)
4. [Architecture des fichiers](#4-architecture-des-fichiers)
5. [Architecture des composants](#5-architecture-des-composants)
6. [Gestion d'état — Stores Pinia](#6-gestion-détat--stores-pinia)
7. [Routing & Pages](#7-routing--pages)
8. [Design System](#8-design-system)

---

## 1. Contexte & Problématique

### Le Guide Michelin en 2026

Fondé en 1900 par André et Édouard Michelin, le Guide Michelin s'est imposé pendant plus d'un siècle comme **la référence mondiale de la prescription gastronomique**.

### La problématique centrale

> **Comment le Guide Michelin peut-il regagner du terrain face aux réseaux sociaux, aux plateformes, et aux influenceurs, pour conquérir un marché plus jeune et redevenir le guide prescripteur de référence ?**

Le Guide reste incontournable pour les professionnels de la restauration, mais souffre d'une image trop élitiste, trop institutionnelle et trop peu interactive auprès des Guides Y et Z.

---

## 2. Installation & Lancement

### Prérequis

| Outil | Version minimale | Vérification |
|---|---|---|
| **Node.js** | 18.x LTS | `node -v` |
| **npm** | 9.x | `npm -v` |

> Nuxt 3 requiert Node.js ≥ 18. Il est recommandé d'utiliser [nvm](https://github.com/nvm-sh/nvm) pour gérer les versions Node.

---

### 1. Cloner le dépôt

```bash
git clone <url-du-repo>
cd michelin-gen
```

---

### 2. Installer les dépendances

```bash
npm install
```

Cette commande installe l'ensemble des dépendances déclarées dans `package.json` :
- `nuxt` — framework principal
- `pinia` + `@pinia/nuxt` — gestion d'état
- `@nuxtjs/tailwindcss` — styles utilitaires
- `vite` — bundler (géré automatiquement par Nuxt)

Le script `postinstall` défini dans `package.json` exécute automatiquement `nuxt prepare`, qui génère les types TypeScript et initialise le dossier `.nuxt/`.

---

### 3. Lancer le serveur de développement

```bash
npm run dev
```

Nuxt démarre un serveur de développement Vite avec **Hot Module Replacement (HMR)** : toute modification de fichier est reflétée instantanément dans le navigateur sans rechargement complet.

L'application est accessible à l'adresse : **`http://localhost:3000`**

---

### 4. Build de production

```bash
npm run build
```

Nuxt compile l'application en mode SSR (Server-Side Rendering) dans le dossier `.output/`. Vite optimise et minifie les assets (JS, CSS).

```bash
npm run preview   # Prévisualiser le build de production en local
```

---

### 5. Génération statique (optionnel)

```bash
npm run generate
```

Génère un site 100% statique dans `.output/public/` — déployable sur tout CDN (Vercel, Netlify, GitHub Pages). Adapté si aucun rendu serveur n'est nécessaire.

---

### Scripts disponibles

| Commande | Description |
|---|---|
| `npm run dev` | Serveur de développement avec HMR sur `localhost:3000` |
| `npm run build` | Build de production SSR dans `.output/` |
| `npm run preview` | Prévisualisation du build de production |
| `npm run generate` | Génération statique dans `.output/public/` |

---

## 3. Stack technique

```
Framework      : Nuxt 3 (^3.13.0)
UI             : Vue 3 (Composition API, <script setup>)
Bundler        : Vite (^5.4.0)
Styling        : Tailwind CSS (@nuxtjs/tailwindcss ^6.12.0)
State          : Pinia (^2.2.0) + @pinia/nuxt (^0.5.4)
Fonts          : Google Fonts — Figtree · Inter · JetBrains Mono
Routing        : Nuxt file-based routing (auto)
Données        : Mock data (in-store, hardcodé) — pas de backend
```

### Pourquoi Nuxt 3 ?

- **SSR/SSG-ready** : optimal pour le SEO d'une plateforme de contenu gastronomique
- **Auto-routing** : les fichiers dans `/pages` deviennent automatiquement des routes
- **Modules officiels** : intégration native de Tailwind CSS et Pinia
- **Composition API** : code Vue 3 moderne, réutilisable, testable

---

## 3. Architecture des fichiers

```
michelin-gen/
│
├── assets/
│   └── css/
│       └── main.css              # Design tokens CSS, animations globales, typography
│
├── components/                   # Composants réutilisables (UI bricks)
│   ├── FilterSelect.vue          # Dropdown de filtre
│   ├── PodcastPlayer.vue         # Player audio persistant (bottom bar)
│   ├── RestaurantCard.vue        # Carte restaurant (grille)
│   ├── SiteFooter.vue            # Pied de page global
│   └── SiteHeader.vue            # En-tête de navigation global
│
├── layouts/
│   └── default.vue               # Layout racine : Header + slot + Footer + PodcastPlayer
│
├── pages/                        # Routes auto-générées par Nuxt
│   ├── index.vue                 # / — Page d'accueil (hero, mood, editorial)
│   ├── community.vue             # /community — Fil social
│   ├── podcasts.vue              # /podcasts — Catalogue podcasts
│   ├── profile.vue               # /profile — Profil utilisateur
│   └── restaurants/
│       ├── index.vue             # /restaurants — Listing + filtres
│       └── [id].vue              # /restaurants/:id — Fiche restaurant
│
├── stores/                       # État global (Pinia)
│   ├── restaurants.js            # Données + filtres restaurants
│   ├── user.js                   # Profil utilisateur + wishlist + badges
│   ├── collections.js            # Collections curatées
│   ├── events.js                 # Événements communautaires
│   └── podcasts.js               # Episodes + état du player
│
├── public/                       # Assets statiques (images, favicons…)
│
├── nuxt.config.ts                # Config Nuxt (modules, CSS, meta)
├── tailwind.config.js            # Design tokens Tailwind (couleurs, fonts, animations)
└── package.json
```

---

## 4. Architecture des composants

### Vue d'ensemble

```
layouts/default.vue
├── components/SiteHeader.vue
├── <slot> (page active)
│   ├── components/RestaurantCard.vue  (utilisé dans index.vue et restaurants/index.vue)
│   └── components/FilterSelect.vue   (utilisé dans restaurants/index.vue)
└── components/SiteFooter.vue
    + components/PodcastPlayer.vue     (conditionnel, monté si nowPlaying)
```

### Détail de chaque composant

---

#### `SiteHeader.vue`

**Rôle** : Navigation principale persistante (sticky).

---

#### `SiteFooter.vue`

**Rôle** : Pied de page éditorial.

---

#### `RestaurantCard.vue`

**Rôle** : Carte visuelle d'un restaurant pour les vues en grille.

---

#### `FilterSelect.vue`

**Rôle** : Composant de select stylisé pour les filtres de la page restaurants.

---

#### `PodcastPlayer.vue`

**Rôle** : Lecteur audio persistant en bas de page (style Spotify).

---

## 5. Gestion d'état — Stores Pinia

Tous les stores suivent le pattern **Options Store** de Pinia (`state` / `getters` / `actions`), sans persistance (état réinitialisé au rechargement).

---

## 6. Routing & Pages

Nuxt 3 génère les routes automatiquement depuis le dossier `/pages`.

| Route              | Fichier                 | Composants utilisés              | Stores utilisés                                                                    |
| ------------------ | ----------------------- | -------------------------------- | ---------------------------------------------------------------------------------- |
| `/`                | `index.vue`             | `RestaurantCard`                 | `useRestaurantsStore`, `useCollectionsStore`, `useEventsStore`, `usePodcastsStore` |
| `/restaurants`     | `restaurants/index.vue` | `RestaurantCard`, `FilterSelect` | `useRestaurantsStore`, `useUserStore`                                              |
| `/restaurants/:id` | `restaurants/[id].vue`  | —                                | `useRestaurantsStore`, `useUserStore`, `useCollectionsStore`, `useEventsStore`     |
| `/community`       | `community.vue`         | —                                | `useUserStore`, `useCollectionsStore`, `useEventsStore`                            |
| `/podcasts`        | `podcasts.vue`          | —                                | `usePodcastsStore`                                                                 |
| `/profile`         | `profile.vue`           | —                                | `useUserStore`, `useRestaurantsStore`, `useCollectionsStore`                       |

### Page d'accueil `index.vue`

Structure en sections verticales :

1. **Hero** : visuel plein écran, headline "Guide", CTA vers `/restaurants`
2. **Mood picker** : icônes d'occasions (Date, Solo luxe, En famille…) → filtrage rapide
3. **Restaurants en vedette** : grille `RestaurantCard` (6 premiers restaurants)
4. **Citation éditoriale** : bloc typographique style magazine
5. **Événements à venir** : 2 prochains events
6. **Podcasts** : épisode du moment

### Page listing `/restaurants`

- **Barre de recherche** plein largeur
- **5 filtres** via `FilterSelect` : Ville, Cuisine, Budget, Distinction, Occasion
- **Toggle vue** : grille (cards) ↔ liste (éditorial)
- **Résultats réactifs** : `restaurantsStore.filtered` (computed en temps réel)
- **Compteur** : "X restaurants trouvés"

### Page détail `/restaurants/[id]`

Sections :

1. Hero image + overlay informations (étoiles, chef, ville, budget)
2. Description + critique éditoriale
3. Plat signature
4. Tags & occasions
5. Actions utilisateur : Tester, Sauvegarder, Ajouter à une collection
6. Commentaires communautaires (mockés)
7. Événements liés à ce restaurant
8. Restaurants similaires

### Page profil `/profile`

Onglets :

- **Mes goûts** : cuisines favorites, budget, occasions, villes visitées, badges
- **Testés** : restaurants marqués comme testés
- **Sauvegardés** : wishlist
- **Collections** : collections créées par l'utilisateur
- **Activité** : historique des actions

Modal "Modifier le profil" avec `useUserStore.updateField`.

---

## 7. Design System

### Palette de couleurs (Tailwind config)

```js
colors: {
  'michelin-red':   '#C8102E',   // Rouge iconique Michelin
  'michelin-cream': '#FFF8F0',   // Fond chaud
  'michelin-ink':   '#1A1A1A',   // Texte principal
  'michelin-gold':  '#C9A84C',   // Accents premium (étoiles)
  'michelin-grey':  '#6B6B6B',   // Texte secondaire
}
```

### Typographie

| Famille     | Usage                       |
| ----------- | --------------------------- |
| **Figtree** | Headings display, éditorial |

La solution principale est déployée à l'adresse: `http://57.129.13.147/`

La landing page du guide Michelin est disponible à l'adresse: `https://welcome-guide-michelin.vercel.app/`
