
import { updateAppConfig } from '#app'
<<<<<<< HEAD
import { defuFn } from 'C:/Users/shrey/cmput-404/Project/404f23project-21-average/node_modules/defu/dist/defu.mjs'
=======
import { defuFn } from '/Users/aryamanraina/404f23project-21-average-1/node_modules/defu/dist/defu.mjs'
>>>>>>> 35bd763bc9d458a934ee96527104d8411fdd7bfd

const inlineConfig = {
  "nuxt": {
    "buildId": "test"
  }
}

// Vite - webpack is handled directly in #app/config
if (import.meta.hot) {
  import.meta.hot.accept((newModule) => {
    updateAppConfig(newModule.default)
  })
}



export default /* #__PURE__ */ defuFn(inlineConfig)
