import AcceptedProjectsCard from "./accepted-projects";
import Adminnavbar from "./navbar";

const AcceptedProjectDashboard = () => {
  return (
    <div className="min-h-screen p-14 bg-base-blue">
      <Adminnavbar />
      <h2 className="text-4xl font-extrabold text-white mb-10">Hi, Admin</h2>
      <AcceptedProjectsCard />
    </div>
  );
};

export default AcceptedProjectDashboard;
