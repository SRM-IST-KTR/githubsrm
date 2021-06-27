import { Project } from "./";
import { ProjectProps } from "../../utils/interfaces";

interface ProjectsProps {
  projects: ProjectProps[];
}

const Projects = ({ projects }: ProjectsProps) => {
  return (
    <div>
      <h1 className="text-center text-5xl font-bold mb-10 text-base-black">
        Projects
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {projects?.map((project) => (
          <Project key={project.project_name.trim()} project={project} />
        ))}
      </div>
    </div>
  );
};

export default Projects;
