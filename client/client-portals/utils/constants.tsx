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
  {
    id: "confirm_password",
    label: "Confirm Password",
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
    id: "project_url",
    label: "Project URL",
    type: "text",
    placeholder: "https://github.com/ID/PROJECT-NAME",
    required: true,
  },
];

export const academicYearInputs: InputProps[] = [
  {
    id: "academic_year",
    label: "Academic Year",
    type: "text",
    placeholder: "20XX",
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
  confirm_password: Yup.string()
    .oneOf([Yup.ref("password")], "Passwords must match")
    .required("**Confirm Password:** Missing"),
});

export const projectVisibiltyValidation = Yup.object().shape({
  private: Yup.boolean().required("**Project Type:** Missing"),
  project_url: Yup.string().trim().required("**Project URL:** Missing"),
});

export const academicYearValidation = Yup.object().shape({
  academic_year: Yup.number()
    .required("**Academic Year:** Missing")
    .min(4)
    .max(4),
});
