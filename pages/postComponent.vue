<template>
  <div>
    <!-- Post Component -->
    <div class="post">
      <div class="post-status-icon">
        <i v-if="isPublic" class="bi bi-globe"></i> <!-- Public Icon -->
        <i v-else class="bi bi-lock-fill"></i> <!-- Private Icon -->
      </div>
      <div class="user-info">
        <img :src="profilePicture" alt="User Profile Picture" class="profile-pic" />
        <span class="user-id">{{ userId }}</span>
      </div>
      <p>{{ postContent }}</p>
      <div class="post-actions">
        <button @click="toggleLike">{{ liked ? 'Unlike' : 'Like' }}</button>
        <button @click="toggleCommentBox">Comment</button>
        <button class='edit' @click="showEditPost = !showEditPost">Edit</button>
      </div>
      <div v-if="showCommentBox">
        <comment-component v-if="showCommentBox" :postId="postID"></comment-component>
      </div>
    </div>

    <!-- Edit Post Component -->
    <div v-if="showEditPost" class="edit-post">
      <textarea v-model="editedPostContent" placeholder="Edit your post"></textarea>
      <div class="post-actions">
        <label class="upload-image">
          Change Image
          <input type="file" @change="onImageSelected">
        </label>
        <div class="toggle-container">
          <label class="switch">
            <input type="checkbox" v-model="isPublic">
            <span class="slider"></span>
          </label>
          <span style="color:white">{{ isPublic ? 'Public' : 'Private' }}</span>
        </div>
      </div>
      <button @click="updatePost">Update Post</button>
    </div>
  </div>
</template>

<script>
import commentComponent from './commentComponent.vue';
import axios from 'axios'
import { useAuthorStore } from '../stores/authorStore';
export default {
  components: {
    commentComponent,
  },
  props: {
    postContent: {
      type: String,
      default: ''
    },
    profilePicture: {
      type: String,
      default: ''
    },
    userId: String,
    postID: String,
    postContent: String,
  },

  data() {
    return {
      liked: false,
      showCommentBox: false,
      showEditPost: false,
      postMainContent: this.postContent,
      editedPostContent: '',  // initialized from the prop
      postImage: null,
      isPublic: false  // You can set the initial value as needed
    };
  },
  async created() {
    const authorStore = useAuthorStore();
    try {
      console.log('http://localhost:8000/api/post/' + this.postID)
      const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/');
      console.log(response)
      this.postMainContent = response.data.results['content'] // Updat
      // Fetch post details
      const response1 = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/' + this.postID);
      if (response.status === 200) {
        this.post = response.data;
        // Fetch likes
        this.getLikes();
      } else {
        console.error('Error fetching post:', response);
      }
    } catch (error) {
      console.error('Error while fetching post:', error);
    }
  },


  methods: {
    async getLikes() {
      // Implement the logic to get likes
      // Example:
      try {
        const response = await axios.get(authorStore.BASE_URL + '/api/post/' + this.postID + '/likes');
        if (response.status === 200) {
          this.likeCount = response.data.likeCount;
          this.liked = response.data.userLiked; // Assuming the API returns if the current user liked the post
        }
      } catch (error) {
        console.error('Error while fetching likes:', error);
      }
    },
    async toggleLike() {
      try {
        if (this.liked) {
          // Logic to unlike the post
          await axios.post(authorStore.BASE_URL + '/api/post/' + this.postID + '/unlike');
          this.likeCount -= 1;
        } else {
          // Logic to like the post
          await axios.post(authorStore.BASE_URL + '/api/post/' + this.postID + '/like');
          this.likeCount += 1;
        }
        this.liked = !this.liked;
      } catch (error) {
        console.error('Error while toggling like:', error);
      }
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
      // this.postContent = this.editedPostContent;  // Update the main content
      this.showEditPost = false;
      this.postMainContent = this.editedPostContent;
      const payload = {
        visibility: this.isPublic ? 'PUBLIC' : 'FRIENDS', // Adjust as per your requirement
        unlisted: false,
        title: 'string', // You can add a title input field in your template
        source: 'string', // Adjust as per your requirement
        origin: 'string', // Adjust as per your requirement
        description: 'string', // You can add a description input field in your template
        contentType: 'string', // Adjust based on your content type
        content: this.editedPostContent,
        published: new Date().toISOString(),
        categories: 'string', // Adjust as per your requirement
      };
      axios.defaults.headers.common["Authorization"] = `Bearer ${authorStore.getAuthToken}`;
      const response = await axios.post(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/' + this.postID, payload);
      console.log(response)
    }

  }
};
</script>

<!-- Combining styles from both components -->
<style scoped>
/* Styles from PostComponent.vue */
/* ... */
.post {
  background-color: black;
  padding: 20px;
  width: 80%;
  margin: auto;
  color: white;
  margin-bottom: 20px;
  border-radius: 5px;
  position: relative;
}

.post-status-icon {
  position: absolute;
  top: 17px;
  right: 17px;
  font-size: 1.5em;
  /* adjust as needed */
}

.bi {
  vertical-align: middle;
}

.post-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button {
  background-color: #00C58E;
  color: black;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #007744;
}

textarea {
  background-color: grey;
  color: white;
}

.user-info {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  align-items: center;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 5px;
}

.user-id {
  color: #00C58E;
}

.edit-post {
  display: flex;
  margin-left: auto;
  margin-right: auto;
  margin-bottom: 17px;
  flex-direction: column;
  align-items: center;
  padding: 25px;
  width: 400px;
  height: 400px;
  background-color: rgb(31, 32, 31);
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

.toggle-container {
  display: flex;
  align-items: center;
}

.toggle-container span {
  margin-left: 10px;
  color: black;
}

/* Styles from EditPostComponent.vue */
/* ... */
</style>
