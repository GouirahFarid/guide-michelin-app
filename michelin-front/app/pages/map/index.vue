<script setup lang="ts">

</script>

<template>
  <MapboxMap
      map-id="hello-aaa"
      style="position: absolute; top: 0; bottom: 0; width: 100%"
      :options="{
        style: 'mapbox://styles/mapbox/dark-v11', // style URL
        center: [2.2137, 46.2276], // starting position
        zoom: 5 // starting zoom
      }"
  />

</template>

<style scoped>

</style>