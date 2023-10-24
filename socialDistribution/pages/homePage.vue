<template>
    <div class="homepage-container">
      <SidebarComponent />
      <main class="homepage-main-content">
        <div class="posts-feed">
          <h2>Your Feed</h2>
          <!-- Here we loop through an array of posts and display each using the PostComponent -->
          <div v-for="post in posts" :key="post.id">
            <PostComponent :postContent="post.content"/>
          </div>
        </div>
      </main>
    </div>
  </template>
  
  <script>
  import PostComponent from './postComponent.vue';
  import SidebarComponent from './sidebar.vue';
  
  export default {
    name: "HomePage",
    components: {
      PostComponent,
      SidebarComponent
    },
    data() {
      return {
        // Sample posts data
        posts: [
          { id: 1, content: "User2's post content here" },
          { id: 2, content: "User3's post content here" },
          // ... add as many posts as you like
        ]
      };
    }
  };
  </script>
  
  <style scoped>
  .homepage-container {
    display: flex;
    width: 100%;
    height: 100%;
    position: fixed;
    top: 0;
    right: 0;
  }
  
  .homepage-main-content {
    position: fixed;
    left: 26%;
    top: 0;
    bottom: 0;
    right: 0;
    background-color: #00C58E;
    overflow-y: auto;
    overflow-x: hidden;
    padding: 20px;
  }
  
  .posts-feed {
    margin: 20px 0;
  }
  
  .posts-feed h2 {
    color: black;
    text-align: center;
    margin-bottom: 20px;
  }
  </style>
  