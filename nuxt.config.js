export default defineNuxtConfig({
  target: "static",
  preset: "node-server",
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
  axios: {
    baseURL: process.env.BASE_URL,
    common: {
      Accept: "application/json, text/plain, */*",
      "Access-Control-Allow-Origin": "*",
    },
  },
});
