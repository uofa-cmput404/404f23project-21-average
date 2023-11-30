<template>
  <div class="homepage-container">

    <!-- Homepage Main Content -->
    <div class="homepage-main-content">
      <!-- Button to Show CreatePostComponent as a Popup -->
      <div class="add-post-button-container">
        <button @click="showPostPopup = true">Add New Post</button>
      </div>

      <!-- Posts rendering section -->
      <div class="posts-feed">
        <h2>Posts</h2>
        <PostComponent v-for="post in posts" :key="post.id" :postContent="post.content" :userId="post.author.username"
          :postImage="post.image" :postID="post.id" :isPublic="post.visibility" :contentType="post.contentType"
          :remotePost="checkRemote()" />
      </div>
      <SidebarComponent />
    </div>

    <!-- CreatePostComponent Popup -->
    <div v-if="showPostPopup" class="post-popup">
      <div class="create-post">
        <!-- Close button -->
        <button type="button" class="close btn-close" aria-label="Close" @click="showPostPopup = false">
          <span aria-hidden="true">&times;</span>
        </button>

        <textarea v-model="postContent" placeholder="What's on your mind?"></textarea>

        <div class="post-actions">
          <label class="upload-image">
            Upload Image
            <input type="file" @change="onImageSelected">
          </label>
          <div class="toggle-container">
            <label class="switch">
              <input type="checkbox" v-model="isPublic">
              <span class="slider"></span>
            </label>
            <span>{{ isPublic ? 'Public' : 'Private' }}</span>
          </div>
          <!-- Add this inside your create-post form -->
          <!-- Add this inside your create-post form -->

          <div class="toggle-container">
            <label class="switch">
              <input type="checkbox" v-model="isPlainText">
              <span class="slider"></span>
            </label>
            <span>{{ isPlainText ? 'Plain Text' : 'Markdown' }}</span>
          </div>

        </div>

        <button @click="submitPost">Post</button>
      </div>
    </div>

  </div>
</template>


<script>
import { useAuthorStore } from '../stores/authorStore';
import PostComponent from './postComponent.vue';
import SidebarComponent from './sidebar.vue';
import axios from 'axios';
import * as marked from 'marked'

export default {
  name: "SocialDistributionApp",
  components: {
    PostComponent,
    SidebarComponent,
  },

  computed: {
    // renderedContent() {
    //   if (this.contentType === 'text/markdown') {
    //     return marked(this.postContent);
    //   }
    //   return this.postContent; // For plain text, return as-is
    // },
  },

  data() {
    return {
      posts: [],
      postContent: '',
      postImage: null,
      isPublic: true,
      showPostPopup: false, // Variable to control the visibility of the create post popup
      isPlainText: true,
    };
  },
  async mounted() {
    // this.fetchPosts();
    const authorStore = useAuthorStore();
    axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
    const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/allposts/stream/?page_size=100');
    console.log('102', response.data.items)
    this.posts = response.data.items;
  },
  methods: {
    // Methods for CreatePostComponent
    onImageSelected(event) {
      const file = event.target.files[0];
      if (file) {
        this.postImage = file;
      }
    },

    async submitPost() {
      const authorStore = useAuthorStore();
      try {
        let formData = new FormData();
        formData.append('visibility', this.isPublic ? 'PUBLIC' : 'FRIENDS');
        formData.append('unlisted', false);
        formData.append('title', 'Your Title Here'); // Adjust accordingly
        formData.append('source', 'Your Source Here'); // Adjust accordingly
        formData.append('origin', 'Your Origin Here'); // Adjust accordingly
        formData.append('description', 'Your Description Here'); // Adjust accordingly
        formData.append('contentType', this.isPlainText === false ? 'text/markdown' : 'text/plain');
        formData.append('content', this.postContent);
        formData.append('published', new Date().toISOString());
        formData.append('categories', 'Your Categories Here'); // Adjust accordingly
        if (this.postImage) {
          formData.append('image', this.postImage);
        }

        axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
        const response = await axios.post(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
      } catch (error) {
        console.error('Error while creating post:', error);
      }
      this.showPostPopup = false; // Close the popup after submitting the post
    },

    async checkRemote(post) {
      const authorStore = useAuthorStore();
      console.log('checkRemote', post)
      return post.origin.split('/')[2] !== authorStore.BASE_URL.split('/')[2];
    },
    async created() {
      const authorStore = useAuthorStore();
      try {
        const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/');
      } catch (error) {
        console.error('Error while fetching posts:', error);
      }
    },

  }
};
</script>

<style>
/* Add styles for the popup overlay and the existing styles for create-post */
.post-popup {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  /* Semi-transparent background */
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  /* To ensure it's on top of other content */
}

.create-post {
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 25px;
  width: 400px;
  height: 400px;
  background-color: #00C58E;
  border-radius: 15px;
}

textarea {
  width: 95%;
  height: 200px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid black;
  background-color: black;
  color: white;
  margin-bottom: 15px;
}

.post-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 95%;
  margin-bottom: 15px;
}

.upload-image input[type="file"] {
  display: none;
}

.upload-image {
  cursor: pointer;
  background-color: black;
  color: white;
  padding: 6px 12px;
  border-radius: 5px;
}

button {
  width: 95%;
  padding: 12px;
  background-color: black;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #333;
}

.switch {
  position: relative;
  display: inline-block;
  width: 60px;
  height: 20px;
  /* Adjusted to make it rectangular */
}

.switch input {
  opacity: 0;
  width: 0;
  height: 0;
}

.slider {
  position: absolute;
  cursor: pointer;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: black;
  transition: 0.4s;
  border-radius: 10px;
  /* Rounded edges for the slider */
}

.slider:before {
  position: absolute;
  content: "";
  height: 15px;
  width: 15px;
  left: 3px;
  bottom: 3px;
  background-color: #00C58E;
  transition: 0.4s;
  margin-bottom: -1px;
  border-radius: 7px;
  /* Rounded edges for the handle */
}

input:checked+.slider {
  background-color: black;
}

input:checked+.slider:before {
  transform: translateX(29px);
  display: flex;
  align-items: center;
}

.toggle-container span {
  margin-left: 10px;
  color: black;
}

.homepage-container {
  display: flex;
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  right: 0;
}

.homepage-main-content {
  position: fixed;
  left: 26%;
  top: 0;
  bottom: 0;
  right: 0;
  background-color: #00C58E;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 20px;
}

.posts-feed {
  margin: 20px 0;
}

.posts-feed h2 {
  color: black;
  text-align: center;
  margin-bottom: 20px;
}

.add-post-button-container {
  display: flex;
  justify-content: center;
  margin: 20px 0;
}

.btn-close {
  position: absolute;
  width: 30px;
  /* Square button dimensions */
  height: 30px;
  top: 10px;
  right: 10px;
  background-color: black;
  border: none;
  display: flex;
  align-items: center;
  /* Centers the 'x' vertically */
  justify-content: center;
  /* Centers the 'x' horizontally */
  padding: 0;
  /* Override Bootstrap's padding to maintain the square shape */
}
</style>