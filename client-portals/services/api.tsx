import axios from "axios";

const instance = axios.create({
  baseURL: `https://ac572f57a3a1.ngrok.io/`,
});

export default instance;
