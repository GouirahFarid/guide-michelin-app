<script setup>
import { ref, computed } from "vue";
import { usePodcastsStore } from "~/stores/podcasts";

const podcasts = usePodcastsStore();

const activeShow = ref("Tous");
const shows = [
  "Tous",
  "Tables Ouvertes",
  "Le Comptoir",
  "Inside Michelin",
  "Villes à table",
];

const filteredEpisodes = computed(() => {
  if (activeShow.value === "Tous") return podcasts.episodes;
  return podcasts.episodes.filter((e) => e.show === activeShow.value);
});

const featured = computed(() => podcasts.episodes[0]);
const otherEpisodes = computed(() =>
  filteredEpisodes.value.filter((e) => e.id !== featured.value.id),
);

function formatDuration(sec) {
  const m = Math.floor(sec / 60);
  return `${m} min`;
}

function togglePlay(ep) {
  podcasts.play(ep);
}

useHead({
  title: "Podcasts — Michelin Guide",
});
</script>

<template>
  <div class="bg-cream min-h-screen pb-32">
    <!-- HERO -->
    <section class="relative bg-ink text-cream overflow-hidden">
      <div class="absolute inset-0 grain opacity-30"></div>
      <div
        class="absolute top-0 right-0 w-1/2 h-full bg-gradient-to-l from-red/20 to-transparent"
      ></div>

      <div class="relative max-w-7xl mx-auto px-6 lg:px-12 py-20 lg:py-28">
        <div class="grid lg:grid-cols-12 gap-12 items-center">
          <div class="lg:col-span-7">
            <div class="flex items-center gap-3 mb-6">
              <span class="w-12 h-px bg-red"></span>
              <!-- <span
                class="text-xs tracking-[0.25em] uppercase text-red font-mono"
                >Studio Michelin</span
              > -->
            </div>
            <h1
              class="font-display text-5xl md:text-7xl lg:text-8xl leading-[0.9] mb-8"
            >
              Écoutez<br />
              la cuisine se
              <em class="text-red not-italic italic">raconter</em>.
            </h1>
            <p
              class="text-lg md:text-xl text-cream/70 max-w-xl mb-8 leading-relaxed"
            >
              Des chefs, des hôtes, des critiques, des insiders. Quatre
              émissions pour comprendre comment la gastronomie se vit
              aujourd'hui.
            </p>
            <!-- <div class="flex flex-wrap gap-4 text-sm font-mono text-cream/60">
              <span>4 émissions</span>
              <span class="text-red">—</span>
              <span>{{ podcasts.episodes.length }} épisodes</span>
              <span class="text-red">—</span>
              <span>Nouveau chaque semaine</span>
            </div> -->
          </div>

          <div class="lg:col-span-5 relative">
            <div
              class="relative aspect-square rounded-2xl overflow-hidden shadow-2xl"
              :style="{ background: featured.color }"
            >
              <div class="absolute inset-0 flex flex-col justify-between p-8">
                <div class="flex items-center justify-between">
                  <span
                    class="text-xs tracking-[0.25em] uppercase text-cream/80 font-mono"
                    >Épisode à la une</span
                  >
                  <div
                    class="w-3 h-3 bg-cream rounded-full animate-pulse-soft"
                  ></div>
                </div>
                <div>
                  <div
                    class="text-xs tracking-widest uppercase text-cream/70 font-mono mb-3"
                  >
                    {{ featured.show }}
                  </div>
                  <h2
                    class="font-display text-3xl md:text-4xl text-cream leading-tight mb-4"
                  >
                    {{ featured.title }}
                  </h2>
                  <p class="text-cream/80 text-sm mb-6 line-clamp-2">
                    {{ featured.description }}
                  </p>
                  <button
                    @click="togglePlay(featured)"
                    class="group flex items-center gap-4 bg-cream text-ink px-6 py-3 rounded-full hover:bg-red hover:text-cream transition-all"
                  >
                    <span
                      class="w-10 h-10 rounded-full bg-ink text-cream group-hover:bg-cream group-hover:text-red flex items-center justify-center transition-all"
                    >
                      <svg
                        v-if="
                          podcasts.nowPlaying?.id === featured.id &&
                          podcasts.isPlaying
                        "
                        class="w-4 h-4"
                        fill="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <rect x="6" y="5" width="4" height="14" />
                        <rect x="14" y="5" width="4" height="14" />
                      </svg>
                      <svg
                        v-else
                        class="w-4 h-4 ml-0.5"
                        fill="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path d="M8 5v14l11-7z" />
                      </svg>
                    </span>
                    <span class="font-semibold tracking-tight">
                      {{
                        podcasts.nowPlaying?.id === featured.id &&
                        podcasts.isPlaying
                          ? "En écoute"
                          : "Lancer l'épisode"
                      }}
                    </span>
                    <span
                      class="text-xs text-ink/60 font-mono group-hover:text-cream/80"
                      >{{ featured.duration }}</span
                    >
                  </button>
                </div>
              </div>
            </div>

            <!-- Floating tag -->
            <!-- <div
              class="absolute -bottom-4 -left-4 bg-red text-cream px-5 py-3 rounded-full shadow-xl flex items-center gap-2"
            >
              <span class="w-2 h-2 bg-cream rounded-full animate-pulse"></span>
              <span class="text-xs tracking-widest uppercase font-mono"
                >Écouté 12K fois</span
              >
            </div> -->
          </div>
        </div>
      </div>
    </section>

    <!-- SHOWS FILTER -->
    <section
      class="sticky top-[88px] z-30 bg-cream/95 backdrop-blur-md border-b border-stone/40"
    >
      <div class="max-w-7xl mx-auto px-6 lg:px-12 py-4 overflow-x-auto">
        <div class="flex gap-3 whitespace-nowrap">
          <button
            v-for="show in shows"
            :key="show"
            @click="activeShow = show"
            :class="[
              'px-5 py-2 rounded-full text-sm font-medium transition-all border',
              activeShow === show
                ? 'bg-ink text-cream border-ink'
                : 'bg-transparent text-ink border-stone hover:border-ink',
            ]"
          >
            {{ show }}
          </button>
        </div>
      </div>
    </section>

    <!-- EPISODES GRID -->
    <section class="max-w-7xl mx-auto px-6 lg:px-12 py-16">
      <div class="flex items-end justify-between mb-10">
        <div>
          <div class="flex items-center gap-3 mb-2">
            <span class="w-8 h-px bg-red"></span>
            <!-- <span class="text-xs tracking-[0.25em] uppercase text-red font-mono"
              >Épisodes</span
            > -->
          </div>
          <h2 class="font-display text-4xl md:text-5xl">
            {{ activeShow === "Tous" ? "Tous les épisodes" : activeShow }}
          </h2>
        </div>
        <div class="text-sm font-mono text-ink-soft hidden md:block">
          {{ filteredEpisodes.length }} épisode{{
            filteredEpisodes.length > 1 ? "s" : ""
          }}
        </div>
      </div>

      <div
        v-if="filteredEpisodes.length === 0"
        class="text-center py-20 text-ink-soft"
      >
        <p class="font-display text-2xl mb-2">
          Aucun épisode pour cette émission.
        </p>
        <button @click="activeShow = 'Tous'" class="text-red underline">
          Voir tous les épisodes
        </button>
      </div>

      <div v-else class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <article
          v-for="ep in filteredEpisodes"
          :key="ep.id"
          class="group bg-white rounded-2xl overflow-hidden border border-stone/50 hover:border-ink transition-all hover:-translate-y-1 hover:shadow-xl"
        >
          <div
            class="relative aspect-[4/3] overflow-hidden"
            :style="{ background: ep.color }"
          >
            <div class="absolute inset-0 flex items-center justify-center">
              <div
                class="font-display text-6xl md:text-7xl text-cream/20 leading-none"
              >
                {{ ep.show.slice(0, 1) }}
              </div>
            </div>
            <!-- <div
              class="absolute top-4 left-4 bg-black/30 backdrop-blur-sm text-cream text-[10px] tracking-[0.2em] uppercase font-mono px-3 py-1 rounded-full"
            >
              {{ ep.show }}
            </div> -->
            <button
              @click="togglePlay(ep)"
              class="absolute bottom-4 right-4 w-14 h-14 rounded-full bg-cream text-ink flex items-center justify-center shadow-lg hover:bg-red hover:text-cream transition-all group-hover:scale-110"
              :aria-label="
                podcasts.nowPlaying?.id === ep.id && podcasts.isPlaying
                  ? 'Pause'
                  : 'Lire'
              "
            >
              <svg
                v-if="podcasts.nowPlaying?.id === ep.id && podcasts.isPlaying"
                class="w-5 h-5"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <rect x="6" y="5" width="4" height="14" />
                <rect x="14" y="5" width="4" height="14" />
              </svg>
              <svg
                v-else
                class="w-5 h-5 ml-1"
                fill="currentColor"
                viewBox="0 0 24 24"
              >
                <path d="M8 5v14l11-7z" />
              </svg>
            </button>
            <div
              v-if="podcasts.nowPlaying?.id === ep.id && podcasts.isPlaying"
              class="absolute top-4 right-4 bg-red text-cream text-[10px] tracking-[0.2em] uppercase font-mono px-3 py-1 rounded-full flex items-center gap-1.5"
            >
              <span
                class="w-1.5 h-1.5 bg-cream rounded-full animate-pulse"
              ></span>
              En écoute
            </div>
          </div>

          <div class="p-6">
            <div
              class="flex items-center justify-between text-xs font-mono text-ink-soft mb-3"
            >
              <span>Animé par {{ ep.host }}</span>
              <span>{{ ep.duration }}</span>
            </div>
            <h3
              class="font-display text-2xl mb-3 leading-tight group-hover:text-red transition-colors"
            >
              {{ ep.title }}
            </h3>
            <p class="text-sm text-ink-soft leading-relaxed mb-4 line-clamp-3">
              {{ ep.description }}
            </p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in ep.tags"
                :key="tag"
                class="text-[10px] tracking-[0.15em] uppercase font-mono text-ink-soft bg-sand px-2 py-1 rounded"
              >
                {{ tag }}
              </span>
            </div>
          </div>
        </article>
      </div>
    </section>

    <!-- ABOUT / SUBSCRIBE -->
    <section class="max-w-7xl mx-auto px-6 lg:px-12 pb-20">
      <div class="bg-ink text-cream rounded-3xl overflow-hidden relative">
        <div class="absolute inset-0 grain opacity-20"></div>
        <div
          class="absolute top-0 right-0 w-96 h-96 bg-red/20 rounded-full blur-3xl"
        ></div>

        <div class="relative grid md:grid-cols-2 gap-12 p-10 md:p-16">
          <div>
            <span class="text-xs tracking-[0.25em] uppercase text-red font-mono"
              >Abonnez-vous</span
            >
            <h2 class="font-display text-4xl md:text-5xl mt-4 leading-tight">
              Ne ratez plus un
              <em class="text-red not-italic italic">épisode</em>.
            </h2>
            <p class="text-cream/70 mt-6 leading-relaxed">
              Retrouvez tous nos podcasts sur vos plateformes préférées, ou
              activez les notifications pour être prévenu dès la sortie d'un
              nouvel épisode.
            </p>
          </div>
          <div class="flex flex-col justify-center gap-3">
            <a
              href="#"
              class="flex items-center justify-between bg-cream/10 hover:bg-cream/20 backdrop-blur-sm px-6 py-4 rounded-xl transition-all group"
            >
              <span class="font-medium">Spotify</span>
              <svg
                class="w-5 h-5 text-cream/60 group-hover:translate-x-1 transition-transform"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M17 8l4 4m0 0l-4 4m4-4H3"
                />
              </svg>
            </a>
            <a
              href="#"
              class="flex items-center justify-between bg-cream/10 hover:bg-cream/20 backdrop-blur-sm px-6 py-4 rounded-xl transition-all group"
            >
              <span class="font-medium">Apple Podcasts</span>
              <svg
                class="w-5 h-5 text-cream/60 group-hover:translate-x-1 transition-transform"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M17 8l4 4m0 0l-4 4m4-4H3"
                />
              </svg>
            </a>
            <a
              href="#"
              class="flex items-center justify-between bg-cream/10 hover:bg-cream/20 backdrop-blur-sm px-6 py-4 rounded-xl transition-all group"
            >
              <span class="font-medium">Deezer</span>
              <svg
                class="w-5 h-5 text-cream/60 group-hover:translate-x-1 transition-transform"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M17 8l4 4m0 0l-4 4m4-4H3"
                />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>
