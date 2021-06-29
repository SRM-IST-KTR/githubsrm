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
import { errorHandler } from "../utils/functions/toast";

const instance: AxiosInstance = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_API_BASE_URL}/api`,
});

export const getTeam = async (): Promise<MemberProps[] | false> => {
  try {
    return await (
      await instance.get("/team")
    ).data;
  } catch (error) {
    console.log(error);
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
    console.log(error);
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
    console.log(error.response as AxiosError);
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
    console.log(error.response as AxiosError);
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
    console.log(error.response as AxiosError);
    return false;
  }
};
