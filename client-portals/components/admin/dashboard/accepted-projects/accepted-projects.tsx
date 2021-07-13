import AcceptedProjectsCards from "./accepted-projects-cards";
import React from "react";
import { Layout } from "../../../shared";

const AcceptedProjectDashboard = () => {
  return (
    <Layout type="admin">
      <h1 className="text-center my-5 text-4xl font-extrabold text-white">
        All Accepted Projects
      </h1>
      <AcceptedProjectsCards />
    </Layout>
  );
};

export default AcceptedProjectDashboard;
