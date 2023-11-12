export default defineNuxtConfig({
  // ... other options
  target: "static",
  modules: [
    // ...
    "@pinia/nuxt",
  ],
  nitro: {
    prerender: {
      ignore: ["/"],
    },
  },
});
