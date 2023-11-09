<!-- SearchPage.vue -->
<template>
  <div class="app-container">
    <SidebarComponent/>
    <main class="main-content">
      <div class="search-bar">
        <input type="text" placeholder="Search for friends" v-model="searchQuery" @input="searchFriends"/>
      </div>
      <div class="user-list">
        <FriendComponent
          v-for="friend in filteredFriends"
          :id="friend.id"
          :username="friend.username"
          :fs = "friends.first_name"
          :ls = "friends.last_name"
        />
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
    const response = await axios.get(authorStore.BASE_URL + '/authors/');
    this.filteredFriends = response.data.results;
    console.log(this.filteredFriends)
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
  
  .search-bar input {
    width: 80%;
    padding: 10px;
    margin: 20px;
    border: none;
    background-color: white;
  }
  
  .user-list {
    padding: 20px;
    width: 80%;
    margin-left: auto;
    margin-right: auto;
  }
  
</style>
