//table
import ProjectTable from "../../../shared/table";
import Adminnavbar from "./navbar";
const ProjectApplications = () => {
  return (
    <div className="bg-base-blue h-screen flex flex-col justify-center items-center">
      <Adminnavbar />
      <ProjectTable />
    </div>
  );
};

export default ProjectApplications;
