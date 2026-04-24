<template>
  <div>
    <!-- HERO -->
    <section class="relative overflow-hidden bg-michelin-cream grain">
      <!-- Decorative red stripe -->
      <div
        class="absolute top-0 right-0 w-[35%] h-full bg-michelin-red hidden lg:block"
      >
        <div class="absolute inset-0 grain opacity-30"></div>
      </div>

      <div
        class="relative max-w-[1400px] mx-auto px-6 pt-12 lg:pt-20 pb-16 lg:pb-24 grid lg:grid-cols-12 gap-10"
      >
        <!-- Left column -->
        <div class="lg:col-span-7 relative z-10">
          <!-- Eyebrow -->
          <!-- <div
            class="flex items-center gap-3 mb-8 animate-fade-up"
            style="animation-delay: 50ms"
          >
            <div class="h-[1px] w-12 bg-michelin-red"></div>
            <span
              class="text-xs tracking-[0.3em] uppercase font-semibold text-michelin-red"
              >Édition 2026 · Nouvelle Guide</span
            >
          </div> -->

          <h1
            class="font-display font-black leading-[0.92] tracking-[-0.03em] text-[clamp(3rem,8vw,7rem)]"
          >
            <!-- <span
              class="block animate-fade-up"
              style="animation-delay: 100ms"
            ></span> -->
            <span
              class="block italic font-medium animate-fade-up"
              style="animation-delay: 200ms"
              >La table d'aujourd'hui, racontée par vous.</span
            >
            <span
              class="block text-michelin-red animate-fade-up"
              style="animation-delay: 300ms"
            >
              <span class="relative inline-block">
                <svg
                  class="absolute -bottom-2 left-0 w-full"
                  viewBox="0 0 200 12"
                  preserveAspectRatio="none"
                >
                  <path
                    d="M2 6 Q50 2 100 6 T198 6"
                    stroke="currentColor"
                    stroke-width="3"
                    fill="none"
                    stroke-linecap="round"
                  />
                </svg>
              </span>
            </span>
          </h1>

          <p
            class="mt-10 max-w-xl text-lg leading-relaxed text-michelin-ink-soft font-display animate-fade-up"
            style="animation-delay: 400ms"
          >
            Le Guide Michelin quitte sa couverture rouge pour rejoindre la Guide
            qui cuisine le monde autrement.
            <span class="italic">Mêmes exigences. Regard neuf.</span>
          </p>

          <!-- CTAs -->
          <div
            class="mt-10 flex flex-wrap gap-4 animate-fade-up"
            style="animation-delay: 500ms"
          >
            <NuxtLink to="/restaurants" class="btn-primary group">
              Explorer la sélection
              <svg
                class="w-4 h-4 transition-transform group-hover:translate-x-1"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                viewBox="0 0 24 24"
              >
                <path d="M5 12h14m-6-6 6 6-6 6" />
              </svg>
            </NuxtLink>
          </div>

          <!-- Stats -->
          <div
            class="mt-14 grid grid-cols-3 gap-6 max-w-xl animate-fade-up"
            style="animation-delay: 600ms"
          >
            <div class="border-l-2 border-michelin-red pl-4">
              <div class="font-display text-4xl font-bold">2&nbsp;847</div>
              <div
                class="text-xs uppercase tracking-wider text-michelin-stone mt-1"
              >
                Adresses
              </div>
            </div>
            <div class="border-l-2 border-michelin-red pl-4">
              <div class="font-display text-4xl font-bold">143K</div>
              <div
                class="text-xs uppercase tracking-wider text-michelin-stone mt-1"
              >
                Membres
              </div>
            </div>
            <!-- <div class="border-l-2 border-michelin-red pl-4">
              <div class="font-display text-4xl font-bold">612</div>
              <div
                class="text-xs uppercase tracking-wider text-michelin-stone mt-1"
              >
                Tables ouvertes
              </div>
            </div> -->
          </div>
        </div>

        <!-- Right column: stacked images -->
        <div
          class="lg:col-span-5 relative h-[500px] lg:h-[640px] animate-fade-up"
          style="animation-delay: 400ms"
        >
          <div
            class="absolute top-0 right-0 w-[70%] aspect-[3/4] overflow-hidden shadow-2xl"
          >
            <img
              src="https://images.unsplash.com/photo-1552566626-52f8b828add9?w=800&q=80"
              class="w-full h-full object-cover"
            />
          </div>
          <!-- <div
            class="absolute bottom-0 left-0 w-[60%] aspect-square overflow-hidden shadow-2xl border-8 border-michelin-cream"
          >
            <img
              src="https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=600&q=80"
              class="w-full h-full object-cover"
            />
          </div> -->
          <!-- Floating rating card -->
          <!-- <div
            class="absolute top-[45%] left-4 bg-michelin-cream shadow-2xl p-4 w-52 hidden md:block"
          >
            <div class="flex items-center gap-2 mb-2">
              <div class="flex text-michelin-red">
                <span>★</span>
                <span class="text-michelin-ink/20">★</span>
                <span class="text-michelin-ink/20">★</span>
              </div>
            </div>
            <div class="font-display text-lg font-bold">Septime</div>
            <div class="text-xs text-michelin-stone">Paris 11ᵉ · 4.8/5</div>
            <div
              class="mt-3 pt-3 border-t border-michelin-ink/10 text-xs italic text-michelin-ink-soft"
            >
              « Une table d'instinct qui a réécrit la bistronomie. »
            </div>
          </div> -->
        </div>
      </div>

      <!-- Bottom ticker -->
      <!-- <div class="border-y border-michelin-ink/10 py-4 bg-michelin-cream marquee-container overflow-hidden">
        <div class="flex items-center gap-10 animate-marquee whitespace-nowrap text-sm uppercase tracking-[0.25em] font-medium">
          <template v-for="n in 2" :key="n">
            <template v-for="item in tickerItems" :key="item">
              <span class="flex items-center gap-3">
                <span class="text-michelin-red">◆</span>
                {{ item }}
              </span>
            </template>
          </template>
        </div>
      </div> -->
    </section>

    <!-- QUICK ACCESS -->
    <section class="max-w-[1400px] mx-auto px-6 py-20">
      <!-- <div class="flex items-end justify-between mb-10">
        <div>
          <div
            class="text-xs tracking-[0.3em] uppercase font-semibold text-michelin-red mb-3"
          >
            Entrer par l'envie
          </div>
          <h2 class="font-display text-5xl md:text-6xl font-bold">
            Qu'est-ce qui vous fait faim&nbsp;?
          </h2>
        </div>
      </div> -->
      <!-- <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3">
        <button
          v-for="(m, i) in moods"
          :key="m.label"
          @click="selectMood(m)"
          class="group relative aspect-square overflow-hidden bg-michelin-ink"
          :style="{ animationDelay: `${i * 60}ms` }"
        >
          <img
            :src="m.image"
            class="absolute inset-0 w-full h-full object-cover opacity-60 group-hover:opacity-80 group-hover:scale-110 transition-all duration-500"
          />
          <div
            class="absolute inset-0 bg-gradient-to-t from-michelin-ink to-transparent"
          ></div>
          <div
            class="absolute inset-0 flex flex-col justify-between p-4 text-michelin-cream"
          >
            <div class="text-2xl">{{ m.emoji }}</div>
            <div>
              <div
                class="font-display text-xl md:text-2xl font-bold leading-tight"
              >
                {{ m.label }}
              </div>
              <div
                class="text-[10px] uppercase tracking-widest opacity-70 mt-1"
              >
                {{ m.sub }}
              </div>
            </div>
          </div>
        </button>
      </div> -->
    </section>

    <!-- FEATURED -->
    <section class="bg-michelin-sand py-20">
      <div class="max-w-[1400px] mx-auto px-6">
        <div class="flex items-end justify-between mb-10 flex-wrap gap-4">
          <div>
            <div
              class="text-xs tracking-[0.3em] uppercase font-semibold text-michelin-red mb-3"
            >
              Sélection de la semaine
            </div>
            <h2 class="font-display text-5xl md:text-6xl font-bold">
              Les inratables<span class="text-michelin-red">.</span>
            </h2>
          </div>
          <NuxtLink
            to="/restaurants"
            class="text-sm uppercase tracking-wider font-medium hover:text-michelin-red flex items-center gap-2 transition-colors"
          >
            Tout voir
            <svg
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <path d="M5 12h14m-6-6 6 6-6 6" />
            </svg>
          </NuxtLink>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <RestaurantCard v-for="r in featured" :key="r.id" :r="r" />
        </div>
      </div>
    </section>

    <!-- EDITORIAL -->
    <section
      class="relative bg-michelin-ink text-michelin-cream py-24 overflow-hidden"
    >
      <div class="absolute inset-0 opacity-20">
        <img
          src="https://images.unsplash.com/photo-1510812431401-41d2bd2722f3?w=1600&q=80"
          class="w-full h-full object-cover"
        />
      </div>
      <div
        class="relative max-w-[1400px] mx-auto px-6 grid lg:grid-cols-12 gap-10 items-center"
      >
        <div class="lg:col-span-6">
          <div
            class="text-xs tracking-[0.3em] uppercase font-semibold text-michelin-red mb-4"
          >
            L'édito · Avril 2026
          </div>
          <h2
            class="font-display text-4xl md:text-6xl font-bold leading-[1.05] mb-6"
          >
            La bonne table n'appartient plus aux critiques.
          </h2>
          <p
            class="text-lg leading-relaxed text-michelin-cream/80 font-display"
          >
            Elle se construit dans les stories, dans les groupes WhatsApp du
            vendredi soir, dans les tables partagées où l'on dîne avec des
            inconnus. Michelin n'arrête pas de juger. Il commence à écouter.
          </p>
          <div class="mt-8 flex items-center gap-3">
            <img
              src="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&q=80"
              class="w-10 h-10 rounded-full"
            />
            <div>
              <div class="font-medium">Léa Moreau</div>
              <div class="text-xs text-michelin-cream/60">
                Rédactrice en chef · 8 min de lecture
              </div>
            </div>
          </div>
        </div>
        <div class="lg:col-span-6 lg:pl-10">
          <blockquote
            class="editorial-quote font-display text-3xl md:text-4xl italic leading-relaxed"
          >
            On ne choisit plus un restaurant pour se rassurer. On le choisit
            pour raconter une soirée qu'on n'a pas encore vécue.
          </blockquote>
        </div>
      </div>
    </section>

    <!-- COMMUNITY TEASER -->
    <section class="max-w-[1400px] mx-auto px-6 py-24">
      <div class="grid lg:grid-cols-2 gap-10">
        <NuxtLink
          to="/tables-ouvertes"
          class="group relative aspect-[4/3] overflow-hidden bg-michelin-ink"
        >
          <img
            src="https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=1200&q=80"
            class="absolute inset-0 w-full h-full object-cover opacity-70 group-hover:scale-105 transition-transform duration-700"
          />
          <div
            class="absolute inset-0 bg-gradient-to-tr from-michelin-red/70 to-transparent mix-blend-multiply"
          ></div>
          <div
            class="absolute inset-0 p-10 flex flex-col justify-between text-michelin-cream"
          >
            <div class="text-xs uppercase tracking-[0.3em] font-semibold">
              Tables Ouvertes
            </div>
            <div>
              <h3
                class="font-display text-4xl md:text-5xl font-bold leading-tight mb-4"
              >
                Dînez avec des inconnus. Repartez avec des amis.
              </h3>
              <div
                class="inline-flex items-center gap-2 border-b-2 border-michelin-cream pb-1 text-sm uppercase tracking-wider group-hover:gap-4 transition-all"
              >
                Voir les événements
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M5 12h14m-6-6 6 6-6 6" />
                </svg>
              </div>
            </div>
          </div>
        </NuxtLink>
        <NuxtLink
          to="/collections"
          class="group relative aspect-[4/3] overflow-hidden bg-michelin-gold"
        >
          <img
            src="https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=1200&q=80"
            class="absolute inset-0 w-full h-full object-cover opacity-70 group-hover:scale-105 transition-transform duration-700"
          />
          <div
            class="absolute inset-0 bg-gradient-to-tr from-michelin-ink/80 to-transparent"
          ></div>
          <div
            class="absolute inset-0 p-10 flex flex-col justify-between text-michelin-cream"
          >
            <div class="text-xs uppercase tracking-[0.3em] font-semibold">
              Collections
            </div>
            <div>
              <h3
                class="font-display text-4xl md:text-5xl font-bold leading-tight mb-4"
              >
                Les listes que vos potes vous enverraient.
              </h3>
              <div
                class="inline-flex items-center gap-2 border-b-2 border-michelin-cream pb-1 text-sm uppercase tracking-wider group-hover:gap-4 transition-all"
              >
                Parcourir
                <svg
                  class="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M5 12h14m-6-6 6 6-6 6" />
                </svg>
              </div>
            </div>
          </div>
        </NuxtLink>
      </div>
    </section>

    <!-- PODCASTS TEASER -->
    <section class="bg-michelin-ink text-michelin-cream py-24">
      <div class="max-w-[1400px] mx-auto px-6">
        <div class="flex items-end justify-between mb-12 flex-wrap gap-4">
          <div>
            <div
              class="text-xs tracking-[0.3em] uppercase font-semibold text-michelin-red mb-3"
            >
              Podcast
            </div>
            <h2 class="font-display text-5xl md:text-6xl font-bold">
              À écouter<span class="text-michelin-red">.</span>
            </h2>
          </div>
          <NuxtLink
            to="/podcasts"
            class="text-sm uppercase tracking-wider font-medium hover:text-michelin-red flex items-center gap-2 transition-colors"
          >
            Tous les épisodes →
          </NuxtLink>
        </div>
        <div class="grid md:grid-cols-3 gap-6">
          <div
            v-for="ep in podcasts.episodes.slice(0, 3)"
            :key="ep.id"
            class="group cursor-pointer"
            @click="podcasts.play(ep.id)"
          >
            <div class="relative aspect-square overflow-hidden mb-4">
              <img
                :src="ep.cover"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div
                class="absolute inset-0 bg-michelin-ink/30 group-hover:bg-michelin-ink/50 transition-colors"
              ></div>
              <div class="absolute inset-0 flex items-center justify-center">
                <div
                  class="w-16 h-16 bg-michelin-red rounded-full flex items-center justify-center group-hover:scale-110 transition-transform"
                >
                  <svg
                    v-if="
                      podcasts.nowPlaying?.id === ep.id && podcasts.isPlaying
                    "
                    class="w-6 h-6"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <rect x="6" y="5" width="4" height="14" />
                    <rect x="14" y="5" width="4" height="14" />
                  </svg>
                  <svg
                    v-else
                    class="w-6 h-6 ml-1"
                    fill="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path d="M8 5v14l11-7z" />
                  </svg>
                </div>
              </div>
            </div>
            <div
              class="text-xs uppercase tracking-widest text-michelin-red mb-1"
            >
              {{ ep.show }}
            </div>
            <h3
              class="font-display text-xl font-bold group-hover:text-michelin-red transition-colors"
            >
              {{ ep.title }}
            </h3>
            <div class="text-sm text-michelin-cream/60 mt-1">
              {{ ep.duration }} · {{ ep.date }}
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRestaurantsStore } from "~/stores/restaurants";
import { usePodcastsStore } from "~/stores/podcasts";

