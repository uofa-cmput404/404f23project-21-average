<!-- EditPostComponent.vue -->
<template>
    <div class="edit-post">
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
          <span>{{ isPublic ? 'Public' : 'Private' }}</span>
        </div>
      </div>
  
      <button @click="updatePost">Update Post</button>
    </div>
  </template>
  
  <script>
  export default {
    props: ['initialPostContent', 'initialIsPublic'],
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
          privacy: this.isPublic ? 'public' : 'private'
        });
      }
    }
  };
  </script>
  
  <style scoped>
  .edit-post {
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
    height: 20px; /* Adjusted to make it rectangular */
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
    border-radius: 10px;  /* Rounded edges for the slider */
  }
  
  .slider:before {
    position: absolute;
    content: "";
    height: 15px;
    width: 15px;
    left: 3px;
    bottom: 3px;
    background-color:  #00C58E;
    transition: 0.4s;
    margin-bottom: -1px;
    border-radius: 7px;  /* Rounded edges for the handle */
  }
  
  input:checked + .slider {
    background-color:black ;
  }
  
  input:checked + .slider:before {
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
  </style>
  