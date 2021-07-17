import axios from "axios";
import { getRecaptchaToken } from "./recaptcha";
import {
  AdminLoginData,
  AdminRegisterData,
  MaintainerLoginData,
  ResetPasswordData,
  SetPasswordData,
} from "../utils/interfaces";
import { AxiosError } from "axios";
import { errToast } from "../utils/functions/toast";

const instance = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_API_BASE_URL}`,
});

export const postAcceptProjectHandler = async (
  project_id,
  isprivate,
  project_url
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const token = sessionStorage.getItem("token");
    await instance.post(
      `admin/projects?projectId=${project_id}&role=project`,
      {
        project_id: project_id,
        private: isprivate,
        project_url: project_url,
      },
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "X-RECAPTCHA-TOKEN": recaptchaToken,
        },
      }
    );
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postAdminLogin = async (
  values: AdminLoginData
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const res = await instance.post("/admin/login", values, {
      headers: {
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
    });
    sessionStorage.setItem("token", res.data.keys);
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postAdminRegister = async (
  values: AdminRegisterData,
  authToken
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const res = await instance.post("/admin/register", values, {
      headers: {
        Authorization: `Bearer ${authToken}`,
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
    });
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const getAcceptedProjects = async (pageNo, token): Promise<Object> => {
  try {
    return await (
      await instance.get(`admin/projects/accepted?page=${pageNo}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
    ).data;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postMaintainerLogin = async (
  values: MaintainerLoginData
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const res = await instance.post("maintainer/login", values, {
      headers: {
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
    });
    sessionStorage.setItem("token", res.data.key);
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postResetPassword = async (
  values: ResetPasswordData
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const res = await instance.post("maintainer/reset-password/reset", values, {
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

export const postSetPassword = async (
  values: SetPasswordData,
  queryToken
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const res = await instance.post("maintainer/reset-password/set", values, {
      headers: {
        "X-RECAPTCHA-TOKEN": recaptchaToken,
        Authorization: `Bearer ${queryToken}`,
      },
    });
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postAcceptContributor = async (
  project_id,
  contributor_id
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const token = sessionStorage.getItem("token");
    await instance.post(
      "maintainer/projects?role=contributor",
      { project_id: project_id, contributor_id: contributor_id },
      {
        headers: {
          Authorization: `Bearer ${token}`,
          "X-RECAPTCHA-TOKEN": recaptchaToken,
        },
      }
    );
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
        errMessage = "Unauthorized.";
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

export default instance;
