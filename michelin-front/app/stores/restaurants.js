import { defineStore } from 'pinia'

export const useRestaurantsStore = defineStore('restaurants', {
  state: () => ({
    restaurants: [
      {
        id: 'r1',
        name: 'Septime',
        chef: 'Bertrand Grébaut',
        city: 'Paris',
        district: '11ᵉ',
        cuisine: 'Bistronomie',
        vibe: 'Intimiste · Naturel',
        budget: '€€€',
        price: '80–120€',
        stars: 1,
        bib: false,
        rating: 4.8,
        occasions: ['Date', 'Entre amis'],
        tags: ['Vin nature', 'Produits locaux', 'Menu unique'],
        image: 'https://images.unsplash.com/photo-1552566626-52f8b828add9?w=1200&q=80',
        description: 'Une cuisine vivante et spontanée qui a redéfini la bistronomie parisienne.',
        review: 'La réservation est un sport national, mais chaque assiette justifie la patience. Bertrand Grébaut impose sa griffe avec une cuisine d\'instinct, nerveuse et généreuse.',
        signature: 'Pigeonneau, cerise noire, jus aux épices',
        lat: 48.8527,
        lng: 2.3775
      },
      {
        id: 'r2',
        name: 'Clamato',
        chef: 'Bertrand Grébaut',
        city: 'Paris',
        district: '11ᵉ',
        cuisine: 'Iodée · Partage',
        vibe: 'Décontracté · Comptoir',
        budget: '€€',
        price: '40–60€',
        stars: 0,
        bib: true,
        rating: 4.6,
        occasions: ['Entre amis', 'Solo', 'Date'],
        tags: ['Sans réservation', 'Produits de la mer', 'Natural wine'],
        image: 'https://images.unsplash.com/photo-1579027989536-b7b1f875659b?w=1200&q=80',
        description: 'Le petit frère iodé de Septime. Comptoir, produits de la mer, énergie folle.',
        review: 'L\'attente vaut le coup. Petites assiettes percutantes, service affûté, une salle qui bat comme un cœur.',
        signature: 'Oursin, huile d\'olive, pain grillé',
        lat: 48.8524,
        lng: 2.3776
      },
      {
        id: 'r3',
        name: 'Le Chateaubriand',
        chef: 'Iñaki Aizpitarte',
        city: 'Paris',
        district: '11ᵉ',
        cuisine: 'Bistronomie',
        vibe: 'Rock · Libre',
        budget: '€€€',
        price: '75–100€',
        stars: 0,
        bib: false,
        rating: 4.5,
        occasions: ['Entre amis', 'Date'],
        tags: ['Menu surprise', 'Vin nature', 'Iconique'],
        image: 'https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=1200&q=80',
        description: 'Le laboratoire de la bistronomie. Brut, affûté, toujours en avance.',
        review: 'Aizpitarte cuisine comme un punk bien élevé. Un menu qui refuse le confort, et c\'est tant mieux.',
        signature: 'Maquereau, wasabi, framboise',
        lat: 48.8669,
        lng: 2.3717
      },
      {
        id: 'r4',
        name: 'Datil',
        chef: 'Manon Fleury',
        city: 'Paris',
        district: '11ᵉ',
        cuisine: 'Végétale · Saison',
        vibe: 'Lumineux · Minéral',
        budget: '€€€',
        price: '90–130€',
        stars: 1,
        bib: false,
        rating: 4.9,
        occasions: ['Date', 'Occasion spéciale'],
        tags: ['Végétal', 'Jeune chef', 'Design'],
        image: 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=1200&q=80',
        description: 'Manon Fleury orchestre une cuisine végétale d\'une précision chorégraphique.',
        review: 'Chaque plat est une phrase courte et juste. Le végétal n\'a jamais semblé si sensuel.',
        signature: 'Betterave, groseille, sarrasin torréfié',
        lat: 48.8631,
        lng: 2.3708
      },
      {
        id: 'r5',
        name: 'Chez Aline',
        chef: 'Delphine Zampetti',
        city: 'Paris',
        district: '11ᵉ',
        cuisine: 'Sandwicherie',
        vibe: 'Cantine · Quartier',
        budget: '€',
        price: '10–18€',
        stars: 0,
        bib: true,
        rating: 4.7,
        occasions: ['Solo', 'Déjeuner rapide'],
        tags: ['Petit budget', 'Sandwich', 'Épicerie'],
        image: 'https://images.unsplash.com/photo-1509722747041-616f39b57569?w=1200&q=80',
        description: 'Une ancienne boucherie chevaline devenue temple du sandwich d\'auteur.',
        review: 'La meilleure pause déjeuner du 11ᵉ. Pain bio, produits impeccables, prix doux.',
        signature: 'Sandwich porc confit, pickles maison',
        lat: 48.8536,
        lng: 2.3793
      },
      {
        id: 'r6',
        name: 'Plume',
        chef: 'Youssef Marzouk',
        city: 'Lyon',
        district: '2ᵉ',
        cuisine: 'Méditerranéenne',
        vibe: 'Ensoleillé · Généreux',
        budget: '€€',
        price: '45–70€',
        stars: 0,
        bib: true,
        rating: 4.5,
        occasions: ['Entre amis', 'Famille'],
        tags: ['Méditerranée', 'Rapport qualité-prix', 'Cave vivante'],
        image: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1200&q=80',
        description: 'Une cuisine de Méditerranée généreuse, de Marseille à Beyrouth.',
        review: 'Assiettes solaires, service chaleureux. Lyon tenait son nouveau repaire.',
        signature: 'Poulpe grillé, muhammara, chermoula',
        lat: 45.7578,
        lng: 4.8320
      },
      {
        id: 'r7',
        name: 'Racines',
        chef: 'Kiko Aumont',
        city: 'Bordeaux',
        district: 'Chartrons',
        cuisine: 'Terroir · Saison',
        vibe: 'Artisanal · Bois',
        budget: '€€',
        price: '55–80€',
        stars: 0,
        bib: true,
        rating: 4.6,
        occasions: ['Date', 'Entre amis'],
        tags: ['Circuit court', 'Feu de bois', 'Vin nature'],
        image: 'https://images.unsplash.com/photo-1466978913421-dad2ebd01d17?w=1200&q=80',
        description: 'Une cuisine de feu et de saison qui parle le langage du Sud-Ouest.',
        review: 'Le grill au centre, la carte sur une ardoise, tout ce qu\'on aime quand la simplicité rime avec précision.',
        signature: 'Côte de bœuf maturée, pommes de terre à la cendre',
        lat: 44.8530,
        lng: -0.5732
      },
      {
        id: 'r8',
        name: 'Omma',
        chef: 'Yoo Mi Kim',
        city: 'Paris',
        district: '2ᵉ',
        cuisine: 'Coréenne',
        vibe: 'Néon · Nocturne',
        budget: '€€',
        price: '40–65€',
        stars: 0,
        bib: true,
        rating: 4.7,
        occasions: ['Entre amis', 'Date'],
        tags: ['Bbq', 'Soju', 'Tardif'],
        image: 'https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=1200&q=80',
        description: 'BBQ coréen, banchan généreux, soju qui coule. Le Séoul du Sentier.',
        review: 'Le genre d\'adresse où on arrive à 20h et d\'où on sort vers minuit, en chantant.',
        signature: 'Bo ssam, kimchi fermenté 6 mois',
        lat: 48.8693,
        lng: 2.3478
      }
    ],
    filters: {
      search: '',
      city: 'Toutes',
      cuisine: 'Toutes',
      budget: 'Tous',
      distinction: 'Tous',
      occasion: 'Toutes'
    }
  }),

  getters: {
    cities(state) {
      return ['Toutes', ...new Set(state.restaurants.map(r => r.city))]
    },
    cuisines(state) {
      return ['Toutes', ...new Set(state.restaurants.map(r => r.cuisine))]
    },
    filtered(state) {
      return state.restaurants.filter(r => {
        const s = state.filters.search.toLowerCase()
        if (s && !(`${r.name} ${r.chef} ${r.cuisine} ${r.city}`.toLowerCase().includes(s))) return false
        if (state.filters.city !== 'Toutes' && r.city !== state.filters.city) return false
        if (state.filters.cuisine !== 'Toutes' && r.cuisine !== state.filters.cuisine) return false
        if (state.filters.budget !== 'Tous' && r.budget !== state.filters.budget) return false
        if (state.filters.distinction === 'Étoilé' && r.stars === 0) return false
        if (state.filters.distinction === 'Bib Gourmand' && !r.bib) return false
        if (state.filters.occasion !== 'Toutes' && !r.occasions.includes(state.filters.occasion)) return false
        return true
      })
    },
    byId: (state) => (id) => state.restaurants.find(r => r.id === id)
  },

  actions: {
    setFilter(key, value) {
      this.filters[key] = value
    },
    resetFilters() {
      this.filters = {
        search: '', city: 'Toutes', cuisine: 'Toutes',
        budget: 'Tous', distinction: 'Tous', occasion: 'Toutes'
      }
    }
  }
})
