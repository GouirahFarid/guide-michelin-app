<template>
  <button
    class="px-4 py-1.5 rounded-full text-sm font-medium transition-colors border"
    :class="
      selected
        ? 'bg-[#c41e3a] border-[#c41e3a] text-white'
        : 'bg-white border-gray-200 text-gray-400'
    "
  >
    {{ label }}
  </button>
</template>

<script setup>
defineProps({
  label: String,
  selected: Boolean,
});
</script>
