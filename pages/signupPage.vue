<template>
  <div id="app">
    <div class="container">
      <div class="heading">
        <h1soc>SOCIAL<br></h1soc>
        <h1dis>DISTRIBUTION</h1dis>
      </div>

      <div class="registration-box">
        <h2>REGISTER</h2>
        <form>
          <div class="input-group">
          <label for="first_name">First Name</label>
          <input type="text" id="first_name" v-model="firstName" placeholder="First Name" />
        </div>
        <div class="input-group">
          <label for="last_name">Last Name</label>
          <input type="text" id="last_name" v-model="lastName" placeholder="Last Name" />
        </div>
          <div class="input-group">
            <label for="email">Email</label>
            <input type="email" id="email" v-model="email" placeholder="Email" />
          </div>
          <div class="input-group">
            <label for="username">Username</label>
            <input type="text" id="username" v-model="username" placeholder="Username" />
          </div>
          <div class="input-group">
            <label for="password">Password</label>
            <input type="password" id="password" v-model="password" placeholder="Password" />
            <div class="input-group">
          <label for="github_id">GitHub ID (Optional)</label>
          <input type="text" id="github_id" v-model="githubId" placeholder="GitHub ID" />
        </div>
          </div>
          <button type="button" @click="register();">SIGN UP</button>
        </form>
      </div>
    </div>
  </div>
</template>
  
<script lang="ts" setup>
import axios from "axios";
import { ref } from "vue";
import { useAuthorStore } from "../stores/authorStore";

const authorStore = useAuthorStore();
const email = ref('')
const username = ref('')
const password = ref('')
const firstName = ref('')
const lastName = ref('')
const githubId = ref('')
const register = async () => {

  try {
    const data = {
      email: email.value,
      username: username.value,
      password1: password.value,
      password2: password.value,
      first_name: firstName.value,
      last_name: lastName.value,
      github_id: githubId.value 
    }
    try {
      console.log(data)
      const response = await axios.post(authorStore.BASE_URL + '/api/auth/register/', data)
      // axios.defaults.headers.common['Authorization'] = 'Token ' + response.data.key;
      await authorStore.setAuthToken(response.data.access)
      await authorStore.setAuthorId(response.data.user.pk)
      window.location.href = "/homePage";
    } catch (error) {
      console.log(error)
    }
  } catch (error) {
    // Handle errors (e.g., network issues or validation issues)
    console.error("Error during registration:", error);
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

.registration-box {
  background-color: #333;
  padding: 20px;
  border-radius: 10px;
  width: 500px;
  height: auto;
  /* Increased the height to accommodate the additional input field */
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
  