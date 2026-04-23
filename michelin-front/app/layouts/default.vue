<template>
  <div class="min-h-screen pb-20">
    <!-- Main content -->
    <slot />

    <!-- Bottom Navigation -->
    <nav class="fixed bottom-0 w-full bg-white border-t border-gray-200 px-4 py-2 flex justify-around items-center z-50">
      <NuxtLink to="/" class="flex flex-col items-center gap-1 p-2 text-gray-500 hover:text-gray-900 transition-colors" :class="{ 'text-[#c41e3a]': $route.path === '/' }">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M15 21v-8a1 1 0 0 0-1-1h-4a1 1 0 0 0-1 1v8" />
          <path d="M3 10a2 2 0 0 1 .709-1.528l7-6a2 2 0 0 1 2.582 0l7 6A2 2 0 0 1 21 10v9a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z" />
        </svg>
        <span class="text-xs font-medium">Accueil</span>
      </NuxtLink>

      <NuxtLink to="/explore" class="flex flex-col items-center gap-1 p-2 text-gray-500 hover:text-gray-900 transition-colors" :class="{ 'text-[#c41e3a]': $route.path === '/explore' }">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="12" cy="12" r="10" />
          <path d="m16.24 7.76-1.804 5.411a2 2 0 0 1-1.265 1.265L7.76 16.24l1.804-5.411a2 2 0 0 1 1.265-1.265z" />
        </svg>
        <span class="text-xs font-medium">Explorer</span>
      </NuxtLink>

      <NuxtLink to="/assistant" class="flex flex-col items-center gap-1 p-2 text-gray-500 hover:text-gray-900 transition-colors" :class="{ 'text-[#c41e3a]': $route.path === '/assistant' }">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2.992 16.342a2 2 0 0 1 .094 1.167l-1.065 3.29a1 1 0 0 0 1.236 1.168l3.413-.998a2 2 0 0 1 1.099.092 10 10 0 1 0-4.777-4.719" />
        </svg>
        <span class="text-xs font-medium">Assistant</span>
      </NuxtLink>

      <NuxtLink to="/creators" class="flex flex-col items-center gap-1 p-2 text-gray-500 hover:text-gray-900 transition-colors" :class="{ 'text-[#c41e3a]': $route.path === '/creators' }">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="m21 21-4.34-4.34" />
          <circle cx="11" cy="11" r="8" />
        </svg>
        <span class="text-xs font-medium">Créateurs</span>
      </NuxtLink>

      <NuxtLink to="/profile" class="flex flex-col items-center gap-1 p-2 text-gray-500 hover:text-gray-900 transition-colors" :class="{ 'text-[#c41e3a]': $route.path === '/profile' }">
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2" />
          <circle cx="12" cy="7" r="4" />
        </svg>
        <span class="text-xs font-medium">Profil</span>
      </NuxtLink>
    </nav>
  </div>
</template>

<script setup lang="ts">
// Default layout with bottom navigation
</script>
