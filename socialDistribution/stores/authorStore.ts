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
  },
  actions: {
    async setAuthorId(id: string) {
      this.authorId = id;
      localStorage.setItem("authorId", id);
    },
    async setAuthToken(token: string) {
      axios.defaults.headers.common["Authorization"] = `Token ${token}`;
      localStorage.setItem("token", token);
    },
    async fetchAuthor() {
      this.authorId = localStorage.getItem("authorId");
      localStorage.getItem("token");
      axios.defaults.headers.common[
        "Authorization"
      ] = `Token ${localStorage.getItem("token")}`;
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
