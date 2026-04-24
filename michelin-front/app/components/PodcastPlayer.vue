<template>
  <div class="fixed bottom-0 left-0 right-0 z-50 bg-michelin-ink text-michelin-cream border-t-2 border-michelin-red animate-slide-in">
    <div class="h-1 bg-michelin-ink-soft">
      <div class="h-full bg-michelin-red transition-all" :style="{ width: progressPct + '%' }"></div>
    </div>
    <div class="max-w-[1400px] mx-auto px-4 py-3 flex items-center gap-4">
      <img :src="podcasts.nowPlaying.cover" class="w-12 h-12 object-cover" />
      <div class="flex-1 min-w-0">
        <div class="font-medium truncate">{{ podcasts.nowPlaying.title }}</div>
        <div class="text-xs text-michelin-cream/60 truncate">
          {{ podcasts.nowPlaying.show }} · {{ formatTime(currentSec) }} / {{ podcasts.nowPlaying.duration }}
        </div>
      </div>
      <button @click="skip(-15)" class="hidden sm:block p-2 hover:text-michelin-red transition-colors" aria-label="Reculer">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path d="M12.5 8V4L7 9l5.5 5V10a6 6 0 1 1-6 6"/>
        </svg>
      </button>
      <button
        @click="podcasts.isPlaying = !podcasts.isPlaying"
        class="w-11 h-11 bg-michelin-red hover:bg-michelin-cream hover:text-michelin-ink flex items-center justify-center transition-colors"
        :aria-label="podcasts.isPlaying ? 'Pause' : 'Play'"
      >
        <svg v-if="podcasts.isPlaying" class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24">
          <rect x="6" y="5" width="4" height="14"/><rect x="14" y="5" width="4" height="14"/>
        </svg>
        <svg v-else class="w-5 h-5 ml-0.5" fill="currentColor" viewBox="0 0 24 24">
          <path d="M8 5v14l11-7z"/>
        </svg>
      </button>
      <button @click="skip(15)" class="hidden sm:block p-2 hover:text-michelin-red transition-colors" aria-label="Avancer">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24">
          <path d="M11.5 8V4L17 9l-5.5 5V10a6 6 0 1 0 6 6"/>
        </svg>
      </button>
      <button @click="podcasts.stop()" class="p-2 hover:text-michelin-red transition-colors" aria-label="Fermer">
        <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
          <path d="M18 6 6 18M6 6l12 12"/>
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { usePodcastsStore } from '~/stores/podcasts'

const podcasts = usePodcastsStore()
const currentSec = ref(0)
let interval = null

const progressPct = computed(() => {
  if (!podcasts.nowPlaying) return 0
  return (currentSec.value / podcasts.nowPlaying.durationSec) * 100
})

function formatTime(s) {
  const m = Math.floor(s / 60)
  const sec = Math.floor(s % 60)
  return `${m}:${sec.toString().padStart(2, '0')}`
}
function skip(n) {
  currentSec.value = Math.max(0, Math.min((podcasts.nowPlaying?.durationSec || 0), currentSec.value + n))
}

function tick() {
  if (podcasts.isPlaying && podcasts.nowPlaying) {
    currentSec.value += 1
    if (currentSec.value >= podcasts.nowPlaying.durationSec) {
      podcasts.isPlaying = false
    }
  }
}

watch(() => podcasts.nowPlaying?.id, () => { currentSec.value = 0 })

onMounted(() => { interval = setInterval(tick, 1000) })
onBeforeUnmount(() => clearInterval(interval))
</script>
