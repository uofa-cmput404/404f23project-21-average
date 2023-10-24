<!-- PostComponent.vue -->
<template>
  <div class="post">
      <div class="user-info">
          <img :src="profilePicture" alt="User Profile Picture" class="profile-pic"/>
          <span class="user-id">{{ userId }}</span>
      </div>
      <p>{{ postContent }}</p>
      <div class="post-actions">
          <button @click="toggleLike">{{ liked ? 'Unlike' : 'Like' }}</button>
          <button @click="toggleCommentBox">Comment</button>
          <button>Edit</button>
      </div>
      <div v-if="showCommentBox">
          <textarea placeholder="Write a comment"></textarea>
          <button @click="toggleCommentBox">Post Comment</button>
      </div>
  </div>
</template>

<script>
export default {
  props: {
    postContent: String,
    profilePicture: { 
      type: String,
      default: ''  // You can set a default image URL if you like
    },
    userId: String
  },
  data() {
    return {
      liked: false,
      showCommentBox: false
    };
  },
  methods: {
    toggleLike() {
      this.liked = !this.liked;
    },
    toggleCommentBox() {
      this.showCommentBox = !this.showCommentBox;
    }
  }
};
</script>

<style scoped>
.post {
  background-color: black;
  padding: 20px;
  width: 80%;
  margin: auto;
  color: white;
  margin-bottom: 20px;
  border-radius: 5px;
  position: relative;
}

.post-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

button {
  background-color: #00C58E;
  color: black;
  padding: 5px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #007744;
}

textarea{
  background-color: grey;
  color: white;
}

.user-info {
  position: absolute;
  top: 10px;
  left: 10px;
  display: flex;
  align-items: center;
}

.profile-pic {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  object-fit: cover;
  margin-right: 5px;
}

.user-id {
  color: #00C58E;
}
</style>
