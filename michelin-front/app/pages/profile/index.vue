<template>
  <div
    class="min-h-screen bg-[#fdfcfb] pb-24 pt-8 w-full transition-all duration-300"
  >
    <div class="px-6 w-full">
      <header
        class="flex justify-between items-start"
        :style="{ marginBottom: '2rem' }"
      >
        <div class="flex items-center" :style="{ gap: '1rem' }">
          <div
            class="flex items-center justify-center rounded-full bg-[#f8e7e7] text-[#c41e3a] font-serif font-bold"
            :style="{ width: '4rem', height: '4rem', fontSize: '1.5rem' }"
          >
            I
          </div>

          <div class="flex flex-col">
            <h1
              class="font-serif font-bold text-gray-900"
              :style="{ fontSize: '1.25rem' }"
            >
              Ibrahim Fatime
            </h1>
            <p class="text-gray-400" :style="{ fontSize: '0.875rem' }">
              fatimeibrahim530@gmail.com
            </p>
            <div class="mt-1">
              <span
                class="inline-block bg-[#eef2ff] text-[#4f46e5] font-bold rounded-full"
                :style="{ padding: '0.2rem 0.75rem', fontSize: '0.625rem' }"
              >
                Palais Confirmé
              </span>
            </div>
          </div>
        </div>

        <button class="text-gray-400 hover:text-gray-600 transition-colors">
          <svg
            width="24"
            height="24"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="12" cy="12" r="3" />
            <path
              d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"
            />
          </svg>
        </button>
      </header>

      <section
        class="flex flex-wrap"
        :style="{ gap: '0.75rem', marginBottom: '2.5rem' }"
      >
        <StatCard value="24" label="Restaurants testés">
          <template #icon>
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#b33b3b"
              stroke-width="2"
            >
              <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
              <circle cx="12" cy="10" r="3" />
            </svg>
          </template>
        </StatCard>

        <StatCard value="12" label="Avis publiés">
          <template #icon>
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#b33b3b"
              stroke-width="2"
            >
              <polygon
                points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
              />
            </svg>
          </template>
        </StatCard>

        <StatCard value="3" label="Listes créées">
          <template #icon>
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#b33b3b"
              stroke-width="2"
            >
              <line x1="8" y1="6" x2="21" y2="6" />
              <line x1="8" y1="12" x2="21" y2="12" />
              <line x1="8" y1="18" x2="21" y2="18" />
              <line x1="3" y1="6" x2="3.01" y2="6" />
              <line x1="3" y1="12" x2="3.01" y2="12" />
              <line x1="3" y1="18" x2="3.01" y2="18" />
            </svg>
          </template>
        </StatCard>

        <StatCard value="47" label="Adresses sauvées">
          <template #icon>
            <svg
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="#b33b3b"
              stroke-width="2"
            >
              <path
                d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"
              />
            </svg>
          </template>
        </StatCard>
      </section>

      <section :style="{ marginBottom: '2.5rem' }">
        <h2
          class="font-serif font-bold text-gray-900"
          :style="{ fontSize: '1.25rem', marginBottom: '1rem' }"
        >
          Badges
        </h2>
        <div
          class="flex overflow-x-auto pb-2 scrollbar-hide"
          :style="{ gap: '0.75rem' }"
        >
          <BadgeCard
            icon="👨‍🍳"
            title="Palais Curieux"
            subtitle="Premier avis publié"
            active
          />
          <BadgeCard
            icon="👨‍🍳"
            title="Palais Confirmé"
            subtitle="10 avis publiés"
            active
          />
          <BadgeCard
            icon="🥈"
            title="Palais d'Argent"
            subtitle="50 avis utiles"
          />
          <BadgeCard icon="🥇" title="Palais d'Or" subtitle="100 avis utiles" />
        </div>
      </section>

      <section :style="{ marginBottom: '2.5rem' }">
        <div
          class="flex justify-between items-center"
          :style="{ marginBottom: '1rem' }"
        >
          <h2
            class="font-serif font-bold text-gray-900"
            :style="{ fontSize: '1.25rem' }"
          >
            Mes goûts
          </h2>
          <button
            class="text-[#c41e3a] font-bold"
            :style="{ fontSize: '0.875rem' }"
          >
            Modifier
          </button>
        </div>
        <div class="flex flex-wrap" :style="{ gap: '0.5rem' }">
          <TasteTag label="Japonaise" selected />
          <TasteTag label="Italienne" selected />
          <TasteTag label="Française" />
          <TasteTag label="Bistronomique" selected />
          <TasteTag label="Végétarienne" />
        </div>
      </section>

      <section
        class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden"
      >
        <MenuItem label="Mes adresses sauvegardées" />
        <MenuItem label="Mes listes" />
        <MenuItem label="Mon historique" />
        <MenuItem label="Notifications" />
      </section>

      <button
        class="w-full flex justify-center items-center text-[#c41e3a] font-bold transition-opacity hover:opacity-80"
        :style="{ marginTop: '3rem', gap: '0.5rem' }"
      >
        <svg
          class="rotate-180"
          width="18"
          height="18"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2.5"
        >
          <path
            d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4M10 17l5-5-5-5M13.8 12H3"
          />
        </svg>
        <span :style="{ fontSize: '1rem' }">Se déconnecter</span>
      </button>
    </div>
  </div>
</template>

<script setup></script>
