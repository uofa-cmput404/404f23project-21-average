import { mergeProps, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrInterpolate, ssrIncludeBooleanAttr, ssrLooseContain } from "vue/server-renderer";
import { _ as _export_sfc } from "../server.mjs";
import "ofetch";
import "#internal/nitro";
import "hookable";
import "unctx";
import "destr";
import "devalue";
import "defu";
import "klona";
import "unhead";
import "@unhead/shared";
import "vue-router";
import "h3";
import "ufo";
import "@vue/devtools-api";
const editPostComponent_vue_vue_type_style_index_0_scoped_e0d0a91a_lang = "";
const _sfc_main = {
  name: EditPostComponent,
  props: ["initialPostContent", "initialIsPublic"],
  data() {
    return {
      editedPostContent: this.initialPostContent,
      postImage: null,
      isPublic: this.initialIsPublic
    };
  },
  methods: {
    onImageSelected(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.readAsDataURL(file);
        reader.onload = (e) => {
          this.postImage = e.target.result;
        };
      }
    },
    updatePost() {
      console.log({
        content: this.editedPostContent,
        image: this.postImage,
        privacy: this.isPublic ? "public" : "private"
      });
    }
  }
};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(mergeProps({ class: "edit-post" }, _attrs))} data-v-e0d0a91a><textarea placeholder="Edit your post" data-v-e0d0a91a>${ssrInterpolate($data.editedPostContent)}</textarea><div class="post-actions" data-v-e0d0a91a><label class="upload-image" data-v-e0d0a91a> Change Image <input type="file" data-v-e0d0a91a></label><div class="toggle-container" data-v-e0d0a91a><label class="switch" data-v-e0d0a91a><input type="checkbox"${ssrIncludeBooleanAttr(Array.isArray($data.isPublic) ? ssrLooseContain($data.isPublic, null) : $data.isPublic) ? " checked" : ""} data-v-e0d0a91a><span class="slider" data-v-e0d0a91a></span></label><span data-v-e0d0a91a>${ssrInterpolate($data.isPublic ? "Public" : "Private")}</span></div></div><button data-v-e0d0a91a>Update Post</button></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/editPostComponent.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const editPostComponent = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender], ["__scopeId", "data-v-e0d0a91a"]]);
export {
  editPostComponent as default
};
//# sourceMappingURL=editPostComponent-c7192623.js.map
