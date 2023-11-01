import { useSSRContext, defineComponent, ref, resolveComponent, mergeProps, withCtx, createTextVNode, createVNode } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderAttr } from 'vue/server-renderer';
import { u as useAuthorStore } from './authorStore-171782f1.mjs';
import { _ as _export_sfc } from '../server.mjs';
import 'axios';
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

const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "loginPage",
  __ssrInlineRender: true,
  setup(__props) {
    const userId = ref("");
    const password = ref("");
    useAuthorStore();
    return (_ctx, _push, _parent, _attrs) => {
      const _component_h1soc = resolveComponent("h1soc");
      const _component_h1dis = resolveComponent("h1dis");
      _push(`<div${ssrRenderAttrs(mergeProps({ id: "app" }, _attrs))} data-v-e125ccca><div class="container" data-v-e125ccca><div class="heading" data-v-e125ccca>`);
      _push(ssrRenderComponent(_component_h1soc, null, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`SOCIAL<br data-v-e125ccca${_scopeId}>`);
          } else {
            return [
              createTextVNode("SOCIAL"),
              createVNode("br")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(ssrRenderComponent(_component_h1dis, null, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`DISTRIBUTION`);
          } else {
            return [
              createTextVNode("DISTRIBUTION")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(`</div><div class="login-box" data-v-e125ccca><h2 data-v-e125ccca>LOGIN</h2><form data-v-e125ccca><div class="input-group" data-v-e125ccca><label for="user-id" data-v-e125ccca>User ID</label><input type="text" id="user-id"${ssrRenderAttr("value", userId.value)} placeholder="User ID" data-v-e125ccca></div><div class="input-group" data-v-e125ccca><label for="password" data-v-e125ccca>Password</label><input type="password" id="password"${ssrRenderAttr("value", password.value)} placeholder="Password" data-v-e125ccca></div><button type="button" data-v-e125ccca>SUBMIT</button></form></div></div></div>`);
    };
  }
});
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/loginPage.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const loginPage = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-e125ccca"]]);

export { loginPage as default };
//# sourceMappingURL=loginPage-b81eb45f.mjs.map
