// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  modules: [
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/hints',
    '@nuxt/ui',
    '@nuxtjs/i18n',
    '@pinia/nuxt',
    'nuxt-mapbox'
  ],
  mapbox: {
    accessToken: 'pk.eyJ1IjoiZ291aXJhaCIsImEiOiJjbW84bHpkc3kwMnRtMnJzOThoN3N6b3BwIn0.0ICDsmDOtlIypgSFTyWYOw'
  }
})