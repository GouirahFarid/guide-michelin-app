import { defineStore } from "pinia";

export const useUserStore = defineStore("user", {
  state: () => ({
    profile: {
      name: "Léa Moreau",
      handle: "@lea.tastes",
      avatar:
        "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=400&q=80",
      bio: "Chasseuse de bonnes tables depuis 2019. Amatrice de vin nature, de comptoirs et de desserts qui déraisonnent.",
      age: 27,
      memberSince: "2023",
      // level: 'Gourmet · Niveau 4',
      // xp: 1840,
      // nextLevel: 2500,
      favoriteCuisines: [
        "Bistronomie",
        "Coréenne",
        "Végétale",
        "Méditerranéenne",
      ],
      budget: "€€ · 40–80€",
      occasions: ["Date", "Entre amis", "Solo"],
      visitedCities: [
        "Paris",
        "Lyon",
        "Bordeaux",
        "Marseille",
        "Copenhague",
        "Lisbonne",
      ],
      testedRestaurants: ["r1", "r3", "r5", "r8"],
      wishlist: ["r2", "r4", "r7"],
    },
    followers: 247,
    following: 183,
    badges: [
      {
        id: "b1",
        label: "Première étoile",
        emoji: "⭐",
        unlocked: true,
        desc: "Testé un restaurant étoilé",
      },
      {
        id: "b2",
        label: "Explorateur",
        emoji: "🗺️",
        unlocked: true,
        desc: "5 villes visitées",
      },
      {
        id: "b3",
        label: "Night eater",
        emoji: "🌙",
        unlocked: true,
        desc: "10 dîners après 22h",
      },
      {
        id: "b4",
        label: "Collectionneuse",
        emoji: "📚",
        unlocked: true,
        desc: "3 listes créées",
      },
      {
        id: "b5",
        label: "Table ouverte",
        emoji: "🍷",
        unlocked: false,
        desc: "Participer à un dîner communauté",
      },
      {
        id: "b6",
        label: "Critique",
        emoji: "✍️",
        unlocked: false,
        desc: "20 avis publiés",
      },
    ],
  }),

  getters: {
    // xpPercent: (s) =>
    //   Math.min(100, Math.round((s.profile.xp / s.profile.nextLevel) * 100)),
    hasTested: (s) => (id) => s.profile.testedRestaurants.includes(id),
    hasWishlisted: (s) => (id) => s.profile.wishlist.includes(id),
  },

  actions: {
    toggleTested(id) {
      const idx = this.profile.testedRestaurants.indexOf(id);
      if (idx > -1) this.profile.testedRestaurants.splice(idx, 1);
      else {
        this.profile.testedRestaurants.push(id);
        this.profile.xp += 50;
      }
    },
    toggleWishlist(id) {
      const idx = this.profile.wishlist.indexOf(id);
      if (idx > -1) this.profile.wishlist.splice(idx, 1);
      else this.profile.wishlist.push(id);
    },
    addCuisine(c) {
      if (!this.profile.favoriteCuisines.includes(c))
        this.profile.favoriteCuisines.push(c);
    },
    removeCuisine(c) {
      this.profile.favoriteCuisines = this.profile.favoriteCuisines.filter(
        (x) => x !== c,
      );
    },
    updateField(field, value) {
      this.profile[field] = value;
    },
  },
});
