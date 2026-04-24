import { defineStore } from "pinia";

export const usePodcastsStore = defineStore("podcasts", {
  state: () => ({
    nowPlaying: null,
    isPlaying: false,
    progress: 0,
    episodes: [
      {
        id: "p1",
        title: "Bertrand Grébaut · La cuisine comme une phrase",
        show: "Tables Ouvertes",
        host: "Léa Moreau",
        duration: "48 min",
        durationSec: 2880,
        date: "12 avril",
        cover:
          "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&q=80",
        color: "#C8102E",
        description:
          "Le chef de Septime raconte comment il a cessé de cuisiner pour les critiques pour enfin cuisiner pour lui — et pourquoi ça a tout changé.",
        tags: ["Chef", "Paris", "Bistronomie"],
      },
      {
        id: "p2",
        title: "Le vin nature a-t-il gagné ?",
        show: "Le Comptoir",
        host: "Thomas Vidal",
        duration: "36 min",
        durationSec: 2160,
        date: "05 avril",
        cover:
          "https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=800&q=80",
        color: "#C9A961",
        description:
          "Enquête chez les cavistes, les vignerons et les sceptiques. Une Guide, trois visions.",
        tags: ["Vin", "Enquête"],
      },
      {
        id: "p3",
        title: "Manon Fleury · Le végétal, mode d'emploi",
        show: "Tables Ouvertes",
        host: "Léa Moreau",
        duration: "52 min",
        durationSec: 3120,
        date: "28 mars",
        cover:
          "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=800&q=80",
        color: "#3E5B2A",
        description:
          "De Mensae à Datil, la trajectoire d'une chef qui a réinventé le végétal français.",
        tags: ["Chef", "Végétal", "Paris"],
      },
      {
        id: "p4",
        title: "Comment on gagne une étoile (et pourquoi on peut la perdre)",
        show: "Inside Michelin",
        host: "Rédaction",
        duration: "41 min",
        durationSec: 2460,
        date: "20 mars",
        cover:
          "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80",
        color: "#141414",
        description:
          "Les coulisses de la notation, par ceux qui la font. Mythes, critères, réalité.",
        tags: ["Michelin", "Coulisses"],
      },
      {
        id: "p5",
        title: "Lyon, nouvelle scène",
        show: "Villes à table",
        host: "Mia Rossi",
        duration: "44 min",
        durationSec: 2640,
        date: "15 mars",
        cover:
          "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=800&q=80",
        color: "#A8441D",
        description:
          "Trois chefs, deux bistrots et une promesse : Lyon n'est plus seulement la ville de Bocuse.",
        tags: ["Lyon", "Reportage"],
      },
      {
        id: "p6",
        title: "Iñaki Aizpitarte · Punk à table",
        show: "Tables Ouvertes",
        host: "Léa Moreau",
        duration: "55 min",
        durationSec: 3300,
        date: "08 mars",
        cover:
          "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=800&q=80",
        color: "#2A2A2A",
        description:
          "Le père de la bistronomie libre parle cuisine, impatience et liberté.",
        tags: ["Chef", "Icône"],
      },
    ],
  }),

  actions: {
    play(id) {
      if (this.nowPlaying?.id === id) {
        this.isPlaying = !this.isPlaying;
      } else {
        this.nowPlaying = this.episodes.find((e) => e.id === id);
        this.isPlaying = true;
        this.progress = 0;
      }
    },
    stop() {
      this.isPlaying = false;
      this.nowPlaying = null;
      this.progress = 0;
    },
  },
});
