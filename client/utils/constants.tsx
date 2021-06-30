import * as Yup from "yup";

import { PersonIcon, BookIcon, BranchIcon } from "./icons";
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

export const colors: string[] = [
  "base-black",
  "base-green",
  "base-smoke",
  "base-blue",
  "base-teal",
];

export const newMaintainerInputs: {
  section: string;
  description: string;
  icon: JSX.Element;
  inputs: InputProps[];
}[] = [
  {
    section: "Personal",
    icon: <PersonIcon />,
    description: "Let us get to know you better.",
    inputs: [
      {
        id: "name",
        label: "Name",
        type: "text",
        placeholder: "GitHub Community SRM",
        required: true,
      },
      {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "community@githubsrm.tech",
        required: true,
      },
      {
        id: "github_id",
        label: "Github ID",
        type: "text",
        placeholder: "srm-ist-ktr",
        required: true,
      },
    ],
  },
  {
    section: "SRM Details",
    icon: <BookIcon />,
    description: "Help us identify you.",
    inputs: [
      {
        id: "srm_email",
        label: "SRM Email",
        type: "email",
        placeholder: "gs1234@srmist.edu.in",
        required: true,
      },
      {
        id: "reg_number",
        label: "Registration Number or Employee ID",
        type: "text",
        placeholder: "RAXXXXXXXXXXXXX",
        required: true,
      },
      {
        id: "branch",
        label: "Branch",
        type: "text",
        placeholder: "CSE-BD",
        required: true,
      },
    ],
  },
  {
    section: "Projects",
    icon: <BranchIcon />,
    description: "Pitch your next big idea.",
    inputs: [
      {
        id: "project_name",
        label: "Project Name",
        type: "text",
        placeholder: "GitHub Community SRM Landing page",
        required: true,
      },
      {
        id: "project_url",
        label: "Public Repository URL",
        type: "text",
        placeholder: "https://github.com/SRM-IST-KTR/githubsrm",
        description: "Only for a personal existing project!",
      },
      {
        id: "tags",
        label: "Project Tags",
        type: "text",
        placeholder: "ReactJS, TailwindCSS, Django",
        description: "2-4 Comma separated values please!",
        required: true,
      },
      {
        id: "description",
        label: "Project Description",
        type: "textarea",
        placeholder: "This is the landing website for...",
        textareaOptions: { rows: 4, cols: 30 },
        required: true,
      },
    ],
  },
];

export const newMaintainerValidation = Yup.object().shape({
  name: Yup.string().trim().required("**Name**: Missing"),
  email: Yup.string()
    .trim()
    .required("**Email:** Missing")
    .email("**Email:** Invalid"),
  github_id: Yup.string().trim().required("**GitHub ID**: Missing"),
  srm_email: Yup.string()
    .trim()
    .required("**SRM Email ID:** Missing")
    .test("test-srm-email", "**SRM Email ID:** Invalid", (value) =>
      value?.endsWith("@srmist.edu.in")
    ),
  reg_number: Yup.string().trim().required("**Registration Number:** Missing"),
  branch: Yup.string().trim().required("**Branch:** Missing"),
  project_name: Yup.string()
    .trim()
    .required("**Public Repository URL:** Missing"),
  project_url: Yup.string().trim().url("**Public Repository URL:** Invalid"),
  tags: Yup.string()
    .trim()
    .required("**Tags:** Missing")
    .test(
      "test-tags",
      "**Tags:** Invalid Quantity",
      (value) =>
        value?.split(",").filter((i) => i.trim().length > 0).length >= 2 &&
        value?.split(",").filter((i) => i.trim().length > 0).length <= 4
    ),
  description: Yup.string()
    .trim()
    .required("**Description:** Missing")
    .min(30, "**Description:** Too small"),
});

export const existingMaintainerInputs: {
  section: string;
  description: string;
  icon: JSX.Element;
  inputs: InputProps[];
}[] = [
  {
    section: "Personal",
    icon: <PersonIcon />,
    description: "Let us get to know you better.",
    inputs: [
      {
        id: "name",
        label: "Name",
        type: "text",
        placeholder: "GitHub Community SRM",
        required: true,
      },
      {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "community@githubsrm.tech",
        required: true,
      },
      {
        id: "github_id",
        label: "Github ID",
        type: "text",
        placeholder: "srm-ist-ktr",
        required: true,
      },
    ],
  },
  {
    section: "SRM Details",
    icon: <BookIcon />,
    description: "Help us identify you.",
    inputs: [
      {
        id: "srm_email",
        label: "SRM Email",
        type: "email",
        placeholder: "gs1234@srmist.edu.in",
        required: true,
      },
      {
        id: "reg_number",
        label: "Registration Number or Employee ID",
        type: "text",
        placeholder: "RAXXXXXXXXXXXXX",
        required: true,
      },
      {
        id: "branch",
        label: "Branch",
        type: "text",
        placeholder: "CSE-BD",
        required: true,
      },
    ],
  },
  {
    section: "Projects",
    icon: <BranchIcon />,
    description: "Pitch your next big idea.",
    inputs: [
      {
        id: "project_id",
        label: "Project ID",
        type: "text",
        placeholder: "ABCD1234",
        description: "8 digit uppercase alpha-numeric code!",
        required: true,
      },
    ],
  },
];

