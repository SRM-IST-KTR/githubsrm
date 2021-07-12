import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import AcceptedProjectDashboard from "../../../../components/portals/admin/dashboard/accepted-projects";
import AuthContextProvider from "../../../../context/authContext";

const AcceptedProjectsPage = () => {
  const router = useRouter();
  useEffect(() => {
    if (!sessionStorage.getItem("token")) {
      router.push("/admin");
    }
  }, []);

  return (
    <AuthContextProvider>
      <div className="flex items-center justify-center h-screen bg-base-blue">
        <AcceptedProjectDashboard />
      </div>
    </AuthContextProvider>
  );
};

export default AcceptedProjectsPage;
