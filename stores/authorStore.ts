import { defineStore } from "pinia";
import axios from "axios";

export const useAuthorStore = defineStore({
  id: "author",
  state: () => ({
    authorId: "",
    author: null,
    authToken: "",
    BASE_URL: "https://avergae-21-b951939c31ad.herokuapp.com",
  }),
  getters: {},
  actions: {
    getAuthorId() {
      return localStorage.getItem("authorId");
    },
    getAuthToken() {
      return localStorage.getItem("token");
    },
    async setAuthorId(id: string) {
      this.authorId = id;
      localStorage.setItem("authorId", id);
    },
    async setAuthToken(token: string) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      this.authToken = token;
      localStorage.setItem("token", token);
    },
    async fetchAuthor() {
      // this.authorId = localStorage.getItem("authorId");
      axios.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${localStorage.getItem("token")}`;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/authors`);
        console.log(response.data);
        this.author = response.data.results[0];
        this.authorId = response.data.results[0].id;
      } catch (error) {
        console.error(error);
      }
    },
  },
});
