<!-- SearchPage.vue -->
<template>
  <div class="app-container">
    <SidebarComponent />
    <main class="main-content">
      <div class="search-bar">
        <input type="text" placeholder="Search for friends" v-model="searchQuery" @input="searchFriends" />
      </div>

      <div class="user-list">
        <FriendComponent v-for="friend in filteredFriends" :key="friend.id" :id="friend.id" :username="friend.username"
          :fs="friend.first_name" :ls="friend.last_name" @onFriendClick="redirectToProfile" />
      </div>


    </main>
  </div>
</template>

<script>
import axios from 'axios'
import SidebarComponent from './sidebar.vue';
import FriendComponent from './friendComponent.vue';

export default {
  name: "SearchPage",
  components: {
    SidebarComponent,
    FriendComponent,
  },
  data() {
    return {
      searchQuery: '',
      friends: [], // This will hold the list of friends fetched from the server
      filteredFriends: [],
    };
  },

  async created() {
    const authorStore = useAuthorStore();
    try {
      console.log(`Basic ${authorStore.getAuthToken}`)
      axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
      const response = await axios.get(authorStore.BASE_URL + '/authors/?page_size=100');
      this.friends = response.data.results; // Save the data in friends
      console.log("heyyyy")
      // console.log(this.friends)
      // for (friend in this.friends) {
      //   if (friend.userId === authorStore.getAuthorId)
      //   this.friends.push(friend)
      // }

      this.filteredFriends = [...this.friends]; // Initialize filteredFriends
    } catch (error) {
      console.error('Error fetching friends:', error);
    }
  },


  methods: {
    searchFriends() {
      // Implement the search logic here
      // This might involve filtering the `friends` array based on `searchQuery`
      this.filteredFriends = this.friends.filter(friend =>
        friend.username.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
    fetchFriends() {
      // Fetch the list of friends from the server
      // For example, using axios:
      // axios.get('/api/friends').then(response => {
      //   this.friends = response.data;
      //   this.filteredFriends = response.data;
      // });
    },


  },

};
</script>

<style scoped>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box; /* Ensures padding does not affect overall width */
}

.app-container {
  display: flex;
  width: 100%;
  height: 100vh;
  position: relative;
  background-color: #00C58E;
  color: white;
}

.main-content {
  flex-grow: 1;
  overflow-y: auto;
  background-color: #00C58E;
  padding-left: 26%; /* Adjust based on your sidebar width */
}

.search-bar {
  padding-top: 15px;
  width: 70%;
  margin: 0 auto;
  display: flex;
  justify-content: center; /* Center the search bar horizontally */
}

.search-bar input {
  width: 100%;
  padding: 10px;
  border: none;
  background-color: white;
}

.user-list {
  padding: 20px;
  width: 70%;
  margin: 0 auto;
}
</style>
