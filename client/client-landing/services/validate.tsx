import axios, { AxiosInstance } from "axios";

const instance: AxiosInstance = axios.create({
  baseURL: "https://api.github.com",
});

export const getUser = async (id: string): Promise<boolean> => {
  try {
    const { data } = await instance.get(`/users/${id}`); 
    if (data.type === "User")
      return true;
    return false;
  } catch (error) {
    return false;
  }
};

export const getRepo = async (org: string, id: string): Promise<boolean> => {
  try {
    await instance.get(`/repos/${org}/${id}`);
    return true;
  } catch (error) {
    return false;
  }
};
