import AcceptedProjectsCards from "./accepted-projects-cards";
import React from "react";
import { Layout } from "../../../shared";

const AcceptedProjectDashboard = () => {
  return (
    <Layout type="admin">
      <AcceptedProjectsCards />
    </Layout>
  );
};

export default AcceptedProjectDashboard;
