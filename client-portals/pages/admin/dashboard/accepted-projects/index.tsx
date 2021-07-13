import React, { useEffect, useContext } from "react";
import { useRouter } from "next/router";
import AcceptedProjectDashboard from "../../../../components/admin/dashboard/accepted-projects/accepted-projects";
import { AuthContext } from "../../../../context/authContext";

const AcceptedProjectsPage = () => {
  const router = useRouter();

  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (!sessionStorage.getItem("token")) {
      authContext.setIsAuth(false);
      router.push("/admin");
    }
  }, [authContext]);

  return (
    <div className="flex items-center justify-center h-screen bg-base-blue">
      <AcceptedProjectDashboard />
    </div>
  );
};

export default AcceptedProjectsPage;
