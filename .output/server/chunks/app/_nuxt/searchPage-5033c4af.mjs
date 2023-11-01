import SidebarComponent from './sidebar-70eee286.mjs';
import { resolveComponent, mergeProps, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent } from 'vue/server-renderer';
import { _ as _export_sfc } from '../server.mjs';
import './nuxt-link-01469011.mjs';
import '../../nitro/node-server.mjs';
import 'node:http';
import 'node:https';
import 'fs';
import 'path';
import 'node:fs';
import 'node:url';
import 'unhead';
import '@unhead/shared';
import 'vue-router';

const _sfc_main = {
  name: "SocialDistributionApp",
  components: {
    SidebarComponent
  }
};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  const _component_SidebarComponent = resolveComponent("SidebarComponent");
  _push(`<div${ssrRenderAttrs(mergeProps({ class: "app-container" }, _attrs))} data-v-8067870b>`);
  _push(ssrRenderComponent(_component_SidebarComponent, null, null, _parent));
  _push(`<main class="main-content" data-v-8067870b><div class="search-bar" data-v-8067870b><input type="text" placeholder="Search for friends" data-v-8067870b></div></main></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/searchPage.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const searchPage = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender], ["__scopeId", "data-v-8067870b"]]);

export { searchPage as default };
//# sourceMappingURL=searchPage-5033c4af.mjs.map
