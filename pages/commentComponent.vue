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
      postid:"",
      commentid: ""
    };
  },
  async created() {
    await this.fetchComments();
  },
  methods: {
    async fetchComments() {
      console.log(this.postId)
      const authorStore = useAuthorStore();
      this.postid = await (authorStore.getIDFromURL(this.postId) )
      console.log(this.postid)
      try {
        axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
        console.log(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/posts/${this.postid}/comments/`)
        const response = await axios.get(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/posts/${this.postid}/comments/`);
        console.log(this.postid)
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
        this.postid = await (authorStore.getIDFromURL(this.postId) )
        console.log(this.postid)
        try {
          const payload = {
            comment: this.newComment,
            contentType: 'string',
          };
          axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
          await axios.post(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/posts/${this.postid}/comments/`, payload);
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
      this.commentid = await (authorStore.getIDFromURL(commentId) )
      try {
        axios.defaults.headers.common["Authorization"] = `Basic ${authorStore.getAuthToken}`;
        console.log(this.commentId)
        await axios.post(`${authorStore.BASE_URL}/authors/${authorStore.getAuthorId}/posts/${this.postid}/comments/${this.commentid}/likes/`);
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
  