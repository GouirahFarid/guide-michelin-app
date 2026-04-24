<template>
  <article class="group relative bg-michelin-cream">
    <NuxtLink :to="`/restaurants/${r.id}`" class="block">
      <div class="relative aspect-[4/5] overflow-hidden bg-michelin-sand">
        <img
          :src="r.image"
          :alt="r.name"
          class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-[1.05]"
          loading="lazy"
        />
        <!-- Gradient overlay -->
        <div
          class="absolute inset-0 bg-gradient-to-t from-michelin-ink/90 via-michelin-ink/10 to-transparent"
        ></div>

        <!-- Top badges -->
        <div
          class="absolute top-3 left-3 right-3 flex items-start justify-between"
        >
          <div class="flex gap-1.5 flex-wrap">
            <span
              v-if="r.stars > 0"
              class="bg-michelin-red text-michelin-cream text-[10px] font-bold tracking-widest uppercase px-2 py-1 flex items-center gap-1"
            >
              <span v-for="i in r.stars" :key="i">★</span>
              <span>Étoile{{ r.stars > 1 ? "s" : "" }}</span>
            </span>
            <span
              v-if="r.bib"
              class="bg-michelin-cream text-michelin-ink text-[10px] font-bold tracking-widest uppercase px-2 py-1"
            >
              Bib Gourmand
            </span>
          </div>
          <button
            @click.prevent.stop="user.toggleWishlist(r.id)"
            class="w-9 h-9 bg-michelin-cream/95 backdrop-blur-sm flex items-center justify-center hover:bg-michelin-red hover:text-michelin-cream transition-colors"
            :aria-label="user.hasWishlisted(r.id) ? 'Retirer' : 'Sauvegarder'"
          >
            <svg
              v-if="user.hasWishlisted(r.id)"
              class="w-4 h-4 text-michelin-red"
              fill="currentColor"
              viewBox="0 0 24 24"
            >
              <path d="M5 3v18l7-5 7 5V3z" />
            </svg>
            <svg
              v-else
              class="w-4 h-4"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              viewBox="0 0 24 24"
            >
              <path d="M5 3v18l7-5 7 5V3z" />
            </svg>
          </button>
        </div>

        <!-- Bottom content -->
        <div class="absolute bottom-0 inset-x-0 p-5 text-michelin-cream">
          <div
            class="flex items-center gap-2 text-[11px] uppercase tracking-widest opacity-80 mb-2"
          >
            <span>{{ r.city }} · {{ r.district }}</span>
            <span class="w-1 h-1 rounded-full bg-michelin-cream"></span>
            <span>{{ r.budget }}</span>
          </div>
          <h3 class="font-display text-2xl md:text-3xl font-bold leading-tight">
            {{ r.name }}
          </h3>
          <div class="mt-1 text-sm opacity-90">
            {{ r.cuisine }} · {{ r.vibe }}
          </div>
        </div>
      </div>

      <!-- Meta row -->
      <!-- <div class="flex items-center justify-between pt-3 text-sm">
        <div class="flex items-center gap-1.5">
          <svg class="w-4 h-4 text-michelin-gold" fill="currentColor" viewBox="0 0 24 24">
            <path d="M12 2l3 7h7l-5.5 4.5L18 21l-6-4.5L6 21l1.5-7.5L2 9h7z"/>
          </svg>
          <span class="font-semibold">{{ r.rating }}</span>
          <span class="text-michelin-stone">/5</span>
        </div>
        <div class="text-michelin-stone text-xs">
          Par {{ r.chef }}
        </div>
      </div> -->
    </NuxtLink>
  </article>
</template>

<script setup>
import { useUserStore } from "~/stores/user";
defineProps({ r: { type: Object, required: true } });
const user = useUserStore();
</script>
