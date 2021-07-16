import ProjectApplications from "../../../components/admin/dashboard";
import { useRouter } from "next/router";
import React, { useEffect, useContext } from "react";
import { AuthContext } from "../../../context/AuthContext";

const AdminDashPage = () => {
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (!authContext.isAuth || !authContext.isAdmin) {
      router.replace("/dashboard", "/admin");
    }
  }, [authContext]);

  return <ProjectApplications />;
};

export default AdminDashPage;
