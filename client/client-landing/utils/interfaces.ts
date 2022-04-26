import * as Yup from "yup";

import {
  newMaintainerValidation,
  existingMaintainerValidation,
  contributorValidation,
  contactUsValidation,
} from "./constants";

interface Id {
  id: string;
}
export interface MemberProps extends Id {
  name: string;
  designation: string;
  github_id: string;
  linkedin: string;
  twitter: string;
  portfolio: string;
  img_url: string;
  tagline: string;
}

export interface ProjectProps {
  _id: string;
  project_url: string;
  description: string;
  project_name: string;
  tags: string[];
}

export interface InputClassTypes {
  default?: string;
  onError?: string;
}

export interface InputClassNameProps {
  wrapperClassName?: InputClassTypes;
  inputClassName?: InputClassTypes;
  labelClassName?: InputClassTypes;
  descriptionClassName?: InputClassTypes;
  optionClassName?: {
    label?: InputClassTypes;
    option?: InputClassTypes;
  };
}

export interface InputProps extends InputClassNameProps {
  type:
    | "text"
    | "textarea"
    | "select"
    | "email"
    | "password"
    | "checkbox"
    | "radio";
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

export interface NewMaintainerForm
  extends Yup.InferType<typeof newMaintainerValidation> {}

export interface ExistingMaintainerForm
  extends Yup.InferType<typeof existingMaintainerValidation> {}

export interface ContributorFormData
  extends Yup.InferType<typeof contributorValidation> {}

export interface ContactUsFormData
  extends Yup.InferType<typeof contactUsValidation> {}

export interface LinkProps {
  source: {
    href: string;
    title?: string;
    subTitle?: string;
    content?: string;
    name?: string;
    icon?: JSX.Element;
  };
}
