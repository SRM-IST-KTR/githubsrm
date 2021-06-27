import * as Yup from "yup";

import {
  maintainerValidationSchema,
  contributorValidationSchema,
} from "./constants";

interface Id {
  id: string;
}
export interface MemberProps extends Id {
  name: string;
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

export interface InputProps {
  type: "text" | "textarea" | "select" | "email";
  id: string;
  label?: string;
  placeholder?: string;
  selectOptions?: {
    options: { value: string; name: string }[];
    optionClassName?: string;
  };
  description?: { content: string; class?: string };
  textareaOptions?: { rows?: number; cols?: number };
  onError?: boolean;
  wrapperClassName?: { default?: string; onError?: string };
  inputClassName?: { default?: string; onError?: string };
  labelClassName?: { default?: string; onError?: string };
}

export interface MaintainerFormData
  extends Yup.InferType<typeof maintainerValidationSchema> {}

export interface ContributorFormData
  extends Yup.InferType<typeof contributorValidationSchema> {}
