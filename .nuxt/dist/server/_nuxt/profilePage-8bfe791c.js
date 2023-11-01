import PostComponent from "./postComponent-485f3c06.js";
import SidebarComponent from "./sidebar-70eee286.js";
import axios from "axios";
import { u as useAuthorStore } from "./authorStore-171782f1.js";
import { resolveComponent, mergeProps, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderAttr, ssrRenderList } from "vue/server-renderer";
import { _ as _export_sfc } from "../server.mjs";
import "./nuxt-link-01469011.js";
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
const _imports_0 = "" + __buildAssetsURL("spiderman.53e41ff7.jpeg");
const profilePage_vue_vue_type_style_index_0_scoped_70a68eab_lang = "";
const _sfc_main = {
  name: "SocialDistributionApp",
  components: {
    PostComponent,
    SidebarComponent
  },
  data() {
    return {
      posts: []
      // Initialize posts as an empty array
    };
  },
  async created() {
    const authorStore = useAuthorStore();
    console.log(authorStore.authorId, authorStore.authToken);
    console.log(authorStore.getAuthToken);
    try {
      const response = await axios.get("http://127.0.0.1:8000/authors/" + authorStore.authorId + "/posts/");
      console.log(response);
      if (response.status === 200) {
        this.posts = response.data.results;
      } else {
        console.error("Error fetching posts:", response);
      }
    } catch (error) {
      console.error("Error while fetching posts:", error);
    }
  }
};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  const _component_SidebarComponent = resolveComponent("SidebarComponent");
  const _component_PostComponent = resolveComponent("PostComponent");
  _push(`<div${ssrRenderAttrs(mergeProps({ class: "app-container" }, _attrs))} data-v-70a68eab>`);
  _push(ssrRenderComponent(_component_SidebarComponent, null, null, _parent));
  _push(`<main class="main-content" data-v-70a68eab><div class="user-section" data-v-70a68eab><img${ssrRenderAttr("src", _imports_0)} class="profile-photo" data-v-70a68eab><h2 data-v-70a68eab>User1</h2><div class="follow-info" data-v-70a68eab><button data-v-70a68eab>Followers: </button><button data-v-70a68eab>Following: </button></div><div class="bio-section" data-v-70a68eab><textarea placeholder="Write a Bio" data-v-70a68eab></textarea></div><button class="edit" data-v-70a68eab>Edit</button><div class="posts-section" data-v-70a68eab><h3 data-v-70a68eab>MY POSTS:</h3><!--[-->`);
  ssrRenderList($data.posts, (post) => {
    _push(ssrRenderComponent(_component_PostComponent, {
      key: post.id,
      postContent: post.content,
      postID: post.id
    }, null, _parent));
  });
  _push(`<!--]--></div></div></main></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/profilePage.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const profilePage = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender], ["__scopeId", "data-v-70a68eab"]]);
export {
  profilePage as default
};
//# sourceMappingURL=profilePage-8bfe791c.js.map
