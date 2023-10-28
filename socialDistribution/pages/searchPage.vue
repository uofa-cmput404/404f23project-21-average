import 'bootstrap-icons/font/bootstrap-icons.css';
<template>
    <div class="app-container">
      <SidebarComponent/>
      <main class="main-content">
        <div class="search-bar">
          <input type="text" placeholder="Search for friends" />
        </div>
  
      </main>
    </div>
  </template>
  
  <script>
  import SidebarComponent from './sidebar.vue';
  import 'bootstrap-icons/font/bootstrap-icons.css';
  export default {
    name: "SocialDistributionApp",
    components:{
    SidebarComponent
  }
  };


  </script>
  
  <style scoped>
  .app-container {
    width:100%;
    height:100%;
    position:fixed;
    top: 0;
    left: 0;
    right: 0;
    display: flex;
    background-color: black;
    color: white;
  }
  
  
  .main-content {
    position:fixed;
    left:26%;
    top:0;
    bottom:0;
    right:0;
    background-color: #00C58E;
  }
  
  .bi{
    font-size: 60px;
    margin-left:20px;

  }

  .sidebar i.bi {
    display: block;
    margin-bottom: 10px; /* Optional: Add space between the icons */
}
  .search-bar input {
    width: 80%;
    padding: 10px;
    margin: 20px;
    border: none;
    background-color: white;
  }
  
  .user-list {
    background-color: black;
    padding: 20px;
  }
  
  </style>