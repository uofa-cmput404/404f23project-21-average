<template>
    <div class="app-container">
      <div class="sidebar">
        <div class="app-title">
          <span class="title-social">SOCIAL</span>
          <span class="title-distribution">DISTRIBUTION</span>
        </div>
        <div class="icons">
        <i class="bi bi-house" id="home-icon"></i>
        <i class="bi bi-people" id = "friends" ></i>
        <i class="bi bi-search" id="search-icon"></i>
        <i class="bi bi-person" id="profile-icon"></i>
        </div>
      </div>
      <div class="main-content">
        <div class="header">FRIENDS</div>
        <div class="friend-list">
          <button v-for="friend in friends" :key="friend.id" @click="gotoProfile(friend.id)">{{ friend.name }}</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "SocialDistributionApp",
    data() {
      return {
        friends: [
          { id: 1, name: "User_1" },
          { id: 2, name: "User_2" },
          { id: 3, name: "User_3" },
          { id: 4, name: "User_4" },
          { id: 5, name: "User_5" }
        ]
      };
    },
    methods: {
      gotoProfile(id) {
        // Navigate to the friend's profile
        console.log('Navigating to profile of User ID: ${id}');
      }
    }
  };
  </script>
  
  <style scoped>
  .app-container {
    display: flex;
    height: 100%;
    width:100%;
    position:fixed;
    top:0;
    bottom:0;
    right:0;
    background-color: black;
  }
  .sidebar {
    width: 24%;
    height:100%;
    padding: 20px;
    background-color: black;
    color: #00C58E;
  }
  
  .app-title {
    font-size: 40px;
    margin-bottom: 70px;
  }
  
  .title-social,
  .title-distribution {
    display: block;
  }
  
  .title-social {
    color: white;
  }
  
  .bi{
    font-size: 60px;
    margin-left:20px;

  }

  .sidebar i.bi {
    display: block;
    margin-bottom: 40px; /* Optional: Add space between the icons */
}
  
  .main-content {
    flex: 1;
    background-color: #00C58E;
    padding: 20px;
  }
  
  .header {
    background-color: black;
    padding:15px ;
    width: 40%;
    margin: 0 auto;
    color: white;
    overflow-y: auto;  
    font-size: 025px;  
    border: 2px solid white;
    text-align: center;
    margin-bottom: 20px;
    border-radius: 30px; 
  }
  
  .friend-list button {
  
    display: block;
    width: 70%;
    margin: 0 auto;
    padding: 15px;
    margin-bottom: 10px;
    background-color: black;
    color: 00C58E;
    border: none ;
    cursor: pointer;
    border-radius: 20px;
    color: #009B75;
  }
  
  .friend-list button:hover {
    background-color: #009B75;
  }
  </style>