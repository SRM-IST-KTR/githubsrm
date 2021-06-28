import { Project } from "./";
import { ProjectProps } from "../../utils/interfaces";

interface ProjectsProps {
  projects: ProjectProps[];
}

const Projects = ({ projects }: ProjectsProps) => {
  return (
    <div>
      <h1 className="text-center text-3xl lg:text-5xl font-bold mb-10 text-base-black">
        Projects
      </h1>

      {projects.length > 0 ? (
        projects.map((project) => (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            <Project key={project.project_name.trim()} project={project} />
          </div>
        ))
      ) : (
        <h3 className="flex items-center justify-center text-center text-lg lg:text-2xl font-medium text-base-black min-h-30">
          No Projects available right now!
        </h3>
      )}
    </div>
  );
};

export default Projects;
