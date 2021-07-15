import * as Yup from "yup";

import {
  maintainerLoginValidation,
  adminRegisterValidation,
  adminLoginValidation,
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

export interface MaintainerLoginData
  extends Yup.InferType<typeof maintainerLoginValidation> {}

export interface AdminRegisterData
  extends Yup.InferType<typeof adminRegisterValidation> {}

export interface AdminLoginData
  extends Yup.InferType<typeof adminLoginValidation> {}
