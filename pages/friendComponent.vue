<!-- FriendComponent.vue -->
<template>
    <div class="friend-component">
      <span class="author-name">{{username }}</span>
      <button @click="followUser">Follow</button>
    </div>
  </template>
  
  <script>

  export default {
    props: {
        id:{
            type:String,
            default: ''
        },
        username:{
            type:String,
            default:''
        },
        fs:{
            type:String,
            default:''
        },
        ls:{
            type:String,
            default:''
        }
    },
    methods: {
      followUser() {
        // Implement follow user logic here
        // This might involve making an API call to your server
        console.log(`Following ${this.username}`);
      },
    },
  };
  </script>
  
  <style scoped>
  .friend-component {
    width:80%;
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
  
  button {
    width:100px;
    padding: 5px 15px;
    cursor: pointer;
    background-color: #00C58E;
    color: black;
  }
  </style>
  