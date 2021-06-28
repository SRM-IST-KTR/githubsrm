import { ProjectProps } from "../../utils/interfaces";
import { colors } from "../../utils/constants";
import { GitHubIcon, CopyIcon } from "../../utils/icons";

interface ProjectProp {
  project: ProjectProps;
}

const Project = ({ project }: ProjectProp) => {
  const onCopyId = async (id: string) => {
    try {
      await navigator.clipboard.writeText(id);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div
      className={`border-${
        colors[Math.floor(Math.random() * colors.length)]
      } p-2 lg:p-6 border-t-8 max-w-md bg-gray-100 flex flex-col justify-between mx-auto`}
    >
      <div>
        <h2 className="flex w-full justify-between items-start capitalize text-gray-800 text-xl md:text-3xl font-semibold">
          {project.project_name}
          <div className="flex items-center ml-2 mt-2">
            {project.project_url && (
              <a
                className="w-6 mx-1"
                href={project.project_url}
                target="_blank"
                rel="noopener noreferrer"
              >
                <GitHubIcon />
              </a>
            )}

            <button className="w-6 mx-1" onClick={() => onCopyId(project._id)}>
              <CopyIcon />
            </button>
          </div>
        </h2>
        <p className="mt-2 text-gray-600 text-sm md:text-base">
          {project.description}
        </p>
      </div>

      <div className="mt-2 lg:mt-6">
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
