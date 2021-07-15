import React, { useEffect, useContext } from "react";
import { useRouter } from "next/router";
import AcceptedProjectDashboard from "../../../../components/admin/dashboard/accepted-projects/accepted-projects";
import { AuthContext } from "../../../../context/AuthContext";

const AcceptedProjectsPage = () => {
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (!authContext.isAuth || !authContext.isAdmin) {
      router.push("/admin");
    }
  }, [authContext]);

  return authContext.isAuth ? (
    <AcceptedProjectDashboard />
  ) : (
    <h1>Not Authenticated</h1>
  );
};

export default AcceptedProjectsPage;
