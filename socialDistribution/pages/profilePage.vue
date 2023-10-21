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
      <div class="user-section">
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
          <h3>Posts:</h3>
          <div class="post">Something written</div>
          <div class="post">Something written</div>
          <div class="post">Something written</div>
        </div>
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
  display: flex;
  width:100%;
  height:100%;
  position:fixed;
  top:0;
  right:0;
}

.sidebar {
  width: 24%;
  padding: 20px;
  background-color: black;
  color: #00C58E;
}

.app-title {
  font-size: 40px;
  margin-bottom: 50px;
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
  width: 80%;
  background-color: #00C58E;
  padding: 20px;
  overflow-y: auto;
}

.user-section h2 {
  color: black;
  margin-bottom: 20px;
}

.follow-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  color: black;
}

.bio-section textarea {
  width: 100%;
  padding: 10px;
  border: none;
  background-color: black;
  color: white;
  margin-bottom: 20px;
}
.posts-section h3 {
  color: black;
  margin-bottom: 10px;
}

.post {
  background-color: black;
  padding: 60px;
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
}

.edit{
    margin-left: 46%;
    margin-right: 50%;
}
</style>
