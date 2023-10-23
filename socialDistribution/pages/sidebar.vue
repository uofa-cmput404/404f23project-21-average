<!-- Sidebar.vue -->
<template>
    <aside class="sidebar">
      <h1 class="app-title">
        <div class="title-social">SOCIAL</div>
        <div class="title-distribution">DISTRIBUTION</div>
      </h1>
      <i class="bi bi-house" id="home-icon"></i>
      <li><NuxtLink to="/friendsPage"><i class="bi bi-people" id="friends"></i></NuxtLink></li>
      <li><NuxtLink to="/searchPage"><i class="bi bi-search" id="search-icon"></i></NuxtLink></li>
      <li><NuxtLink to="/profilePage"><i class="bi bi-person" id="profile-icon"></i></NuxtLink></li>
    </aside>
  </template>
  
  <script>
  import 'bootstrap-icons/font/bootstrap-icons.css';
  
  export default {
    name: "SidebarComponent"
  };
  </script>
  
  <style scoped>
  .sidebar {
    width: 24%;
    height:100%;
    padding: 20px;
    background-color: black;
    color: #00C58E;
    position:fixed;
    top:0;
    left:0;
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
    margin-bottom: 10px; /* Optional: Add space between the icons */
}
nuxt-link > a:visited,
nuxt-link:visited,
nuxt-link > a:visited .bi,
nuxt-link:visited .bi {
  color: inherit !important; /* Using !important to ensure override */
}
  </style>
  