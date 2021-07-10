import ProjectTable from "../../../shared/table";
import Adminnavbar from "./navbar";
import { tableDataProjects } from "../../../shared/tableData";

const ProjectApplications = () => {
  return (
    <div className="bg-base-blue h-screen flex flex-col justify-center items-center">
      <Adminnavbar />
      <h2 className="text-4xl font-extrabold text-left text-white mb-10">
        Hi, Admin
      </h2>
      <ProjectTable tableData={tableDataProjects} />
    </div>
  );
};

export default ProjectApplications;
