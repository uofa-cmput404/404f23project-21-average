import axios from "axios";
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
const createPostComponent_vue_vue_type_style_index_0_scoped_ece6e3d7_lang = "";
const _sfc_main = {
  data() {
    return {
      postContent: "",
      postImage: null,
      isPublic: true
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
    async submitPost() {
      try {
        const payload = {
          type: this.isPublic ? "public" : "private",
          // Adjust as per your requirement
          title: "",
          // You can add a title input field in your template
          source: "",
          // Adjust as per your requirement
          origin: "",
          // Adjust as per your requirement
          description: "",
          // You can add a description input field in your template
          contentType: "",
          // Adjust based on your content type
          content: this.postContent,
          published: (/* @__PURE__ */ new Date()).toISOString(),
          owner: "UserID",
          // Adjust with your actual owner id
          categories: "",
          // Adjust as per your requirement
          count: 0
          // Adjust as per your requirement
        };
        const response = await axios.post("http://localhost:8000/api/posts", payload);
        if (response.status === 200 || response.status === 201) {
          console.log("Post created successfully:", response.data);
        } else {
          console.error("Error creating post:", response);
        }
      } catch (error) {
        console.error("Error while creating post:", error);
      }
    }
  }
};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(mergeProps({ class: "create-post" }, _attrs))} data-v-ece6e3d7><textarea placeholder="What&#39;s on your mind?" data-v-ece6e3d7>${ssrInterpolate($data.postContent)}</textarea><div class="post-actions" data-v-ece6e3d7><label class="upload-image" data-v-ece6e3d7> Upload Image <input type="file" data-v-ece6e3d7></label><div class="toggle-container" data-v-ece6e3d7><label class="switch" data-v-ece6e3d7><input type="checkbox"${ssrIncludeBooleanAttr(Array.isArray($data.isPublic) ? ssrLooseContain($data.isPublic, null) : $data.isPublic) ? " checked" : ""} data-v-ece6e3d7><span class="slider" data-v-ece6e3d7></span></label><span data-v-ece6e3d7>${ssrInterpolate($data.isPublic ? "Public" : "Private")}</span></div></div><button data-v-ece6e3d7>Post</button></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/createPostComponent.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const createPostComponent = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender], ["__scopeId", "data-v-ece6e3d7"]]);
export {
  createPostComponent as default
};
//# sourceMappingURL=createPostComponent-6d6a6641.js.map
