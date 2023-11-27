<template>
  <div class="app-container">
    <SidebarComponent/>
    <div class="main-content">
      <div class="header">INBOX</div>
      <div class="notification-list">
        <div v-for="(notification, index) in notifications" :key="notification.id" class="notification-item">
          <div class="notification-content">
            <div v-if="notification.type === 'post'">
              <h3>{{ notification.author.username }}</h3>
              <p>{{ notification.content }}</p>
            </div>
            <div v-if="notification.type === 'like'">
              <h3>{{ notification.summary }}</h3>
            </div>
            <div v-if="notification.type === 'follow'">
              <h3>{{ notification.summary }}</h3>
              <div class="button-group">
                <button @click="toggleAccept(index)">
                  {{ isAccepted ? 'Remove Follower' : 'Accept' }}
                </button>
              </div>
            </div>
            <div v-if="notification.type === 'comment'">
              <h3>{{ notification.author.username }} commented "{{ notification.comment }}" on your post</h3>
            </div>
          </div>
          <h4 v-if="notification.type === 'post'" class="notification-type">{{ notification.type.toUpperCase() }}</h4>
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
      isAccepted:false,
      foreignId: '',
    };
  },

  async created() {
    const authorStore = useAuthorStore();
    try {
      axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
      const response = await axios.get(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/inbox/?page_size=100`);

      this.notifications = response.data.items;
      console.log(this.notifications)
    } catch (error) {
      console.error('Error fetching inbox items:', error);
    }
  },
  methods: {

  async toggleAccept(index) {
      const notification = this.notifications[index];
      const authorStore = useAuthorStore();
      axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
      try {
        let response;
        if (this.isAccept) {
          // Call the unfollow API
          response = await axios.delete(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/followers/' + this.id + '/');
        } else {
          // Call the follow API
          response = await axios.post(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/followers/' + notification.object.id+ '/');
          console.log('Following', this.username);
        }
        if (!(response.status === 400 || response.status === 401)) {
          this.isFollowing = !this.isFollowing;
        }
      } catch (error) {
        console.error('Error while toggling follow:', error);
      }
    }}
};
</script>

<style scoped>
.app-container {
  display: flex;
  height: 100%;
  width: 100%;
  position: fixed;
  top: 0;
  bottom: 0;
  right: 0;
  background-color: black;
}

.main-content {
  position: fixed;
  left: 26%;
  top: 0;
  bottom: 0;
  right: 0;
  background-color: #00C58E;
  overflow-y: auto;
  overflow-x: hidden;
}

.header {
  color: black;  
  font-size: 30px;
  text-align: center;
  margin-top: 20px;
  margin-bottom: 20px;
  text-decoration: underline;
  font-weight: bolder;
}

.notification-list .notification-item {
  display: flex;
  justify-content: space-between;
  align-items: start;
  background-color: black;
  margin: 10px auto;
  padding: 15px;
  border-radius: 10px;
  color: white;
  border: 1px solid #00C58E;
}

.notification-content {
  flex-grow: 1;
}

.notification-type {
  text-align: right;
  /* Additional styling as needed */
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

 button {
  width: 100px;
  padding: 5px 15px;
  cursor: pointer;
  background-color: #00C58E;
  color: black;
  margin-right: 10px;
  /* Adds spacing between buttons */
}

button {
  margin-right: 0;
  /* Removes margin from the last button */
}
</style>
