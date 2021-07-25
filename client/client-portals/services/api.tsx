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
import { errToast, successToast } from "../utils/functions/toast";
import router from "next/router";

const instance = (auth: boolean = true) => {
  if (!auth) {
    return axios.create({
      baseURL: `${process.env.NEXT_PUBLIC_API_BASE_URL}`,
    });
  }
  const authToken = sessionStorage.getItem("token");
  const refreshToken = sessionStorage.getItem("refreshToken");
  axios
    .get(`${process.env.NEXT_PUBLIC_API_BASE_URL}/me`, {
      headers: {
        Authorization: `Bearer ${authToken}`,
      },
    })
    .then((res) => {
      if (res.data.success) {
        successToast("/me sucess");
      }
    })
    .catch((err) => {
      axios
        .post(`${process.env.NEXT_PUBLIC_API_BASE_URL}/refresh-token`, {
          headers: {
            Authorization: `Bearer ${refreshToken}`,
          },
        })
        .then((res) => {
          successToast("/refresh sucess");
          sessionStorage.setItem("token", res.data.access_token);
          sessionStorage.setItem("refreshToken", res.data.refresh_token);
          window.location.reload();
        })
        .catch((err) => {
          errToast(`${err} - /refresh error`);
          errToast("Session Expired! Please Login again!");
          sessionStorage.clear();
          router.replace("/");
        });
    });
  return axios.create({
    baseURL: `${process.env.NEXT_PUBLIC_API_BASE_URL}`,
  });
};

