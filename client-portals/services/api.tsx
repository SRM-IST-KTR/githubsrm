import axios, { AxiosInstance, AxiosError } from "axios";

import { errToast } from "../utils/functions/toast";

const instance: AxiosInstance = axios.create({
  baseURL: `${
    process.env.NODE_ENV !== "production"
      ? process.env.NEXT_PUBLIC_API_BASE_URL
      : ""
  }/api`,
});

export const errorHandler = (err?: AxiosError | any) => {
  let errMessage: string = "Oops! Something went wrong.";
  if (err) {
    switch (err.response?.status) {
      case 400:
        errMessage = "Kindly check your inputs.";
        break;
      case 401:
        errMessage = "Recaptcha Invalid. Try again later.";
        break;
      case 403:
        errMessage = "Forbidden.";
        break;
      case 409:
        errMessage = "Artifact already exists.";
        break;
      case 500:
        errMessage = "Internal server error.";
        break;
      default:
        errMessage = "Oops! Something went wrong.";
        break;
    }
  }

  errToast(errMessage);
};
