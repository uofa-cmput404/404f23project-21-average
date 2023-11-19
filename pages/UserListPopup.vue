<template>
    <div class="popup" v-if="visible">
      <div class="popup-content">
        <span class="close" @click="close">&times;</span>
        <h3>{{ title }}</h3>
        <ul>
          <li v-for="user in users" :key="user.id">{{ user.name }}</li>
        </ul>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: {
      visible: Boolean,
      users: Array,
      title: String
    },
    methods: {
      close() {
        this.$emit('update:visible', false);
      }
    }
  }
  </script>
  
  <style scoped>
  /* Add your existing popup styles here */
  .popup {
  display: flex;
  position: fixed;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.6); /* Semi-transparent black background */
  justify-content: center;
  align-items: center;
  z-index: 10000; /* High z-index to make sure it's on top */
}

.popup-content {
  background-color: black; /* Black background for the content */
  color: white; /* White text */
  padding: 40px; /* Increased padding for more space inside */
  border-radius: 5px;
  width: 70%; /* Increase the width as needed */
  max-width: 400px; /* Adjust max-width as needed */
  min-height: 400px; /* Add a minimum height if needed */
  z-index: 10001; /* Ensure content is above the semi-transparent background */
  position: relative; /* Needed for absolute positioning of the close button */
  box-sizing: border-box; /* Ensure padding is included in width calculation */
  overflow-y: auto; /* Add scroll for content overflow */
  overflow-x: auto;
  align-items: center;
  text-align: center;

}
.popup-content h3 {
  font-size: 24px; /* Increase the font size as needed */
  color: white; /* Optional: specify the color if different from the default */
  margin-bottom: 20px; /* Optional: add some space below the heading */
  /* Additional styling like font-weight, letter-spacing, etc., can be added here */
}


.close {
  color: white;
  position: absolute;
  top: 0;
  right: 10px;
  font-size: 30px;
  font-weight: bold;
  cursor: pointer;
}

.close:hover {
  color: #ccc;
  text-decoration: none; /* Removes underline text on hover */
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  padding: 5px 0; /* Spacing between list items */
}

.close {
  position: absolute;
  top: 10px;
  right: 20px;
  cursor: pointer;
  font-size: 1.5em;
}
  </style>
  