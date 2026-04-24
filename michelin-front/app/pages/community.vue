<template>
  <div>
    <!-- Hero -->
    <section
      class="relative bg-michelin-cream py-20 border-b border-michelin-ink/10"
    >
      <div
        class="max-w-[1400px] mx-auto px-6 grid lg:grid-cols-12 gap-10 items-end"
      >
        <div class="lg:col-span-8">
          <div
            class="text-xs tracking-[0.3em] uppercase font-semibold text-michelin-red mb-3"
          >
            La communauté
          </div>
          <h1
            class="font-display text-6xl md:text-8xl font-black leading-[0.9]"
          >
            143&nbsp;000
            <span class="italic font-light text-michelin-red">palais.</span
            ><br />
            Une seule table.
          </h1>
        </div>
        <div class="lg:col-span-4">
          <!-- <div class="flex items-center -space-x-3 mb-4">
            <img
              v-for="(a, i) in avatars"
              :key="i"
              :src="a"
              class="w-12 h-12 rounded-full border-2 border-michelin-cream object-cover"
            />
            <div
              class="w-12 h-12 rounded-full bg-michelin-red border-2 border-michelin-cream flex items-center justify-center text-michelin-cream text-xs font-bold"
            >
              +143K
            </div>
          </div> -->
          <p class="text-lg font-display text-michelin-ink-soft">
            Suivez les avis, les listes, les dîners de celles et ceux qui font
            la scène culinaire d'aujourd'hui.
          </p>
        </div>
      </div>
    </section>

    <div class="max-w-[1400px] mx-auto px-6 py-14 grid lg:grid-cols-12 gap-10">
      <!-- Feed -->
      <div class="lg:col-span-8">
        <!-- <h2
          class="font-display text-3xl font-bold mb-6 flex items-center gap-3"
        >
          Flux
          <span
            class="w-2 h-2 rounded-full bg-michelin-red animate-pulse-soft"
          ></span>
          <span
            class="text-xs uppercase tracking-widest text-michelin-stone font-sans"
            >en direct</span
          >
        </h2> -->
        <div class="space-y-6">
          <article
            v-for="(p, i) in feed"
            :key="p.id"
            class="bg-michelin-cream border border-michelin-ink/10 p-6 hover:border-michelin-red transition-colors"
            :style="{ animationDelay: `${i * 80}ms` }"
          >
            <div class="flex items-start gap-4">
              <img
                :src="p.avatar"
                class="w-12 h-12 rounded-full object-cover flex-shrink-0"
              />
              <div class="flex-1 min-w-0">
                <div class="flex items-baseline gap-2 flex-wrap">
                  <span class="font-display text-lg font-bold">{{
                    p.name
                  }}</span>
                  <span class="text-sm text-michelin-stone">{{
                    p.handle
                  }}</span>
                  <span class="text-sm text-michelin-stone">·</span>
                  <span class="text-sm text-michelin-stone">{{ p.time }}</span>
                </div>
                <div class="mt-1 text-sm text-michelin-stone">
                  <span>{{ p.action }} </span>
                  <span v-if="p.target" class="text-michelin-red font-medium">{{
                    p.target
                  }}</span>
                </div>
                <p
                  class="mt-3 text-michelin-ink leading-relaxed"
                  :class="{
                    'font-display text-lg italic': p.isReview,
                  }"
                >
                  {{ p.text }}
                </p>
                <div v-if="p.image" class="mt-4 aspect-[16/10] overflow-hidden">
                  <img :src="p.image" class="w-full h-full object-cover" />
                </div>
                <div v-if="p.rating" class="mt-3 flex gap-0.5">
                  <span
                    v-for="i in 5"
                    :key="i"
                    :class="
                      i > p.rating
                        ? 'text-michelin-ink/10'
                        : 'text-michelin-gold'
                    "
                    >★</span
                  >
                </div>
                <!-- Actions -->
                <div
                  class="mt-4 pt-4 border-t border-michelin-ink/10 flex items-center gap-6 text-sm text-michelin-stone"
                >
                  <button
                    @click="toggleLike(p)"
                    :class="[
                      'flex items-center gap-2 transition-colors',
                      p._liked
                        ? 'text-michelin-red'
                        : 'hover:text-michelin-red',
                    ]"
                  >
                    <svg
                      class="w-4 h-4"
                      :fill="p._liked ? 'currentColor' : 'none'"
                      stroke="currentColor"
                      stroke-width="1.5"
                      viewBox="0 0 24 24"
                    >
                      <path
                        d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"
                      />
                    </svg>
                    {{ p.likes }}
                  </button>
                  <button
                    class="flex items-center gap-2 hover:text-michelin-red transition-colors"
                  >
                    <svg
                      class="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1.5"
                      viewBox="0 0 24 24"
                    >
                      <path
                        d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                      />
                    </svg>
                    {{ p.comments }}
                  </button>
                  <button
                    class="flex items-center gap-2 hover:text-michelin-red transition-colors"
                  >
                    <svg
                      class="w-4 h-4"
                      fill="none"
                      stroke="currentColor"
                      stroke-width="1.5"
                      viewBox="0 0 24 24"
                    >
                      <path d="M5 3v18l7-5 7 5V3z" />
                    </svg>
                    Sauvegarder
                  </button>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>

      <!-- Sidebar -->
      <aside class="lg:col-span-4 space-y-8 lg:sticky lg:top-32 lg:self-start">
        <!-- Trending -->
        <!-- <div class="bg-michelin-ink text-michelin-cream p-6">
          <div class="text-xs uppercase tracking-[0.3em] text-michelin-red font-semibold mb-4">Tendances</div>
          <div class="space-y-4">
            <div v-for="(t, i) in trending" :key="t.tag" class="flex items-baseline gap-3">
              <span class="font-display text-3xl font-black text-michelin-red/50">{{ String(i+1).padStart(2, '0') }}</span>
              <div class="flex-1 min-w-0">
                <div class="font-display text-lg font-bold">{{ t.tag }}</div>
                <div class="text-xs text-michelin-cream/60">{{ t.posts }} publications</div>
              </div>
            </div>
          </div>
        </div> -->

        <!-- Members to follow -->
        <!-- <div class="border border-michelin-ink/10 p-6">
          <div
            class="text-xs uppercase tracking-[0.3em] text-michelin-red font-semibold mb-4"
          >
            Membres à suivre
          </div>
          <div class="space-y-4">
            <div
              v-for="m in suggestedMembers"
              :key="m.handle"
              class="flex items-center gap-3"
            >
              <img
                :src="m.avatar"
                class="w-11 h-11 rounded-full object-cover"
              />
              <div class="flex-1 min-w-0">
                <div class="font-medium truncate">{{ m.name }}</div>
                <div class="text-xs text-michelin-stone truncate">
                  {{ m.tagline }}
                </div>
              </div>
              <button
                @click="m._followed = !m._followed"
                :class="[
                  'text-xs uppercase tracking-wider px-3 py-1.5 transition-colors border',
                  m._followed
                    ? 'bg-michelin-ink text-michelin-cream border-michelin-ink'
                    : 'border-michelin-ink hover:bg-michelin-ink hover:text-michelin-cream',
                ]"
              >
                {{ m._followed ? "Suivi" : "Suivre" }}
              </button>
            </div>
          </div>
        </div> -->

        <!-- Stats -->
        <!-- <div class="grid grid-cols-2 gap-3">
          <div class="bg-michelin-red text-michelin-cream p-5">
            <div class="font-display text-4xl font-black">8,4M</div>
            <div class="text-xs uppercase tracking-widest opacity-80 mt-1">
              Avis partagés
            </div>
          </div>
          <div class="bg-michelin-ink text-michelin-cream p-5">
            <div class="font-display text-4xl font-black">27K</div>
            <div class="text-xs uppercase tracking-widest opacity-80 mt-1">
              Listes créées
            </div>
          </div>
        </div> -->
      </aside>
    </div>
  </div>
