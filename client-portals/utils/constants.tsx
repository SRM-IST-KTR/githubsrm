import * as Yup from "yup";
import { InputClassNameProps, InputProps } from "./interfaces";

export const customInputClasses: InputClassNameProps = {
  wrapperClassName: { default: "custom-input-wrapper" },
  inputClassName: {
    default: "custom-input",
    onError: "custom-input-error",
  },
  labelClassName: {
    default: "custom-label",
  },
  descriptionClassName: {
    default: "custom-description",
  },
};

export const maintainerLoginInputs: InputProps[] = [
  {
    id: "email",
    label: "Email",
    type: "email",
    placeholder: "community@githubsrm.tech",
    required: true,
  },
  {
    id: "password",
    label: "Password",
    type: "password",
    placeholder: "*********",
    required: true,
  },
];

export const adminRegisterInputs: InputProps[] = [
  {
    id: "email",
    label: "Email",
    type: "email",
    placeholder: "community@githubsrm.tech",
    required: true,
  },
  {
    id: "password",
    label: "Password",
    type: "password",
    placeholder: "*********",
    required: true,
  },
];

export const adminLoginInputs: InputProps[] = [
  {
    id: "email",
    label: "Email",
    type: "email",
    placeholder: "community@githubsrm.tech",
    required: true,
  },
  {
    id: "password",
    label: "Password",
    type: "password",
    placeholder: "*********",
    required: true,
  },
];

export const setPasswordInputs: InputProps[] = [
  {
    id: "password",
    label: "Password",
    type: "password",
    placeholder: "*********",
    required: true,
  },
];

export const resetPasswordInputs: InputProps[] = [
  {
    id: "email",
    label: "Email",
    type: "email",
    placeholder: "jd5673@srmist.edu.in",
    required: true,
  },
];

export const projectVisibilityInputs: InputProps[] = [
  {
    id: "private",
    label: "Project Type",
    type: "select",
    selectOptions: {
      options: [
        { value: "private", name: "Private" },
        { value: "public", name: "Public" },
      ],
    },
    required: true,
  },
  {
    id: "project_url",
    label: "Project URL",
    type: "text",
    placeholder: "https://github.com/ID/PROJECT-NAME",
    required: true,
  },
];

export const maintainerLoginValidation = Yup.object().shape({
  email: Yup.string()
    .trim()
    .required("**Email:** Missing")
    .email("**Email:** Invalid"),
  password: Yup.string().required("**Password:** Missing"),
});

export const adminRegisterValidation = Yup.object().shape({
  email: Yup.string()
    .trim()
    .required("**Email:** Missing")
    .email("**Email:** Invalid"),
  password: Yup.string().required("**Password:** Missing"),
});

export const adminLoginValidation = Yup.object().shape({
  email: Yup.string()
    .trim()
    .required("**Email:** Missing")
    .email("**Email:** Invalid"),
  password: Yup.string().required("**Password:** Missing"),
});

export const resetPasswordValidation = Yup.object().shape({
  email: Yup.string()
    .trim()
    .required("**Email:** Missing")
    .email("**Email:** Invalid"),
});

export const setPasswordValidation = Yup.object().shape({
  password: Yup.string().required("**Password:** Missing").min(2),
});

export const projectVisibiltyValidation = Yup.object().shape({
  private: Yup.string().trim().required("**Project Visiblity:** Missing"),
  project_url: Yup.string().trim().required("**Project URL:** Missing"),
});
