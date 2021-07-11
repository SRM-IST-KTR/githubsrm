import axios from "axios";

const instance = axios.create({
  baseURL: `https://118524a5a0d0.ngrok.io/`,
});

export default instance;
