<template>
  <footer
    class="bg-michelin-ink text-michelin-cream mt-24 relative overflow-hidden"
  >
    <!-- Marquee -->

    <div class="max-w-[1400px] mx-auto px-6 py-16 grid md:grid-cols-4 gap-10">
      <div class="md:col-span-2">
        <div class="flex items-center gap-3 mb-6">
          <!-- <div
            class="w-10 h-10 bg-michelin-red flex items-center justify-center"
          >
            <div class="w-5 h-5 star-shape bg-michelin-cream"></div>
          </div> -->
          <div class="font-display text-2xl font-black">
            <img
              src="/images/michelin-guide-logo.svg"
              alt="Michelin Guide"
              class="h-8"
            />
          </div>
        </div>
        <p
          class="text-michelin-cream/70 max-w-md leading-relaxed text-lg font-display"
        >
          La sélection officielle du Guide Michelin, repensée avec et pour
          celles et ceux qui inventent la table d'aujourd'hui.
        </p>
        <div class="mt-8 flex items-center gap-3">
          <input
            type="email"
            placeholder="votre@email.fr"
            class="flex-1 bg-transparent border-b border-michelin-cream/30 py-2 outline-none focus:border-michelin-red transition-colors"
          />
          <button
            class="px-5 py-2 bg-michelin-red hover:bg-michelin-red-dark text-sm uppercase tracking-wider transition-colors"
          >
            S'abonner
          </button>
        </div>
      </div>

      <div>
        <div class="text-xs uppercase tracking-[0.2em] text-michelin-red mb-4">
          Découvrir
        </div>
        <ul class="space-y-2">
          <li
            v-for="l in [
              'Restaurants',
              'Collections',
              'Tables ouvertes',
              'Podcasts',
              'Communauté',
            ]"
            :key="l"
          >
            <a href="#" class="hover:text-michelin-red transition-colors">{{
              l
            }}</a>
          </li>
        </ul>
      </div>

      <div>
        <div class="text-xs uppercase tracking-[0.2em] text-michelin-red mb-4">
          Maison
        </div>
        <ul class="space-y-2">
          <li
            v-for="l in [
              'À propos',
              'Méthode d\'inspection',
              'Presse',
              'Carrières',
              'Contact',
            ]"
            :key="l"
          >
            <a href="#" class="hover:text-michelin-red transition-colors">{{
              l
            }}</a>
          </li>
        </ul>
      </div>
    </div>

    <div class="border-t border-michelin-cream/10 py-6">
      <div
        class="max-w-[1400px] mx-auto px-6 flex flex-col md:flex-row items-center justify-between text-sm text-michelin-cream/50 gap-3"
      >
        <div>© 2026 Michelin Guide · Tous droits réservés</div>
        <div class="flex gap-5">
          <a href="#" class="hover:text-michelin-cream transition-colors"
            >Mentions</a
          >
          <a href="#" class="hover:text-michelin-cream transition-colors"
            >Confidentialité</a
          >
          <a href="#" class="hover:text-michelin-cream transition-colors"
            >Cookies</a
          >
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
const marqueeWords = [
  "Bistronomie",
  "Bib Gourmand",
  "Tables Ouvertes",
  "Vin Nature",
  "Communauté",
  "Chefs",
  "Guide",
];
</script>
