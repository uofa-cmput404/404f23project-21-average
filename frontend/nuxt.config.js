export default defineNuxtConfig({
  // ... other options
  modules: [
    // ...
    "@pinia/nuxt",
  ],
  nitro: {
    prerender: {
      ignore: ["/"],
    },
  },
  ssr: false,
});
