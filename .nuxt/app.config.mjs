
import { updateAppConfig } from '#app'
import { defuFn } from '/Users/afaqnabi/Desktop/CMPUT404/project/404f23project-21-average/node_modules/defu/dist/defu.mjs'

const inlineConfig = {
  "nuxt": {
    "buildId": "42b3373b-e750-401b-bb80-0f3cb200e490"
  }
}

// Vite - webpack is handled directly in #app/config
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    updateAppConfig(newModule.default)
  })
}



export default /* #__PURE__ */ defuFn(inlineConfig)
