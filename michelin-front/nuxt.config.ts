// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  ssr: false,

  // Explicitly enable pages directory (required for app/pages routing)
  pages: true,

  modules: [
    '@nuxt/eslint',
    '@nuxt/image',
    '@nuxt/hints',
    '@nuxt/ui',
    '@nuxtjs/i18n',
    '@pinia/nuxt',
    'nuxt-mapbox'
  ],

  css: ['~/assets/css/main.css'],

  // Vite proxy for development (works with Nuxt 4)
  vite: {
    server: {
      proxy: {
        '/api': {
          target: 'http://localhost:8000',
          changeOrigin: true,
          rewrite: (path) => path.replace(/^\/api/, ''),
          configure: (proxy, _options) => {
            proxy.on('error', (err, _req, _res) => {
              console.log('proxy error', err);
            });
            proxy.on('proxyReq', (proxyReq, req, _res) => {
              console.log('Sending request to the target:', req.method, req.url);
            });
            proxy.on('proxyRes', (proxyReq, req, _res) => {
              console.log('Received response from the target:', proxyReq.statusCode, req.url);
            });
          }
        }
      }
    }
  },

  mapbox: {
    accessToken: 'pk.eyJ1IjoiZ291aXJhaCIsImEiOiJjbW84bHpkc3kwMnRtMnJzOThoN3N6b3BwIn0.0ICDsmDOtlIypgSFTyWYOw'
  }
})