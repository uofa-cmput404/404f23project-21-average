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
  __name: "signupPage",
  __ssrInlineRender: true,
  setup(__props) {
    useAuthorStore();
    const email = ref("");
    const username = ref("");
    const password = ref("");
    return (_ctx, _push, _parent, _attrs) => {
      const _component_h1soc = resolveComponent("h1soc");
      const _component_h1dis = resolveComponent("h1dis");
      _push(`<div${ssrRenderAttrs(mergeProps({ id: "app" }, _attrs))} data-v-2a5b96da><div class="container" data-v-2a5b96da><div class="heading" data-v-2a5b96da>`);
      _push(ssrRenderComponent(_component_h1soc, null, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`SOCIAL<br data-v-2a5b96da${_scopeId}>`);
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
      _push(`</div><div class="registration-box" data-v-2a5b96da><h2 data-v-2a5b96da>REGISTER</h2><form data-v-2a5b96da><div class="input-group" data-v-2a5b96da><label for="email" data-v-2a5b96da>Email</label><input type="email" id="email"${ssrRenderAttr("value", email.value)} placeholder="Email" data-v-2a5b96da></div><div class="input-group" data-v-2a5b96da><label for="username" data-v-2a5b96da>Username</label><input type="text" id="username"${ssrRenderAttr("value", username.value)} placeholder="Username" data-v-2a5b96da></div><div class="input-group" data-v-2a5b96da><label for="password" data-v-2a5b96da>Password</label><input type="password" id="password"${ssrRenderAttr("value", password.value)} placeholder="Password" data-v-2a5b96da></div><button type="button" data-v-2a5b96da>SIGN UP</button></form></div></div></div>`);
    };
  }
});
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/signupPage.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const signupPage = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-2a5b96da"]]);

export { signupPage as default };
//# sourceMappingURL=signupPage-7a183ef5.mjs.map