</template>

<script setup>
import { reactive } from "vue";

const avatars = [
  "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80",
  "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=100&q=80",
  "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&q=80",
  "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&q=80",
  "https://images.unsplash.com/photo-1463453091185-61582044d556?w=100&q=80",
];

const feed = reactive([
  {
    id: 1,
    name: "Thomas Vidal",
    handle: "@thom.eats",
    avatar:
      "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&q=80",
    time: "2h",
    action: "a publié un avis sur",
    target: "Septime",
    rating: 5,
    isReview: true,
    likes: 47,
    comments: 12,
    text: "Le menu unique est un pari risqué et Bertrand Grébaut le gagne à chaque service. La sériole, fumée minute devant nous, a ouvert le repas en beauté.",
    image:
      "https://images.unsplash.com/photo-1552566626-52f8b828add9?w=1000&q=80",
  },
  {
    id: 2,
    name: "Mia Rossi",
    handle: "@mia.roma",
    avatar:
      "https://images.unsplash.com/photo-1488426862026-3ee34a7d66df?w=100&q=80",
    time: "4h",
    action: "a créé la collection",
    target: "Restaurants pour un premier date",
    likes: 203,
    comments: 38,
    isReview: false,
    text: "J'ai mis à jour ma collection préférée avec 3 nouvelles adresses testées ce mois-ci. Lumière tamisée + acoustique = tout le reste suit.",
    image:
      "https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?w=1000&q=80",
  },
  {
    id: 3,
    name: "Yann Kanté",
    handle: "@yann.plates",
    avatar:
      "https://images.unsplash.com/photo-1463453091185-61582044d556?w=100&q=80",
    time: "6h",
    action: "a rejoint la table ouverte",
    target: "BBQ coréen & soju",
    likes: 14,
    comments: 3,
    isReview: false,
    text: "RDV samedi à 21h30 chez Omma. On est 17 maintenant, ça va être épique. (Ma première table ouverte, je stresse un peu.)",
  },
  {
    id: 4,
    name: "Clara Nguyen",
    handle: "@clara.ate",
    avatar:
      "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&q=80",
    time: "1j",
    action: "a testé",
    target: "Datil",
    rating: 5,
    isReview: true,
    likes: 89,
    comments: 21,
    text: "Dîner suspendu. Manon Fleury fait du végétal une évidence : tout a l'air simple et rien ne l'est. J'y retourne la semaine prochaine avec ma sœur.",
    image:
      "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?w=1000&q=80",
  },
]);

function toggleLike(p) {
  p._liked = !p._liked;
  p.likes += p._liked ? 1 : -1;
}

const trending = [
  { tag: "#bistronomie", posts: "2 417" },
  { tag: "#tableouverte", posts: "1 892" },
  { tag: "#vinnature", posts: "1 523" },
  { tag: "#paris11", posts: "1 104" },
  { tag: "#bibgourmand", posts: "987" },
];

const suggestedMembers = reactive([
  {
    name: "Bertrand G.",
    handle: "@chef.septime",
    tagline: "Chef · Septime, Paris",
    avatar:
      "https://images.unsplash.com/photo-1577219491135-ce391730fb2c?w=200&q=80",
  },
  {
    name: "Camille L.",
    handle: "@cam.dines",
    tagline: "Critique gastronomique",
    avatar:
      "https://images.unsplash.com/photo-1554151228-14d9def656e4?w=200&q=80",
  },
  {
    name: "Alex R.",
    handle: "@alex.fermente",
    tagline: "Vin nature & fermentation",
    avatar:
      "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=200&q=80",
  },
]);
</script>
