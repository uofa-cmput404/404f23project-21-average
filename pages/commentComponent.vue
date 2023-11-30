<template>
  <div class="comment-section">
    <div v-for="comment in comments" :key="comment.id" class="comment">
      <div class="comment-author">{{ comment.author.username }}</div>
      <div class="comment-content">{{ comment.comment }}</div>
      <div class="comment-actions">
        <button @click="likeComment(comment.id)">Like</button>
      </div>
    </div>

    <div class="add-comment">
      <textarea v-model="newComment" placeholder="Add a comment"></textarea>
      <button @click="submitComment">Submit</button>
    </div>
  </div>
</template>

  
<script>
import { useAuthorStore } from '../stores/authorStore';
import axios from 'axios'

export default {
  props: {
    postId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      comments: [],
      newComment: '',
    };
  },
  async created() {
    await this.fetchComments();
  },
  methods: {
    async fetchComments() {
      const authorStore = useAuthorStore();
      try {
        axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
        const response = await axios.get(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/posts/${this.postId}/comments/`);
        console.log('40', response.data)
        this.comments = response.data.items;
        console.log("jjkkkjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")
        console.log(response.data.items[0].id)
      } catch (error) {
        console.error('Error while fetching comments:', error);
      }
    },
    async submitComment() {
      if (this.newComment.trim() !== '') {
        const authorStore = useAuthorStore();
        try {
          const payload = {
            comment: this.newComment,
            contentType: 'string',
          };
          axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
          await axios.post(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/posts/${this.postId}/comments/`, payload);
          console.log(payload)
          this.newComment = '';
          await this.fetchComments(); // Fetch comments again to update the list
        }
        catch (error) {
          console.error('Error while creating comment:', error);
        }
      }
    },

    async likeComment(commentId) {
      const authorStore = useAuthorStore();
      try {
        axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
        await axios.post(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/posts/${this.postId}/comments/${commentId}/likes/`);
        await this.fetchComments(); // Update comments to reflect new like count
      } catch (error) {
        console.error('Error while liking comment:', error);
      }
    },
  }
};
</script>

  
<style>
.comment-section {
  border-top: 1px solid #ccc;
  padding-top: 10px;
}

.comment {
  padding: 10px;
  border-bottom: 1px solid #eee;
}

.comment-author {
  font-weight: bold;
  margin-bottom: 5px;
}

.add-comment {
  margin-top: 10px;
}

textarea {
  width: 100%;
  height: 60px;
  margin-bottom: 10px;
}

button {
  background-color: #00C58E;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
  border-radius: 3px;
}

button:hover {
  background-color: #009966;
}
</style>
  