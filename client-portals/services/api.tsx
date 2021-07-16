import axios from "axios";

const instance = axios.create({
  baseURL: `https://dev.githubsrm.tech`,
});

export default instance;
