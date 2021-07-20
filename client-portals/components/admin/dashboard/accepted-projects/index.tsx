import AcceptedProjectsCards from "./accepted-projects-cards";
import React from "react";
import { Layout, Footer } from "@/shared/index";

const AcceptedProjectDashboard = () => {
  return (
    <>
      <Layout type="admin">
        <h1 className="text-center text-4xl mt-5 mb-10 font-extrabold text-white">
          All Accepted Projects
        </h1>
        <AcceptedProjectsCards />
      </Layout>
      <div className="fixed bottom-0 w-full">
        <Footer />
      </div>
    </>
  );
};

export default AcceptedProjectDashboard;
