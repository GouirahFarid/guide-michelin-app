<template>
  <header
    :class="[
      'sticky top-0 z-50 transition-all duration-300 border-b',
      scrolled
        ? 'bg-michelin-cream/95 backdrop-blur-md border-michelin-ink/10'
        : 'bg-michelin-cream border-transparent',
    ]"
  >
    <!-- Top strip -->
    <div
      class="bg-michelin-ink text-michelin-cream text-[11px] tracking-[0.2em] uppercase"
    >
      <!-- <div
        class="max-w-[1400px] mx-auto px-6 py-2 flex items-center justify-between"
      >
        <div class="flex items-center gap-6">
          <span class="hidden md:inline opacity-70">Depuis 1900 · Réinventé en 2026</span>
          <span class="text-michelin-gold">⭐ Sélection officielle Michelin</span>
        </div>
        <div class="flex items-center gap-4 opacity-70 hidden md:flex">
          <span>FR</span>
          <span>·</span>
          <span>Paris · 18°C</span>
        </div>
      </div> -->
    </div>

    <!-- Main nav -->
    <div class="max-w-[1400px] mx-auto px-6">
      <div class="flex items-center justify-between h-20">
        <!-- Logo -->
        <NuxtLink to="/" class="group flex items-center gap-3">
          <!-- <div
            class="relative w-11 h-11 bg-michelin-red text-michelin-cream flex items-center justify-center overflow-hidden transition-transform group-hover:rotate-[15deg]"
          >
            <svg
              viewBox="0 0 24 24"
              class="w-6 h-6 star-shape bg-michelin-cream"
            ></svg>
            <div
              class="absolute inset-0 border-2 border-michelin-cream/30"
            ></div>
          </div> -->
          <div class="leading-none">
            <div class="font-display text-2xl font-black">
              <img
                src="/images/michelin-guide-logo.svg"
                alt="Michelin Guide"
                class="h-8"
              />
            </div>
          </div>
        </NuxtLink>

        <!-- Desktop Nav -->
        <nav class="hidden lg:flex items-center gap-1">
          <NuxtLink
            v-for="link in links"
            :key="link.to"
            :to="link.to"
            class="relative px-4 py-2 text-sm font-medium tracking-wide hover:text-michelin-red transition-colors"
            active-class="text-michelin-red"
          >
            {{ link.label }}
            <span
              v-if="
                $route.path === link.to || $route.path.startsWith(link.to + '/')
              "
              class="absolute bottom-0 left-4 right-4 h-[2px] bg-michelin-red"
            ></span>
          </NuxtLink>
        </nav>

        <!-- Actions -->
        <div class="flex items-center gap-3">
          <button
            @click="searchOpen = true"
            class="p-2.5 hover:bg-michelin-ink hover:text-michelin-cream transition-colors"
            aria-label="Rechercher"
          >
            <svg
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
              viewBox="0 0 24 24"
            >
              <circle cx="11" cy="11" r="7" />
              <path d="m21 21-4.35-4.35" />
            </svg>
          </button>
          <NuxtLink
            to="/profile"
            class="hidden md:flex items-center gap-2 pl-3 pr-4 py-1.5 border border-michelin-ink hover:bg-michelin-ink hover:text-michelin-cream transition-colors"
          >
            <img
              :src="user.profile.avatar"
              class="w-7 h-7 rounded-full object-cover"
            />
            <span class="text-sm font-medium">{{
              user.profile.name.split(" ")[0]
            }}</span>
          </NuxtLink>
          <button
            @click="mobileOpen = !mobileOpen"
            class="lg:hidden p-2"
            aria-label="Menu"
          >
            <div class="w-6 flex flex-col gap-1.5">
              <span
                class="block h-[2px] bg-michelin-ink transition-all"
                :class="{ 'translate-y-[7px] rotate-45': mobileOpen }"
              ></span>
              <span
                class="block h-[2px] bg-michelin-ink transition-all"
                :class="{ 'opacity-0': mobileOpen }"
              ></span>
              <span
                class="block h-[2px] bg-michelin-ink transition-all"
                :class="{ '-translate-y-[7px] -rotate-45': mobileOpen }"
              ></span>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile menu -->
    <Transition
      enter-active-class="transition duration-300"
      enter-from-class="opacity-0 -translate-y-4"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition duration-200"
      leave-to-class="opacity-0"
    >
      <div
        v-if="mobileOpen"
        class="lg:hidden bg-michelin-cream border-t border-michelin-ink/10"
      >
        <nav class="max-w-[1400px] mx-auto px-6 py-4 flex flex-col">
          <NuxtLink
            v-for="link in links"
            :key="link.to"
            :to="link.to"
            @click="mobileOpen = false"
            class="py-3 border-b border-michelin-ink/5 font-display text-2xl hover:text-michelin-red transition-colors"
          >
            {{ link.label }}
          </NuxtLink>
        </nav>
      </div>
    </Transition>

    <!-- Search overlay -->
    <Transition
      enter-active-class="transition duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200"
      leave-to-class="opacity-0"
    >
      <div
        v-if="searchOpen"
        @click.self="searchOpen = false"
        class="fixed inset-0 z-[100] bg-michelin-ink/60 backdrop-blur-sm flex items-start justify-center pt-32 px-6"
      >
        <div
          class="w-full max-w-2xl bg-michelin-cream p-8 shadow-2xl animate-fade-up"
        >
          <div
            class="flex items-center gap-3 border-b-2 border-michelin-ink pb-4"
          >
            <svg
              class="w-6 h-6 text-michelin-red"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
              viewBox="0 0 24 24"
            >
              <circle cx="11" cy="11" r="7" />
              <path d="m21 21-4.35-4.35" />
            </svg>
            <input
              ref="searchInput"
              v-model="searchQuery"
              @keydown.enter="submitSearch"
              @keydown.esc="searchOpen = false"
              type="text"
              placeholder="Chercher un restaurant, un chef, une ville…"
              class="flex-1 bg-transparent text-xl outline-none placeholder:text-michelin-stone font-display"
            />
            <kbd
              class="text-xs bg-michelin-ink text-michelin-cream px-2 py-1 font-mono"
              >ESC</kbd
            >
          </div>
          <div class="mt-6">
            <div
              class="text-xs uppercase tracking-wider text-michelin-stone mb-3"
            >
              Recherches populaires
            </div>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="q in [
                  'Bistronomie Paris',
                  'Bib Gourmand',
                  'Date ambiance',
                  'Restaurants étoilés Lyon',
                  'Petit budget',
                ]"
                :key="q"
                @click="
                  searchQuery = q;
                  submitSearch();
                "
                class="px-3 py-1.5 border border-michelin-ink/20 text-sm hover:border-michelin-red hover:text-michelin-red transition-colors"
              >
                {{ q }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </header>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from "vue";
import { useUserStore } from "~/stores/user";
import { useRestaurantsStore } from "~/stores/restaurants";

const user = useUserStore();
const restaurants = useRestaurantsStore();
const router = useRouter();

const links = [
  { to: "/", label: "Accueil" },
  { to: "/restaurants", label: "Restaurants" },
  { to: "/collections", label: "Hébergements" },
  { to: "/tables-ouvertes", label: "Voyages" },
  { to: "/community", label: "Communauté" },
  { to: "/podcasts", label: "Podcasts" },
];

const scrolled = ref(false);
const mobileOpen = ref(false);
const searchOpen = ref(false);
const searchQuery = ref("");
const searchInput = ref(null);

watch(searchOpen, async (v) => {
  if (v) {
    await nextTick();
    searchInput.value?.focus();
  }
});

function submitSearch() {
  restaurants.setFilter("search", searchQuery.value);
  searchOpen.value = false;
  router.push("/restaurants");
}

function onScroll() {
  scrolled.value = window.scrollY > 20;
}
onMounted(() => window.addEventListener("scroll", onScroll, { passive: true }));
onBeforeUnmount(() => window.removeEventListener("scroll", onScroll));
</script>
