<script setup lang="ts">
import { ref, onMounted } from 'vue'

const mapContainer = ref<HTMLElement>()
const isLoading = ref(true)

// Mapbox access token is configured in nuxt.config.ts
onMounted(() => {
  // Initialize map when component mounts
  isLoading.value = false
  // Note: Full Mapbox implementation would go here
  // For now, showing a placeholder
})
</script>

<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Header -->
    <div class="bg-white px-4 py-3 border-b border-gray-200">
      <h1 class="text-xl font-serif font-bold text-gray-900">Carte</h1>
      <p class="text-sm text-gray-500">Trouvez des restaurants près de chez vous</p>
    </div>

    <!-- Map Placeholder -->
    <div ref="mapContainer" class="relative h-[calc(100vh-120px)] bg-gray-200 flex items-center justify-center">
      <div v-if="isLoading" class="text-center">
        <div class="w-8 h-8 border-2 border-[#c41e3a] border-t-transparent rounded-full animate-spin mx-auto mb-2"></div>
        <p class="text-gray-500">Chargement de la carte...</p>
      </div>
      <div v-else class="text-center p-6">
        <svg class="w-16 h-16 text-gray-400 mx-auto mb-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" />
          <circle cx="12" cy="10" r="3" />
        </svg>
        <h2 class="text-lg font-semibold text-gray-900 mb-2">Carte interactive</h2>
        <p class="text-gray-500 mb-4">La carte interactive sera bientôt disponible.</p>
        <NuxtLink to="/assistant" class="inline-flex items-center gap-2 px-4 py-2 bg-[#c41e3a] text-white rounded-lg hover:bg-[#a31836] transition-colors">
          <svg class="w-4 h-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719" />
          </svg>
          Utiliser l'assistant
        </NuxtLink>
      </div>
    </div>
  </div>
</template>