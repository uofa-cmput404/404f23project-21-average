import axios from "axios";
import { u as useAuthorStore } from "./authorStore-171782f1.js";
import { ssrRenderAttrs, ssrRenderAttr, ssrInterpolate, ssrIncludeBooleanAttr, ssrLooseContain, ssrRenderStyle } from "vue/server-renderer";
import { useSSRContext } from "vue";
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
const postComponent_vue_vue_type_style_index_0_scoped_a95db836_lang = "";
const _sfc_main = {
  props: {
    profilePicture: {
      type: String,
      default: ""
    },
    userId: String,
    postID: String,
    postContent: String
  },
  data() {
    return {
      liked: false,
      showCommentBox: false,
      showEditPost: false,
      postMainContent: this.postContent,
      editedPostContent: "",
      // initialized from the prop
      postImage: null,
      isPublic: false
      // You can set the initial value as needed
    };
  },
  async created() {
    const authorStore = useAuthorStore();
    try {
      console.log("http://localhost:8000/api/post/" + this.postID);
      const response = await axios.get("http://127.0.0.1:8000/authors/" + authorStore.getAuthorId + "/posts/");
      console.log(response);
      this.postMainContent = response.data.results["content"];
      if (response.status === 200) {
        this.post = response.data;
      } else {
        console.error("Error fetching post:", response);
      }
    } catch (error) {
      console.error("Error while fetching post:", error);
    }
  },
  methods: {
    toggleLike() {
      this.liked = !this.liked;
    },
    toggleCommentBox() {
      this.showCommentBox = !this.showCommentBox;
    },
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
    async updatePost() {
      const authorStore = useAuthorStore();
      this.postContent = this.editedPostContent;
      this.showEditPost = false;
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
        categories: "string"
        // Adjust as per your requirement
      };
      const response = await axios.get("http://127.0.0.1:8000/authors/" + authorStore.getAuthorId + "/posts/" + this.postID, payload);
      console.log(response);
    }
  }
};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs, $props, $setup, $data, $options) {
  _push(`<div${ssrRenderAttrs(_attrs)} data-v-a95db836><div class="post" data-v-a95db836><div class="post-status-icon" data-v-a95db836>`);
  if ($data.isPublic) {
    _push(`<i class="bi bi-globe" data-v-a95db836></i>`);
  } else {
    _push(`<i class="bi bi-lock-fill" data-v-a95db836></i>`);
  }
  _push(`</div><div class="user-info" data-v-a95db836><img${ssrRenderAttr("src", $props.profilePicture)} alt="User Profile Picture" class="profile-pic" data-v-a95db836><span class="user-id" data-v-a95db836>${ssrInterpolate($props.userId)}</span></div><p data-v-a95db836>${ssrInterpolate($props.postContent)}</p><div class="post-actions" data-v-a95db836><button data-v-a95db836>${ssrInterpolate($data.liked ? "Unlike" : "Like")}</button><button data-v-a95db836>Comment</button><button class="edit" data-v-a95db836>Edit</button></div>`);
  if ($data.showCommentBox) {
    _push(`<div data-v-a95db836><textarea placeholder="Write a comment" data-v-a95db836></textarea><button data-v-a95db836>Post Comment</button></div>`);
  } else {
    _push(`<!---->`);
  }
  _push(`</div>`);
  if ($data.showEditPost) {
    _push(`<div class="edit-post" data-v-a95db836><textarea placeholder="Edit your post" data-v-a95db836>${ssrInterpolate($data.editedPostContent)}</textarea><div class="post-actions" data-v-a95db836><label class="upload-image" data-v-a95db836> Change Image <input type="file" data-v-a95db836></label><div class="toggle-container" data-v-a95db836><label class="switch" data-v-a95db836><input type="checkbox"${ssrIncludeBooleanAttr(Array.isArray($data.isPublic) ? ssrLooseContain($data.isPublic, null) : $data.isPublic) ? " checked" : ""} data-v-a95db836><span class="slider" data-v-a95db836></span></label><span style="${ssrRenderStyle({ "color": "white" })}" data-v-a95db836>${ssrInterpolate($data.isPublic ? "Public" : "Private")}</span></div></div><button data-v-a95db836>Update Post</button></div>`);
  } else {
    _push(`<!---->`);
  }
  _push(`</div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/postComponent.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const PostComponent = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender], ["__scopeId", "data-v-a95db836"]]);
export {
  PostComponent as default
};
//# sourceMappingURL=postComponent-485f3c06.js.map
