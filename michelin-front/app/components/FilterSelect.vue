<template>
  <div class="relative">
    <label class="absolute -top-2 left-3 px-1.5 bg-michelin-cream text-[10px] uppercase tracking-[0.2em] text-michelin-stone z-10">{{ label }}</label>
    <select
      :value="value"
      @change="$emit('input', $event.target.value)"
      class="w-full appearance-none bg-michelin-cream border border-michelin-ink/30 hover:border-michelin-red focus:border-michelin-red px-4 py-3 pr-10 text-sm font-medium cursor-pointer outline-none transition-colors"
    >
      <option v-for="o in options" :key="o" :value="o">{{ o }}</option>
    </select>
    <svg class="absolute right-3 top-1/2 -translate-y-1/2 w-4 h-4 pointer-events-none text-michelin-stone" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
      <path d="m6 9 6 6 6-6"/>
    </svg>
  </div>
</template>

<script setup>
defineProps({
  label: String,
  options: Array,
  value: [String, Number]
})
defineEmits(['input'])
</script>