const restaurants = useRestaurantsStore();
const podcasts = usePodcastsStore();
const router = useRouter();

const tickerItems = [
  "Septime · 1 étoile",
  "Clamato · Bib Gourmand",
  "Tables ouvertes ce week-end",
  "Nouveau · Datil par Manon Fleury",
  "Lyon · 12 nouvelles adresses",
  "Podcast · Iñaki Aizpitarte",
];

const moods = [
  {
    label: "Premier date",
    sub: "Ambiance",
    emoji: "💌",
    filter: "Date",
    image:
      "https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=500&q=80",
  },
  {
    label: "Entre amis",
    sub: "Partage",
    emoji: "🍷",
    filter: "Entre amis",
    image:
      "https://images.unsplash.com/photo-1414235077428-338989a2e8c0?w=500&q=80",
  },
  {
    label: "Solo luxe",
    sub: "Comptoir",
    emoji: "🎧",
    filter: "Solo",
    image:
      "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?w=500&q=80",
  },
  {
    label: "Petit budget",
    sub: "—30€",
    emoji: "💸",
    filter: null,
    budget: "€",
    image:
      "https://images.unsplash.com/photo-1509722747041-616f39b57569?w=500&q=80",
  },
  {
    label: "Late night",
    sub: "Après 22h",
    emoji: "🌙",
    filter: null,
    image:
      "https://images.unsplash.com/photo-1498654896293-37aacf113fd9?w=500&q=80",
  },
  {
    label: "Étoilé",
    sub: "Grand frisson",
    emoji: "⭐",
    filter: null,
    distinction: "Étoilé",
    image:
      "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=500&q=80",
  },
];

const featured = computed(() => restaurants.restaurants.slice(0, 4));

function selectMood(m) {
  restaurants.resetFilters();
  if (m.filter) restaurants.setFilter("occasion", m.filter);
  if (m.budget) restaurants.setFilter("budget", m.budget);
  if (m.distinction) restaurants.setFilter("distinction", m.distinction);
  router.push("/restaurants");
}
</script>
