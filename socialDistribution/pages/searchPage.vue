<template>
    <div class="app-container">
      <aside class="sidebar">
        <h1 class="app-title">
          <div class="title-social">SOCIAL</div>
          <div class="title-distribution">DISTRIBUTION</div>
        </h1>
        <div class="icon" id="home-icon"></div>
        <div class="icon" id="group-icon"></div>
        <div class="icon" id="search-icon"></div>
        <div class="icon" id="profile-icon"></div>
      </aside>
      <main class="main-content">
        <div class="search-bar">
          <input type="text" placeholder="Search for a user" />
        </div>
  
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: "SocialDistributionApp"
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
  
  .icon {
    margin-left:10%;
    height: 40px;
    width: 40px;
    margin-bottom: 70px;
    background-color: #00C58E;
    /* This is just a placeholder shape; you'll replace these with your actual icons */
    clip-path: polygon(50% 0%, 0% 100%, 100% 100%);
  }
  
  .main-content {
    width: 80%;
    background-color: #00C58E;
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