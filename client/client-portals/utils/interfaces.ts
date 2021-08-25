import * as Yup from "yup";
import {
  maintainerLoginValidation,
  adminRegisterValidation,
  adminLoginValidation,
  resetPasswordValidation,
  setPasswordValidation,
  projectVisibiltyValidation,
  academicYearValidation,
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
    options: { value: boolean; name: string }[];
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
  year: string;
}

export interface ContributorsProps {
  _id: string;
  is_admin_approved: boolean;
  is_admin_rejected: boolean;
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
  is_admin_rejected: boolean;
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
export interface AcceptedProjectsAdminProps {
  contributor: [
    _id: string,
    name: string,
    email: string,
    srm_email: string,
    github_id: string,
    reg_number: string,
    branch: string,
    poa: string,
    is_maintainer_approved: boolean
  ];
  project: [project_name: string];
  maintainer: [];
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
  is_maintainer_rejected: boolean;
}

export interface AcceptedProjectsProps {
  hasNextPage: boolean;
  hasPreviousPage: boolean;
  records: [];
}

export interface ButtonWrapperProps {
  type?: "button" | "submit" | "reset";
  btnStyle?: "primary" | "secondary";
  disabled?: boolean;
  children?: JSX.Element | string;
  onClick?: (event?: React.MouseEvent<HTMLButtonElement, MouseEvent>) => void;
}

export interface ModalProps {
  setIsOpen: (_isOpen: boolean) => void;
  children: JSX.Element;
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

export interface ProjectVisibilityData
  extends Yup.InferType<typeof projectVisibiltyValidation> {}
export interface AcademicYearData
  extends Yup.InferType<typeof academicYearValidation> {}
