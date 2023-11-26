<template>
  <div class="app-container">
    <SidebarComponent/>
    <div class="main-content">
      <div class="header">INBOX</div>
      <div class="notification-list">
        <div v-for="notification in notifications" :key="notification.id" class="notification-item">
          <div v-if="notification.type ==='post'">
          <h3>{{ notification.type }}</h3>
          <h3>{{ notification.author.username }}</h3>
          <p>{{ notification.content }}</p>
        </div>
          <div v-if="notification.type === 'like'">
            <h3>{{ notification.author }} liked your post</h3>
            </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import SidebarComponent from './sidebar.vue';

export default {
  name: "InboxApp",
  components: {
    SidebarComponent
  },
  data() {
    return {
      notifications: [], // This will hold the fetched notifications
      likes:[]
    };
  },

  async created() {
    const authorStore = useAuthorStore();
    try {
      axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
      const response = await axios.get(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/inbox/?page_size=100`);

      // Assuming the response data is an array of notifications
      this.notifications = response.data.items;
      console.log(this.notifications)
    } catch (error) {
      console.error('Error fetching inbox items:', error);
    }
  }
};
</script>

  
  <style scoped>
  .app-container {
    display: flex;
    height: 100%;
    width:100%;
    position:fixed;
    top:0;
    bottom:0;
    right:0;
    background-color: black;
  }

.main-content {
    position:fixed;
    left:26%;
    top:0;
    bottom:0;
    right:0;
    background-color: #00C58E;
    overflow-y: auto;
    overflow-x:hidden;
  }
  
  .header {
  color: black;  
  font-size: 30px;  /* Corrected the font size value */
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
  text-decoration: underline; /* Underlining the text */
  font-weight: bolder; /* Making the text bold */
}

  
  .notification-list .notification-item {
  background-color: black;
  margin: 10px auto;
  padding: 15px;
  border-radius: 10px;
  color: white;
  border: 1px solid #00C58E;
}

.notification-list .notification-item h3 {
  margin: 0;
  color: #009B75;
}

.notification-list .notification-item p {
  margin: 5px 0;
}

.notification-list .notification-item button {
  background-color: #00C58E;
  color: white;
  border: none;
  cursor: pointer;
  padding: 10px 20px;
  border-radius: 5px;
}

.notification-list .notification-item button:hover {
  background-color: #009B75;
  color: white;
}

</style>