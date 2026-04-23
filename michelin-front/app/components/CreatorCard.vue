<template>
  <div
    class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden mb-6"
  >
    <div class="h-32 md:h-48 overflow-hidden">
      <img :src="banner" class="w-full h-full object-cover" alt="Banner" />
    </div>

    <div class="px-6 pb-6 relative">
      <div class="absolute -top-10 left-6">
        <img
          :src="avatar"
          class="w-20 h-20 rounded-full border-4 border-white object-cover"
          alt="Avatar"
        />
      </div>

      <div
        class="pt-12 flex flex-col md:flex-row md:justify-between md:items-start"
      >
        <div class="flex-1">
          <h3 class="text-xl font-bold text-gray-900 flex items-center gap-2">
            {{ name }}
            <span class="text-red-600 text-xs">●</span>
          </h3>
          <p class="text-sm text-gray-500 font-medium">
            {{ handle }} • {{ specialty }}
          </p>
          <p class="mt-2 text-gray-600 text-sm leading-relaxed max-w-2xl">
            {{ bio }}
          </p>

          <div class="mt-4 flex gap-4 text-sm font-semibold text-gray-900">
            <span
              >{{ followers }}
              <span class="font-normal text-gray-500">abonnés</span></span
            >
            <span
              >{{ lists }}
              <span class="font-normal text-gray-500">listes</span></span
            >
          </div>
        </div>

        <button
          class="mt-6 md:mt-0 bg-[#c41e3a] hover:bg-red-800 text-white px-6 py-2 rounded-full flex items-center gap-2 transition-colors duration-200 text-sm font-bold"
        >
          <span class="text-lg">+</span> Suivre
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps([
  "name",
  "handle",
  "specialty",
  "bio",
  "followers",
  "lists",
  "avatar",
  "banner",
]);
</script>
