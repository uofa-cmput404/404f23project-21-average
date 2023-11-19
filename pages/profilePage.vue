<template>
  <div class="app-container">
    <button class="logout-button" @click="logout">Logout</button>
    <SidebarComponent />
    <main class="main-content">
      <div class="user-section">
        <input type="file" id="profilePhotoInput" ref="profilePhotoInput" @change="changeProfilePhoto" style="display: none;">
        <img :src="profilePhoto" class="profile-photo" @click="triggerProfilePhotoUpload">
        
        <div class="username">
          <h2>{{ username }}</h2>
        </div>
        <div class="follow-info">
          <button>Followers: </button>
          <button>Friends: </button>
          <button>Following: </button>
        </div>
        <div class="posts-section">
          <h3>MY POSTS:</h3>
          <PostComponent v-for="post in posts" :key="post.id" :postContent="post.content" :userId="post.owner.username"
          :postID="post.id" />
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import PostComponent from './postComponent.vue';
import SidebarComponent from './sidebar.vue';
import commentComponent from './commentComponent.vue';
import axios from 'axios';
import { useAuthorStore } from '../stores/authorStore';
import defaultProfilePic from '../pages/defualtprofilepic.jpg'; // Import the default profile image

export default {
  name: "SocialDistributionApp",
  components: {
    PostComponent,
    SidebarComponent,
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
      posts: [], // Initialize posts as an empty array
      editingBio: false,
      profilePhoto: defaultProfilePic, // Initialize with default image
      username : '' 
    };

  },
  async mounted() {
    const authorStore = useAuthorStore();
    try {
      // Fetch user's posts
      let postsResponse = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/');
      this.posts = postsResponse.data.results;

      // Fetch user's profile
      let profileResponse = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId);
      this.username = profileResponse.data.username; // Update this line to match your API response structure
      
      // Set profile photo if available
      if (profileResponse.data.profilePicture) {
        this.profilePhoto = profileResponse.data.profilePicture;
      }

    } catch (error) {
      console.error('Error while fetching data:', error);
    }
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
    
    logout() {
    // Here you should implement the logic to clear user data and redirect
    // For demonstration, let's just log out and redirect to a login page
    console.log("Logging out");
    // Clear user data (local storage/session storage)
    // Redirect to login page
    window.location.href = '/loginPage'; // Replace with your login page URL
  }
  },
  
  async created() {

    const authorStore = useAuthorStore();

    try {
      const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/');
    } catch (error) {
      console.error('Error while fetching posts:', error);
    }
    
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
<<<<<<< HEAD
 
=======

.logout-button {
  position: fixed; /* changed from absolute to fixed to ensure it's relative to the viewport */
  top: 10px; /* distance from the top */
  right: 10px; /* distance from the right, changed from left to right */
  padding: 8px 15px;
  background-color: black; /* background color changed to black */
  color: white; /* text color changed to white */
  border: none;
  border-radius: 5px;
  cursor: pointer;
  z-index: 1000; /* high z-index to ensure it's above other elements */
}

>>>>>>> 35bd763bc9d458a934ee96527104d8411fdd7bfd
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
</style>
 