<template>
  <div class="app-container">
    <SidebarComponent/>
    <main class="main-content">
      <div class="user-section">
        <img src="404f23project-21-average\socialDistribution\pages\spiderman.jpeg" alt="Profile photo" class="profile-photo">
        <h2>User1</h2>
        <div class="follow-info">
          <button>Followers:  </button>
          <button>Following:  </button>
        </div>
        <div class="bio-section">
          <textarea placeholder="Write a Bio"></textarea>
        </div>
        <button class = 'edit'>Edit</button>
        <div class="posts-section">
          <h3>MY POSTS:</h3>
          <PostComponent postContent="First post content here"/>
          <PostComponent postContent="Second post content here"/>
          <PostComponent postContent="Third post content here"/>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import PostComponent from './postComponent.vue';
import SidebarComponent from './sidebar.vue';
export default {
  name: "SocialDistributionApp",
  components:{
    PostComponent,
    SidebarComponent
  }
};
</script>

<style scoped>
.app-container {
  display: flex;
  width:100%;
  height:100%;
  position:fixed;
  top:0;
  right:0;
}


.main-content {
    position:fixed;
    left:26%;
    top:0;
    bottom:0;
    right:0;
    background-color: #00C58E;
    overflow-y: auto;
    overflow-x:hidden;
  }

.user-section h2 {
  color: black;
  margin-bottom: 20px;
}

.profile-photo {
  width: 150px;  /* Adjust based on your requirement */
  height: 150px; /* Adjust based on your requirement */
  border-radius: 50%;  /* Makes the photo circular */
  display: block;
  margin: 20px auto;  /* Center the image horizontally and add some margin */
  border: 3px solid white;  /* Optional: Add a border around the image */
}
.follow-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  color: black;
}

.bio-section textarea {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 80%;
  margin:auto auto;
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
  width:80%;
  margin:auto auto;
  color: white;
  margin-bottom: 10px;
}
h2{
    text-align: center;
    font-size: 40px;
}
button{
    background-color: black;
    color:white;
    padding: 10px 15px;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.2s;
    margin: auto auto;
}

.edit{
    margin-left: 46%;
    margin-right: 50%;
}
</style>
