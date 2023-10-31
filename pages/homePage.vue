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
        <PostComponent v-for="post in posts" :key="post.id" :postContent="post.content" :postID="post.id" />
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
        </div>

        <button @click="submitPost">Post</button>
      </div>
    </div>

  </div>
</template>


<script lang="ts">
import { useAuthorStore } from '../stores/authorStore';
import PostComponent from './postComponent.vue';
import SidebarComponent from './sidebar.vue';
import { storeToRefs } from 'pinia'
import axios from 'axios';

export default {
  name: "SocialDistributionApp",
  components: {
    PostComponent,
    SidebarComponent,
  },
  data() {
    return {
      posts: [],
      postContent: '',
      postImage: null,
      isPublic: true,
      showPostPopup: false, // Variable to control the visibility of the create post popup
    };
  },
  async mounted() {
    // this.fetchPosts();
    const authorStore = useAuthorStore();
    const response = await axios.get(process.env.API_URL +  authorStore.getAuthorId + '/posts/');
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
      // Image selection logic
    },
    async submitPost() {
      const authorStore = useAuthorStore();
      // authorStore.fetchAuthor()
      // Post submission logic
      try {
        const payload = {
          type: this.isPublic ? 'PUBLIC' : 'FRIENDS', // Adjust as per your requirement
          title: 'string', // You can add a title input field in your template
          source: 'string', // Adjust as per your requirement
          origin: 'string', // Adjust as per your requirement
          description: 'string', // You can add a description input field in your template
          contentType: 'string', // Adjust based on your content type
          content: this.postContent,
          published: new Date().toISOString(),
          categories: 'string', // Adjust as per your requirement
          image: this.postImage,
        };
        axios.defaults.headers.common["Authorization"] = `Bearer ${authorStore.getAuthToken}`;
        const response = await axios.post(process.env.API_URL +  authorStore.getAuthorId + '/posts/', payload);
        console.log(response.data)
      } catch (error) {
        console.error('Error while creating post:', error);
      }
      this.showPostPopup = false; // Close the popup after submitting the post
    }
  },
  async created() {
    const authorStore = useAuthorStore();
    try {
      console.log(authorStore.authorId, authorStore.authToken)
      const response = await axios.get(process.env.API_URL +  authorStore.getAuthorId + '/posts/');
    } catch (error) {
      console.error('Error while fetching posts:', error);
    }
  },

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