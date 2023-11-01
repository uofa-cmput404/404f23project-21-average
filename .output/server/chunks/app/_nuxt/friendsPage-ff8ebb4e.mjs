import SidebarComponent from './sidebar-70eee286.mjs';
import { resolveComponent, mergeProps, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderList, ssrInterpolate } from 'vue/server-renderer';
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
  },
  data() {
    return {
      friends: [
        { id: 1, name: "User_1" },
        { id: 2, name: "User_2" },
        { id: 3, name: "User_3" },
        { id: 4, name: "User_4" },
        { id: 5, name: "User_5" }
      ]
    };
  },
  methods: {
    gotoProfile(id) {
      console.log("Navigating to profile of User ID: ${id}");
    }
  }
};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  const _component_SidebarComponent = resolveComponent("SidebarComponent");
  _push(`<div${ssrRenderAttrs(mergeProps({ class: "app-container" }, _attrs))} data-v-9fb2879d>`);
  _push(ssrRenderComponent(_component_SidebarComponent, null, null, _parent));
  _push(`<div class="main-content" data-v-9fb2879d><div class="header" data-v-9fb2879d>FRIENDS</div><div class="friend-list" data-v-9fb2879d><!--[-->`);
  ssrRenderList($data.friends, (friend) => {
    _push(`<button data-v-9fb2879d>${ssrInterpolate(friend.name)}</button>`);
  });
  _push(`<!--]--></div></div></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/friendsPage.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const friendsPage = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender], ["__scopeId", "data-v-9fb2879d"]]);

export { friendsPage as default };
//# sourceMappingURL=friendsPage-ff8ebb4e.mjs.map
