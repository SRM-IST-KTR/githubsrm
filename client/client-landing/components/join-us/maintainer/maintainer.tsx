import { useState } from "react";
import Link from "next/link";
import { ArrowIcon } from "../../../utils/icons";
const Maintainer = () => {
  let [isNewProject, setisNewProject] = useState<boolean>(true);
  const projects: {
    name: string;
    href: string;
    statement: string;
    description: string[];
    icon: JSX.Element;
    isNewProject: boolean;
  }[] = [
    {
      name: "New Project",
      href: "/join-us/maintainer/new-project",
      statement: "Register a new Project",
      description: [
        "Project which is not registered with Github SRM.",
        "You are the First Maintainer to apply for the project."        
      ],
      icon: <ArrowIcon />,
      isNewProject: true,
    },
    {
      name: "Registered Project",
      href: "/join-us/maintainer/registered-project",
      statement: "Apply for a Registered Project",
      description: [
        "Project which is already registered with Github SRM.",
        "You have the Secret code for the respective project.",
        "You want to apply as the co-maintainer of the project.",
      ],
      icon: <ArrowIcon />,
      isNewProject: false,
    },
  ];
  return (
    <div>
      <div>
        <div className="font-medium">
          <h1 className="text-4xl">Maintainer</h1>
          <h2 className="text-xl mt-2">Maintain and manage projects</h2>
        </div>

        <p className="lg:text-right text-lg mt-3">
          Interested in a project? Join us as a{" "}
          <Link href="/join-us/contributor">
            <a className="text-base-green font-bold hover:underline">
              Contributor
            </a>
          </Link>
          .
        </p>
      </div>

      <div className="">
        <div className="flex  flex-col">
          <p className="text-xl lg:text-4xl font-semibold text-base-blue my-5">
            Please Choose One below
          </p>
        </div>
      </div>

      <div>
      <div className="flex flex-col md:flex-row justify-evenly mt-8">
        <div className="w-full md:w-4/12 flex flex-col sm:flex-row md:flex-col">
          {projects.map((project) => (
            <div key={project.name} className="flex mx-2 w-full">
              <div
                onClick={() => setisNewProject(project.isNewProject)}
                className={`${
                  isNewProject === project.isNewProject
                    ? "border-base-green"
                    : "md:border-transparent"
                } border-b-4 md:border-b-0 md:border-r-4 w-full cursor-pointer py-4 flex items-center justify-between transform hover:md:-translate-x-4`}
              >
                <div>
                  <h3
                    className={`${
                      isNewProject === project.isNewProject ? "font-medium" : ""
                    } text-xl mb-2`}
                  >
                    {project.name}
                  </h3>
                  <p className="text-sm w-full">{project.statement}</p>
                </div>

                <div className="mx-4">
                  <span
                    className={`${
                      isNewProject === project.isNewProject
                        ? "bg-base-green bg-opacity-80"
                        : "bg-base-smoke"
                    } w-12 hidden md:flex justify-center items-center p-2 rounded-full`}
                  >
                    {project.icon}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        <div className="w-full md:px-8 mt-8 md:mt-0">
          <div className="px-8 py-4 lg:px-8 bg-gray-100 border-t-8 rounded-sm border-base-green">
            {projects.map(
              (project) =>
                project.isNewProject === isNewProject && (
                  <div key={project.name}>
                    <h2 className="text-2xl mb-7">
                      What do we mean by <strong>{project.name}</strong>?
                    </h2>
                    <ul className="list-disc">
                      {project.description.map((item) => (
                        <li key={item} className="my-1">
                          {item}
                        </li>
                      ))}
                    </ul>

                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-x-2 items-center justify-center mt-5">
                      <span className="hidden lg:block" />
                      <span />
                      <Link href={project.href}>
                        <a className="text-white bg-base-green px-4 py-2 font-semibold rounded-lg text-center mx-auto">
                          Apply Now!
                        </a>
                      </Link>
                    </div>
                  </div>
                )
            )}
          </div>
        </div>
      </div>
      </div>
    </div>
  );
};

export default Maintainer;
