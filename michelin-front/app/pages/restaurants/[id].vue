<template>
  <div v-if="r">
    <!-- Hero -->
    <section class="relative h-[70vh] min-h-[500px] overflow-hidden">
      <img :src="r.image" class="absolute inset-0 w-full h-full object-cover" />
      <div
        class="absolute inset-0 bg-gradient-to-t from-michelin-ink via-michelin-ink/40 to-transparent"
      ></div>

      <div class="absolute top-8 left-0 right-0 max-w-[1400px] mx-auto px-6">
        <NuxtLink
          to="/restaurants"
          class="inline-flex items-center gap-2 text-michelin-cream text-sm uppercase tracking-wider hover:text-michelin-red transition-colors"
        >
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
            viewBox="0 0 24 24"
          >
            <path d="M19 12H5m6 6-6-6 6-6" />
          </svg>
          Retour aux restaurants
        </NuxtLink>
      </div>

      <div
        class="absolute bottom-0 left-0 right-0 max-w-[1400px] mx-auto px-6 pb-12 text-michelin-cream"
      >
        <div class="flex gap-2 mb-5">
          <span
            v-if="r.stars === 1"
            class="bg-michelin-red px-3 py-1.5 text-xs font-bold tracking-widest uppercase"
          >
            {{ "★".repeat(r.stars) }} Étoile{{ r.stars > 1 ? "s" : "" }}
          </span>
          <span
            v-if="r.bib"
            class="bg-michelin-cream text-michelin-ink px-3 py-1.5 text-xs font-bold tracking-widest uppercase"
          >
            Bib Gourmand
          </span>
          <span
            class="border border-michelin-cream/40 px-3 py-1.5 text-xs tracking-widest uppercase"
          >
            {{ r.cuisine }}
          </span>
        </div>
        <h1 class="font-display text-6xl md:text-8xl font-black leading-none">
          {{ r.name }}
        </h1>
        <div class="mt-4 flex flex-wrap items-center gap-4 text-sm">
          <span>{{ r.city }} · {{ r.district }}</span>
          <span class="w-1 h-1 rounded-full bg-michelin-cream"></span>
          <span>Par {{ r.chef }}</span>
          <span class="w-1 h-1 rounded-full bg-michelin-cream"></span>
          <span>{{ r.price }}</span>
        </div>
      </div>
    </section>

    <!-- Actions bar -->
    <section
      class="sticky top-[112px] z-40 bg-michelin-cream border-b border-michelin-ink/10"
    >
      <div
        class="max-w-[1400px] mx-auto px-6 py-4 flex items-center justify-between gap-4 flex-wrap"
      >
        <div class="flex items-center gap-1.5">
          <svg
            class="w-5 h-5 text-michelin-gold"
            fill="currentColor"
            viewBox="0 0 24 24"
          >
            <path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4.5L6 21l1.5-7.5L2 9h7z" />
          </svg>
          <span class="font-display font-bold text-xl">{{ r.rating }}</span>
          <span class="text-michelin-stone text-sm ml-1">· 342 avis</span>
        </div>
        <div class="flex items-center gap-2">
          <button
            @click="user.toggleTested(r.id)"
            :class="[
              'px-4 py-2 text-sm uppercase tracking-wider transition-all flex items-center gap-2',
              user.hasTested(r.id)
                ? 'bg-michelin-red text-michelin-cream'
                : 'border border-michelin-ink hover:bg-michelin-ink hover:text-michelin-cream',
            ]"
          >
            <svg
              v-if="user.hasTested(r.id)"
              class="w-4 h-4"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M9 16.17 4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
            </svg>
            {{ user.hasTested(r.id) ? "Testé" : "J'ai testé" }}
          </button>
          <button
            @click="user.toggleWishlist(r.id)"
            :class="[
              'px-4 py-2 text-sm uppercase tracking-wider transition-all flex items-center gap-2',
              user.hasWishlisted(r.id)
                ? 'bg-michelin-ink text-michelin-cream'
                : 'border border-michelin-ink hover:bg-michelin-ink hover:text-michelin-cream',
            ]"
          >
            <svg
              class="w-4 h-4"
              :fill="user.hasWishlisted(r.id) ? 'currentColor' : 'none'"
              stroke="currentColor"
              stroke-width="1.5"
              viewBox="0 0 24 24"
            >
              <path d="M5 3v18l7-5 7 5V3z" />
            </svg>
            Sauvegarder
          </button>
          <button
            class="px-4 py-2 text-sm uppercase tracking-wider border border-michelin-ink hover:bg-michelin-ink hover:text-michelin-cream transition-all"
          >
            Réserver
          </button>
        </div>
      </div>
    </section>

    <div class="max-w-[1400px] mx-auto px-6 py-16 grid lg:grid-cols-12 gap-12">
      <!-- Main content -->
      <div class="lg:col-span-8">
        <!-- Review -->
        <div class="mb-12">
          <div
            class="text-xs tracking-[0.3em] uppercase font-semibold text-michelin-red mb-3"
          >
            L'avis Michelin
          </div>
          <blockquote
            class="editorial-quote font-display text-3xl md:text-4xl italic leading-snug"
          >
            {{ r.review }}
          </blockquote>
        </div>

        <!-- Signature -->
        <div class="bg-michelin-sand p-8 mb-12 relative overflow-hidden">
          <div
            class="absolute top-4 right-4 text-[120px] font-display text-michelin-red/10 leading-none"
          >
            ✦
          </div>
          <div
            class="text-xs tracking-[0.3em] uppercase font-semibold text-michelin-red mb-2"
          >
            Plat signature
          </div>
          <div class="font-display text-2xl font-bold">{{ r.signature }}</div>
        </div>

        <!-- Description -->
        <div
          class="prose max-w-none font-display text-lg leading-relaxed text-michelin-ink-soft"
        >
          <p>{{ r.description }}</p>
        </div>

        <!-- Tags -->
        <div class="mt-10 flex flex-wrap gap-2">
          <span
            v-for="t in r.tags"
            :key="t"
            class="px-3 py-1.5 border border-michelin-ink/20 text-sm"
            >#{{ t }}</span
          >
        </div>

        <!-- Community posts -->
        <div class="mt-16">
          <div class="flex items-center gap-3 mb-6">
            <h2 class="font-display text-3xl font-bold">La communauté parle</h2>
            <div class="flex-1 h-px bg-michelin-ink/10"></div>
          </div>
          <div class="space-y-6">
            <div
              v-for="p in posts"
              :key="p.id"
              class="p-6 border border-michelin-ink/10 hover:border-michelin-red/40 transition-colors"
            >
              <div class="flex items-center gap-3 mb-3">
                <img
                  :src="p.avatar"
                  class="w-10 h-10 rounded-full object-cover"
                />
                <div>
                  <div class="font-semibold">{{ p.name }}</div>
                  <div class="text-xs text-michelin-stone">
                    {{ p.handle }} · {{ p.date }}
                  </div>
                </div>
                <div class="ml-auto flex text-michelin-gold text-sm">
                  <span
                    v-for="i in 5"
                    :key="i"
                    :class="i > p.rating ? 'text-michelin-ink/20' : ''"
                    >★</span
                  >
                </div>
              </div>
              <p class="text-michelin-ink-soft">{{ p.text }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="lg:col-span-4 space-y-8">
        <!-- Info card -->
        <div class="bg-michelin-ink text-michelin-cream p-8">
          <div class="font-display text-2xl font-bold mb-6">Informations</div>
          <dl class="space-y-4 text-sm">
            <div
              class="flex justify-between border-b border-michelin-cream/10 pb-3"
            >
              <dt
                class="text-michelin-cream/60 uppercase tracking-wider text-xs"
              >
                Chef
              </dt>
              <dd class="font-medium">{{ r.chef }}</dd>
            </div>
            <div
              class="flex justify-between border-b border-michelin-cream/10 pb-3"
            >
              <dt
                class="text-michelin-cream/60 uppercase tracking-wider text-xs"
              >
                Prix moyen
              </dt>
              <dd class="font-medium">{{ r.price }}</dd>
            </div>
            <div
              class="flex justify-between border-b border-michelin-cream/10 pb-3"
            >
              <dt
                class="text-michelin-cream/60 uppercase tracking-wider text-xs"
              >
                Ambiance
              </dt>
              <dd class="font-medium">{{ r.vibe }}</dd>
            </div>
            <div class="flex justify-between">
              <dt
                class="text-michelin-cream/60 uppercase tracking-wider text-xs"
              >
                Occasions
              </dt>
              <dd class="font-medium text-right">
                {{ r.occasions.join(" · ") }}
              </dd>
            </div>
          </dl>
        </div>

        <!-- Add to collection -->
        <div class="border border-michelin-ink p-6">
          <div
            class="text-xs uppercase tracking-[0.3em] text-michelin-red font-semibold mb-3"
          >
            Ajouter à une collection
          </div>
          <div class="space-y-2 mb-4">
            <label
              v-for="c in collections.myCollections"
              :key="c.id"
              class="flex items-center gap-3 p-3 border border-michelin-ink/10 cursor-pointer hover:border-michelin-red transition-colors"
            >
              <input
                type="checkbox"
                :checked="c.restaurants.includes(r.id)"
                @change="toggleCol(c.id)"
                class="w-4 h-4 accent-michelin-red"
              />
              <span class="text-xl">{{ c.emoji }}</span>
              <span class="flex-1 text-sm font-medium">{{ c.title }}</span>
              <span class="text-xs text-michelin-stone">{{
                c.restaurants.length
              }}</span>
            </label>
          </div>
          <NuxtLink
            to="/collections"
            class="text-xs uppercase tracking-wider hover:text-michelin-red transition-colors"
            >+ Créer une nouvelle collection</NuxtLink
          >
        </div>

        <!-- Tables ouvertes -->
        <div
          v-if="eventsHere.length"
          class="bg-michelin-red text-michelin-cream p-6"
        >
          <div class="text-xs uppercase tracking-[0.3em] font-semibold mb-2">
            Table ouverte ici
          </div>
          <div v-for="e in eventsHere" :key="e.id" class="mt-4">
            <div class="font-display text-xl font-bold">{{ e.title }}</div>
            <div class="text-sm opacity-90 mt-1">
              {{ formatDate(e.date) }} · {{ e.time }}
            </div>
            <NuxtLink
              :to="`/tables-ouvertes`"
              class="mt-4 inline-flex items-center gap-2 text-sm uppercase tracking-wider border-b border-michelin-cream pb-1 hover:gap-4 transition-all"
            >
              Rejoindre →
            </NuxtLink>
          </div>
        </div>
      </aside>
    </div>
  </div>
  <div v-else class="max-w-[1400px] mx-auto px-6 py-20 text-center">
    <div class="font-display text-4xl mb-4">Restaurant introuvable</div>
    <NuxtLink to="/restaurants" class="btn-ghost"
      >Retour aux restaurants</NuxtLink
    >
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRestaurantsStore } from "~/stores/restaurants";
import { useCollectionsStore } from "~/stores/collections";
import { useUserStore } from "~/stores/user";
import { useEventsStore } from "~/stores/events";

