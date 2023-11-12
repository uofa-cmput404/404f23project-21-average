export default defineNuxtConfig({
  // ... other options
  target: "static",
  mode: "spa",
  ssr: false,
  modules: [
    // ...
    "@pinia/nuxt",
  ],
  nitro: {
    prerender: {
      ignore: ["/"],
    },
  },
  server: {
    host: "0.0.0.0", // default: localhost
  },
});
