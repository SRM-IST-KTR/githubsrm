import axios, { AxiosInstance, AxiosError } from "axios";

import {
  MemberProps,
  ProjectProps,
  ContributorFormData,
  NewMaintainerForm,
  ExistingMaintainerForm,
  ContactUsFormData,
} from "../utils/interfaces";
import { getRecaptchaToken } from "./recaptcha";
import { errToast } from "../utils/functions/toast";

const instance: AxiosInstance = axios.create({
  baseURL: `${
    process.env.NODE_ENV !== "production"
      ? process.env.NEXT_PUBLIC_API_BASE_URL
      : ""
  }/api`,
});

const staticInstance: AxiosInstance = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_API_BASE_STATIC}/api`,
});

export const getTeam = async (): Promise<MemberProps[] | false> => {
  try {
    return await (
      await staticInstance.get("/team")
    ).data;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const getProjects = async (): Promise<ProjectProps[] | false> => {
  try {
    return await (
      await instance.get("/maintainer")
    ).data;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postContributor = async (
  data: ContributorFormData
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    await instance.post("/contributor?role=contributor", data, {
      headers: {
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
    });
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postMaintainer = async (
  data: NewMaintainerForm | ExistingMaintainerForm,
  role: "alpha" | "beta"
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    await instance.post(`/maintainer?role=${role}`, data, {
      headers: {
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
    });
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postContactUs = async (
  data: ContactUsFormData
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    await instance.post("/contact-us", data, {
      headers: {
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
    });
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

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
