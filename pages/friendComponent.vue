<template>
  <div class="friend-component">
    <span class="author-name">{{ id }}</span>
    <div class="button-group">
      <button @click="toggleFollow">
        {{ isFollowing ? 'Unfollow' : 'Follow' }}
      </button>
      <button @click="toggleFriendship">
        {{ isFriend ? 'Remove Friend' : 'Add Friend' }}
      </button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  props: {
    id: {
      type: String,
      default: ''
    },
    username: {
      type: String,
      default: ''
    },
    // ... other props
  },
  data() {
    return {
      isFollowing: false, // Assuming default state is not following
      isFriend: false, // Assuming default state is not a friend
    };
  },
  methods: {
    async toggleFollow() {
      if (this.isFollowing) {
        // Implement logic to unfollow
        console.log(`Unfollowing ${this.username}`);
      } else {
        const authorStore = useAuthorStore();
        const response = await axios.put(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/followers/' + this.id + '/');
        console.log(`Following ${this.username}`);
      }
      this.isFollowing = !this.isFollowing;
    },
    toggleFriendship() {
      if (this.isFriend) {
        // Implement logic to remove friend
        console.log(`Removing ${this.username} as a friend`);
      } else {
        // Implement logic to add as friend
        console.log(`Adding ${this.username} as a friend`);
      }
      this.isFriend = !this.isFriend;
    },
  },
};
</script>
<style scoped>
.friend-component {
  width: 80%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px;
  margin-bottom: 20px;
  background-color: black;
  color: white;
  border-radius: 5px;
}

.author-name {
  margin-left: 20px;
}

.button-group button {
  width: 100px;
  padding: 5px 15px;
  cursor: pointer;
  background-color: #00C58E;
  color: black;
  margin-right: 10px; /* Adds spacing between buttons */
}

.button-group button:last-child {
  margin-right: 0; /* Removes margin from the last button */
}
</style>
