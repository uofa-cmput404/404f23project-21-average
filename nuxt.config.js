export default defineNuxtConfig({
  // target: "static",
  // preset: "node-server",
  mode: "spa",
  ssr: false,

  modules: [
    // ...
    "@pinia/nuxt",
    // "@nuxtjs/axios",
  ],
  nitro: {
    prerender: {
      ignore: ["/"],
    },
  },
  runtimeConfig: {
    public: {
      baseUrl: process.env.BASE_URL,
    },
  },
});
