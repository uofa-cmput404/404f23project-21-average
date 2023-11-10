import { defineStore } from "pinia";
import axios from "axios";

export const useAuthorStore = defineStore({
  id: "author",
  state: () => ({
    authorId: "",
    author: null,
    authToken: "",
    BASE_URL: "http://127.0.0.1/api",
  }),
  getters: {
    getAuthorId() {
      return localStorage.getItem("authorId");
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
      this.authToken = token;
      localStorage.setItem("token", token);
    },
  },
});
