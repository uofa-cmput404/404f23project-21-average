<template>
  <div id="app">
    <div class="container">
      <div class="heading">
        <h1soc>SOCIAL<br></h1soc>
        <h1dis>DISTRIBUTION</h1dis>
      </div>

      <div class="login-box">
        <h2>LOGIN</h2>
        <form>
          <div class="input-group">
            <label for="user-id">User ID</label>
            <input type="text" id="user-id" v-model="userId" placeholder="User ID" />
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" placeholder="Password" />
          </div>
          <button type="button" v-on:click="login">SUBMIT</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import axios from "axios";
import { ref } from "vue";
const csrfToken = 'your-csrf-token-here';

const userId = ref('');
const password = ref('');

const login = async () => {
  try {
    const data = {
      username: userId.value,
      password: password.value
    };

    const response = await axios.post('http://127.0.0.1:8000/api/auth/login/', data)
    if (response.status === 200 || response.status === 201) {
      // Handle successful login
      console.log("Login successful!");
      console.log(response)
      window.location.href = "http://localhost:3000/homePage";
      // Redirect or perform other actions
    } else {
      // Handle login failure
      console.error("Login failed:", response.data.error);
    }
  } catch (error) {
    // Handle errors (e.g., network issues)
    console.error("Error during login:", error);
  }
}
</script>

<style scoped>
#app {
  font-family: 'Arial', sans-serif;
  background-color: #000;
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
}

.heading {
  text-align: left;
  position: absolute;
  top: 20px;
  left: 25px;
}

.container {
  text-align: center;
  color: #fff;
}

.login-box {
  background-color: #333;
  padding: 20px;
  border-radius: 10px;
  width: 450px;
  height: 450px;
  margin: 0 auto;
}

h1soc,
h1dis {
  font-size: 55px;
  margin-bottom: 30px;
  color: #00C58E;
  font-family: Montserrat;
}

h2 {
  font-size: 35px;
  margin-bottom: 20px;
}

.input-group {

  margin: 10px 0;
  text-align: left;
  margin-right: 17px;
}

label {
  display: block;
  margin-bottom: 20px;
  color: #aaa;
}

input {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 5px;
  background-color: #eee;
}

button {
  font-size: 40;
  margin-top: 20px;
  padding: 20px 35px;
  background-color: #00C58E;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background-color: #45a049;
}
</style>
  