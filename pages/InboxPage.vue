<template>
  <div class="app-container">
    <SidebarComponent />
    <div class="main-content">
      <div class="header-container">
        <div class="header">INBOX</div>
        <button class="clear-inbox-button" @click="clearInbox">Clear Inbox</button>
        <div class="notification-list">
          <div v-for="(notification, index) in notifications" :key="notification.id" class="notification-item">
            <div class="notification-content">
              <div v-if="notification.type.toLowerCase() === 'post'">
                <PostComponent :key="notification.id" :postContent="notification.content"
                  :userId="notification.author.username" :postImage="notification.image" :postID="notification.id"
                  :isPublic="notification.visibility" :contentType="notification.contentType" />
              </div>
              <div v-if="notification.type.toLowerCase() === 'like'">
                <h3>{{ notification.summary }}</h3>
              </div>
              <div v-if="notification.type.toLowerCase() === 'follow'">
                <h3>{{ notification.summary }}</h3>
                <div class="button-group">
                  <button @click="toggleAccept(notification, index)">
                    {{ notification.isFollower ? 'Remove Follower' : 'Accept' }}
                  </button>
                </div>
              </div>
              <div v-if="notification.type.toLowerCase() === 'comment'">
                <h3>{{ notification.author.username }} commented "{{ notification.comment }}" on your post</h3>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import SidebarComponent from './sidebar.vue';
import PostComponent from './postComponent.vue'

export default {
  name: "InboxApp",
  components: {
    SidebarComponent,
    PostComponent
  },
  data() {
    return {
      notifications: [], // This will hold the fetched notifications
      isAccepted: false,
      foreignId: '',
      isAFollower: false
    };
  },

  async created() {
    const authorStore = useAuthorStore();
    try {
      axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
      const response = await axios.get(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/inbox/?size=100`);

      this.notifications = response.data.items;
      console.log(this.notifications)
    } catch (error) {
      console.error('Error fetching inbox items:', error);
    }
    this.checkFollower(this.notifications)
    console.log(this.isAFollower)
  },
  methods: {

    async checkFollower(notifications) {
      const authorStore = useAuthorStore();
      axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;

      for (let notification of notifications) {
        if (notification.type.toLowerCase() === 'follow') {
          let response = await axios.get(authorStore.BASE_URL + '/authors/' + await authorStore.getIDFromURL(notification.object.id) + '/followers/' + authorStore.getAuthorId + '/');
          notification.isFollower = response.data === true;
          console.log(response.data, notification, response.url)
        }
      }
    },


    async toggleAccept(notification, index) {
      const authorStore = useAuthorStore();
      axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
      try {
        let response;
        console.log(this.isAFollower)
        if (notification.isFollower) {
          // Call the unfollow API
          response = await axios.delete(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/followers/' + await authorStore.getIDFromURL(notification.object.id) + '/');
        } else {
          // Call the follow API
          response = await axios.post(authorStore.BASE_URL + '/authors/' + authorStore.getAuthorId + '/followers/' + await authorStore.getIDFromURL(notification.object.id) + '/');
        }
        if (response && (response.status === 200 || response.status === 204)) {
          this.notifications[index].isFollower = !this.notifications[index].isFollower;
        }
      } catch (error) {
        console.error('Error while toggling follow:', error);
      }
    },
    async clearInbox() {
      // Logic to clear the inbox
      // Example: Send a request to the backend to clear the inbox
      try {
        const authorStore = useAuthorStore();
        axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
        const response = await axios.delete(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/inbox/`);
        if (response.status === 200) {
          // Clear the notifications in the local state
          this.notifications = [];
        }
      } catch (error) {
        console.error('Error clearing inbox:', error);
      }
    },
  },
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

.header-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  /* Adjust as needed */
}

.header {
  color: black;
  font-size: 30px;
  text-align: center;
  text-decoration: underline;
  font-weight: bolder;
}

.clear-inbox-button {
  width: 80%;
  background-color: #f44336;
  /* Red color for clear action */
  color: white;
  border: none;
  padding: 5px 10px;
  border-radius: 4px;
  cursor: pointer;
}

.clear-inbox-button:hover {
  background-color: #d32f2f;
  /* Darker shade on hover */
}

.header-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
