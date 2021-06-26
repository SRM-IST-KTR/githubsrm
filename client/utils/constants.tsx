import { PersonIcon, BookIcon, BranchIcon } from "./icons";
import { InputProps } from "./interfaces";

export const wrapperClassName: string = "flex flex-col mb-8";
export const inputClassName: string =
  "text-lg py-2 w-full px-4 text-lg rounded-lg border-2 border-opacity-40 focus:border-opacity-100 mt-1 bg-white";
export const inputClassNameError: string = "border-red-500 border-opacity-100";
export const labelClassName: string = "font-medium";

//* INFO: will be fetched from backend
const projects: { value: string; name: string }[] = [
  { name: "Project 1", value: "project1" },
  { name: "Project 2", value: "project2" },
  { name: "Project 3", value: "project3" },
  { name: "Project 4", value: "project4" },
];

// TODO: combine section props in one key
export const maintainerInputs: {
  section: string;
  description: string;
  icon: JSX.Element;
  inputs: InputProps[];
}[] = [
  {
    section: "Personal",
    icon: <PersonIcon />,
    description:
      "Ipsum id ullamco ipsum qui voluptate esse ad excepteur dolore commodo.",
    inputs: [
      { id: "name", label: "Name", type: "text", placeholder: "GithubSRM" },
      {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "johndoe@mail.com",
      },
      {
        id: "github_id",
        label: "Github Id",
        type: "text",
        placeholder: "srm-ist-ktr",
      },
    ],
  },
  {
    section: "SRM Details",
    icon: <BookIcon />,
    description: "Nostrud id officia dolor Lorem mollit aute consectetur est.",
    inputs: [
      {
        id: "srm_email",
        label: "SRM Email",
        type: "email",
        placeholder: "gs123@srmist.edu.in",
      },
      {
        id: "reg_number",
        label: "Reg No.",
        type: "text",
        placeholder: "RAXXXXXXXXXXXXX",
      },
      {
        id: "branch",
        label: "Branch",
        type: "text",
        placeholder: "CSE-BD",
      },
    ],
  },
  {
    section: "Projects",
    icon: <BranchIcon />,
    description:
      "Incididunt aute quis culpa aute in dolor aliqua laboris commodo exercitation laboris.",
    inputs: [
      {
        id: "project_url",
        label: "Project",
        type: "text",
        placeholder: "Calculator",
      },
      {
        id: "poa",
        label: "Feature or Bugfix",
        type: "textarea",
        placeholder: "Your project proposal",
        textareaOptions: { rows: 4, cols: 30 },
      },
    ],
  },
];

export const contributorInputs: {
  section: string;
  description: string;
  icon: JSX.Element;
  inputs: InputProps[];
}[] = [
  {
    section: "Personal",
    icon: <PersonIcon />,
    description:
      "Ipsum id ullamco ipsum qui voluptate esse ad excepteur dolore commodo.",
    inputs: [
      { id: "name", label: "Name", type: "text", placeholder: "GithubSRM" },
      {
        id: "email",
        label: "Email",
        type: "email",
        placeholder: "johndoe@mail.com",
      },
      {
        id: "github_id",
        label: "Github Id",
        type: "text",
        placeholder: "srm-ist-ktr",
      },
    ],
  },
  {
    section: "SRM Details",
    icon: <BookIcon />,
    description: "Nostrud id officia dolor Lorem mollit aute consectetur est.",
    inputs: [
      {
        id: "srm_email",
        label: "SRM Email",
        type: "email",
        placeholder: "gs123@srmist.edu.in",
      },
      {
        id: "reg_number",
        label: "Reg No.",
        type: "text",
        placeholder: "RAXXXXXXXXXXXXX",
      },
      {
        id: "branch",
        label: "Branch",
        type: "text",
        placeholder: "CSE-BD",
      },
    ],
  },
  {
    section: "Projects",
    icon: <BranchIcon />,
    description:
      "Incididunt aute quis culpa aute in dolor aliqua laboris commodo exercitation laboris.",
    inputs: [
      {
        id: "interested_project",
        label: "Project",
        type: "select",
        placeholder: "Calculator",
        selectOptions: { options: projects },
      },
      {
        id: "feature",
        label: "Feature or Bugfix",
        type: "textarea",
        placeholder: "Your project proposal",
        textareaOptions: { rows: 4, cols: 30 },
      },
    ],
  },
];
