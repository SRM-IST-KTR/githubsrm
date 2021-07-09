import * as Yup from "yup";

import {
  maintainerLoginValidation,
  adminRegisterValidation,
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

export interface MaintainerLoginData
  extends Yup.InferType<typeof maintainerLoginValidation> {}

export interface AdminRegisterData
  extends Yup.InferType<typeof adminRegisterValidation> {}
