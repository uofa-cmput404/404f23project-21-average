<template>
  <div>
    <!-- Post Component -->
    <div class="post">
      <div class="post-status-icon">
        <i v-if="isPublic === 'PUBLIC'" class="bi bi-globe"></i> <!-- Public Icon -->
        <i v-else class="bi bi-lock-fill"></i> <!-- Private Icon -->
      </div>
      <div class="user-info">
        <img :src="profilePicture" alt="User Profile Picture" class="profile-pic" />
        <span class="user-id">{{ userId }}</span>
      </div>

      <div class="post-content">
        
        <div>
          <div v-if="postImage !== null">
            <img v-if="postImage" :src="postImage">
          </div>
          <div v-if = "contentType === 'text/markdown'">
            <div v-html="renderedContent"></div>
          </div>
          <div v-else>
            <p style="margin-top: 25px;">{{ postContent }}</p>
          </div>
          
        </div>

        <div class="post-actions">
          <button @click="toggleLike">{{ liked ? 'Unlike' : 'Like' }}</button>
          <button @click="toggleCommentBox">Comment</button>
          <button @click="sharePostWithUser">Share</button> 
        </div>
        <div v-if="showCommentBox">
          <comment-component v-if="showCommentBox" :postId="postID"></comment-component>
        </div>
      </div>
    </div>

    
    <!-- Edit Post Component -->
    <div v-if="showEditPost" class="edit-post">
      <textarea v-model="editedPostContent" placeholder="Edit your post"></textarea>
      <button @click="deletePost" class="delete-button">Delete Post</button>

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
import * as marked from 'marked'
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
    postImage: String,
    isPublic: String,
    contentType: String,
    remotePost: Boolean
  },

  data() {
    return {
      liked: false,
      showCommentBox: false,
      showEditPost: false,
      postMainContent: this.postContent,
      editedPostContent: '',  // initialized from the prop
      postImage: this.postImage,
      isPublic: this.isPublic,
      userList: [{ id: 1, name: 'User 1' }, { id: 2, name: 'User 2' }],
      postid: String,
      

    };
  },

  computed: {
    renderedContent() {
      if (this.contentType === 'text/markdown') {
        return marked.marked(this.postContent);
      }
      return this.postContent; // For plain text, return as-is
    },
  },
  async mounted() {
    const authorStore = useAuthorStore();
    this.postid = await (authorStore.getIDFromURL(this.postID) )
    this.postImage = authorStore.BASE_URL.split('/api')[0] + this.postImage;
    const response = await axios.get(authorStore.BASE_URL + '/posts/' + authorStore.getAuthorId + '/liked/')
    for (let i = 0; i < response.data.items.length; i++) {
      if (response.data.items[i].comment !== undefined){
        continue
      }
      else{
      if (response.data.items[i].post === this.postid) {
        console.log("lol")
        this.liked = true
      }
    }
  }
  },

  async created() {
    const authorStore = useAuthorStore();
    this.commentid = await (authorStore.getIDFromURL(commentId) )
    this.postid = await (authorStore.getIDFromURL(this.postID) )
    try {
      axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
      const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/');
      // Fetch post details
      if (response.status === 200) {
        this.post = response.data;
        this.postImageUrl = this.post.image;
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
      const authorStore = useAuthorStore();
      this.postid = await (authorStore.getIDFromURL(this.postID) )
      // Implement the logic to get likes
      // Example:
      try {
        axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
        if (!this.remotePost) {
          const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/' + this.postid + '/likes/');
          if (response.status === 200) {
            this.likeCount = response.data.count;
            this.liked = response.data.userLiked; // Assuming the API returns if the current user liked the post
          }
        }

      } catch (error) {
        console.error('Error while fetching likes:', error);
      }
    },
    async toggleLike() {
      const authorStore = useAuthorStore();
      this.postid = await (authorStore.getIDFromURL(this.postID) )
      try {
        axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
        if (this.liked) {
          // Logic to unlike the post
          await axios.post(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/' + this.postid + '/likes/');
          this.likeCount -= 1;
        } else {
          // Logic to like the post
          console.log(this.postID)
          await axios.post(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/' + this.postid + '/likes/');
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
          this.postImageUrl = e.target.result; // Update the image URL for display
        };
      }
    },
    async updatePost() {
      const authorStore = useAuthorStore();
      // this.postContent = this.editedPostContent;  // Update the main content
      this.showEditPost = false;
      this.postMainContent = this.editedPostContent;
      let formData = new FormData();
      formData.append('visibility', this.isPublic ? 'PUBLIC' : 'FRIENDS');
      formData.append('unlisted', false);
      formData.append('title', 'Your Title Here'); // Adjust accordingly
      formData.append('source', 'Your Source Here'); // Adjust accordingly
      formData.append('origin', 'Your Origin Here'); // Adjust accordingly
      formData.append('description', 'Your Description Here'); // Adjust accordingly
      formData.append('content', this.editedPostContent);
      formData.append('published', new Date().toISOString());
      formData.append('categories', 'Your Categories Here'); // Adjust accordingly
      if (this.postImage) {
        formData.append('image', this.postImage);
      }
      axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
      const response = await axios.post(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/' + this.postid + "/", formData);
    },
    async deletePost() {
      const authorStore = useAuthorStore();
      this.postid = await (authorStore.getIDFromURL(this.postID) )
      const authorId = authorStore.getAuthorId; // Replace with actual way to get author_id
      const postId = this.postID; // Assuming this is a prop or data property

      try {
        axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
        const response = await axios.delete(`${authorStore.BASE_URL}/authors/${authorId}/posts/${this.postid}`);

        if (response.status === 200 || response.status === 204) {
          // Handle successful deletion, like updating UI or redirecting
        }
      } catch (error) {
        console.error('Error while deleting post:', error);
        // Handle error
      }
    },


    async sharePostWithUser() {
      console.log('Sharing post with users');
      const authorStore = useAuthorStore();
      const response = await axios.post(authorStore.BASE_URL + '/share/' + this.postid + '/');
    }

  }
};
</script>
  
  <!-- Combining styles from both components -->
<style scoped>

/* General Styles */
* {
  box-sizing: border-box;
}

body {
  font-family: 'Arial', sans-serif;
}

/* Post Component Styles */
.post {
  background-color: #1f1f1f;
  padding: 20px;
  margin: 20px auto;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  max-width: 100%; /* Ensures it doesn't overflow the parent container */
  word-wrap: break-word; /* Prevents long text strings from overflowing */
}

.post img {
  max-width: 100%; /* Ensures images are responsive */
  height: auto; /* Maintains aspect ratio */
  border-radius: 5px;
}

.post-content, .user-info, .post-actions {
  width: 100%; /* Ensures these elements don't overflow */
}

.post-status-icon {
  position: absolute;
  top: 17px;
  right: 17px;
  font-size: 1.5em;
  color: #00C58E; /* Green color for icons */
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 10px;
  border: 2px solid #00C58E; /* Green border for profile pic */
}

.user-id {
  color: #00C58E;
  font-weight: bold;
}

.post-content {
  margin-top: 15px;
  color: white;
}

.post-actions {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}
.post-actions button {
  margin-right: 10px; /* Adds space to the right of each button */
}

.post-actions button:last-child {
  margin-right: 0px; /* Removes the margin from the last button */
}

button {
  background-color: #00C58E;
  color: black;
  padding: 8px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s, transform 0.2s;
}

button:hover {
  background-color: #007744;
  transform: scale(1.05); /* Slightly enlarge buttons on hover */
}

/* Edit Post Component Styles */
.edit-post {
  background-color: #2c2c2c; /* Darker background for edit area */
  padding: 25px;
  border-radius: 8px;
  margin-top: 20px;
  width: 90%;
  max-width: 500px; /* Limit maximum width */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3); /* More pronounced shadow */
}

textarea {
  width: 100%;
  height: 150px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #333;
  background-color: #1f1f1f;
  color: white;
  margin-bottom: 15px;
  resize: vertical; /* Allow vertical resizing */
}

.upload-image {
  background-color: #333;
  color: white;
  padding: 6px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.upload-image:hover {
  background-color: #1f1f1f;
}

.delete-button {
  background-color: red;
  margin-top: 10px;
}

.delete-button:hover {
  background-color: darkred;
}

/* Toggle Switch Styles */
.switch {
  width: 60px;
  height: 24px;
}

.slider:before {
  height: 20px;
  width: 20px;
}

input:checked + .slider {
  background-color: #4CAF50; /* Green background for active toggle */
}

/* Additional Hover Effects */
a:hover, button:hover {
  opacity: 0.9; /* Slight opacity change on hover */
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .post, .edit-post {
    width: 95%; /* Full width on smaller screens */
    margin: 10px auto;
  }
}
/* Share Popup Styles */
.share-popup {
  background-color: #2c2c2c;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  padding: 15px;
  width: 100%; /* Take full width of the post */
  margin-top: 10px; /* Space between post content and share popup */
}

/* Rest of the share-popup styles remain the same */

.share-popup ul {
  list-style-type: none;
  padding: 0;
  margin: 0;
}

.share-popup li {
  margin-bottom: 10px; /* Space between list items */
}

.share-popup li:last-child {
  margin-bottom: 0; /* Remove margin for the last item */
}

.share-popup button {
  background-color: #00C58E;
  color: black;
  width: 100%;
  padding: 8px 10px;
  text-align: left; /* Align text to the left */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.share-popup button:hover {
  background-color: #007744;
}

/* Adjustments for smaller screens */
@media (max-width: 768px) {
  .share-popup {
    width: 100%; /* Full width on smaller screens */
    right: 0; /* Align with the right edge */
  }
}

</style>


  