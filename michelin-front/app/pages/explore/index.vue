<template>
  <div class="min-h-screen bg-[#fdfcfb] pt-8 px-4">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-serif font-bold text-gray-900">Explorer</h1>
      <p class="text-gray-500">Découvrez des restaurants exceptionnels</p>
    </div>

    <!-- Search Bar -->
    <div class="relative mb-6">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Rechercher un restaurant, une cuisine..."
        class="w-full px-4 py-3 pl-10 bg-gray-100 rounded-lg outline-none focus:ring-1 focus:ring-[#c41e3a]"
      />
      <svg class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="11" cy="11" r="8" />
        <path d="m21 21-4.34-4.34" />
      </svg>
    </div>

    <!-- Quick Filters -->
    <div class="flex gap-2 overflow-x-auto pb-4 -mx-4 px-4 scrollbar-hide">
      <button
        v-for="filter in quickFilters"
        :key="filter.id"
        @click="selectedFilter = filter.id"
        class="px-4 py-2 rounded-full text-sm font-medium whitespace-nowrap transition-colors"
        :class="selectedFilter === filter.id ? 'bg-[#c41e3a] text-white' : 'bg-gray-100 text-gray-700'"
      >
        {{ filter.label }}
      </button>
    </div>

    <!-- Featured Categories -->
    <div class="mb-6">
      <h2 class="text-lg font-bold text-gray-900 mb-3">Catégories</h2>
      <div class="grid grid-cols-2 gap-3">
        <div
          v-for="category in categories"
          :key="category.id"
          class="bg-white rounded-xl p-4 border border-gray-100 shadow-sm"
        >
          <div class="text-2xl mb-2">{{ category.icon }}</div>
          <h3 class="font-semibold text-gray-900">{{ category.name }}</h3>
          <p class="text-xs text-gray-500">{{ category.count }} restaurants</p>
        </div>
      </div>
    </div>

    <!-- Popular Destinations -->
    <div>
      <h2 class="text-lg font-bold text-gray-900 mb-3">Destinations populaires</h2>
      <div class="flex gap-3 overflow-x-auto pb-4 -mx-4 px-4 scrollbar-hide">
        <div
          v-for="city in popularCities"
          :key="city.name"
          class="min-w-[140px] bg-white rounded-xl overflow-hidden border border-gray-100 shadow-sm"
        >
          <div class="h-20 bg-gradient-to-br from-[#c41e3a] to-[#8a1428]"></div>
          <div class="p-3">
            <h3 class="font-semibold text-gray-900 text-sm">{{ city.name }}</h3>
            <p class="text-xs text-gray-500">{{ city.count }} étoilés</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const searchQuery = ref('')
const selectedFilter = ref('all')

const quickFilters = [
  { id: 'all', label: 'Tous' },
  { id: '3stars', label: '3 Étoiles' },
  { id: 'bib', label: 'Bib Gourmand' },
  { id: 'new', label: 'Nouveaux' },
  { id: 'green', label: 'Green Star' },
]

const categories = [
  { id: 'french', name: 'Français', icon: '🇫🇷', count: 632 },
  { id: 'japanese', name: 'Japonais', icon: '🇯🇵', count: 324 },
  { id: 'italian', name: 'Italien', icon: '🇮🇹', count: 218 },
  { id: 'chinese', name: 'Chinois', icon: '🇨🇳', count: 156 },
]

const popularCities = [
  { name: 'Paris', count: 124 },
  { name: 'Tokyo', count: 187 },
  { name: 'New York', count: 73 },
  { name: 'Hong Kong', count: 64 },
  { name: 'Kyoto', count: 89 },
]
</script>

<style scoped>
.scrollbar-hide {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.scrollbar-hide::-webkit-scrollbar {
  display: none;
}
</style>
