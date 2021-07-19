import { useState, useEffect } from "react";

import { Project } from ".";
import { ProjectProps } from "../../utils/interfaces";
import { LoadingIcon } from "../../utils/icons";
import { getProjects } from "../../services/api";

const Projects = () => {
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<boolean>(false);
  const [projects, setProjects] = useState<ProjectProps[]>([]);

  useEffect(() => {
    (async () => {
      try {
        const res = await getProjects();
        if (res) {
          setProjects(res);
        } else {
          setError(true);
        }
      } catch (error) {
        setError(true);
      }
      setLoading(false);
    })();
  }, []);

  return (
    <div>
      <h1 className="text-center text-3xl lg:text-5xl font-bold mb-10 text-base-black">
        Projects
      </h1>

      {loading ? (
        <div className="w-10 mx-auto text-base-smoke text-2xl">
          <LoadingIcon />
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5 items-start">
          {!error ? (
            projects.length > 0 ? (
              projects.map((project) => (
                <Project key={project.project_name.trim()} project={project} />
              ))
            ) : (
              <>
                <span />
                <h3 className="text-center text-lg lg:text-2xl font-medium text-base-black min-h-30">
                  No Projects available right now!
                </h3>
                <span />
              </>
            )
          ) : (
            <>
              <span />
              <h3 className="text-center text-lg lg:text-2xl font-medium text-red-500 min-h-30">
                Error fetching projects!
              </h3>
              <span />
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default Projects;
