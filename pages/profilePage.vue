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
          
          <button @click="fetchFollowers">Followers</button>
          <button @click="fetchFollowing">Following</button> <!-- New Friends button -->
          
          </div>
          <UserListPopup 
            :visible="showFollowersPopup" 
            :users="followers" 
            title="Followers" 
            @update:visible="showFollowersPopup = $event" />
          <UserListPopup 
            :visible="showFriendsPopup" 
            :users="friends" 
            title="Friends" 
            @update:visible="showFriendsPopup = $event" />
          <UserListPopup 
            :visible="showFollowingPopup" 
            :users="following" 
            title="Following" 
            @update:visible="showFollowingPopup = $event" />
          <!-- ... other content ... -->
  
        
        
        
        <div class="posts-section">
          <h3>MY POSTS:</h3>
          <PostComponent v-for="post in posts" :key="post.id" :postContent="post.content" :userId="post.author.username"
          :postImage="post.image" :postID="post.id" />
        </div>

        <div class = "github">
          <h3>GITHUB STREAM</h3>

          <div v-for="activity in github" :key="activity.id" class="github_activity">
            <div>
              <h4>Activity Type: {{ activity.type }}</h4>
              <h4>Activity Repository: {{ activity.repo.name }} </h4>
              <h4>Activity Author: {{ activity.actor.login }}</h4>
            </div>
        </div>
      </div>
        </div>
    </main>
  </div>
</template>

<script>
import PostComponent from './userPost.vue';
import SidebarComponent from './sidebar.vue';
import commentComponent from './commentComponent.vue';
import axios from 'axios';
import { useAuthorStore } from '../stores/authorStore';
import defaultProfilePic from '../pages/defualtprofilepic.jpg'; // Import the default profile image
import UserListPopup from './UserListPopup.vue';

export default {
  name: "SocialDistributionApp",
  components: {
    PostComponent,
    SidebarComponent,
    commentComponent,
    UserListPopup,
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
      followers: [],
      following:[],
      bio: "Write a Bio",
      editingBio: false,
      profilePhoto: defaultProfilePic, // Initialize with default image
      showFollowersPopup: false,
      showFriendsPopup: false,
      showFollowingPopup: false,
      username : '' ,
      github: [],
      formattedGithubActivities: []
    };

  },
  async mounted() {
    const authorStore = useAuthorStore();
    try {
      // Fetch user's posts
      let postsResponse = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/');
      this.posts = postsResponse.data.items;

      // Fetch user's profile
      let profileResponse = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId);
      this.username = profileResponse.data.username; // Update this line to match your API response structure
      
      // Set profile photo if available
      if (profileResponse.data.profilePicture) {
        this.profilePhoto = profileResponse.data.profilePicture;
      }

      // fetch github
      this.getGithub();

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
    async fetchFollowers() {
    // Fetch and populate followers
    const authorStore = useAuthorStore();
    const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/followers/');
    console.log("yoyoyoyo")
    this.followers = response.data.items
    console.log(this.followers)
    this.showFollowersPopup = true;
  },
  fetchFriends() {
    // Fetch and populate friends
    this.showFriendsPopup = true;
  },
  async fetchFollowing() {
    const authorStore = useAuthorStore();
    const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/following/');
    this.following = response.data.items;
    console.log(this.following)
    this.showFollowingPopup = true;
  },

  async getGithub(){
    const authorStore = useAuthorStore();
    const response = await axios.post(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/github/');
    this.github = response.data
    console.log(this.github)
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
      const author = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/');
      console.log(author.data)
      const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/posts/');
      console.log(response)
      if (response.status === 200) {
        this.posts = response.data.items; // Update the posts data property with the fetched posts
        this.author = author.data;
        this.profileImage = author.data.image;
        // console.log((await this).profileImage, (await this).author)
      } else {
        console.error('Error fetching posts:', response);
      }
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


.popup {
  display: flex;
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* Semi-transparent black background */
  justify-content: center;
  align-items: center;
  z-index: 10000; /* High z-index to make sure it's on top */
}

.popup-content {
  background-color: grey; /* Black background for the content */
  color: white; /* White text */
  padding: 40px; /* Increased padding for more space inside */
  border-radius: 5px;
  width: 70%; /* Increase the width as needed */
  max-width: 400px; /* Adjust max-width as needed */
  min-height: 400px; /* Add a minimum height if needed */
  z-index: 10001; /* Ensure content is above the semi-transparent background */
  position: relative; /* Needed for absolute positioning of the close button */
  box-sizing: border-box; /* Ensure padding is included in width calculation */
  overflow-y: auto; /* Add scroll for content overflow */
  overflow-x: auto;
  align-items: center;
  text-align: center;

}
.popup-content h3 {
  font-size: 24px; /* Increase the font size as needed */
  color: white; /* Optional: specify the color if different from the default */
  margin-bottom: 20px; /* Optional: add some space below the heading */
  /* Additional styling like font-weight, letter-spacing, etc., can be added here */
}


.close {
  color: white;
  position: absolute;
  top: 0;
  right: 10px;
  font-size: 30px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover {
  color: #ccc;
  text-decoration: none; /* Removes underline text on hover */
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 5px 0; /* Spacing between list items */
}

.close {
  position: absolute;
  top: 10px;
  right: 20px;
  cursor: pointer;
  font-size: 1.5em;
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

.github_activity{
  display: flex;
  justify-content: space-between;
  align-items: start;
  background-color: black;
  margin: 10px auto;
  padding: 15px;
  border-radius: 10px;
  color: white;
  border: 1px solid #00C58E;
}

h4{
  color:white
}
</style>
 