export const postAcceptProjectHandler = async (values): Promise<boolean> => {
  try {
    let API;
    try {
      API = instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      const recaptchaToken = await getRecaptchaToken("post");
      const token = sessionStorage.getItem("token");

      await API?.post(`admin/projects?role=project`, values, {
        headers: {
          Authorization: `Bearer ${token}`,
          "X-RECAPTCHA-TOKEN": recaptchaToken,
        },
      });
      return true;
    }
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postAdminLogin = async (
  values: AdminLoginData
): Promise<boolean> => {
  try {
    let API;
    try {
      API = instance(false);
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      const recaptchaToken = await getRecaptchaToken("post");
      const res = await API?.post("/admin/login", values, {
        headers: {
          "X-RECAPTCHA-TOKEN": recaptchaToken,
        },
      });
      sessionStorage.setItem("token", res.data.access_token);
      sessionStorage.setItem("refreshToken", res.data.refresh_token);
      return true;
    }
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
    let API;
    try {
      API = instance(false);
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      const recaptchaToken = await getRecaptchaToken("post");
      const res = await API?.post("/admin/register", values, {
        headers: {
          Authorization: `Bearer ${authToken}`,
          "X-RECAPTCHA-TOKEN": recaptchaToken,
        },
      });
      return true;
    }
  } catch (error) {
    if (error.response?.status === 400) {
      errToast("User already exists");
    } else {
      errorHandler(error);
    }
    return false;
  }
};

export const getAcceptedProjects = async (
  pageNo,
  token
): Promise<any | false> => {
  try {
    let API;
    try {
      API = instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      return await (
        await API?.get(`admin/projects/accepted?page=${pageNo}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
      ).data;
    }
  } catch (error) {
    return false;
  }
};

export const getContributorsApplications = async (
  token,
  slug
): Promise<any | false> => {
  try {
    let API;
    try {
      API = instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      return await (
        await API?.get(
          `maintainer/projects?projectId=${slug}&contributor=1&maintainer=1`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
      ).data;
    }
  } catch (error) {
    return false;
  }
};

export const getAdminProjectApplications = async (
  token,
  pageNo
): Promise<any | false> => {
  try {
    let API;
    try {
      API = instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      return await (
        await API?.get(`admin/projects?page=${pageNo}`, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
      ).data;
    }
  } catch (error) {
    return false;
  }
};

export const postMaintainerLogin = async (
  values: MaintainerLoginData
): Promise<boolean> => {
  try {
    let API;
    try {
      API = instance(false);
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      const recaptchaToken = await getRecaptchaToken("post");
      const res = await API?.post("maintainer/login", values, {
        headers: {
          "X-RECAPTCHA-TOKEN": recaptchaToken,
        },
      });
      sessionStorage.setItem("token", res.data.access_token);
      sessionStorage.setItem("refreshToken", res.data.refresh_token);
      return true;
    }
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postResetPassword = async (
  values: ResetPasswordData
): Promise<boolean> => {
  try {
    let API;
    try {
      API = instance(false);
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      const recaptchaToken = await getRecaptchaToken("post");
      const res = await API?.post("maintainer/reset-password/reset", values, {
        headers: {
          "X-RECAPTCHA-TOKEN": recaptchaToken,
        },
      });
      return true;
    }
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
    let API;
    try {
      API = instance(false);
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      const recaptchaToken = await getRecaptchaToken("post");
      const res = await API?.post("maintainer/reset-password/set", values, {
        headers: {
          "X-RECAPTCHA-TOKEN": recaptchaToken,
          Authorization: `Bearer ${queryToken}`,
        },
      });
      return true;
    }
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
    let API;
    try {
      API = instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      const recaptchaToken = await getRecaptchaToken("post");
      const token = sessionStorage.getItem("token");
      await API?.post(
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
    }
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const deletefromMaintainerContributor = async (
  contributor_id
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const token = sessionStorage.getItem("token");
    await instance.delete("maintainer/projects?role=contributor", {
      headers: {
        Authorization: `Bearer ${token}`,
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
      data: { contributor_id: contributor_id },
    });
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const postAcceptMaintainer = async (
  project_id,
  maintainer_id,
  email
): Promise<boolean> => {
  try {
    let API;
    try {
      API = instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      const recaptchaToken = await getRecaptchaToken("post");
      const token = sessionStorage.getItem("token");
      await API?.post(
        "admin/projects?role=maintainer",
        { project_id: project_id, maintainer_id: maintainer_id, email },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "X-RECAPTCHA-TOKEN": recaptchaToken,
          },
        }
      );
      return true;
    }
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const deleteMaintainer = async (maintainer_id) => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const token = sessionStorage.getItem("token");
    await instance.delete("admin/projects?role=maintainer", {
      headers: {
        Authorization: `Bearer ${token}`,
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
      data: { maintainer_id: maintainer_id },
    });
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const deleteContributor = async (contributor_id) => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const token = sessionStorage.getItem("token");
    await instance.delete("admin/projects?role=contributor", {
      headers: {
        Authorization: `Bearer ${token}`,
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
      data: { contributor_id: contributor_id },
    });
    return true;
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const getMaintainerApplications = async (
  slug,
  token
): Promise<any | false> => {
  try {
    let API;
    try {
      API = instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      return await (
        await API?.get(
          `admin/projects?projectId=${slug}&contributor=false&maintainer=true`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
      ).data;
    }
  } catch (error) {
    return false;
  }
};

export const postAcceptProject = async (
  project_id,
  contributor_id
): Promise<boolean> => {
  try {
    let API;
    try {
      API = instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      const recaptchaToken = await getRecaptchaToken("post");
      const token = sessionStorage.getItem("token");
      await API?.post(
        "admin/projects?role=contributor",
        { contributor_id: contributor_id, project_id: project_id },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "X-RECAPTCHA-TOKEN": recaptchaToken,
          },
        }
      );
      return true;
    }
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const getProject = async (slug, token): Promise<any> => {
  try {
    let API;
    try {
      API = instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      sessionStorage.clear();
      router.replace("/");
    } finally {
      return await (
        await API?.get(
          `admin/projects?projectId=${slug}&contributor=true&maintainer=true`,
          {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          }
        )
      ).data;
    }
  } catch (error) {
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
