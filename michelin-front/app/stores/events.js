import { defineStore } from 'pinia'

export const useEventsStore = defineStore('events', {
  state: () => ({
    events: [
      {
        id: 'e1',
        title: 'Dîner à l\'aveugle · Vins nature du Jura',
        restaurantId: 'r1',
        restaurantName: 'Septime',
        city: 'Paris',
        date: '2026-05-14',
        time: '20:00',
        price: 95,
        spots: 12,
        taken: 9,
        host: 'Léa Moreau',
        hostAvatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&q=80',
        hostHandle: '@lea.tastes',
        cover: 'https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=1200&q=80',
        description: '5 services, 5 vins à deviner, une salle complète et des inconnus qui repartent potes. Validé par Michelin.',
        validated: true,
        vibe: 'Curieux · Connaisseurs',
        attendees: [
          'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80',
          'https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=100&q=80',
          'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&q=80',
          'https://images.unsplash.com/photo-1463453091185-61582044d556?w=100&q=80'
        ]
      },
      {
        id: 'e2',
        title: 'Brunch long format · Bistronomie végétale',
        restaurantId: 'r4',
        restaurantName: 'Datil',
        city: 'Paris',
        date: '2026-05-18',
        time: '12:30',
        price: 65,
        spots: 16,
        taken: 11,
        host: 'Thomas Vidal',
        hostAvatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80',
        hostHandle: '@thom.eats',
        cover: 'https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=1200&q=80',
        description: 'Quatre heures, huit assiettes végétales, une playlist lente. Dress code: naturel.',
        validated: true,
        vibe: 'Doux · Slow',
        attendees: [
          'https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=100&q=80',
          'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&q=80'
        ]
      },
      {
        id: 'e3',
        title: 'BBQ coréen & soju · Late night',
        restaurantId: 'r8',
        restaurantName: 'Omma',
        city: 'Paris',
        date: '2026-05-22',
        time: '21:30',
        price: 55,
        spots: 20,
        taken: 17,
        host: 'Mia Rossi',
        hostAvatar: 'https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=100&q=80',
        hostHandle: '@mia.roma',
        cover: 'https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=1200&q=80',
        description: 'Viande au charbon, soju au shaker, ambiance Séoul 2h du mat. On finit au karaoké d\'à côté.',
        validated: true,
        vibe: 'High energy · Nocturne',
        attendees: [
          'https://images.unsplash.com/photo-1463453091185-61582044d556?w=100&q=80',
          'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&q=80',
          'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80',
          'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&q=80'
        ]
      },
      {
        id: 'e4',
        title: 'Table des chefs · Lyon',
        restaurantId: 'r6',
        restaurantName: 'Plume',
        city: 'Lyon',
        date: '2026-06-04',
        time: '19:30',
        price: 85,
        spots: 10,
        taken: 4,
        host: 'Youssef M.',
        hostAvatar: 'https://images.unsplash.com/photo-1463453091185-61582044d556?w=100&q=80',
        hostHandle: '@chef.yms',
        cover: 'https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=1200&q=80',
        description: 'Le chef cuisine devant vous, commente chaque plat, répond aux questions. Pour les vrais curieux.',
        validated: true,
        vibe: 'Intime · Chef\'s table',
        attendees: [
          'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&q=80'
        ]
      }
    ]
  }),

  getters: {
    byId: (s) => (id) => s.events.find(e => e.id === id),
    upcoming: (s) => s.events.filter(e => new Date(e.date) >= new Date('2026-04-23'))
  },

  actions: {
    join(id) {
      const e = this.events.find(x => x.id === id)
      if (e && e.taken < e.spots && !e._joined) {
        e._joined = true
        e.taken += 1
      } else if (e && e._joined) {
        e._joined = false
        e.taken -= 1
      }
    }
  }
})
