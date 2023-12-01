<template>
  <div class="friend-component">
    <span class="author-name">{{ username }}</span>
    <div class="button-group">
      <button @click="toggleFollow">
        {{ isFollowing ? 'Unfollow' : 'Follow' }}
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
    host: {
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
  async created() {
    await this.checkFollowingStatus();
  },

  methods: {

    async checkFollowingStatus() {
      const authorStore = useAuthorStore();
      try {
        axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
        const response = await axios.get(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/followers/' + this.id.split('/').pop() + '/');
        if (!(response.status === 400 || response.status === 401 || response.status === 500)) {
          this.isFollowing = response.data;
          console.log(this.isFollowing)
        }
      } catch (error) {
        console.error('Error while checking following status:', error);
      }
    },

    async toggleFollow() {
      const authorStore = useAuthorStore();
      axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
      try {
        let response;
        if (this.isFollowing) {
          // Call the unfollow API
          response = await axios.delete(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/followers/' + this.id.split('/').pop() + '/');
          console.log('Unfollowing', this.username);
        } else {
          // Call the follow API
          response = await axios.put(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/followers/' + this.id.split('/').pop() + '/',
            { objectHost: this.host });
          console.log('Following', this.username);
        }
        if (!(response.status === 400 || response.status === 401)) {
          this.isFollowing = !this.isFollowing;
        }
      } catch (error) {
        console.error('Error while toggling follow:', error);
      }
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
  margin-right: 10px;
  /* Adds spacing between buttons */
}

.button-group button:last-child {
  margin-right: 0;
  /* Removes margin from the last button */
}
</style>
