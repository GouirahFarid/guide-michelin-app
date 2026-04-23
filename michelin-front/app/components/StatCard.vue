<template>
  <div
    class="flex flex-col items-center justify-center bg-white border border-gray-100 rounded-xl shadow-sm"
    :style="{ padding: '1.25rem', flex: '1 1 0px', minWidth: '8rem' }"
  >
    <div :style="{ marginBottom: '0.5rem' }">
      <slot name="icon"></slot>
    </div>
    <span class="font-bold text-gray-900" :style="{ fontSize: '1.125rem' }">
      {{ value }}
    </span>
    <span
      class="text-gray-400 text-center leading-tight"
      :style="{ fontSize: '0.625rem' }"
    >
      {{ label }}
    </span>
  </div>
</template>

<script setup>
defineProps(["value", "label"]);
</script>
