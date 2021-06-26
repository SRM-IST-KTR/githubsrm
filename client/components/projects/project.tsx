import { ProjectProps } from "../../utils/interfaces";
import { colors } from "../../utils/constants";
import { GitHubIcon } from "../../utils/icons";

interface ProjectProp {
  project: ProjectProps;
}

const Project = ({ project }: ProjectProp) => {
  return (
    <div
      className={`border-${
        colors[Math.floor(Math.random() * colors.length)]
      } p-5 border-t-8 max-w-md bg-gray-100 flex flex-col justify-between`}
    >
      <div className="">
        <h2 className="flex justify-between items-center text-gray-800 text-xl md:text-3xl font-semibold">
          {project.name}
          {project.src && (
            <a
              className="w-6"
              href={project.src}
              target="_blank"
              rel="noopener noreferrer"
            >
              <GitHubIcon />
            </a>
          )}
        </h2>
        <p className="mt-2 text-gray-600 text-sm md:text-base">
          {project.description}
        </p>
      </div>

      <div className="mt-6">
        {project.tags.map((tag) => (
          <p
            key={tag.trim()}
            className={`bg-${
              colors[Math.floor(Math.random() * colors.length)]
            } my-1 uppercase text-xs font-bold text-gray-100 mx-1 rounded p-2 inline-block`}
          >
            {tag}
          </p>
        ))}
      </div>
    </div>
  );
};

export default Project;
