<!-- CreatePostComponent.vue -->
<template>
  <div class="create-post">
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
</template>
  
<script>
import axios from 'axios';
import { useAuthorStore } from '../stores/authorStore';

export default {
  data() {
    return {
      postContent: '',
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
      const authorStore = useAuthorStore();
      try {
        const payload = {
          type: this.isPublic ? 'public' : 'private', // Adjust as per your requirement
          title: '', // You can add a title input field in your template
          source: '', // Adjust as per your requirement
          origin: '', // Adjust as per your requirement
          description: '', // You can add a description input field in your template
          contentType: '', // Adjust based on your content type
          content: this.postContent,
          published: new Date().toISOString(),
          author: 'UserID', // Adjust with your actual owner id
          categories: '', // Adjust as per your requirement
          count: 0 // Adjust as per your requirement
        };
        const response = await axios.post(authorStore.BASE_URL + '/posts', payload);
        if (response.status === 200 || response.status === 201) {
          // Handle success scenario
          console.log('Post created successfully:', response.data);
        } else {
          // Handle any other response scenario
          console.error('Error creating post:', response);
        }
      } catch (error) {
        console.error('Error while creating post:', error);
      }
    }
  }
};
</script>
  
  
<style scoped>
.create-post {
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
</style>
  