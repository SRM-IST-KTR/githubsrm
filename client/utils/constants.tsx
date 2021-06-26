import * as Yup from "yup";

import { PersonIcon, BookIcon, BranchIcon } from "./icons";
import { InputProps, ProjectProps } from "./interfaces";

export const wrapperClassName: string = "flex flex-col mb-8";
export const inputClassName: string =
  "text-lg py-2 w-full px-4 text-lg rounded-lg border-2 border-opacity-40 focus:border-opacity-100 mt-1 bg-white";
export const inputClassNameError: string = "border-red-500 border-opacity-100";
export const labelClassName: string = "font-medium";
export const descriptionClass: string = "text-sm font-medium text-right";

export const colors: string[] = [
  "base-black",
  "base-green",
  "base-smoke",
  "base-blue",
  "base-teal",
];

// * INFO: will be fetched
export const projectCardDetails: ProjectProps[] = [
  {
    name: "Project Name",
    description: "Lorem in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["tailwind ", "javascript ", "typescript "],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["python ", "django ", "vue"],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["web-app ", "javascript ", "typescript "],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["web-app ", "javascript ", "typescript "],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["web-app ", "javascript ", "typescript "],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["python ", "django ", "vue"],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["web-app ", "javascript ", "typescript "],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["web-app ", "javascript ", "typescript "],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["web-app ", "javascript ", "typescript "],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["web-app ", "javascript ", "typescript "],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["web-app ", "javascript ", "typescript "],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["web-app ", "javascript ", "typescript "],
  },
  {
    name: "Project Name",
    description:
      "Lorem ipsum dolor sit amet consectetur adipisicing elit. Quae dolores deserunt ea doloremque natus error, rerum quas quaerat nam ex commodi hic, suscipit in a veritatis pariatur minus consequuntur!",
    src: "https://images.unsplash.com/photo-1499714608240-22fc6ad53fb2?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    tags: ["web-app ", "javascript ", "typescript "],
  },
];

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
        label: "Registration Number or Employee ID",
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
        id: "project_name",
        label: "Project Name",
        type: "text",
        placeholder: "GitHubSRM",
      },
      {
        id: "project_url",
        label: "Project GitHub URL",
        type: "text",
        placeholder: "https://github.com/SRM-IST-KTR/githubsrm",
        description: {
          content: "If an existing project, please give its GitHub URL!",
          class: descriptionClass,
        },
      },
      {
        id: "tags",
        label: "Project Tags",
        type: "text",
        placeholder: "ReactJS, TailwindCSS, Django",
        description: {
          content: "2-4 Comma separated values please!",
          class: descriptionClass,
        },
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

export const maintainerValidationSchema = Yup.object().shape({
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
  project_url: Yup.string()
    .trim()
    .required("**Project URL**: Missing")
    .url("**Project URL**: Invalid"),
  tags: Yup.string()
    .trim()
    .required("**Tags:** Missing")
    .test(
      "test-tags",
      "**Tags**: Invalid Quantity",
      (value) =>
        value?.split(",").filter((i) => i.trim().length > 0).length >= 2 &&
        value?.split(",").filter((i) => i.trim().length > 0).length <= 4
    ),
  poa: Yup.string()
    .trim()
    .required("**Feature or Bugfix:** Missing")
    .min(30, "**Feature or Bugfix:** Too small"),
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
        label: "Registration Number or Employee ID",
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

export const contributorValidationSchema = Yup.object().shape({
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
  interested_project: Yup.string().trim(),
  // .required("**Interested Project**: Missing"),
  feature: Yup.string().trim(),
});
