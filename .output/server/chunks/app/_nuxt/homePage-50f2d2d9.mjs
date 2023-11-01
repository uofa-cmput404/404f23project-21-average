import { u as useAuthorStore } from './authorStore-171782f1.mjs';
import PostComponent from './postComponent-485f3c06.mjs';
import SidebarComponent from './sidebar-70eee286.mjs';
import axios from 'axios';
import { resolveComponent, mergeProps, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderList, ssrRenderComponent, ssrInterpolate, ssrIncludeBooleanAttr, ssrLooseContain } from 'vue/server-renderer';
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
    PostComponent,
    SidebarComponent
  },
  data() {
    return {
      posts: [],
      postContent: "",
      postImage: null,
      isPublic: true,
      showPostPopup: false
      // Variable to control the visibility of the create post popup
    };
  },
  async mounted() {
    const authorStore = useAuthorStore();
    const response = await axios.get(process.env.API_URL + authorStore.getAuthorId + "/posts/");
    this.posts = response.data.results;
  },
  methods: {
    // Methods for CreatePostComponent
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
      const authorStore = useAuthorStore();
      try {
        const payload = {
          type: this.isPublic ? "PUBLIC" : "FRIENDS",
          // Adjust as per your requirement
          title: "string",
          // You can add a title input field in your template
          source: "string",
          // Adjust as per your requirement
          origin: "string",
          // Adjust as per your requirement
          description: "string",
          // You can add a description input field in your template
          contentType: "string",
          // Adjust based on your content type
          content: this.postContent,
          published: (/* @__PURE__ */ new Date()).toISOString(),
          categories: "string",
          // Adjust as per your requirement
          image: this.postImage
        };
        axios.defaults.headers.common["Authorization"] = `Bearer ${authorStore.getAuthToken}`;
        const response = await axios.post(process.env.API_URL + authorStore.getAuthorId + "/posts/", payload);
        console.log(response.data);
      } catch (error) {
        console.error("Error while creating post:", error);
      }
      this.showPostPopup = false;
    }
  },
  async created() {
    const authorStore = useAuthorStore();
    try {
      console.log(authorStore.authorId, authorStore.authToken);
      const response = await axios.get(process.env.API_URL + authorStore.getAuthorId + "/posts/");
    } catch (error) {
      console.error("Error while fetching posts:", error);
    }
  }
};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  const _component_PostComponent = resolveComponent("PostComponent");
  const _component_SidebarComponent = resolveComponent("SidebarComponent");
  _push(`<div${ssrRenderAttrs(mergeProps({ class: "homepage-container" }, _attrs))}><div class="homepage-main-content"><div class="add-post-button-container"><button>Add New Post</button></div><div class="posts-feed"><h2>Posts</h2><!--[-->`);
  ssrRenderList($data.posts, (post) => {
    _push(ssrRenderComponent(_component_PostComponent, {
      key: post.id,
      postContent: post.content,
      postID: post.id
    }, null, _parent));
  });
  _push(`<!--]--></div>`);
  _push(ssrRenderComponent(_component_SidebarComponent, null, null, _parent));
  _push(`</div>`);
  if ($data.showPostPopup) {
    _push(`<div class="post-popup"><div class="create-post"><button type="button" class="close btn-close" aria-label="Close"><span aria-hidden="true">\xD7</span></button><textarea placeholder="What&#39;s on your mind?">${ssrInterpolate($data.postContent)}</textarea><div class="post-actions"><label class="upload-image"> Upload Image <input type="file"></label><div class="toggle-container"><label class="switch"><input type="checkbox"${ssrIncludeBooleanAttr(Array.isArray($data.isPublic) ? ssrLooseContain($data.isPublic, null) : $data.isPublic) ? " checked" : ""}><span class="slider"></span></label><span>${ssrInterpolate($data.isPublic ? "Public" : "Private")}</span></div></div><button>Post</button></div></div>`);
  } else {
    _push(`<!---->`);
  }
  _push(`</div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/homePage.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const homePage = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender]]);

export { homePage as default };
//# sourceMappingURL=homePage-50f2d2d9.mjs.map
