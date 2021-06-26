import { Project } from "./";
import { projectCardDetails } from "../../utils/constants";

const Projects = () => {
  return (
    <div>
      <h1 className="text-center text-5xl font-bold mb-10 text-base-black">
        Projects
      </h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {projectCardDetails.map((project) => (
          <Project key={project.name.trim()} project={project} />
        ))}
      </div>
    </div>
  );
};

export default Projects;
