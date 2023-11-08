<template>
  <div class="app-container">
    <SidebarComponent />
    <main class="main-content">
      <div class="user-section">
        <input type="file" id="profilePhotoInput" ref="profilePhotoInput" @change="changeProfilePhoto" style="display: none;">
        <img :src="profilePhoto" class="profile-photo" @click="triggerProfilePhotoUpload">
        <h2>{{ username }}</h2>
        <div class="follow-info">
          <button>Followers: </button>
          <button>Following: </button>
        </div>
        <div class="bio-section" v-if="!editingBio">
          <p>{{ bio }}</p>
          <button class="edit" @click="editingBio = true">Edit</button>
        </div>
        <div class="bio-section" v-else>
          <textarea v-model="bio"></textarea>
          <button class="edit" @click="saveBio">Save</button>
        </div>
        <div class="posts-section">
          <h3>MY POSTS:</h3>
          <PostComponent v-for="post in posts" :key="post.id" :postContent="post.content" :postID="post.id" />
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import PostComponent from './postComponent.vue';
import SidebarComponent from './sidebar.vue';
import axios from 'axios';
import { useAuthorStore } from '../stores/authorStore';

export default {
  name: "SocialDistributionApp",
  components: {
    PostComponent,
    SidebarComponent,
  },
  data() {
    return {
      posts: [], // Initialize posts as an empty array
      bio: "Write a Bio",
      editingBio: false,
      //profilePhoto: "@/pages/spiderman.jpeg", // Initialize with default image
      
      username: 'USER', // Add this line to store the fetched username
    };

  },
  async mounted() {
    // this.fetchPosts();
    const authorStore = useAuthorStore();
    const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/');
    this.posts = response.data.results;
  },
  
  methods: {
    triggerProfilePhotoUpload() {
      this.$refs.profilePhotoInput.click();
    },
    changeProfilePhoto(event) {
      const file = event.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          this.profilePhoto = e.target.result;
        };
        reader.readAsDataURL(file);
      }
    },
    saveBio() {
      // Here you should implement the logic to save the bio, perhaps sending it to a server
      this.editingBio = false;
      // For demonstration purposes, we'll just log it
      console.log(this.bio);
    },
    // fetchPosts() {
    //   const authorStore = useAuthorStore();
    //   // Replace '/api/posts/' with your actual endpoint that retrieves the user's posts
    //   axios.get(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/posts/`)
    //     .then(response => {
    //       if (response.status === 200) {
    //         this.posts = response.data; // Assuming the data is an array of posts
    //       } else {
    //         console.error('Failed to fetch posts:', response);
    //       }
    //     })
    //     .catch(error => {
    //       console.error("Error fetching posts:", error);
    //     });
    // },
  },
  async created() {

    const authorStore = useAuthorStore();
    this.fetchPosts();
  },
};
</script>



<style scoped>
.app-container {
  display: flex;
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  right: 0;
}


.main-content {
  position: fixed;
  left: 26%;
  top: 0;
  bottom: 0;
  right: 0;
  background-color: #00C58E;
  overflow-y: auto;
  overflow-x: hidden;
}

.user-section h2 {
  color: black;
  margin-bottom: 20px;
}

.profile-photo {
  width: 150px;
  /* Adjust based on your requirement */
  height: 150px;
  /* Adjust based on your requirement */
  border-radius: 50%;
  /* Makes the photo circular */
  display: block;
  margin: 20px auto;
  /* Center the image horizontally and add some margin */
  border: 3px solid white;
  /* Optional: Add a border around the image */
}

.follow-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  color: black;

}

.bio-section p {
  display: block; /* Ensures the element is block-level, affecting layout */
  width: 80%; /* Match textarea width */
  margin: auto auto; /* Center it */
  margin-bottom: 20px; /* Adjust this value to increase or decrease the space */
  padding: 10px; /* Match textarea padding */
  background-color: black; /* Match textarea background color */
  color: white; /* Match textarea text color */
  border: none; /* No border as per textarea */
  white-space: pre-wrap; /* Ensures that whitespace and newlines are preserved */
  word-wrap: break-word; /* Ensures the text breaks to prevent overflow */
}

.bio-section textarea {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80%;
  margin: auto auto;
  padding: 10px;
  border: none;
  background-color: black;
  color: white;
  margin-bottom: 20px;
}

.posts-section h3 {
  color: black;
  margin-bottom: 20px;
  text-align: center;
}

.post {
  background-color: black;
  padding: 60px;
  width: 80%;
  margin: auto auto;
  color: white;
  margin-bottom: 10px;
}

h2 {
  text-align: center;
  font-size: 40px;
}

button {
  background-color: black;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
  margin: auto auto;
  width: auto;
}

.edit {
  margin-left: auto;
  margin-right: auto;
  margin-top: 20px; /* Add top margin to the edit button for space */
  display: block;
  /* To enable margin auto to work for horizontal centering */
  font-size: 10px;
  /* Smaller font size */
  padding: 10px 15px;
  width: auto;

}
</style>
 