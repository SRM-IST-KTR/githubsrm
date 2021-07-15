import AcceptedProjectsCards from "./accepted-projects-cards";
import React from "react";
import { Layout } from "../../../shared";

const AcceptedProjectDashboard = () => {
  return (
    <Layout type="admin">
      <h1 className="text-center text-4xl mt-5 mb-10 font-extrabold text-white">
        All Accepted Projects
      </h1>
      <AcceptedProjectsCards />
    </Layout>
  );
};

export default AcceptedProjectDashboard;
