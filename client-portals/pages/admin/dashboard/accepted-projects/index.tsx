import React, { useEffect, useContext } from "react";
import { useRouter } from "next/router";
import AcceptedProjectDashboard from "../../../../components/admin/dashboard/accepted-projects/accepted-projects";
import { AuthContext } from "../../../../context/AuthContext";

const AcceptedProjectsPage = () => {
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (!authContext.isAuth || !authContext.isAdmin) {
      router.replace("admin/dashboard/accepted-projects", "/");
    }
  }, [authContext]);

  return <AcceptedProjectDashboard />;
};

export default AcceptedProjectsPage;
