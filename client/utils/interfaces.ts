import * as Yup from 'yup';

import {
  newMaintainerValidation,
  existingMaintainerValidation,
  contributorValidation,
  contactUsValidation,
  maintainerLoginValidation,
} from './constants';

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

export interface InputClassNameProps {
  wrapperClassName?: { default?: string; onError?: string };
  inputClassName?: { default?: string; onError?: string };
  labelClassName?: { default?: string; onError?: string };
  descriptionClassName?: { default?: string; onError?: string };
}

export interface InputProps extends InputClassNameProps {
  type: 'text' | 'textarea' | 'select' | 'email' | 'password';
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

export interface MaintainerLoginData
  extends Yup.InferType<typeof maintainerLoginValidation> {}
