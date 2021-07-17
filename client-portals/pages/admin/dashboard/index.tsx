import ProjectApplications from "../../../components/admin/dashboard";
import { useRouter } from "next/router";
import React, { useEffect, useContext } from "react";
import { AuthContext } from "../../../context/authContext";

const AdminDashPage = () => {
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (!authContext.isAuth || !authContext.isAdmin) {
      router.replace("/");
    }
  }, [authContext]);

  return <ProjectApplications />;
};

export default AdminDashPage;
