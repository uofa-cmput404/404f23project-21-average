
import { updateAppConfig } from '#app'
import { defuFn } from '/Users/afaqnabi/Desktop/CMPUT404/project/404f23project-21-average/node_modules/defu/dist/defu.mjs'

const inlineConfig = {
  "nuxt": {
    "buildId": "b87a4539-417b-418d-bd3a-80adba7b05e4"
  }
}

// Vite - webpack is handled directly in #app/config
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    updateAppConfig(newModule.default)
  })
}



export default /* #__PURE__ */ defuFn(inlineConfig)
