<template>
  <button
    class="w-full flex items-center justify-between border-b border-gray-50 last:border-0 transition-colors hover:bg-gray-50 active:bg-gray-100"
    :style="{ padding: '1rem' }"
  >
    <div class="flex items-center" :style="{ gap: '0.75rem' }">
      <div
        class="flex items-center justify-center bg-gray-100 rounded"
        :style="{ width: '1.25rem', height: '1.25rem' }"
      >
        <slot name="icon">
          <span class="text-gray-400" :style="{ fontSize: '0.625rem' }">#</span>
        </slot>
      </div>

      <span class="font-medium text-gray-700" :style="{ fontSize: '0.875rem' }">
        {{ label }}
      </span>
    </div>

    <span class="text-gray-300 font-light" :style="{ fontSize: '1.125rem' }">
      <svg
        xmlns="http://www.w3.org/2000/svg"
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <path d="m9 18 6-6-6-6" />
      </svg>
    </span>
  </button>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
});
</script>
