<template>
  <div>
    <!-- Profile header -->
    <section
      class="relative bg-gradient-to-br from-michelin-red to-michelin-red-dark text-michelin-cream overflow-hidden"
    >
      <div
        class="absolute top-0 right-0 font-display text-[400px] font-black leading-none opacity-[0.06] select-none translate-x-20 -translate-y-10"
      >
        ★
      </div>
      <div class="max-w-[1400px] mx-auto px-6 py-16 relative">
        <div class="flex flex-col md:flex-row gap-10 md:items-end">
          <div class="relative">
            <img
              :src="user.profile.avatar"
              class="w-36 h-36 md:w-48 md:h-48 object-cover border-4 border-michelin-cream"
            />
            <!-- <div
              class="absolute -bottom-3 -right-3 bg-michelin-cream text-michelin-red px-3 py-1 text-xs font-bold tracking-widest uppercase"
            >
              {{ user.profile.level.split("·")[0].trim() }}
            </div> -->
          </div>
          <div class="flex-1">
            <div
              class="text-xs tracking-[0.3em] uppercase font-semibold opacity-80 mb-2"
            >
              Profil · Membre depuis {{ user.profile.memberSince }}
            </div>
            <h1
              class="font-display text-5xl md:text-7xl font-black leading-none"
            >
              {{ user.profile.name }}
            </h1>
            <div class="text-lg mt-2 opacity-90">{{ user.profile.handle }}</div>
            <p
              class="mt-4 max-w-xl font-display text-lg leading-relaxed opacity-90"
            >
              {{ user.profile.bio }}
            </p>
            <div class="mt-6 flex flex-wrap items-center gap-5 text-sm">
              <div class="flex items-center gap-2">
                <span class="font-display text-2xl font-bold">{{
                  user.followers
                }}</span>
                <span class="opacity-80">abonnés</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="font-display text-2xl font-bold">{{
                  user.following
                }}</span>
                <span class="opacity-80">abonnements</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="font-display text-2xl font-bold">{{
                  user.profile.testedRestaurants.length
                }}</span>
                <span class="opacity-80">testés</span>
              </div>
            </div>
          </div>
          <div class="flex flex-col gap-2">
            <button
              @click="editOpen = true"
              class="bg-michelin-cream text-michelin-ink px-6 py-3 text-sm uppercase tracking-wider font-medium hover:bg-michelin-ink hover:text-michelin-cream transition-colors"
            >
              Modifier le profil
            </button>
            <button
              class="border border-michelin-cream/50 px-6 py-3 text-sm uppercase tracking-wider hover:bg-michelin-cream hover:text-michelin-ink transition-colors"
            >
              Partager
            </button>
          </div>
        </div>

        <!-- XP bar -->
      </div>
    </section>

    <!-- Tabs -->
    <section
      class="border-b border-michelin-ink/10 bg-michelin-cream sticky top-[112px] z-40"
    >
      <div class="max-w-[1400px] mx-auto px-6 flex gap-1 overflow-x-auto">
        <button
          v-for="t in tabs"
          :key="t.key"
          @click="tab = t.key"
          :class="[
            'px-5 py-4 text-sm uppercase tracking-wider font-medium transition-colors relative whitespace-nowrap',
            tab === t.key
              ? 'text-michelin-red'
              : 'text-michelin-stone hover:text-michelin-ink',
          ]"
        >
          {{ t.label }}
          <span
            v-if="tab === t.key"
            class="absolute bottom-0 left-0 right-0 h-[2px] bg-michelin-red"
          ></span>
        </button>
      </div>
    </section>

    <div class="max-w-[1400px] mx-auto px-6 py-14">
      <!-- GOÛTS -->
      <div v-if="tab === 'taste'" class="grid md:grid-cols-2 gap-10">
        <div>
          <h2 class="font-display text-3xl font-bold mb-6">
            Cuisines favorites
          </h2>
          <div class="flex flex-wrap gap-2 mb-4">
            <span
              v-for="c in user.profile.favoriteCuisines"
              :key="c"
              class="group flex items-center gap-2 bg-michelin-ink text-michelin-cream pl-4 pr-2 py-2 text-sm"
            >
              {{ c }}
              <button
                @click="user.removeCuisine(c)"
                class="w-5 h-5 rounded-full bg-michelin-cream/10 hover:bg-michelin-red flex items-center justify-center transition-colors"
              >
                <svg
                  class="w-3 h-3"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                  viewBox="0 0 24 24"
                >
                  <path d="M18 6 6 18M6 6l12 12" />
                </svg>
              </button>
            </span>
            <div class="relative">
              <input
                v-model="newCuisine"
                @keydown.enter="addCuisine"
                type="text"
                placeholder="+ Ajouter…"
                class="border border-dashed border-michelin-ink/30 px-4 py-2 text-sm w-32 focus:border-michelin-red outline-none"
              />
            </div>
          </div>

          <h2 class="font-display text-3xl font-bold mb-6 mt-10">
            Budget habituel
          </h2>
          <div class="flex gap-2">
            <button
              v-for="b in ['€', '€€', '€€€', '€€€€']"
              :key="b"
              @click="
                user.updateField(
                  'budget',
                  b +
                    (b === '€'
                      ? ' · —30€'
                      : b === '€€'
                        ? ' · 40–80€'
                        : b === '€€€'
                          ? ' · 80–150€'
                          : ' · 150€+'),
                )
              "
              :class="[
                'px-5 py-3 border-2 font-display text-xl font-bold transition-colors',
                user.profile.budget.startsWith(b)
                  ? 'bg-michelin-red text-michelin-cream border-michelin-red'
                  : 'border-michelin-ink/20 hover:border-michelin-red',
              ]"
            >
              {{ b }}
            </button>
          </div>
          <div class="mt-2 text-sm text-michelin-stone">
            Actuel:
            <span class="font-medium text-michelin-ink">{{
              user.profile.budget
            }}</span>
          </div>

          <h2 class="font-display text-3xl font-bold mb-6 mt-10">
            Occasions préférées
          </h2>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="o in [
                'Date',
                'Entre amis',
                'Solo',
                'Famille',
                'Déjeuner rapide',
                'Occasion spéciale',
              ]"
              :key="o"
              @click="toggleOccasion(o)"
              :class="[
                'px-4 py-2 border text-sm transition-colors',
                user.profile.occasions.includes(o)
                  ? 'bg-michelin-ink text-michelin-cream border-michelin-ink'
                  : 'border-michelin-ink/20 hover:border-michelin-red',
              ]"
            >
              {{ o }}
            </button>
          </div>
        </div>

        <!-- <div>
          <h2 class="font-display text-3xl font-bold mb-6">Villes visitées</h2>
          <div
            class="relative p-6 bg-michelin-sand border border-michelin-ink/10"
          >
            <div class="font-display text-6xl font-black mb-2">
              {{ user.profile.visitedCities.length }}
            </div>
            <div
              class="text-sm uppercase tracking-wider text-michelin-stone mb-5"
            >
              villes gourmandes
            </div>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="c in user.profile.visitedCities"
                :key="c"
                class="px-3 py-1.5 bg-michelin-cream border border-michelin-ink/10 text-sm"
                >📍 {{ c }}</span
              >
            </div>
          </div>

          <h2 class="font-display text-3xl font-bold mb-6 mt-10">
            Badges débloqués
          </h2>
          <div class="grid grid-cols-3 gap-3">
            <div
              v-for="b in user.badges"
              :key="b.id"
              :class="[
                'aspect-square p-4 text-center flex flex-col items-center justify-center border-2 transition-all',
                b.unlocked
                  ? 'border-michelin-red bg-michelin-red/5'
                  : 'border-dashed border-michelin-ink/20 opacity-40',
              ]"
            >
              <div class="text-3xl mb-2" :class="{ grayscale: !b.unlocked }">
                {{ b.emoji }}
              </div>
              <div class="font-display text-sm font-bold leading-tight">
                {{ b.label }}
              </div>
              <div class="text-[10px] text-michelin-stone mt-1 leading-tight">
                {{ b.desc }}
              </div>
            </div>
          </div>
        </div> -->
      </div>

      <!-- TESTÉS -->
      <div v-if="tab === 'tested'">
        <h2 class="font-display text-3xl font-bold mb-6">
          Restaurants testés ({{ user.profile.testedRestaurants.length }})
        </h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <RestaurantCard
            v-for="rid in user.profile.testedRestaurants"
            :key="rid"
            :r="restaurants.byId(rid)"
          />
        </div>
        <div
          v-if="user.profile.testedRestaurants.length === 0"
          class="text-center py-16 text-michelin-stone"
        >
          Aucun restaurant testé pour l'instant.
          <NuxtLink to="/restaurants" class="text-michelin-red underline"
            >Explorer</NuxtLink
          >
        </div>
      </div>

      <!-- WISHLIST -->
      <div v-if="tab === 'wishlist'">
        <h2 class="font-display text-3xl font-bold mb-6">
          Sauvegardés ({{ user.profile.wishlist.length }})
        </h2>
        <div class="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          <RestaurantCard
            v-for="rid in user.profile.wishlist"
            :key="rid"
            :r="restaurants.byId(rid)"
          />
        </div>
      </div>

      <!-- COLLECTIONS -->
      <div v-if="tab === 'collections'">
        <div class="flex items-center justify-between mb-6">
          <h2 class="font-display text-3xl font-bold">
            Mes collections ({{ collections.myCollections.length }})
          </h2>
          <NuxtLink to="/collections" class="btn-primary">Voir toutes</NuxtLink>
        </div>
        <div class="grid md:grid-cols-3 gap-6">
          <div
            v-for="c in collections.myCollections"
            :key="c.id"
            class="group relative aspect-[5/4] overflow-hidden bg-michelin-ink"
          >
            <img
              :src="c.cover"
              class="w-full h-full object-cover opacity-60 group-hover:scale-105 transition-transform duration-500"
            />
            <div
              class="absolute inset-0 p-6 flex flex-col justify-between text-michelin-cream"
            >
              <div class="text-4xl">{{ c.emoji }}</div>
              <div>
                <h3 class="font-display text-2xl font-bold leading-tight">
                  {{ c.title }}
                </h3>
                <div class="text-xs uppercase tracking-widest opacity-80 mt-2">
                  {{ c.restaurants.length }} adresses · {{ c.likes }} ♥
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- ACTIVITY -->
      <div v-if="tab === 'activity'">
        <h2 class="font-display text-3xl font-bold mb-8">Activité récente</h2>
        <div class="relative border-l-2 border-michelin-red/20 pl-8 space-y-8">
          <div v-for="(act, i) in activity" :key="i" class="relative">
            <div
              class="absolute -left-[41px] top-1 w-5 h-5 bg-michelin-red rounded-full border-4 border-michelin-cream"
            ></div>
            <div
              class="text-xs uppercase tracking-widest text-michelin-stone mb-1"
            >
              {{ act.date }}
            </div>
            <div class="font-display text-lg">{{ act.text }}</div>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit profile modal -->
    <Transition
      enter-active-class="transition duration-300"
      enter-from-class="opacity-0"
      enter-to-class="opacity-100"
      leave-active-class="transition duration-200"
      leave-to-class="opacity-0"
    >
      <div
        v-if="editOpen"
        @click.self="editOpen = false"
        class="fixed inset-0 z-[100] bg-michelin-ink/70 backdrop-blur-sm flex items-center justify-center p-4 overflow-y-auto"
      >
        <div class="w-full max-w-lg bg-michelin-cream animate-fade-up my-8">
          <div class="p-8">
            <div
              class="text-xs tracking-[0.3em] uppercase font-semibold text-michelin-red mb-2"
            >
              Modifier le profil
            </div>
            <h2 class="font-display text-4xl font-bold mb-6">À votre goût.</h2>
            <div class="space-y-4">
              <div>
                <label
                  class="text-xs uppercase tracking-widest text-michelin-stone block mb-2"
                  >Nom</label
                >
                <input
                  v-model="editForm.name"
                  class="w-full border-2 border-michelin-ink px-4 py-3 focus:border-michelin-red outline-none font-display text-lg"
                />
              </div>
              <div>
                <label
                  class="text-xs uppercase tracking-widest text-michelin-stone block mb-2"
                  >Handle</label
                >
                <input
                  v-model="editForm.handle"
                  class="w-full border-2 border-michelin-ink px-4 py-3 focus:border-michelin-red outline-none"
                />
              </div>
              <div>
                <label
                  class="text-xs uppercase tracking-widest text-michelin-stone block mb-2"
                  >Bio</label
                >
                <textarea
                  v-model="editForm.bio"
                  rows="3"
                  class="w-full border-2 border-michelin-ink px-4 py-3 focus:border-michelin-red outline-none"
                ></textarea>
              </div>
              <div class="flex gap-3 pt-2">
                <button @click="editOpen = false" class="btn-ghost flex-1">
                  Annuler
                </button>
                <button @click="saveProfile" class="btn-primary flex-1">
                  Enregistrer
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useUserStore } from "~/stores/user";
import { useRestaurantsStore } from "~/stores/restaurants";
import { useCollectionsStore } from "~/stores/collections";