const route = useRoute();
const restaurants = useRestaurantsStore();
const collections = useCollectionsStore();
const user = useUserStore();
const events = useEventsStore();

const r = computed(() => restaurants.byId(route.params.id));
const eventsHere = computed(() =>
  events.events.filter((e) => e.restaurantId === route.params.id),
);

const posts = [
  {
    id: 1,
    name: "Thomas V.",
    handle: "@thom.eats",
    avatar:
      "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80",
    rating: 5,
    date: "il y a 3 jours",
    text: "La meilleure table où j'ai mis les pieds ce trimestre. Service précis, rythme parfait, et cette assiette de pigeon qu'on n'oublie pas.",
  },
  {
    id: 2,
    name: "Mia R.",
    handle: "@mia.roma",
    avatar:
      "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=100&q=80",
    rating: 4,
    date: "il y a 1 semaine",
    text: "Ambiance électrique, cartes des vins qui éduque. Petit bémol sur l'attente à table (25 min) mais tout est pardonné au dessert.",
  },
  {
    id: 3,
    name: "Yann K.",
    handle: "@yann.plates",
    avatar:
      "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80",
    rating: 5,
    date: "il y a 2 semaines",
    text: "Quatrième passage. Ils gardent le niveau. Et ça, en 2026, ça mérite une médaille.",
  },
];

function toggleCol(id) {
  const c = collections.byId(id);
  if (!c) return;
  if (c.restaurants.includes(route.params.id))
    collections.removeFromCollection(id, route.params.id);
  else collections.addToCollection(id, route.params.id);
}

function formatDate(d) {
  return new Date(d).toLocaleDateString("fr-FR", {
    day: "numeric",
    month: "long",
  });
}
</script>
