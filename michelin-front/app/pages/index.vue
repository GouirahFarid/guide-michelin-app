<template>
  <div class="min-h-screen flex flex-col items-center justify-center px-4 py-12 md:py-0 bg-gradient-to-br from-gray-50 to-white">
    <div class="w-full max-w-2xl text-center">
      <!-- Logo/Icon -->
      <div class="w-16 h-16 md:w-20 md:h-20 bg-black rounded-2xl flex items-center justify-center mx-auto mb-6 md:mb-8 shadow-lg">
        <span class="text-white text-2xl md:text-3xl font-bold">M</span>
      </div>

      <!-- Title -->
      <h1 class="text-3xl md:text-5xl font-extrabold text-gray-900 mb-4 md:mb-6 tracking-tight">
        Michelin Guide
        <span class="block bg-gradient-to-r from-yellow-500 via-orange-500 to-red-600 bg-clip-text text-transparent">AI Assistant</span>
      </h1>

      <!-- Subtitle -->
      <p class="text-base md:text-lg text-gray-600 mb-8 md:mb-10 max-w-lg mx-auto leading-relaxed">
        Discover the world's best restaurants with AI-powered recommendations from the Michelin Guide.
      </p>

      <!-- CTA Buttons -->
      <div class="flex flex-col sm:flex-row gap-3 justify-center mb-12 md:mb-16">
        <UButton
          size="xl"
          icon="i-heroicons-chat-bubble-left-right"
          class="w-full sm:w-auto justify-center"
          color="black"
        >
          Start Chatting
        </UButton>
        <UButton
          size="xl"
          variant="outline"
          icon="i-heroicons-map"
          class="w-full sm:w-auto justify-center"
        >
          Explore Map
        </UButton>
      </div>

      <!-- Features Grid -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4 md:gap-6 text-left">
        <div class="p-4 md:p-5 bg-white rounded-xl border border-gray-200 hover:border-gray-300 transition-colors">
          <div class="w-10 h-10 bg-yellow-100 rounded-lg flex items-center justify-center mb-3">
            <UIcon name="i-heroicons-sparkles" class="text-xl text-yellow-600" />
          </div>
          <h3 class="font-semibold text-gray-900 mb-1">AI-Powered</h3>
          <p class="text-sm text-gray-600">Smart recommendations based on your preferences</p>
        </div>

        <div class="p-4 md:p-5 bg-white rounded-xl border border-gray-200 hover:border-gray-300 transition-colors">
          <div class="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mb-3">
            <UIcon name="i-heroicons-globe-americas" class="text-xl text-blue-600" />
          </div>
          <h3 class="font-semibold text-gray-900 mb-1">Global Coverage</h3>
          <p class="text-sm text-gray-600">Michelin-rated restaurants worldwide</p>
        </div>

        <div class="p-4 md:p-5 bg-white rounded-xl border border-gray-200 hover:border-gray-300 transition-colors">
          <div class="w-10 h-10 bg-red-100 rounded-lg flex items-center justify-center mb-3">
            <UIcon name="i-heroicons-star" class="text-xl text-red-600" />
          </div>
          <h3 class="font-semibold text-gray-900 mb-1">Expert Ratings</h3>
          <p class="text-sm text-gray-600">Bib Gourmand to 3 Stars dining</p>
        </div>
      </div>
    </div>
  </div>
</template>
