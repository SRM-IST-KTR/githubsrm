import React, { useEffect, useContext } from "react";
import { useRouter } from "next/router";
import AcceptedProjectDashboard from "../../../../components/admin/dashboard/accepted-projects/accepted-projects";
import { AuthContext } from "../../../../context/authContext";

const AcceptedProjectsPage = () => {
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (authContext.authReady) {
      if (!authContext.isAuth || !authContext.isAdmin) {
        router.replace("/");
      }
    }
  }, [authContext]);

  return <AcceptedProjectDashboard />;
};

export default AcceptedProjectsPage;
