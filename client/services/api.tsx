import axios, { AxiosInstance, AxiosError } from "axios";

import {
  MemberProps,
  ProjectProps,
  ContributorFormData,
  NewMaintainerForm,
  ExistingMaintainerForm,
} from "../utils/interfaces";
import { getRecaptchaToken } from "./recaptcha";

const instance: AxiosInstance = axios.create({
  baseURL: `${process.env.NEXT_PUBLIC_API_BASE_URL}/api`,
});

export const getTeam = async (): Promise<MemberProps[] | false> => {
  try {
    const team = await (await instance.get("/team")).data;
    return team;
  } catch (error) {
    console.log(error);
    return false;
  }
};

export const getProjects = async (): Promise<ProjectProps[] | false> => {
  try {
    const projects = await (await instance.get("/maintainer")).data;
    console.log(projects);
    return projects;
  } catch (error) {
    console.log(error);
    return false;
  }
};

export const postContributor = async (
  data: ContributorFormData
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken("post");
    const res = await instance.post("/contributor", data, {
      headers: {
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
    });
    console.log(res);
    return true;
  } catch (error) {
    console.log(error);
    return false;
  }
};

export const postMaintainer = async (
  data: NewMaintainerForm | ExistingMaintainerForm,
  role: "alpha" | "beta"
): Promise<boolean> => {
  try {
    const recaptchaToken = await getRecaptchaToken(`post?${role}`);
    const res = await instance.post("/maintainer", data, {
      headers: {
        "X-RECAPTCHA-TOKEN": recaptchaToken,
      },
    });
    console.log(res);
    return true;
  } catch (error) {
    console.log(error);
    return false;
  }
};

// const errorHandler = (err?: AxiosError | any) => {
//   let errMessage: string = "Oops! Something went wrong.";
//   if (err) {
//     switch (err.response?.status) {
//       case 400:
//         errMessage = "Bad request. Kindly check your inputs.";
//         break;
//       case 401:
//         errMessage = "Unauthorized.";
//         break;
//       case 403:
//         errMessage = "Forbidden.";
//         break;
//       case 409:
//         errMessage = "Already exists.";
//         break;
//       case 500:
//         errMessage = "Internal server error.";
//         break;
//       default:
//         errMessage = "Oops! Something went wrong.";
//         break;
//     }
//   }

//   toast.error(errMessage, {
//     position: "bottom-left",
//     autoClose: 5000,
//     hideProgressBar: false,
//     closeOnClick: true,
//     pauseOnHover: true,
//     draggable: true,
//     progress: undefined,
//   });
// };

// const successHandler = (errMessage: string) => {
//   toast.success(errMessage, {
//     position: "bottom-left",
//     autoClose: 5000,
//     hideProgressBar: false,
//     closeOnClick: true,
//     pauseOnHover: true,
//     draggable: true,
//     progress: undefined,
//   });
// };
