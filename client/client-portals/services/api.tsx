import { useContext } from "react";
import axios, { AxiosInstance } from "axios";
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
import { AuthContext } from "context/authContext";

const instance = async (auth: boolean = true): Promise<AxiosInstance> => {
  const api = axios.create({
    baseURL: `${process.env.NEXT_PUBLIC_API_BASE_URL}`,
  });
  api.defaults.headers.common["X-RECAPTCHA-TOKEN"] = await getRecaptchaToken(
    "post"
  );
  if (!auth) {
    return api;
  }
  const authToken = sessionStorage.getItem("token");
  const refreshToken = sessionStorage.getItem("refreshToken");
  const recaptchaToken = await getRecaptchaToken("post");
  try {
    try {
      const { data } = await axios.get(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/me`,
        {
          headers: {
            Authorization: `Bearer ${authToken}`,
          },
        }
      );
      if (data.success) {
        api.defaults.headers.common["Authorization"] = `Bearer ${authToken}`;
        return api;
      }
    } catch (err) {
      const { data } = await axios.post(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/refresh-token`,
        {},
        {
          headers: {
            Authorization: `Bearer ${refreshToken}`,
            "X-RECAPTCHA-TOKEN": recaptchaToken,
          },
        }
      );
      sessionStorage.setItem("token", data.access_token);
      sessionStorage.setItem("refreshToken", data.refresh_token);
      window.location.reload();
      api.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${data.access_token}`;
      return api;
    }
  } catch (err) {
    throw "NotAuthenticatedError";
  }
};

export const postAcceptProjectHandler = async (values): Promise<boolean> => {
  try {
    let API;
    try {
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      await API?.post(`admin/projects?role=project`, values);
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
      API = await instance(false);
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      const res = await API?.post("/admin/login", values);
      sessionStorage.setItem("token", res.data.access_token);
      sessionStorage.setItem("refreshToken", res.data.refresh_token);
      return true;
    }
  } catch (error) {
    errorHandler(error);
    console.dir(error);
    return false;
  }
};

export const postAdminRegister = async (
  values: AdminRegisterData,
  token: string
): Promise<boolean> => {
  try {
    let API;
    try {
      API = await instance(false);
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      API.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      const res = await API?.post("/admin/register", values);
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

export const getAcceptedProjects = async (pageNo): Promise<any | false> => {
  try {
    let API;
    try {
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      return await (
        await API?.get(`admin/projects/accepted?page=${pageNo}`)
      ).data;
    }
  } catch (error) {
    return false;
  }
};

export const getContributorsApplications = async (
  slug: string,
  cPageNo: number,
  mPageNo: number
): Promise<any | false> => {
  try {
    let API;
    try {
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      return await (
        await API?.get(
          `maintainer/projects?projectId=${slug}&contributor=${cPageNo}&maintainer=${mPageNo}`
        )
      ).data;
    }
  } catch (error) {
    return false;
  }
};

export const getAdminProjectApplications = async (
  pageNo
): Promise<any | false> => {
  try {
    let API;
    try {
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      return await (
        await API?.get(`admin/projects?page=${pageNo}`)
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
      API = await instance(false);
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      const res = await API?.post("maintainer/login", values);
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
      API = await instance(false);
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      const res = await API?.post("maintainer/reset-password/reset", values);
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
      API = await instance(false);
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      API.defaults.headers.common["Authorization"] = `Bearer ${queryToken}`;
      const res = await API?.post("maintainer/reset-password/set", values);
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
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      await API?.post("maintainer/projects?role=contributor", {
        project_id: project_id,
        contributor_id: contributor_id,
      });
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
    let API;
    try {
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      await API?.delete("maintainer/projects?role=contributor", {
        data: {
          contributor_id: contributor_id,
        },
      });
      return true;
    }
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
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      await API?.post("admin/projects?role=maintainer", {
        project_id: project_id,
        maintainer_id: maintainer_id,
        email,
      });
      return true;
    }
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const deleteMaintainer = async (maintainer_id) => {
  try {
    let API;
    try {
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      await API?.delete("admin/projects?role=maintainer", {
        data: {
          maintainer_id: maintainer_id,
        },
      });
      return true;
    }
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const deleteContributor = async (contributor_id): Promise<boolean> => {
  try {
    let API;
    try {
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      await API?.delete("admin/projects?role=contributor", {
        data: {
          contributor_id: contributor_id,
        },
      });
      return true;
    }
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const getMaintainerApplications = async (slug): Promise<any | false> => {
  try {
    let API;
    try {
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      return await (
        await API?.get(
          `admin/projects?projectId=${slug}&contributor=false&maintainer=true`
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
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      await API?.post("admin/projects?role=contributor", {
        contributor_id: contributor_id,
        project_id: project_id,
      });
      return true;
    }
  } catch (error) {
    errorHandler(error);
    return false;
  }
};

export const getProject = async (slug): Promise<any> => {
  try {
    let API;
    try {
      API = await instance();
    } catch (error) {
      errToast("Session Expired! Please Login again!");
      const authContext = useContext(AuthContext);
      authContext.logoutHandler();
    } finally {
      return await (
        await API?.get(
          `admin/projects?projectId=${slug}&contributor=true&maintainer=true`
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
