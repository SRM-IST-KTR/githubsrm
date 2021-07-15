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

export const resetPasswordInputs: InputProps[] = [
  {
    id: "srm_email",
    label: "SRM Email",
    type: "email",
    placeholder: "jd5673@srmist.edu.in",
    required: true,
  },
  {
    id: "current_password",
    label: "Current Password",
    type: "password",
    placeholder: "*********",
    required: true,
  },
  {
    id: "new_password",
    label: "New Password",
    type: "password",
    placeholder: "*********",
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
  srm_email: Yup.string()
    .trim()
    .required("**Email:** Missing")
    .email("**Email:** Invalid"),
  current_password: Yup.string().required("**Current Password:** Missing"),
  new_password: Yup.string().required("**New Password:** Missing"),
});
