import * as Yup from "yup";

import {
  maintainerLoginValidation,
  adminRegisterValidation,
  adminLoginValidation,
  resetPasswordValidation,
  setPasswordValidation,
} from "./constants";

export interface InputClassNameProps {
  wrapperClassName?: { default?: string; onError?: string };
  inputClassName?: { default?: string; onError?: string };
  labelClassName?: { default?: string; onError?: string };
  descriptionClassName?: { default?: string; onError?: string };
}

export interface InputProps extends InputClassNameProps {
  type: "text" | "textarea" | "select" | "email" | "password";
  required?: boolean;
  id: string;
  label?: string;
  placeholder?: string;
  selectOptions?: {
    options: { value: string; name: string }[];
    optionClassName?: string;
  };
  description?: string;
  textareaOptions?: { rows?: number; cols?: number };
  onError?: boolean;
}

export interface AcceptedProjectProps {
  _id: string;
  is_admin_approved: boolean;
  description: string;
  project_name: string;
}

export interface TableProjectsProps {
  _id: string;
  is_admin_approved: boolean;
  private: boolean;
  description: string;
  project_name: string;
  project_url: string;
  tags: string[];
}

export interface ContributorsProps {
  _id: string;
  is_admin_approved: boolean;
  branch: string;
  email: string;
  name: string;
  github_id: string;
  reg_number: string;
  poa: string;
  is_maintainer_approved: boolean;
  is_added_to_repo: boolean;
  srm_email: string;
}

export interface MaintainersProps {
  _id: string;
  is_admin_approved: boolean;
  branch: string;
  email: string;
  name: string;
  github_id: string;
  reg_number: string;
}

export interface MaintainerProjectsProps {
  _id: string;
  description: string;
  project_name: string;
}

export interface OtherMaintainersProps {
  github: string;
  name: string;
}

export interface ContributorProps {
  _id: string;
  name: string;
  email: string;
  srm_email: string;
  github_id: string;
  reg_number: string;
  branch: string;
  poa: string;
  is_maintainer_approved: boolean;
}

export interface MaintainerLoginData
  extends Yup.InferType<typeof maintainerLoginValidation> {}

export interface AdminRegisterData
  extends Yup.InferType<typeof adminRegisterValidation> {}

export interface AdminLoginData
  extends Yup.InferType<typeof adminLoginValidation> {}

export interface ResetPasswordData
  extends Yup.InferType<typeof resetPasswordValidation> {}

export interface SetPasswordData
  extends Yup.InferType<typeof setPasswordValidation> {}