export const existingMaintainerValidation = Yup.object().shape({
  name: Yup.string().trim().required("**Name**: Missing"),
  email: Yup.string()
    .trim()
    .required("**Email:** Missing")
    .email("**Email:** Invalid"),
  github_id: Yup.string().trim().required("**GitHub ID:** Missing"),
  srm_email: Yup.string()
    .trim()
    .required("**SRM Email ID:** Missing")
    .test("test-srm-email", "**SRM Email ID:** Invalid", (value) =>
      value?.endsWith("@srmist.edu.in")
    ),
  reg_number: Yup.string().trim().required("**Registration Number:** Missing"),
  branch: Yup.string().trim().required("**Branch:** Missing"),
  project_id: Yup.string()
    .trim()
    .required("**Project ID:** Missing")
    .matches(/^[A-Z0-9]{8}$/, "**Project ID**: Invalid"),
});

export const contributorInputs: {
  section: string;
  description: string;
  icon: JSX.Element;
  inputs: InputProps[];
}[] = [
  {
    section: "Personal",
    icon: <PersonIcon />,
    description: "Let us get to know you better.",
    inputs: [
      {
        id: "name",
        label: "Name",
        type: "text",
        placeholder: "GitHub Community SRM",
        required: true,
      },
      {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "community@githubsrm.tech",
        required: true,
      },
      {
        id: "github_id",
        label: "Github ID",
        type: "text",
        placeholder: "srm-ist-ktr",
        required: true,
      },
    ],
  },
  {
    section: "SRM Details",
    icon: <BookIcon />,
    description: "Help us identify you.",
    inputs: [
      {
        id: "srm_email",
        label: "SRM Email",
        type: "email",
        placeholder: "gs1234@srmist.edu.in",
        required: true,
      },
      {
        id: "reg_number",
        label: "Registration Number or Employee ID",
        type: "text",
        placeholder: "RAXXXXXXXXXXXXX",
        required: true,
      },
      {
        id: "branch",
        label: "Branch",
        type: "text",
        placeholder: "CSE-BD",
        required: true,
      },
    ],
  },
  {
    section: "Projects",
    icon: <BranchIcon />,
    description: "Be a part of the OSS revolution.",
    inputs: [
      {
        id: "interested_project",
        label: "Project ID",
        type: "text",
        placeholder: "Select your preferred project!",
        description:
          "Given to you by the Maintainer or found on the Projects Page!",
        required: true,
      },
      {
        id: "poa",
        label: "Feature or Bugfix",
        type: "textarea",
        placeholder: "The inputs fields have ClassName...",
        description: "Should have atleast 30 characters!",
        textareaOptions: { rows: 4, cols: 30 },
        required: true,
      },
    ],
  },
];

export const contributorValidation = Yup.object().shape({
  name: Yup.string().trim().required("**Name**: Missing"),
  email: Yup.string()
    .trim()
    .required("**Email**: Missing")
    .email("**Email**: Invalid"),
  github_id: Yup.string().trim().required("**GitHub ID**: Missing"),
  srm_email: Yup.string()
    .trim()
    .required("**SRM Email ID**: Missing")
    .test("test-srm-email", "**SRM Email ID**: Invalid", (value) =>
      value?.endsWith("@srmist.edu.in")
    ),
  reg_number: Yup.string().trim().required("**Registration Number**: Missing"),
  branch: Yup.string().trim().required("**Branch**: Missing"),
  interested_project: Yup.string()
    .trim()
    .required("**Project ID**: Missing")
    .matches(/^[A-Z0-9]{8}$/, "**Project ID**: Invalid"),
  poa: Yup.string()
    .trim()
    .required("**Feature or Bugfix**: Missing")
    .min(30, "**Feature or Bugfix**: Too Small"),
});

export const contactUsInputs: InputProps[][] = [
  [
    {
      id: "name",
      label: "Name",
      type: "text",
      placeholder: "John Doe",
      required: true,
    },
    {
      id: "email",
      label: "Email",
      type: "email",
      placeholder: "community@githubsrm.tech",
      required: true,
    },
    {
      id: "phone_number",
      label: "Phone Number",
      type: "text",
      placeholder: "9999999999",
      description: "Should be 10 digits!",
    },
  ],
  [
    {
      id: "message",
      label: "Message",
      type: "textarea",
      placeholder: "I had a query regarding...",
      required: true,
      textareaOptions: { rows: 4, cols: 30 },
      wrapperClassName: {
        default: "w-full mx-2",
      },
    },
  ],
];

export const contactUsValidation = Yup.object().shape({
  name: Yup.string().trim().required("**Name:** Missing"),
  email: Yup.string()
    .trim()
    .required("**Email:** Missing")
    .email("**Email:** Invalid"),
  phone_number: Yup.string()
    .trim()
    .matches(/^[0-9]{10}$/, "**Phone Number:** Invalid"),
  message: Yup.string()
    .trim()
    .required("**Message:** Missing")
    .min(30, "**Message:** Too small"),
});
