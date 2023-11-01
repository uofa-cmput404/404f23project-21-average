
import { updateAppConfig } from '#app'
import { defuFn } from '/Users/afaqnabi/Desktop/CMPUT404/project/404f23project-21-average/node_modules/defu/dist/defu.mjs'

const inlineConfig = {
  "nuxt": {
    "buildId": "9585399c-8d6e-4953-8454-3f54d8250445"
  }
}

// Vite - webpack is handled directly in #app/config
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    updateAppConfig(newModule.default)
  })
}



export default /* #__PURE__ */ defuFn(inlineConfig)
