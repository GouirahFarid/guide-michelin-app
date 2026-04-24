import { defineStore } from 'pinia'

export const useCollectionsStore = defineStore('collections', {
  state: () => ({
    collections: [
      {
        id: 'c1',
        title: 'Mes meilleurs bistrots',
        emoji: '🍷',
        author: 'Léa Moreau',
        authorHandle: '@lea.tastes',
        collaborative: false,
        cover: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1200&q=80',
        description: 'Des adresses où on se sent chez soi, où la carte change avec les saisons et où le vin coule juste.',
        restaurants: ['r1', 'r3', 'r7'],
        likes: 142,
        saves: 87,
        collaborators: [],
        tags: ['bistronomie', 'vin nature', 'cosy']
      },
      {
        id: 'c2',
        title: 'Adresses de week-end à Paris',
        emoji: '🗼',
        author: 'Thomas Vidal',
        authorHandle: '@thom.eats',
        collaborative: true,
        cover: 'https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=1200&q=80',
        description: 'La liste collaborative que tout le monde partage à ses potes qui débarquent le vendredi soir.',
        restaurants: ['r1', 'r2', 'r4', 'r5', 'r8'],
        likes: 892,
        saves: 534,
        collaborators: [
          { name: 'Léa Moreau', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&q=80' },
          { name: 'Yann K.', avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80' },
          { name: 'Mia R.', avatar: 'https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=100&q=80' }
        ],
        tags: ['paris', 'week-end', 'collaborative']
      },
      {
        id: 'c3',
        title: 'Restaurants pour un premier date',
        emoji: '💌',
        author: 'Mia Rossi',
        authorHandle: '@mia.roma',
        collaborative: true,
        cover: 'https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=1200&q=80',
        description: 'Lumière tamisée, acoustique qui laisse parler, et une carte qui impressionne sans intimider.',
        restaurants: ['r1', 'r4', 'r8'],
        likes: 1204,
        saves: 891,
        collaborators: [
          { name: 'Léa Moreau', avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&q=80' },
          { name: 'Clara N.', avatar: 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&q=80' }
        ],
        tags: ['date', 'romantique', 'ambiance']
      },
      {
        id: 'c4',
        title: 'Petits budgets, grands moments',
        emoji: '💸',
        author: 'Yann Kanté',
        authorHandle: '@yann.plates',
        collaborative: false,
        cover: 'https://images.unsplash.com/photo-1509722747041-616f39b57569?w=1200&q=80',
        description: 'Moins de 25€ le ticket. Zéro compromis sur le plaisir.',
        restaurants: ['r5'],
        likes: 456,
        saves: 312,
        collaborators: [],
        tags: ['budget', 'pépite', 'étudiant']
      }
    ]
  }),

  getters: {
    byId: (s) => (id) => s.collections.find(c => c.id === id),
    myCollections: (s) => s.collections.filter(c => c.author === 'Léa Moreau')
  },

  actions: {
    like(id) {
      const c = this.collections.find(x => x.id === id)
      if (c) { c._liked = !c._liked; c.likes += c._liked ? 1 : -1 }
    },
    save(id) {
      const c = this.collections.find(x => x.id === id)
      if (c) { c._saved = !c._saved; c.saves += c._saved ? 1 : -1 }
    },
    addToCollection(collectionId, restaurantId) {
      const c = this.collections.find(x => x.id === collectionId)
      if (c && !c.restaurants.includes(restaurantId)) c.restaurants.push(restaurantId)
    },
    removeFromCollection(collectionId, restaurantId) {
      const c = this.collections.find(x => x.id === collectionId)
      if (c) c.restaurants = c.restaurants.filter(r => r !== restaurantId)
    },
    create(payload) {
      const id = 'c' + (this.collections.length + 1) + Date.now().toString().slice(-4)
      this.collections.unshift({
        id,
        title: payload.title,
        emoji: payload.emoji || '📍',
        author: 'Léa Moreau',
        authorHandle: '@lea.tastes',
        collaborative: !!payload.collaborative,
        cover: payload.cover || 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1200&q=80',
        description: payload.description || '',
        restaurants: payload.restaurants || [],
        likes: 0,
        saves: 0,
        collaborators: [],
        tags: payload.tags || []
      })
      return id
    }
  }
})
