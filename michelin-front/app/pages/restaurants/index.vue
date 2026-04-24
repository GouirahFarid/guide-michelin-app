<template>
  <div class="max-w-[1400px] mx-auto px-6 py-12">
    <!-- Header -->
    <div class="mb-10 flex items-end justify-between flex-wrap gap-6">
      <div>
        <!-- <div class="text-xs tracking-[0.3em] uppercase font-semibold text-michelin-red mb-3">Sélection Michelin · 2026</div> -->
        <h1 class="font-display text-6xl md:text-7xl font-black leading-[0.95]">
          Restaurants
          <!-- <span class="text-michelin-red">.</span> -->
        </h1>
        <p class="mt-4 text-lg text-michelin-ink-soft max-w-xl font-display">
          Chaque adresse est visitée, jugée et commentée par la communauté.
          Toujours validée par nos inspecteurs.
        </p>
      </div>

      <!-- View toggle -->
      <div class="flex border border-michelin-ink">
        <button
          @click="view = 'grid'"
          :class="[
            'px-4 py-2 text-xs uppercase tracking-wider transition-colors',
            view === 'grid'
              ? 'bg-michelin-ink text-michelin-cream'
              : 'hover:bg-michelin-ink/5',
          ]"
        >
          Grille
        </button>
        <button
          @click="view = 'list'"
          :class="[
            'px-4 py-2 text-xs uppercase tracking-wider transition-colors',
            view === 'list'
              ? 'bg-michelin-ink text-michelin-cream'
              : 'hover:bg-michelin-ink/5',
          ]"
        >
          Liste éditoriale
        </button>
      </div>
    </div>

    <!-- Search -->
    <div class="relative mb-6">
      <svg
        class="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-michelin-stone"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        viewBox="0 0 24 24"
      >
        <circle cx="11" cy="11" r="7" />
        <path d="m21 21-4.35-4.35" />
      </svg>
      <input
        :value="store.filters.search"
        @input="store.setFilter('search', $event.target.value)"
        type="text"
        placeholder="Chercher un restaurant, un chef, une cuisine…"
        class="w-full pl-12 pr-4 py-4 bg-michelin-cream border-2 border-michelin-ink focus:border-michelin-red outline-none text-lg font-display"
      />
    </div>

    <!-- Filter chips -->
    <div class="grid grid-cols-2 md:grid-cols-5 gap-3 mb-10">
      <FilterSelect
        label="Ville"
        :options="store.cities"
        :value="store.filters.city"
        @input="store.setFilter('city', $event)"
      />
      <FilterSelect
        label="Cuisine"
        :options="store.cuisines"
        :value="store.filters.cuisine"
        @input="store.setFilter('cuisine', $event)"
      />
      <FilterSelect
        label="Budget"
        :options="['Tous', '€', '€€', '€€€', '€€€€']"
        :value="store.filters.budget"
        @input="store.setFilter('budget', $event)"
      />
      <FilterSelect
        label="Distinction"
        :options="['Tous', 'Étoilé', 'Bib Gourmand']"
        :value="store.filters.distinction"
        @input="store.setFilter('distinction', $event)"
      />
      <FilterSelect
        label="Occasion"
        :options="[
          'Toutes',
          'Date',
          'Entre amis',
          'Solo',
          'Famille',
          'Occasion spéciale',
        ]"
        :value="store.filters.occasion"
        @input="store.setFilter('occasion', $event)"
      />
    </div>

    <!-- Active filters + count -->
    <div
      class="flex items-center justify-between mb-8 pb-4 border-b border-michelin-ink/10"
    >
      <div class="text-sm">
        <span class="font-display text-2xl font-bold">{{
          store.filtered.length
        }}</span>
        <span class="text-michelin-stone ml-2"
          >adresse{{ store.filtered.length > 1 ? "s" : "" }}</span
        >
      </div>
      <button
        @click="store.resetFilters()"
        class="text-sm uppercase tracking-wider hover:text-michelin-red transition-colors flex items-center gap-1.5"
      >
        <svg
          class="w-4 h-4"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          viewBox="0 0 24 24"
        >
          <path d="M3 12a9 9 0 1 0 3-6.7L3 8m0-5v5h5" />
        </svg>
        Réinitialiser
      </button>
    </div>

    <!-- Grid view -->
    <div
      v-if="view === 'grid'"
      class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
    >
      <RestaurantCard v-for="r in store.filtered" :key="r.id" :r="r" />
    </div>

    <!-- List editorial view -->
    <div v-else class="space-y-0">
      <NuxtLink
        v-for="(r, i) in store.filtered"
        :key="r.id"
        :to="`/restaurants/${r.id}`"
        class="group grid grid-cols-12 gap-6 py-8 border-t border-michelin-ink/10 first:border-t-0 hover:bg-michelin-sand/50 -mx-4 px-4 transition-colors"
      >
        <div class="col-span-1 font-mono text-sm text-michelin-stone pt-2">
          {{ String(i + 1).padStart(2, "0") }}
        </div>
        <div class="col-span-3 md:col-span-2">
          <div class="aspect-square overflow-hidden bg-michelin-sand">
            <img
              :src="r.image"
              class="w-full h-full object-cover group-hover:scale-105 transition-transform"
            />
          </div>
        </div>
        <div class="col-span-8 md:col-span-6 flex flex-col justify-center">
          <div
            class="flex items-center gap-2 text-xs uppercase tracking-widest text-michelin-stone mb-2"
          >
            <span>{{ r.city }} · {{ r.district }}</span>
            <span>·</span>
            <span>{{ r.cuisine }}</span>
            <span v-if="r.stars > 0" class="text-michelin-red"
              >★{{ r.stars }}</span
            >
            <span v-if="r.bib" class="text-michelin-red">Bib</span>
          </div>
          <h3
            class="font-display text-3xl md:text-4xl font-bold group-hover:text-michelin-red transition-colors leading-tight"
          >
            {{ r.name }}
          </h3>
          <p class="mt-2 text-michelin-ink-soft hidden md:block">
            {{ r.description }}
          </p>
        </div>
        <div
          class="col-span-12 md:col-span-3 flex md:flex-col md:items-end md:justify-center gap-2 text-right"
        >
          <div class="text-2xl font-display font-bold">{{ r.budget }}</div>
          <div class="text-sm text-michelin-stone">{{ r.price }}</div>
          <div class="flex items-center gap-1 text-sm mt-2 md:mt-3">
            <span class="text-michelin-gold">★</span>
            <span class="font-semibold">{{ r.rating }}</span>
          </div>
        </div>
      </NuxtLink>
    </div>

    <!-- Empty -->
    <div v-if="store.filtered.length === 0" class="py-20 text-center">
      <div class="font-display text-3xl mb-3">
        Aucune adresse ne correspond.
      </div>
      <p class="text-michelin-stone mb-6">Essayez de relâcher un filtre.</p>
      <button @click="store.resetFilters()" class="btn-ghost">
        Tout réinitialiser
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRestaurantsStore } from "~/stores/restaurants";
const store = useRestaurantsStore();
const view = ref("grid");
</script>
