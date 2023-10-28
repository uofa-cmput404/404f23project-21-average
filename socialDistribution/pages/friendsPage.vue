<template>
    <div class="app-container">
      <SidebarComponent/>
      <div class="main-content">
        <div class="header">FRIENDS</div>
        <div class="friend-list">
          <button v-for="friend in friends" :key="friend.id" @click="gotoProfile(friend.id)">{{ friend.name }}</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import SidebarComponent from './sidebar.vue';
  export default {
    name: "SocialDistributionApp",
    components:{
    SidebarComponent
  },
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
  
  .header {
    background-color: black;
    padding:15px ;
    width: 40%;
    margin: 20px auto;
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