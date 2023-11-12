export default defineNuxtConfig({
  // ... other options
  target: "static",
  // mode: "spa",
  // ssr: false,

  modules: [
    // ...
    "@pinia/nuxt",
  ],
  nitro: {
    prerender: {
      ignore: ["/"],
    },
  },
  // generate: {
  //   staticAssets: {
  //     version: "1",
  //   },
  // },
  // server: {
  //   host: "0.0.0.0", // default: localhost
  // },
  // outputDir must be added to Django's TEMPLATE_DIRS
  // outputDir: "./dist/",
  // // assetsDir must match Django's STATIC_URL
  // assetsDir: "static",
  // head: {
  //   title: "Django Nuxt SSR - To Do With Vue",
  //   meta: [
  //     { charset: "utf-8" },
  //     { name: "viewport", content: "width=device-width, initial-scale=1" },
  //     { hid: "description", name: "description", content: "Django & Nuxt SSR" },
  //   ],
  //   link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  // },
  axios: {
    baseURL: "https://cmput-average-21-b54788720538.herokuapp.com/api/",
  },
  // build: {
    // analyze: {
    //   analyzerMode: 'server',
    //   openAnalyzer: true
    // },
    // publicPath: "https://cdn.nuxtjs.org",
    // extractCSS: true,
    // postcss: {
    //   parser: "postcss-scss",
    //   // Add plugin names as key and arguments as value
    //   plugins: {
    //     tailwindcss: path.resolve(__dirname, "./tailwind.config.js"),
    //     "postcss-nested": {},
    //   },
    // },
  // },

  /*
   ** You can extend webpack config here
   */
  // extend(config, ctx) {
  //   config.resolve.alias["@fortawesome/fontawesome-free-brands$"] =
  //     "@fortawesome/fontawesome-free-brands/shakable.es.js";
  //   // Remove unused CSS using purgecss. See https://github.com/FullHuman/purgecss
  //   // for more information about purgecss.
  //   config.plugins.push(
  //     new PurgecssPlugin({
  //       // Specify the locations of any files you want to scan for class names.
  //       paths: glob.sync([
  //         path.join(__dirname, "./pages/**/*.vue"),
  //         path.join(__dirname, "./layouts/**/*.vue"),
  //         path.join(__dirname, "./components/**/*.vue"),
  //       ]),
  //       extractors: [
  //         {
  //           extractor: TailwindExtractor,
  //           // Specify the file extensions to include when scanning for
  //           // class names.
  //           extensions: ["html", "vue"],
  //         },
  //       ],
  //       whitelist: ["html", "body", "ul", "ol", "pre", "code", "blockquote"],
  //       whitelistPatterns: [/\bhljs\S*/, /fa/], // also ignore font-awesome (find a better way)
  //     })
  //   );
  // },
});
