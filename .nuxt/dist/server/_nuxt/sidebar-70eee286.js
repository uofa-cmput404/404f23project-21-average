import { _ as __nuxt_component_0 } from "./nuxt-link-01469011.js";
import { mergeProps, withCtx, createVNode, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrRenderComponent } from "vue/server-renderer";
import { _ as _export_sfc } from "../server.mjs";
import "ufo";
import "hookable";
import "ofetch";
import "#internal/nitro";
import "unctx";
import "destr";
import "devalue";
import "defu";
import "klona";
import "unhead";
import "@unhead/shared";
import "vue-router";
import "h3";
import "@vue/devtools-api";
const bootstrapIcons = "";
const sidebar_vue_vue_type_style_index_0_scoped_ccbb0416_lang = "";
const _sfc_main = {
  name: "SidebarComponent"
};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  const _component_NuxtLink = __nuxt_component_0;
  _push(`<aside${ssrRenderAttrs(mergeProps({ class: "sidebar" }, _attrs))} data-v-ccbb0416><h1 class="app-title" data-v-ccbb0416><div class="title-social" data-v-ccbb0416>SOCIAL</div><div class="title-distribution" data-v-ccbb0416>DISTRIBUTION</div></h1><li data-v-ccbb0416>`);
  _push(ssrRenderComponent(_component_NuxtLink, { to: "/homePage" }, {
    default: withCtx((_, _push2, _parent2, _scopeId) => {
      if (_push2) {
        _push2(`<i class="bi bi-house" id="home-icon" data-v-ccbb0416${_scopeId}></i>`);
      } else {
        return [
          createVNode("i", {
            class: "bi bi-house",
            id: "home-icon"
          })
        ];
      }
    }),
    _: 1
  }, _parent));
  _push(`</li><li data-v-ccbb0416>`);
  _push(ssrRenderComponent(_component_NuxtLink, { to: "/friendsPage" }, {
    default: withCtx((_, _push2, _parent2, _scopeId) => {
      if (_push2) {
        _push2(`<i class="bi bi-people" id="friends" data-v-ccbb0416${_scopeId}></i>`);
      } else {
        return [
          createVNode("i", {
            class: "bi bi-people",
            id: "friends"
          })
        ];
      }
    }),
    _: 1
  }, _parent));
  _push(`</li><li data-v-ccbb0416>`);
  _push(ssrRenderComponent(_component_NuxtLink, { to: "/searchPage" }, {
    default: withCtx((_, _push2, _parent2, _scopeId) => {
      if (_push2) {
        _push2(`<i class="bi bi-search" id="search-icon" data-v-ccbb0416${_scopeId}></i>`);
      } else {
        return [
          createVNode("i", {
            class: "bi bi-search",
            id: "search-icon"
          })
        ];
      }
    }),
    _: 1
  }, _parent));
  _push(`</li><li data-v-ccbb0416>`);
  _push(ssrRenderComponent(_component_NuxtLink, { to: "/profilePage" }, {
    default: withCtx((_, _push2, _parent2, _scopeId) => {
      if (_push2) {
        _push2(`<i class="bi bi-person" id="profile-icon" data-v-ccbb0416${_scopeId}></i>`);
      } else {
        return [
          createVNode("i", {
            class: "bi bi-person",
            id: "profile-icon"
          })
        ];
      }
    }),
    _: 1
  }, _parent));
  _push(`</li></aside>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/sidebar.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const SidebarComponent = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender], ["__scopeId", "data-v-ccbb0416"]]);
export {
  SidebarComponent as default
};
//# sourceMappingURL=sidebar-70eee286.js.map