const user = useUserStore();
const restaurants = useRestaurantsStore();
const collections = useCollectionsStore();

const tab = ref("taste");
const tabs = [
  { key: "taste", label: "Mes goûts" },
  { key: "tested", label: "Testés" },
  { key: "wishlist", label: "Sauvegardés" },
  // { key: "collections", label: "Collections" },
  // { key: "activity", label: "Activité" },
];

const newCuisine = ref("");
function addCuisine() {
  if (newCuisine.value.trim()) {
    user.addCuisine(newCuisine.value.trim());
    newCuisine.value = "";
  }
}
function toggleOccasion(o) {
  const idx = user.profile.occasions.indexOf(o);
  if (idx > -1) user.profile.occasions.splice(idx, 1);
  else user.profile.occasions.push(o);
}

const editOpen = ref(false);
const editForm = ref({ ...user.profile });
function saveProfile() {
  user.updateField("name", editForm.value.name);
  user.updateField("handle", editForm.value.handle);
  user.updateField("bio", editForm.value.bio);
  editOpen.value = false;
}

const activity = [
  { date: "Il y a 2 jours", text: "✨ Vous avez testé Septime et gagné 50 XP" },
  {
    date: "Il y a 5 jours",
    text: '📚 Vous avez créé la collection "Mes meilleurs bistrots"',
  },
  {
    date: "Il y a 1 semaine",
    text: '🍷 Vous avez rejoint la table ouverte "Dîner à l\'aveugle"',
  },
  {
    date: "Il y a 2 semaines",
    text: '⭐ Vous avez débloqué le badge "Première étoile"',
  },
  {
    date: "Il y a 3 semaines",
    text: "💌 Vous avez sauvegardé Datil dans votre wishlist",
  },
];
</script>
