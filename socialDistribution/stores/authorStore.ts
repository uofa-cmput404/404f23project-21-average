import { defineStore } from "pinia";
import axios from "axios";

export const useAuthorStore = defineStore({
  id: "author",
  state: () => ({
    authorId: "",
    author: null,
  }),
  getters: {
    getAuthorId() {
      return this.authorId;
    },
    getAuthToken() {
      return localStorage.getItem("token");
    },
  },
  actions: {
    async setAuthorId(id: string) {
      this.authorId = id;
      localStorage.setItem("authorId", id);
    },
    async setAuthToken(token: string) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      localStorage.setItem("token", token);
    },
    async fetchAuthor() {
      this.authorId = localStorage.getItem("authorId");
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
