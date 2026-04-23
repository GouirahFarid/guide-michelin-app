<template>
  <div class="min-h-screen flex flex-col bg-gradient-to-br from-gray-50 to-white">
    <!-- Header -->
    <header class="flex items-center justify-between px-6 py-4 border-b border-gray-200 bg-white">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-gradient-to-br from-red-600 to-red-700 rounded-lg flex items-center justify-center shadow-md">
          <span class="text-white text-lg font-bold">M</span>
        </div>
        <div>
          <span class="font-bold text-gray-900 text-lg">Michelin Guide</span>
          <p class="text-xs text-gray-500">AI Restaurant Assistant</p>
        </div>
      </div>
      <NuxtLink to="/chat">
        <UButton
          icon="i-heroicons-chat-bubble-left-right"
          size="md"
          color="red"
          class="shadow-md"
        >
          Start Chat
        </UButton>
      </NuxtLink>
    </header>

    <!-- Hero Section -->
    <main class="flex-1 flex flex-col items-center justify-center px-4 py-12">
      <div class="w-full max-w-3xl text-center">
        <!-- Logo/Icon -->
        <div class="w-20 h-20 bg-gradient-to-br from-red-600 to-red-700 rounded-2xl flex items-center justify-center mx-auto mb-6 shadow-lg">
          <UIcon name="i-heroicons-sparkles" class="w-10 h-10 text-white" />
        </div>

        <!-- Title -->
        <h1 class="text-4xl md:text-6xl font-extrabold text-gray-900 mb-4 tracking-tight">
          Michelin Guide
          <span class="block bg-gradient-to-r from-red-600 via-orange-500 to-yellow-500 bg-clip-text text-transparent">
            AI Assistant
          </span>
        </h1>

        <!-- Subtitle -->
        <p class="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl mx-auto leading-relaxed">
          Discover the world's best restaurants with AI-powered recommendations from the Michelin Guide.
          From Bib Gourmand to 3 Stars, find your perfect dining experience.
        </p>

        <!-- CTA Buttons -->
        <div class="flex flex-col sm:flex-row gap-4 justify-center mb-16">
          <NuxtLink to="/chat">
            <UButton
              size="xl"
              icon="i-heroicons-chat-bubble-left-right"
              class="w-full sm:w-auto justify-center shadow-lg"
              color="red"
            >
              Start Chatting
            </UButton>
          </NuxtLink>
        </div>

        <!-- Michelin Award Guide -->
        <div class="mb-12">
          <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4">Michelin Award Levels</h2>
          <div class="flex flex-wrap justify-center gap-3">
            <div class="flex items-center gap-2 px-4 py-2 bg-white rounded-full border border-gray-200 shadow-sm">
              <span class="flex gap-0.5">
                <span class="w-2 h-2 bg-red-600 rounded-full"></span>
                <span class="w-2 h-2 bg-red-600 rounded-full"></span>
                <span class="w-2 h-2 bg-red-600 rounded-full"></span>
              </span>
              <span class="text-sm font-medium text-gray-700">3 Stars - Exceptional</span>
            </div>
            <div class="flex items-center gap-2 px-4 py-2 bg-white rounded-full border border-gray-200 shadow-sm">
              <span class="flex gap-0.5">
                <span class="w-2 h-2 bg-orange-500 rounded-full"></span>
                <span class="w-2 h-2 bg-orange-500 rounded-full"></span>
              </span>
              <span class="text-sm font-medium text-gray-700">2 Stars - Excellent</span>
            </div>
            <div class="flex items-center gap-2 px-4 py-2 bg-white rounded-full border border-gray-200 shadow-sm">
              <span class="w-2 h-2 bg-amber-500 rounded-full"></span>
              <span class="text-sm font-medium text-gray-700">1 Star - Very Good</span>
            </div>
            <div class="flex items-center gap-2 px-4 py-2 bg-white rounded-full border border-gray-200 shadow-sm">
              <UIcon name="i-heroicons-face-smile" class="w-4 h-4 text-yellow-600" />
              <span class="text-sm font-medium text-gray-700">Bib Gourmand</span>
            </div>
          </div>
        </div>

        <!-- Features Grid -->
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
          <div class="p-6 bg-white rounded-2xl border border-gray-200 hover:border-red-200 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-red-100 rounded-xl flex items-center justify-center mb-4">
              <UIcon name="i-heroicons-sparkles" class="text-2xl text-red-600" />
            </div>
            <h3 class="font-bold text-gray-900 mb-2">AI-Powered Search</h3>
            <p class="text-sm text-gray-600 leading-relaxed">Natural language queries to find the perfect restaurant for any occasion</p>
          </div>

          <div class="p-6 bg-white rounded-2xl border border-gray-200 hover:border-blue-200 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center mb-4">
              <UIcon name="i-heroicons-globe-americas" class="text-2xl text-blue-600" />
            </div>
            <h3 class="font-bold text-gray-900 mb-2">Global Coverage</h3>
            <p class="text-sm text-gray-600 leading-relaxed">Michelin-rated restaurants across 40+ countries worldwide</p>
          </div>

          <div class="p-6 bg-white rounded-2xl border border-gray-200 hover:border-orange-200 hover:shadow-lg transition-all">
            <div class="w-12 h-12 bg-orange-100 rounded-xl flex items-center justify-center mb-4">
              <UIcon name="i-heroicons-star" class="text-2xl text-orange-600" />
            </div>
            <h3 class="font-bold text-gray-900 mb-2">Expert Ratings</h3>
            <p class="text-sm text-gray-600 leading-relaxed">Trusted Michelin inspectors' anonymous reviews and recommendations</p>
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="px-6 py-4 border-t border-gray-200 bg-white">
      <div class="max-w-3xl mx-auto text-center text-sm text-gray-500">
        <p>Powered by Michelin Guide data • AI-generated content may not always be accurate</p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
// SEO Meta
useHead({
  title: 'Michelin Guide AI Assistant',
  meta: [
    { name: 'description', content: 'Discover the world\'s best restaurants with AI-powered recommendations from the Michelin Guide.' }
  ]
})
</script>
