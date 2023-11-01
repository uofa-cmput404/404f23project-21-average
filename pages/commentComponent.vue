<template>
    <div class="comment-section">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <div class="comment-author">{{ comment.commenter }}</div>
        <div class="comment-content">{{ comment.comment }}</div>
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
    async mounted() {
    // this.fetchPosts();
    const authorStore = useAuthorStore();
    const response = await axios.get('http://127.0.0.1:8000/authors/' + authorStore.getAuthorId + '/posts/' + this.postId + '/comments/');
    this.comments = response.data.results;
  },
    methods: {
      async submitComment() {
        if (this.newComment.trim() !== '') {
            const authorStore = useAuthorStore();
      try {
        const payload = {
            comment: this.newComment,
            contentType: 'string', 
            published: new Date().toISOString(),
        };
        axios.defaults.headers.common["Authorization"] = `Bearer ${authorStore.getAuthToken}`;
        const response = await axios.post('http://127.0.0.1:8000/authors/' + authorStore.getAuthorId + '/posts/' + this.postId + '/comments/', payload);
          this.newComment = '';
        }
         catch (error) {
        console.error('Error while creating post:', error);
      }
    }
    },
    async created() {
    const authorStore = useAuthorStore();
    try {
      console.log(authorStore.authorId, authorStore.authToken)
      const response = await axios.get('http://127.0.0.1:8000/authors/' + authorStore.getAuthorId + '/posts/' + this.postId + '/comments/');
      console.log('http://127.0.0.1:8000/authors/' + authorStore.getAuthorId + '/posts/' + this.postId + '/comments/')
      // this.comments.push({
      //     author: response.data.commenter, 
      //     content: response.comment,
      //   });
    } catch (error) {
      console.error('Error while fetching posts:', error);
    }
  },
  }};
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
  