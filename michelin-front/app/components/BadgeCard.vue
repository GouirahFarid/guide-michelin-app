<template>
  <div
    class="flex flex-col items-center p-4 rounded-xl border min-w-[110px]"
    :class="
      active
        ? 'bg-white border-gray-100 shadow-sm'
        : 'bg-gray-50/50 border-transparent opacity-50'
    "
  >
    <div class="text-3xl mb-2">{{ icon }}</div>
    <h4 class="text-xs font-bold text-gray-900 text-center leading-tight">
      {{ title }}
    </h4>
    <p class="text-[10px] text-gray-500 text-center mt-1">{{ subtitle }}</p>
  </div>
</template>

<script setup>
defineProps({
  icon: String,
  title: String,
  subtitle: String,
  active: Boolean,
});
</script>
