import AcceptedProjectsCards from "./accepted-projects-cards";
import Adminnavbar from "./navbar";
import React from "react";

const AcceptedProjectDashboard = () => {
  return (
    <div className="min-h-screen p-14 bg-base-blue">
      <Adminnavbar />
      <AcceptedProjectsCards />
    </div>
  );
};

export default AcceptedProjectDashboard;
