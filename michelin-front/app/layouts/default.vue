<template>
  <div class="min-h-screen bg-michelin-cream text-michelin-ink flex flex-col">
    <SiteHeader />
    <main class="flex-1">
      <slot />
    </main>
    <SiteFooter />
    <PodcastPlayer v-if="podcasts.nowPlaying" />
  </div>
</template>

<script setup>
import { usePodcastsStore } from "~/stores/podcasts";
const podcasts = usePodcastsStore();
</script>
