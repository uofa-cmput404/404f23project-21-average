import { d as defineStore } from "../server.mjs";
import axios from "axios";
const useAuthorStore = defineStore({
  id: "author",
  state: () => ({
    authorId: "",
    author: null,
    authToken: ""
  }),
  getters: {
    getAuthorId() {
      return localStorage.getItem("authorId");
    },
    getAuthToken() {
      return localStorage.getItem("token");
    }
  },
  actions: {
    async setAuthorId(id) {
      this.authorId = id;
      localStorage.setItem("authorId", id);
    },
    async setAuthToken(token) {
      axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      this.authToken = token;
      localStorage.setItem("token", token);
    },
    async fetchAuthor() {
      axios.defaults.headers.common["Authorization"] = `Bearer ${localStorage.getItem("token")}`;
      try {
        const response = await axios.get(`http://127.0.0.1:8000/authors`);
        console.log(response.data);
        this.author = response.data.results[0];
        this.authorId = response.data.results[0].id;
      } catch (error) {
        console.error(error);
      }
    }
  }
});
export {
  useAuthorStore as u
};
//# sourceMappingURL=authorStore-171782f1.js.map
