import 'bootstrap-icons/font/bootstrap-icons.css';
<template>
    <div class="app-container">
      <aside class="sidebar">
        <h1 class="app-title">
          <div class="title-social">SOCIAL</div>
          <div class="title-distribution">DISTRIBUTION</div>
        </h1>
        <i class="bi bi-house" id="home-icon"></i>
        <i class="bi bi-people" id = "friends" ></i>
        <i class="bi bi-search" id="search-icon"></i>
        <i class="bi bi-person" id="profile-icon"></i>
      </aside>
      <main class="main-content">
        <div class="search-bar">
          <input type="text" placeholder="Search for friends" />
        </div>
  
      </main>
    </div>
  </template>
  
  <script>
  import 'bootstrap-icons/font/bootstrap-icons.css';
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
  
  
  
  .main-content {
    width: 80%;
    background-color: #00C58E;
  }
  
  .bi{
    font-size: 60px;
    margin-left:20px;

  }

  .sidebar i.bi {
    display: block;
    margin-bottom: 40px; /* Optional: Add space between the icons */
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